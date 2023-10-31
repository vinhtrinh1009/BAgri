import asyncio
import os
import shutil
import traceback
from pathlib import Path
from uuid import uuid4

from django.conf import settings
from django.db.models import Q
from django.http.response import FileResponse
from django.shortcuts import get_object_or_404
from fabric_service.chaincode_handler import ChaincodeHandler
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from utilities.request import parse_int_array_or_400, parse_int_or_400

from api.celery_task import generate_chaincode, generate_mint_script
from api.serializers import *
from api.tasks import compile_token_contract, generate_smart_contract_code_v2
from api.tasks.token_contract_tasks import (generate_token_contract_sdk,
                                            inspect_fungible_token)


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 50
    page_query_param = 'page'

def parse_token_type(data, action='retrieve'):
    token_type = data.get('token_type')
    if token_type == 'fungible':
        serializer_class = FTContractCreateSerializer if action == 'create' else FTContractSerializer
        model_class = FTContract
    elif token_type == 'non_fungible':
        serializer_class = NFTContractCreateSerializer if action == 'create' else NFTContractSerializer
        model_class = NFTContract
    elif token_type is None:
        raise ValidationError(detail="Parameter 'token_type' is required.")
    else:
        raise ValidationError(detail="Unregconized parameter 'token_type'.")
    return model_class, serializer_class


class NetworkViewSet(ModelViewSet):
    model = Network

    def get_serializer_class(self):
        return NetworkSerializer
    
    def get_queryset(self):
        return self.model.objects.all()


class BridgeContractViewSet(ModelViewSet):
    model = BridgeSmartContract

    def get_serializer_class(self):
        return BridgeSmartContractSerializer
    
    def get_queryset(self):
        network_name = self.request.query_params.get('network')
        return self.model.objects.filter(network=network_name)
    
    @action(detail=False, methods=['get'])
    def abi(self, request):
        network_name = self.request.query_params.get('network')
        obj = self.model.objects.filter(network=network_name).first()

        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return FileResponse(obj.abi, as_attachment=True, filename='abi.json')


class TokenContractViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    pagination_class = CustomPagination
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_serializer_class(self):
        _, serializer_class = parse_token_type(self.request.query_params, action='list')
        return serializer_class
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context
    
    def get_queryset(self):
        model, _ = parse_token_type(self.request.query_params)

        network = self.request.query_params.get('network')
        linked_contract = parse_int_or_400(self.request.query_params, 'linked_contract')

        q = Q(user_id=self.request.user.user_id)
        if network:
            q = q & Q(network_id=network)
    
        contracts = model.objects.filter(q).order_by('-id')

        if linked_contract is not None:
            linked_contracts = [link.to_contract for link in LinkedFTContracts.objects.filter(from_contract_id=linked_contract)]
            result_contracts = [contract for contract in contracts if contract in linked_contracts]
            return result_contracts
        return contracts
    
    def create(self, request, *args, **kwargs):
        """ Create a new token contract and try to compile it

        Return 500 if compiling or generating process fail.
        Return 201 if success.
        """

        model_class, serializer_class = parse_token_type(request.data, action='create')
        _, view_serializer_class = parse_token_type(request.data)
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        contract = serializer.save(user_id=request.user.user_id)

        print(request.data)

        try:
            content = generate_smart_contract_code_v2(contract.id, request.data.get('token_type'))
            contract = compile_token_contract(contract, content)
        except Exception as e:
            model_class.objects.filter(id=contract.id).delete()
            traceback.print_exc()
            return Response(f'{e}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = view_serializer_class(contract, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='link')
    def link_contract(self, request, pk):
        model_class, serializer_class = parse_token_type(request.data, action='retrieve')
        contract = get_object_or_404(model_class, id=pk)
        id_list = parse_int_array_or_400(request.data, 'contracts', [])

        for _contract in model_class.objects.filter(id__in=id_list):
            a = LinkedFTContracts.objects.filter(from_contract=contract, to_contract=_contract)
            if not a.exists():
                LinkedFTContracts.objects.create(from_contract=contract, to_contract=_contract)
            
            b = LinkedFTContracts.objects.filter(from_contract=_contract, to_contract=contract)
            if not b.exists():
                LinkedFTContracts.objects.create(from_contract=_contract, to_contract=contract)
        
        return Response({'detail': 'Contracts are linked successfully.'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], url_path='unlink')
    def unlink_contract(self, request, pk):
        model_class, serializer_class = parse_token_type(request.data, action='retrieve')
        contract = get_object_or_404(model_class, id=pk)
        id_list = parse_int_array_or_400(request.data, 'contracts', [])

        for _contract in model_class.objects.filter(id__in=id_list):
            LinkedFTContracts.objects.filter(from_contract=contract, to_contract=_contract).delete()
            LinkedFTContracts.objects.filter(from_contract=_contract, to_contract=contract).delete()

        return Response({'detail': 'Contracts are unlinked successfully.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def interface(self, request):
        token_standard = request.query_params.get('token_standard', TokenSmartContract.TOKEN_STANDARDS.ERC_20)

        if token_standard == TokenSmartContract.TOKEN_STANDARDS.ERC_20:
            return FileResponse(open(os.path.join(settings.BASE_DIR, 'data', 'abi', 'erc20.json'), 'rb'), as_attachment=True, filename='erc20.json')

        return Response(status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=['get'], url_path='sdk')
    def sdk(self, request, pk):
        token_type = request.query_params.get('token_type', 'fungible')

        model_class, serializer_class = parse_token_type(request.query_params, action='retrieve')
        contract = get_object_or_404(model_class, id=pk)

        if contract.user_defined_network is not None:
            chaincode_handler = ChaincodeHandler(settings.VCHAIN_DB_HOST, 
                                settings.VCHAIN_DB_PORT,
                                settings.VCHAIN_DB_NAME,
                                settings.VCHAIN_DB_USERNAME,
                                settings.VCHAIN_DB_PASSWORD,
                                settings.K8S_TOKEN)
            async def handler_generate_sdk(handler, network_id, user_info, token_name):
                await chaincode_handler.ConnectDB()
                response = await handler.handler_generate_sdk(token_name, network_id, user_info)
                return response
            network_id = str(contract.user_defined_network)
            print(network_id)
            user_info={ 
                'user_id': request.user.user_id,
                'username': request.user.username }
            token_name = contract.token_name
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop = asyncio.get_event_loop()
            response = loop.run_until_complete(handler_generate_sdk(chaincode_handler, network_id, user_info, token_name))
            loop.close()
            temp_dir = os.path.join(settings.BASE_DIR, 'data', 'temp')
            Path(temp_dir).mkdir(parents=True, exist_ok=True)
            archive_filepath = os.path.join(settings.BASE_DIR, 'data', 'temp', f'{uuid4()}.zip')
            shutil.make_archive(archive_filepath[:-4], 'zip', response)
            return FileResponse(open(archive_filepath, 'rb'), as_attachment=True, filename=f'{token_name}_{network_id}_sdk.zip')
        
        res = generate_token_contract_sdk(contract.id, token_type)

        if res['status'] != 0:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        temp_dir = os.path.join(settings.BASE_DIR, 'data', 'temp')
        Path(temp_dir).mkdir(parents=True, exist_ok=True)
        archive_filepath = os.path.join(settings.BASE_DIR, 'data', 'temp', f'{uuid4()}.zip')
        shutil.make_archive(archive_filepath[:-4], 'zip', res['output_path'])

        return FileResponse(open(archive_filepath, 'rb'), as_attachment=True, filename=f'{token_type}_token_{contract.id}_sdk.zip')


    @action(detail=True, methods=['get'], url_path='inspect')
    def inspect(self, request, pk):
        """Call view function and return the result
        
        This feature is useful as user doesn't need to connect wallet on browser to inspect a token
        """

        token_type = request.query_params.get('token_type', 'fungible')

        if token_type != 'fungible':
            return Response({'detail': 'NFT is not supported'}, status=status.HTTP_400_BAD_REQUEST)

        function_name = request.query_params.get('function')

        if not function_name:
            return Response({'detail': 'function name is empty'}, status=status.HTTP_400_BAD_REQUEST)

        inputs = []

        for i in range(1, 6):
            arg = request.query_params.get(f'input_{i}')
            arg_type = request.query_params.get(f'input_type_{i}')

            if not (arg and arg_type):
                break

            inputs.append({
                'value': arg,
                'type': arg_type
            })
        
        
        model_class, serializer_class = parse_token_type(request.query_params, action='retrieve')
        contract = get_object_or_404(model_class, id=pk)

        func = {
            'name': function_name,
            'inputs': inputs,
        }
        
        res = inspect_fungible_token(contract, func)

        return Response(res, status=status.HTTP_200_OK)



class TokenContractsAPIView(APIView):
    parser_classes = (FormParser, MultiPartParser, JSONParser)

    def get(self, request):
        model_class, serializer_class = parse_token_type(request.query_params)
        contract_id = request.query_params.get('id')
        user_id = request.query_params.get('user_id')

        if contract_id is not None:
            # get a single contract
            contract = get_object_or_404(model_class, id=contract_id)
            serializer = serializer_class(contract, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif user_id is not None:
            # get a list of contracts
            contracts = model_class.objects.filter(user_id=user_id).order_by('id')
            serializer = serializer_class(contracts, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        contracts = model_class.objects.all()
        serializer = serializer_class(contracts, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenContractUpdateAPIView(APIView):
    parser_classes = (FormParser, MultiPartParser, JSONParser)

    def post(self, request):
        model_class, serializer_class = parse_token_type(request.data)
        contract_id = request.data.get('id')

        if contract_id is None:
            return Response({'detail': "Parameter 'id' is missing."}, status=status.HTTP_400_BAD_REQUEST)
        
        contract = get_object_or_404(model_class, id=contract_id)
        serializer = serializer_class(contract, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TokenContractDeleteAPIView(APIView):
    def post(self, request):
        model_class, _ = parse_token_type(request.data)
        contract_id = request.data.get('id')
        if contract_id is None:
            return Response({'detail': "Parameter 'id' is missing."}, status=status.HTTP_400_BAD_REQUEST)
        
        contract = get_object_or_404(model_class, id=contract_id)
        contract.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Fabric token service
class FabricFTContractsAPIView(APIView):
    def get(self, request):
        if not request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        network = request.query_params.get('network')
        linked_contract = parse_int_or_400(self.request.query_params, 'linked_token')
        q = Q(user_id=self.request.user.user_id)
        if network:
            q = q & Q(user_defined_network=network)
        contracts = FTContract.objects.filter(q)
        if linked_contract is not None:
            linked_contracts = [link.to_contract for link in LinkedFTContracts.objects.filter(from_contract_id=linked_contract)]
            result_contracts = [contract for contract in contracts if contract in linked_contracts]
            serializer = FTContractSerializer(result_contracts, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)       
        serializer = FTContractSerializer(contracts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class FabricFTContractCreateAPIView(APIView):
    handler = ChaincodeHandler(settings.VCHAIN_DB_HOST, 
                                settings.VCHAIN_DB_PORT,
                                settings.VCHAIN_DB_NAME,
                                settings.VCHAIN_DB_USERNAME,
                                settings.VCHAIN_DB_PASSWORD,
                                settings.K8S_TOKEN)
    parser_classes = (FormParser, MultiPartParser, JSONParser)
    def post(self, request):
        if not request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        model_class = FTContract
        model_create_serializer_class = FTContractCreateSerializer
        serializer = model_create_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        contract = serializer.save(user_id=request.user.user_id)
        network_id = str(request.data.get('network_id'))
        token_config = {
            'token_name': request.data['token_name'],
            'token_symbol': request.data['token_symbol'],
            'decimal': request.data['decimal'],
            'token_standard': request.data['token_standard'],
            'initial_supply': request.data['initial_supply'],
        }
        user_info={ 
            'user_id': request.user.user_id,
            'username': request.user.username }
        generate_chaincode.delay(chaincode_config=token_config,
                                    contract_id=contract.id,
                                    user=user_info,
                                    network=network_id)
        response_serializer = FTContractSerializer(contract)
        return Response(data=response_serializer.data, status=status.HTTP_200_OK)

class InvokeFabricContractAPIView(APIView):
    handler = ChaincodeHandler(settings.VCHAIN_DB_HOST, 
                                settings.VCHAIN_DB_PORT,
                                settings.VCHAIN_DB_NAME,
                                settings.VCHAIN_DB_USERNAME,
                                settings.VCHAIN_DB_PASSWORD,
                                settings.K8S_TOKEN)
    
    def post(self, request):
        if not request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        network_id = str(request.data.get('network_id'))
        token_name = request.data.get('token_name')
        quantity = request.data.get('quantity')
        quantity = quantity
        method = request.query_params.get('method')
        minter_org = request.data.get('minter_org')
        minter_username = request.data.get('minter_username')
        user_info={ 
            'user_id': request.user.user_id,
            'username': request.user.username }
        print(token_name)
        if method=='mint':
            generate_mint_script.delay(token_name=token_name, user=user_info, network=network_id, quantity=quantity, minter_org=minter_org, minter_username=minter_username)
        else:
            return Response({'detail': "Parameter 'method' is missing."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)

class GetFabricNetworkAPIView(APIView):
    handler = ChaincodeHandler(settings.VCHAIN_DB_HOST, 
                                settings.VCHAIN_DB_PORT,
                                settings.VCHAIN_DB_NAME,
                                settings.VCHAIN_DB_USERNAME,
                                settings.VCHAIN_DB_PASSWORD,
                                settings.K8S_TOKEN)
    def get(self, request):
        async def handler(handler, request):
            await handler.ConnectDB()
            networks = await handler.get_networks(user_id= request.user.user_id)
            response = networks
            return response
        if not request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(handler(self.handler, request))
        loop.close()
        return Response(data=response, status=status.HTTP_200_OK)

class CurrentUserAPIView(APIView):
    def get(self, request):
        return Response(request.user.to_dict(), status=status.HTTP_200_OK)


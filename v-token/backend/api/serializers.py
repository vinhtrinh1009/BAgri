from urllib.parse import urlencode

from django.urls import reverse
from rest_framework import serializers

from api.tasks import get_contract_arguments

from .models import *


class FTContractSerializer(serializers.ModelSerializer):
    contract_file = serializers.SerializerMethodField()
    compiled_code = serializers.SerializerMethodField()
    abi = serializers.SerializerMethodField()
    arguments = serializers.SerializerMethodField()
    sdk = serializers.SerializerMethodField()

    class Meta:
        model = FTContract
        fields = '__all__'

    def get_contract_file(self, instance):
        request = self.context.get('request')
        if not instance.contract_file:
            return None

        url = instance.contract_file.url
        return request.build_absolute_uri(url).replace('http://', 'https://') if request else url

    def get_compiled_code(self, instance):
        request = self.context.get('request')
        if not instance.compiled_code:
            return None
        url = instance.compiled_code.url
        return request.build_absolute_uri(url).replace('http://', 'https://') if request else url
    
    def get_abi(self, instance):
        request = self.context.get('request')
        if not instance.abi:
            return None
        url = instance.abi.url
        return request.build_absolute_uri(url).replace('http://', 'https://') if request else url
    
    def get_arguments(self, instance):
        return get_contract_arguments(instance)
    
    def get_sdk(self, instance):
        request = self.context.get('request')

        url = reverse('token-contract-sdk', args=[instance.id])
        url = f"{url}?{urlencode({'token_type': 'fungible'})}"

        return request.build_absolute_uri(url).replace('http://', 'https://') if request else url


class NFTContractSerializer(serializers.ModelSerializer):
    contract_file = serializers.SerializerMethodField()
    compiled_code = serializers.SerializerMethodField()
    abi = serializers.SerializerMethodField()

    class Meta:
        model = NFTContract
        fields = '__all__'

    def get_contract_file(self, instance):
        request = self.context.get('request')
        if not instance.contract_file:
            return None
        url = instance.contract_file.url
        return request.build_absolute_uri(url).replace('http://', 'https://') if request else url

    def get_compiled_code(self, instance):
        request = self.context.get('request')
        if not instance.compiled_code:
            return None
        url = instance.compile_code.url
        return request.build_absolute_uri(url).replace('http://', 'https://') if request else url
    
    def get_abi(self, instance):
        request = self.context.get('request')
        if not instance.abi:
            return None
        url = instance.abi.url
        return request.build_absolute_uri(url).replace('http://', 'https://') if request else url


class FTContractCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FTContract
        fields = ('token_standard', 'token_name', 'token_symbol', 'token_icon', 'max_supply', 'decimal', 'burnable', 'pausable', 'mintable', 'initial_supply', 'network', 'user_defined_network')


class NFTContractCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFTContract
        fields = ('token_standard', 'token_name', 'token_symbol', 'token_icon', 'max_supply')


class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = ('name', 'network_id', 'chain_id', 'supported')


class BridgeSmartContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = BridgeSmartContract
        fields = '__all__'

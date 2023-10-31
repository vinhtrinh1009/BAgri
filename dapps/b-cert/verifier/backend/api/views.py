from django.shortcuts import render
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from verifier.models import TokenShared
# from .serializers import TokenShareSerializer
from bcertsdk.handler import Handler
from bcertsdk.errors import *
import jwt
import requests
import json

# Create your views here.


class DecryptTokenAPIView(APIView):
    permission_classes = [AllowAny]
    SECRET_TOKEN = 'QRA27XVAFD8A7FD6X'
    handler = Handler()
    def get(self, request, format=None):
        token = request.query_params.get('token')
        data = jwt.decode(token, self.SECRET_TOKEN, algorithms="HS256")
        return Response(data, status=status.HTTP_200_OK)

class GetCertificateDataAPIView(APIView):
    handler = Handler()
    def get(self, request, pk, format=None):
        blockchain_id = pk
        try:
            cert_res = self.handler.get_data_blockchain([blockchain_id])
            return Response(cert_res, status=status.HTTP_200_OK)
        except InternalError as erri:
            return Response({'detail': erri.message}, status=status.HTTP_400_BAD_REQUEST)
        except CommunicationError as errc:
            return Response({'detail': errc.message}, status=status.HTTP_400_BAD_REQUEST)

class GetResultDataBlockchain(APIView):
    handler = Handler()
    def get(self, request, pk, format=None):
        blockchain_tx = pk
        try:
            result_blockchain = self.handler.get_data_blockchain([blockchain_tx])
            return Response(result_blockchain, status=status.HTTP_200_OK)
        except InternalError as erri:
            return Response({'detail': erri.message}, status=status.HTTP_400_BAD_REQUEST)
        except CommunicationError as errc:
            return Response({'detail': errc.message}, status=status.HTTP_400_BAD_REQUEST)

class GetStudentDataBlockchain(APIView):
    handler = Handler()
    def get(self, request, pk, format=None):
        blockchain_id = pk
        try:
            data_blockchain = self.handler.get_student(blockchain_id)
            return Response(data_blockchain, status=status.HTTP_200_OK)
        except InternalError as erri:
            return Response({'detail': erri.message}, status=status.HTTP_400_BAD_REQUEST)
        except CommunicationError as errc:
            return Response({'detail': errc.message}, status=status.HTTP_400_BAD_REQUEST)

class GetProfessorDataBlockchain(APIView):
    handler = Handler()
    def get(self, request, pk, format=None):
        blockchain_id = pk
        try:
            data_blockchain = self.handler.get_professor(blockchain_id)
            return Response(data_blockchain, status=status.HTTP_200_OK)
        except InternalError as erri:
            return Response({'detail': erri.message}, status=status.HTTP_400_BAD_REQUEST)
        except CommunicationError as errc:
            return Response({'detail': errc.message}, status=status.HTTP_400_BAD_REQUEST)


class GetUniversityDataBlockchain(APIView):
    handler = Handler()
    def get(self, request, pk, format=None):
        blockchain_id = pk
        try:
            data_blockchain = self.handler.get_university(blockchain_id)
            return Response(data_blockchain, status=status.HTTP_200_OK)
        except InternalError as erri:
            return Response({'detail': erri.message}, status=status.HTTP_400_BAD_REQUEST)
        except CommunicationError as errc:
            return Response({'detail': errc.message}, status=status.HTTP_400_BAD_REQUEST)

class GetClassesDataBlockchain(APIView):
    handler = Handler()
    def get(self, request, pk, format=None):
        blockchain_id = pk
        try:
            data_blockchain = self.handler.get_classroom(blockchain_id)
            return Response(data_blockchain, status=status.HTTP_200_OK)
        except InternalError as erri:
            return Response({'detail': erri.message}, status=status.HTTP_400_BAD_REQUEST)
        except CommunicationError as errc:
            return Response({'detail': errc.message}, status=status.HTTP_400_BAD_REQUEST)

class GetSubjectDataBlockchain(APIView):
    handler = Handler()
    def get(self, request, pk, format=None):
        blockchain_id = pk
        try:
            data_blockchain = self.handler.get_subject(blockchain_id)
            return Response(data_blockchain, status=status.HTTP_200_OK)
        except InternalError as erri:
            return Response({'detail': erri.message}, status=status.HTTP_400_BAD_REQUEST)
        except CommunicationError as errc:
            return Response({'detail': errc.message}, status=status.HTTP_400_BAD_REQUEST)
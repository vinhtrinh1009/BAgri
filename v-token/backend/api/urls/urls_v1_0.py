from django.urls import path, include
from api.views import *

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'networks', NetworkViewSet, basename='network')
router.register(r'bridge-contracts', BridgeContractViewSet, basename='bridge-contract')

urlpatterns = [
    path('token-contracts/', TokenContractsAPIView.as_view()),
    path('token-contracts/update', TokenContractUpdateAPIView.as_view()),
    path('token-contracts/delete', TokenContractDeleteAPIView.as_view()),
    # path('token-contracts/generate_code', TokenContractGenerateCodeAPIView.as_view()),
    path('fabric-networks/', GetFabricNetworkAPIView.as_view()),
    path('fabric-token-contracts/', FabricFTContractCreateAPIView.as_view()),
    path('fabric-token-contracts/list/', FabricFTContractsAPIView.as_view()),
    # path('fabric-token-contracts/detail/<int:pk>', FabricFTContractDetailAPIView.as_view()),
    path('me', CurrentUserAPIView.as_view()),
    path('', include(router.urls)),
    path('fabric-token-contracts/invoke-transaction/', InvokeFabricContractAPIView.as_view()),
]

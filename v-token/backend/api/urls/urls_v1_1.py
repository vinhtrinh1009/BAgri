from django.urls import path, include
from api.views import *

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'token-contracts', TokenContractViewSet, basename='token-contract')

urlpatterns = [
    path('', include(router.urls))
]

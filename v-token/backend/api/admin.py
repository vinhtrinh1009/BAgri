from django.contrib import admin

from api.models import *

@admin.register(FTContract)
class FTContractAdmin(admin.ModelAdmin):
    list_display = ('id', 'token_name', 'token_symbol', 'network')

@admin.register(Network)
class NetworkAdmin(admin.ModelAdmin):
    list_display = ('name', 'network_id', 'chain_id')

@admin.register(LinkedFTContracts)
class LinkedFTContractsAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_contract', 'to_contract')

@admin.register(BridgeSmartContract)
class BridgeSmartContractAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'network')

# @admin.register(FabricFTContract)
# class FabricFTContractAdmin(admin.ModelAdmin):
#     list_displat = ('id', 'token_name', 'network_id')

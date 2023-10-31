from django.db import models


class UnrecognizedTokenStandardError(Exception):
    pass


class Network(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    network_id = models.PositiveIntegerField(null=True)
    chain_id = models.PositiveIntegerField(null=True)
    url = models.URLField(default='', max_length=256)
    supported = models.BooleanField(default=True)

class BridgeSmartContract(models.Model):
    contract_file = models.FileField(blank=True, null=True, upload_to='contracts')
    compiled_code = models.FileField(blank=True, null=True, upload_to='bin')
    abi = models.FileField(blank=True, null=True, upload_to='abi')
    address = models.CharField(max_length=64, null=True, blank=True)
    network = models.ForeignKey(Network, on_delete=models.SET_NULL, null=True)


class TokenSmartContract(models.Model):
    class TOKEN_STANDARDS(models.TextChoices):
        ERC_20 = 'ERC-20'
        ERC_721 = 'ERC-721'
        ERC_777 = 'ERC-777'
        ERC_1155 = 'ERC-1155'
    
    class FT_STANDARDS(models.TextChoices):
        ERC_20 = 'ERC-20'
        ERC_777 = 'ERC-777'
    
    class NFT_STANDARDS(models.TextChoices):
        ERC_721 = 'ERC-721'
        ERC_1155 = 'ERC-1155'
    
    token_standard = models.CharField(max_length=16, choices=TOKEN_STANDARDS.choices)
    token_name = models.CharField(max_length=64)
    token_symbol = models.CharField(max_length=8)
    token_icon = models.FileField(blank=True, null=True)
    contract_file = models.FileField(blank=True, null=True, upload_to='contracts')
    
    network = models.ForeignKey(Network, on_delete=models.SET_NULL, null=True, blank=True)
    user_defined_network = models.CharField(max_length=64, null=True, blank=True)
    user_id = models.CharField(max_length=64)
    class Meta:
        abstract = True


class FTContract(TokenSmartContract):
    class STATUS(models.TextChoices):
        PENDING = "Pending"
        FAIL = "Fail"
        SUCCESS = "Success"

    id = models.AutoField(primary_key=True)
    decimal = models.PositiveSmallIntegerField(default=18)
    initial_supply = models.PositiveBigIntegerField(default=0)

    compiled_code = models.FileField(blank=True, null=True, upload_to='bin')
    abi = models.FileField(blank=True, null=True, upload_to='abi')
    address = models.CharField(max_length=64, null=True, blank=True)

    max_supply = models.PositiveIntegerField(blank=True, null=True)
    burnable = models.BooleanField(default=False)
    pausable = models.BooleanField(default=False)
    mintable = models.BooleanField(default=False)
    status = models.CharField(max_length=16, choices = STATUS.choices, default=STATUS.PENDING)



class NFTContract(TokenSmartContract):
    id = models.AutoField(primary_key=True)
    pass

class LinkedFTContracts(models.Model):
    from_contract = models.ForeignKey(FTContract, on_delete=models.CASCADE, related_name='from_ft_contracts')
    to_contract = models.ForeignKey(FTContract, on_delete=models.CASCADE, related_name='to_ft_contracts')

# class FabricFTContract(models.Model):
#     class TOKEN_STANDARDS(models.TextChoices):
#         ERC_20 = 'ERC-20'
#         ERC_777 = 'ERC-777'
    
#     class STATUS(models.TextChoices):
#         PENDING = "Pending"
#         FAIL = "Fail"
#         SUCCESS = "Success"

    # token_standard = models.CharField(max_length=16, choices=TOKEN_STANDARDS.choices)
    # token_name = models.CharField(max_length=64)
    # token_symbol = models.CharField(max_length=8)
    # token_icon = models.FileField(blank=True, null=True)
    # decimal = models.PositiveSmallIntegerField(default=18)
    # initial_supply = models.PositiveBigIntegerField(default=0)
    # user_id = models.CharField(max_length=64)
    # network_id = models.CharField(max_length=64, null=True, blank=True)
    # chaincode_id = models.CharField(max_length=64, null=True, blank=True)
    # status = models.CharField(max_length=16, choices = STATUS.choices, default=STATUS.PENDING)


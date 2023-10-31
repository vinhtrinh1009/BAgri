from pathlib import Path

from api.models import FTContract, Network, TokenSmartContract
from api.tasks import compile_token_contract, generate_smart_contract_code_v2
from django.test import TestCase


class GenerateContractTestCase(TestCase):
    def setUp(self):
        self.contract = None

        self.rinkeby_network = Network.objects.create(name='Rinkeby Test Network', chain_id=4, network_id=4)

        pass

    def test_generate_pausable_ft_contract(self):
        """FT contract can have pasausablity"""
        contract = FTContract.objects.create(
            token_name='Axies Infinity',
            token_symbol='AXS',
            token_standard=TokenSmartContract.FT_STANDARDS.ERC_20,
            pausable=True
        )

        try:
            content = generate_smart_contract_code_v2(contract.id, 'fungible')
            contract = compile_token_contract(contract, content, name='test_pausable')
        except Exception as e:
            self.fail(f'Exception: {e}')
        contract.delete()
    
    def test_generate_non_capped_ft_contract(self):
        """FT contract can have unlimited supply"""
        contract = FTContract.objects.create(
            token_name='Axies Infinity',
            token_symbol='AXS',
            max_supply=None,
            token_standard=TokenSmartContract.FT_STANDARDS.ERC_20
        )

        try:
            content = generate_smart_contract_code_v2(contract.id, 'fungible')
            contract = compile_token_contract(contract, content, name='test_non_capped')
        except Exception as e:
            self.fail(f'Exception: {e}')
        contract.delete()
        
    def test_generate_initial_supply_ft_contract(self):
        """FT contract can have initial supply"""
        contract = FTContract.objects.create(
            token_name='Axies Infinity',
            token_symbol='AXS',
            initial_supply=10,
            token_standard=TokenSmartContract.FT_STANDARDS.ERC_20
        )

        try:
            content = generate_smart_contract_code_v2(contract.id, 'fungible')
            contract = compile_token_contract(contract, content, name='test_initial_supply')
        except Exception as e:
            self.fail(f'Exception: {e}')
        contract.delete()

    def test_generate_capped_ft_contract(self):
        """FT contract can have capped supply"""
        contract = FTContract.objects.create(
            token_name='Axies Infinity',
            token_symbol='AXS',
            max_supply=270000000,
            token_standard=TokenSmartContract.FT_STANDARDS.ERC_20
        )

        try:
            content = generate_smart_contract_code_v2(contract.id, 'fungible')
            contract = compile_token_contract(contract, content, name='test_capped')
        except Exception as e:
            self.fail(f'Exception: {e}')
        contract.delete()
    
    def test_generate_burnable_ft_contract(self):
        """Token can be burned"""
        contract = FTContract.objects.create(
            token_name='Axies Infinity',
            token_symbol='AXS',
            token_standard=TokenSmartContract.FT_STANDARDS.ERC_20,
            burnable=True
        )

        try:
            content = generate_smart_contract_code_v2(contract.id, 'fungible')
            contract = compile_token_contract(contract, content, name='test_burnable')
        except Exception as e:
            self.fail(f'Exception: {e}')
        contract.delete()

    def test_generate_mintable_ft_contract(self):
        """Token can be minted"""

        contract = FTContract.objects.create(
            token_name='Axies Infinity',
            token_symbol='AXS',
            token_standard=TokenSmartContract.FT_STANDARDS.ERC_20,
            mintable=True
        )

        try:
            content = generate_smart_contract_code_v2(contract.id, 'fungible')
            contract = compile_token_contract(contract, content, name='test_mintable')
        except Exception as e:
            self.fail(f'Exception: {e}')
        contract.delete()
    
    def test_generate_mintable_and_burnable_ft_contract(self):
        """Token can be minted and be burned"""

        self.contract = FTContract.objects.create(
            token_name='Axies Infinity',
            token_symbol='AXS',
            token_standard=TokenSmartContract.FT_STANDARDS.ERC_20,
            mintable=True,
            burnable=True
        )

        try:
            content = generate_smart_contract_code_v2(self.contract.id, 'fungible')
            self.contract = compile_token_contract(self.contract, content, name='test_mintable_burnable')
        except Exception as e:
            self.fail(f'Exception: {e}')
    
    def test_generate_full_ft_contract(self):
        """Generate fully extended FT contract"""

        self.contract = FTContract.objects.create(
            token_name='V-Chain Token',
            token_symbol='VCHAIN',
            token_standard=TokenSmartContract.FT_STANDARDS.ERC_20,
            burnable=True,
            pausable=True,
            mintable=True,
            max_supply=1000000,
            initial_supply=10,
            network=self.rinkeby_network
        )

        try:
            content = generate_smart_contract_code_v2(self.contract.id, 'fungible')
            self.contract = compile_token_contract(self.contract, content, name='test_full')
        except Exception as e:
            self.fail(f'Exception: {e}')
    
    def tearDown(self):
        if not self.contract or self.contract.id is None:
            return
        
        # if self.contract.contract_file:
        #     Path(self.contract.contract_file.path).unlink(missing_ok=True)
        if self.contract.abi:
            Path(self.contract.abi.path).unlink(missing_ok=True)
        if self.contract.compiled_code:
            Path(self.contract.compiled_code.path).unlink(missing_ok=True)
        
        self.contract.delete()
        

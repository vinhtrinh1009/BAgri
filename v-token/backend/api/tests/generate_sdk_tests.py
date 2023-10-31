import json
from pathlib import Path
from urllib.parse import urlencode

from api.models import FTContract, Network, TokenSmartContract
from api.tasks import compile_token_contract, generate_smart_contract_code_v2
from api.tasks.token_contract_tasks import generate_token_contract_sdk
from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class GenerateTokenContractSDKTestCase(TestCase):
    """Test generating SDK for token contract

    Requirements: Generating contract test case should be passed before running this test case.
    """

    def setUp(self):
        self.token = 'Bearer'

        self.rinkeby_network = Network.objects.create(
            name='Rinkeby Test Network',
            chain_id=4,
            network_id=4,
            url="https://rinkeby.infura.io/v3/"
        )

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

        content = generate_smart_contract_code_v2(self.contract.id, 'fungible')
        self.contract = compile_token_contract(self.contract, content, name='test_full')
        self.contract.address = "0x069a3BdCD5testaddress2afDb4f575337C13685"
        self.contract.save()

    def test_generate_python_sdk(self):
        """Be able to generate Python SDK"""

        try:
            generate_token_contract_sdk(self.contract.id, 'fungible')
        except Exception as e:
            self.fail(f"Exception: {e}")
    
    def test_download_python_sdk(self):
        """Be able to download Python SDK"""

        url = reverse('token-contract-sdk', args=[self.contract.id])
        url = f"{url}?{urlencode({'token_type': 'fungible'})}"

        response = self.client.get(url, HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def tearDown(self):
        if not self.contract or self.contract.id is None:
            return
        
        # if self.contract.contract_file:
        #     Path(self.contract.contract_file.path).unlink(missing_ok=True)
        # if self.contract.abi:
        #     Path(self.contract.abi.path).unlink(missing_ok=True)
        if self.contract.compiled_code:
            Path(self.contract.compiled_code.path).unlink(missing_ok=True)
        
        self.contract.delete()
        

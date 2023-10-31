from pathlib import Path

from api.models import FTContract, Network, TokenSmartContract
from api.tasks import compile_token_contract, generate_smart_contract_code_v2
from api.tasks.token_contract_tasks import compile_contract, generate_token_contract_sdk
from django.test import TestCase
import subprocess
from web3 import Web3
from django.conf import settings

ACC1 = ''
ACC1_PRIVATE_KEY = ''
ACC2 = ''
ACC2_PRIVATE_KEY = ''
ACC3 = ''


class TokenContractSDKTestCase(TestCase):
    """Test SDK of token contract

    Requirements: Generating SDK test case should be passed before running this test case.
    """

    def setUp(self):
        self.token = 'Bearer '

        RPC_URL = "http://172.17.0.1:8545/"
        # RPC_URL = "https://rinkeby.infura.io/v3/"

        self.rinkeby_network = Network.objects.create(
            name='Hardhat Test Network',
            chain_id=31337,
            network_id=31337,
            url=RPC_URL
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

        # deploy contract
        self.web3 = Web3(Web3.HTTPProvider(RPC_URL))

        abi, bin = compile_contract(content)
        instance = self.web3.eth.contract(abi=abi, bytecode=bin)
        acct = self.web3.eth.account.privateKeyToAccount(ACC1_PRIVATE_KEY)

        construct_txn = instance.constructor('V-Chain Token', 'VCHAIN', 1000000000000000000000000, 10000000000000000000).buildTransaction({
            'from': acct.address,
            'nonce': self.web3.eth.getTransactionCount(acct.address),
            # 'gas': 1728712,
            # 'gasPrice': w3.toWei('21', 'gwei')
        })

        signed = acct.signTransaction(construct_txn)

        tx_hash = self.web3.eth.sendRawTransaction(signed.rawTransaction)

        receipt = self.web3.eth.getTransactionReceipt(tx_hash)

        self.contract.address = self.web3.toChecksumAddress(receipt['contractAddress']) # Test SDK token on Rinkeby, deployed by account 1

        self.contract.save()

        generate_token_contract_sdk(self.contract.id, 'fungible')

        from data.media.sdk.test_full.handler import TokenContractHandler

        self.handler = TokenContractHandler(sender_address=ACC1, sender_private_key=ACC1_PRIVATE_KEY)
        self.handler2 = TokenContractHandler(sender_address=ACC2, sender_private_key=ACC2_PRIVATE_KEY)


    def test_basic_read(self):
        self.handler.cap()
        self.handler.decimals()
        self.handler.DEFAULT_ADMIN_ROLE()
        self.handler.MINTER_ROLE()
        self.handler.PAUSER_ROLE()
        self.handler.name()
        self.handler.paused()
        self.handler.symbol()
        self.handler.total_supply()


    def test_allowance(self):
        self.assertEqual(self.handler.allowance(ACC1, ACC2), 0)

    def test_approve(self):
        self.handler.approve(ACC2, 100000)

        self.assertEqual(self.handler.allowance(ACC1, ACC2), 100000)

    def test_balance_of(self):
        self.assertEqual(self.handler.balance_of(ACC1), 10000000000000000000)
        self.assertEqual(self.handler.balance_of(ACC2), 0)

    def test_burn(self):
        try:
            self.handler.burn(1000)
        except Exception as e:
            self.fail(f"Fail when calling burn(): {e}")
    
    def test_burn_from(self):
        try:
            self.handler2.burn_from(ACC1, 10)
            self.fail(f"Should not be able to burn without allowance")
        except Exception as e:
            pass
    
        # increase allowance
        self.handler.approve(ACC2, 10)

        try:
            self.handler2.burn_from(ACC1, 10)
        except Exception as e:
            self.fail(f"Fail when calling burn_from(): {e}")

    def test_change_allowance(self):
        self.handler.increase_allowance(ACC2, 10)
        self.handler.decrease_allowance(ACC2, 10)

    def test_mint(self):
        self.handler.mint(ACC1, 1000)
    
    def test_pause(self):
        self.handler.pause()

    def test_transfer(self):
        self.handler.transfer(ACC2, 100)
    
    def test_unpause(self):
        self.handler.pause()
        self.handler.unpause()
    
    def test_transfer_from(self):
        self.handler.approve(ACC2, 100)

        self.handler2.transfer_from(ACC1, ACC3, 100)

    def test_example(self):
        from data.media.sdk.test_full.example import main
        main()


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
        self.web3.provider.make_request("hardhat_reset", [])
        

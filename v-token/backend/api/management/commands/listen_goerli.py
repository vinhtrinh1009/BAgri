"""
Listen for burn event
"""
import asyncio
import json

from django.conf import settings
from django.core.management.base import BaseCommand
from api.models import Network, FTContract, LinkedFTContracts
from web3 import Web3
from web3.exceptions import ContractLogicError
from web3.middleware import geth_poa_middleware
from asgiref.sync import sync_to_async

class Command(BaseCommand):
    help = 'Run Goerli Listener'

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.rinkeby_bridge_address = settings.RINKEBY_BRIDGE_CONTRACT_ADDRESS_V2
        self.rinkeby_web3 = Web3(Web3.HTTPProvider(settings.INFURA_RINKEBY_HTTP_URL))
        abi = None
        with open(settings.RINKEBY_BRIDGE_CONTRACT_ABI_FILEPATH_V2) as f:
            abi = json.loads(f.read())
        self.rinkeby_bridge_contract = self.rinkeby_web3.eth.contract(address=self.rinkeby_bridge_address, abi=abi)

        self.goerli_bridge_address = settings.GOERLI_BRIDGE_CONTRACT_ADDRESS_V2
        self.goerli_web3 = Web3(Web3.HTTPProvider(settings.INFURA_GOERLI_HTTP_URL))
        self.goerli_web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        abi = None
        with open(settings.GOERLI_BRIDGE_CONTRACT_ABI_FILEPATH_V2) as f:
            abi = json.loads(f.read())
        self.goerli_bridge_contract = self.goerli_web3.eth.contract(address=self.goerli_bridge_address, abi=abi)

        self.rinkeby_network = Network.objects.get(name='Rinkeby Test Network')

        print("Goerli bridge: ", self.goerli_bridge_address)
        print("Rinkeby bridge: ", self.rinkeby_bridge_address)

    async def handle_event(self, event):
        """Receive event"""

        data = json.loads(Web3.toJSON(event))
        args = data['args']

        if args['step'] == 0: # burn
            print(f"Received burn event from {args['from']} with amount {args['amount']}")

            # build transaction
            @sync_to_async
            def _get_target_token_address(from_token_address):
                from_token = FTContract.objects.filter(address=from_token_address).first()
                linked_contracts = [l.to_contract for l in LinkedFTContracts.objects.filter(from_contract=from_token) if l.to_contract.network.name == 'Rinkeby Test Network']

                if not linked_contracts:
                    return None
                
                return linked_contracts[0].address

            token_address = await _get_target_token_address(args['token'])

            if token_address is None:
                print(f"Token {args['token']} does not have any linked token in Rinkeby")
                return

            func = self.rinkeby_bridge_contract.functions.mint(token_address, args['to'], args['amount'], args['nonce'])
            
            try:
                tx = func.buildTransaction({
                    # 'gas': 70000,
                    # 'gasPrice': self.rinkeby_web3.eth.gas_price,
                    'from': settings.RINKEBY_BRIDGE_ADMIN_ADDRESS,
                    'nonce': self.rinkeby_web3.eth.getTransactionCount(settings.RINKEBY_BRIDGE_ADMIN_ADDRESS)
                })
            except ContractLogicError as e:
                print(e)
                return

            # sign transaction
            private_key = self.rinkeby_web3.toHex(hexstr=settings.ETHEREUM_PRIVATE_KEY)
            signed_tx = self.rinkeby_web3.eth.account.sign_transaction(tx, private_key=private_key)

            # send transaction
            try:
                self.rinkeby_web3.eth.send_raw_transaction(signed_tx.rawTransaction)
                print(f"Send mint transaction for {args['to']} with amount {args['amount']}")
            except Exception as e:
                print(e)

        elif args['step'] == 1: # mint
            # TODO: notify user

            print(f"{args['amount']} tokens have been minted for {args['to']}")

    # asynchronous defined function to loop
    # this loop sets up an event filter and is looking for new entires for the "Transfer" event
    # this loop runs on a poll interval
    async def log_loop(self, event_filter, poll_interval):
        while True:
            for Transfer in event_filter.get_new_entries():
                await self.handle_event(Transfer)
            await asyncio.sleep(poll_interval)


    def handle(self, *args, **kwargs):
        print("Listening to bridge contract's events on Goerli...")

        # create a filter for the latest block and look for the "Transfer" event for the bridge contract
        # run an async loop
        # try to run the log_loop function above every 2 seconds


        event_filter = self.goerli_bridge_contract.events.Transfer.createFilter(fromBlock='latest', address=self.goerli_bridge_address)
        #block_filter = web3.eth.filter('latest')
        # tx_filter = web3.eth.filter('pending')

        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(
                asyncio.gather(
                    self.log_loop(event_filter, 2)))
                    # log_loop(block_filter, 2),
                    # log_loop(tx_filter, 2)))
        finally:
            # close loop to free up system resources
            loop.close()

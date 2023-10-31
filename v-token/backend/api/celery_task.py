import asyncio

from django.shortcuts import get_object_or_404
from vtokens import celery_app
from api.models import FTContract
from fabric_service.chaincode_handler import ChaincodeHandler
from django.conf import settings

@celery_app.task(name='generate_chaincode')
def generate_chaincode(chaincode_config, contract_id, user, network):
    handler = ChaincodeHandler(settings.VCHAIN_DB_HOST, 
                                settings.VCHAIN_DB_PORT,
                                settings.VCHAIN_DB_NAME,
                                settings.VCHAIN_DB_USERNAME,
                                settings.VCHAIN_DB_PASSWORD,
                                settings.K8S_TOKEN)

    async def handle(handler, chaincode_config, user, network ):
        await handler.ConnectDB()
        response = await handler.handler_create_chaincode(chaincode_config=chaincode_config,
                                                        network_id=network,
                                                        user_info=user)
        return response
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    response = loop.run_until_complete(handle(handler=handler, chaincode_config=chaincode_config, user=user, network=network))
    loop.close()
    print(response)
    contract = get_object_or_404(FTContract, id=contract_id)
    contract.status = 'Success'
    contract.save()
    contract = get_object_or_404(FTContract, id=contract_id)
    if response == False: 
        contract.status = 'Fail'
        contract.save()
        return True
    contract.status = 'Success'
    return True

@celery_app.task(name='generate_mint_script')
def generate_mint_script(token_name, user, network, quantity, minter_org, minter_username):
    handler = ChaincodeHandler(settings.VCHAIN_DB_HOST, 
                                settings.VCHAIN_DB_PORT,
                                settings.VCHAIN_DB_NAME,
                                settings.VCHAIN_DB_USERNAME,
                                settings.VCHAIN_DB_PASSWORD,
                                settings.K8S_TOKEN)

    async def handle(handler, token_name, user, network, quantity, minter_org, minter_username ):
        await handler.ConnectDB()
        response = await handler.handler_invoke_chaincode_mint(token_name=token_name,
                                                        network_id=network,
                                                        user_info=user, quantity=quantity,
                                                        minter_org= minter_org, minter_username=minter_username)
        return response
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    response = loop.run_until_complete(handle(handler=handler, token_name=token_name, user=user, network=network, quantity=quantity, minter_org=minter_org, minter_username=minter_username))
    loop.close()
    print(response)
    if response == False: 
        return False
    return True

@celery_app.task(name='generate_burn_script')
def generate_burn_script(token_name, user, network, quantity, to_address, to_token):
    handler = ChaincodeHandler(settings.VCHAIN_DB_HOST, 
                                settings.VCHAIN_DB_PORT,
                                settings.VCHAIN_DB_NAME,
                                settings.VCHAIN_DB_USERNAME,
                                settings.VCHAIN_DB_PASSWORD,
                                settings.K8S_TOKEN)

    async def handle(handler, token_name, user, network, quantity, to_address, to_token ):
        await handler.ConnectDB()
        response = await handler.handler_invoke_chaincode_burn(token_name=token_name,
                                                        network_id=network,
                                                        user_info=user, quantity=quantity, to_address=to_address, to_token=to_token)
        return response
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    response = loop.run_until_complete(handle(handler=handler, token_name=token_name, user=user, network=network, quantity=quantity, to_address=to_address, to_token=to_token))
    loop.close()
    print(response)
    if response == False: 
        return False
    return True
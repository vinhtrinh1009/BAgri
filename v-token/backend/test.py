import os
from fabric_service.chaincode_handler import ChaincodeHandler
import asyncio

async def main():
    db_host = os.environ.get('DB_HOST')
    db_port = os.environ.get('DB_PORT')
    db_name = os.environ.get('DB_NAME')
    db_username = os.environ.get('DB_USERNAME')
    db_password = os.environ.get('DB_PASSWORD')
    k8s_token = os.environ.get('K8S_TOKEN')
    handler = ChaincodeHandler(db_host, db_port, db_name, db_username, db_password, k8s_token)
    await handler.ConnectDB()
    # chaincode_config = {'token_name': "token", 'token_standard': 'erc20', 'token_symbol': 'tok', 'decimal': 18, 'initial_supply': 1000, 
    #                     'network_id': "61c548ef0e64fff9771a6e6f"}
    # user_info = {'username': 'none'}
    # response = await handler.handler_create_chaincode(chaincode_config, chaincode_config['network_id'], user_info)
    response = await handler.get_dapps(user_id='618f18de76a63f86a80b5efc')
    print(response)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
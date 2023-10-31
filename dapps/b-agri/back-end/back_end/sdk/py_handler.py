import json
import os
from web3 import Web3
from file_handler import upload_file
from encrypt_aes import AESCipher
from exceptions import SdkError, ThirdPartyRequestError, NetworkError, StorageServiceRequestError, SchemaError

class Handler:
    def __init__(self, sender_address, sender_private_key):
        self.sender_address = sender_address
        self.sender_private_key = sender_private_key
        self.contract_abi_path = f"{os.getcwd()}/build/Bagriv1.json"
        self.contract_abi = json.load(open(self.contract_abi_path, "r"))['abi']
        self.endpoint = "https://rinkeby.infura.io/v3/7f36cec5929045f89cd70f17e5995c7f"
        self.web3 = Web3(Web3.HTTPProvider(self.endpoint))
        self.contract_address = "0xC01A1B7F2859734b781E0c842e69bc393E81155C"
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=self.contract_abi)
        self.sdk_key = 'ba78b420-2a9e-4c1f-aaf0-bca252ea226a'
        self.data_folder_id = "6231a3ede67a9240e3251263"
    
    def get_season(self, season_id, block_id='latest'):
        season_infor = self.contract.functions.getSeason(season_id).call(block_identifier=block_id)
        return season_infor

    def create_season(self, season_id, processes, start_date, end_date, name, garden_id, task_ids, tree_id):
        nonce = self.web3.eth.getTransactionCount(self.sender_address)
        retry = 10
        while retry > 0 and success == False:
            try:
                
                
                _season = { 
                    'season_id': season_id, 
                    'processes': processes, 
                    'start_date': start_date, 
                    'end_date': end_date, 
                    'name': name, 
                    'garden_id': garden_id, 
                    'task_ids': task_ids, 
                    'tree_id': tree_id
                }
                tx_dict = self.contract.functions.createSeason(_season)\
                    .buildTransaction({
                        'from': self.sender_address,
                        'gas': 800000,
                        'gasPrice': self.web3.toWei('200', 'gwei'),
                        'nonce': nonce,
                        'chainId': 4
                    })
                signed_tx = self.web3.eth.account.signTransaction(tx_dict, self.sender_private_key)
                tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
                success = True
            except SchemaError as e:
                print(e.message)
                retry = 0
                raise SdkError(e.message)

            except ThirdPartyRequestError as e:
                print(e.message)
                nonce += 1
                retry -= 1

            except Exception as ex:
                print(ex.args[0])
                nonce += 1
                retry -= 1
        return (self.web3.toHex(tx_hash))


    def update_season(self, season_id, processes, start_date, end_date, name, garden_id, task_ids, tree_id):
        nonce = self.web3.eth.getTransactionCount(self.sender_address)
        retry = 10
        while retry > 0 and success == False:
            try:
                
                
                _season = { 
                    'season_id': season_id, 
                    'processes': processes, 
                    'start_date': start_date, 
                    'end_date': end_date, 
                    'name': name, 
                    'garden_id': garden_id, 
                    'task_ids': task_ids, 
                    'tree_id': tree_id
                }
                tx_dict = self.contract.functions.updateSeason(_season)\
                    .buildTransaction({
                        'from': self.sender_address,
                        'gas': 800000,
                        'gasPrice': self.web3.toWei('200', 'gwei'),
                        'nonce': nonce,
                        'chainId': 4
                    })
                signed_tx = self.web3.eth.account.signTransaction(tx_dict, self.sender_private_key)
                tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
                success = True
            except SchemaError as e:
                print(e.message)
                retry = 0
                raise SdkError(e.message)

            except ThirdPartyRequestError as e:
                print(e.message)
                nonce += 1
                retry -= 1

            except Exception as ex:
                print(ex.args[0])
                nonce += 1
                retry -= 1
        return (self.web3.toHex(tx_hash))

    def get_garden(self, garden_id, block_id='latest'):
        garden_infor = self.contract.functions.getGarden(garden_id).call(block_identifier=block_id)
        return garden_infor

    def create_garden(self, garden_id, name, area, season_id):
        nonce = self.web3.eth.getTransactionCount(self.sender_address)
        retry = 10
        while retry > 0 and success == False:
            try:
                
                
                _garden = { 
                    'garden_id': garden_id, 
                    'name': name, 
                    'area': area, 
                    'season_id': season_id
                }
                tx_dict = self.contract.functions.createGarden(_garden)\
                    .buildTransaction({
                        'from': self.sender_address,
                        'gas': 800000,
                        'gasPrice': self.web3.toWei('200', 'gwei'),
                        'nonce': nonce,
                        'chainId': 4
                    })
                signed_tx = self.web3.eth.account.signTransaction(tx_dict, self.sender_private_key)
                tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
                success = True
            except SchemaError as e:
                print(e.message)
                retry = 0
                raise SdkError(e.message)

            except ThirdPartyRequestError as e:
                print(e.message)
                nonce += 1
                retry -= 1

            except Exception as ex:
                print(ex.args[0])
                nonce += 1
                retry -= 1
        return (self.web3.toHex(tx_hash))


    def update_garden(self, garden_id, name, area, season_id):
        nonce = self.web3.eth.getTransactionCount(self.sender_address)
        retry = 10
        while retry > 0 and success == False:
            try:
                
                
                _garden = { 
                    'garden_id': garden_id, 
                    'name': name, 
                    'area': area, 
                    'season_id': season_id
                }
                tx_dict = self.contract.functions.updateGarden(_garden)\
                    .buildTransaction({
                        'from': self.sender_address,
                        'gas': 800000,
                        'gasPrice': self.web3.toWei('200', 'gwei'),
                        'nonce': nonce,
                        'chainId': 4
                    })
                signed_tx = self.web3.eth.account.signTransaction(tx_dict, self.sender_private_key)
                tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
                success = True
            except SchemaError as e:
                print(e.message)
                retry = 0
                raise SdkError(e.message)

            except ThirdPartyRequestError as e:
                print(e.message)
                nonce += 1
                retry -= 1

            except Exception as ex:
                print(ex.args[0])
                nonce += 1
                retry -= 1
        return (self.web3.toHex(tx_hash))

    def get_task(self, task_id, block_id='latest'):
        task_infor = self.contract.functions.getTask(task_id).call(block_identifier=block_id)
        return task_infor

    def create_task(self, task_id, name, description, date, start_time, end_time, results, season_id, farmer_ids):
        nonce = self.web3.eth.getTransactionCount(self.sender_address)
        retry = 10
        while retry > 0 and success == False:
            try:
                
                
                _task = { 
                    'task_id': task_id, 
                    'name': name, 
                    'description': description, 
                    'date': date, 
                    'start_time': start_time, 
                    'end_time': end_time, 
                    'results': results, 
                    'season_id': season_id, 
                    'farmer_ids': farmer_ids
                }
                tx_dict = self.contract.functions.createTask(_task)\
                    .buildTransaction({
                        'from': self.sender_address,
                        'gas': 800000,
                        'gasPrice': self.web3.toWei('200', 'gwei'),
                        'nonce': nonce,
                        'chainId': 4
                    })
                signed_tx = self.web3.eth.account.signTransaction(tx_dict, self.sender_private_key)
                tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
                success = True
            except SchemaError as e:
                print(e.message)
                retry = 0
                raise SdkError(e.message)

            except ThirdPartyRequestError as e:
                print(e.message)
                nonce += 1
                retry -= 1

            except Exception as ex:
                print(ex.args[0])
                nonce += 1
                retry -= 1
        return (self.web3.toHex(tx_hash))


    def update_task(self, task_id, name, description, date, start_time, end_time, results, season_id, farmer_ids):
        nonce = self.web3.eth.getTransactionCount(self.sender_address)
        retry = 10
        while retry > 0 and success == False:
            try:
                
                
                _task = { 
                    'task_id': task_id, 
                    'name': name, 
                    'description': description, 
                    'date': date, 
                    'start_time': start_time, 
                    'end_time': end_time, 
                    'results': results, 
                    'season_id': season_id, 
                    'farmer_ids': farmer_ids
                }
                tx_dict = self.contract.functions.updateTask(_task)\
                    .buildTransaction({
                        'from': self.sender_address,
                        'gas': 800000,
                        'gasPrice': self.web3.toWei('200', 'gwei'),
                        'nonce': nonce,
                        'chainId': 4
                    })
                signed_tx = self.web3.eth.account.signTransaction(tx_dict, self.sender_private_key)
                tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
                success = True
            except SchemaError as e:
                print(e.message)
                retry = 0
                raise SdkError(e.message)

            except ThirdPartyRequestError as e:
                print(e.message)
                nonce += 1
                retry -= 1

            except Exception as ex:
                print(ex.args[0])
                nonce += 1
                retry -= 1
        return (self.web3.toHex(tx_hash))

    def get_farmer(self, farmer_id, block_id='latest'):
        farmer_infor = self.contract.functions.getFarmer(farmer_id).call(block_identifier=block_id)
        return farmer_infor

    def create_farmer(self, farmer_id, name, task_id):
        nonce = self.web3.eth.getTransactionCount(self.sender_address)
        retry = 10
        while retry > 0 and success == False:
            try:
                
                
                _farmer = { 
                    'farmer_id': farmer_id, 
                    'name': name, 
                    'task_id': task_id
                }
                tx_dict = self.contract.functions.createFarmer(_farmer)\
                    .buildTransaction({
                        'from': self.sender_address,
                        'gas': 800000,
                        'gasPrice': self.web3.toWei('200', 'gwei'),
                        'nonce': nonce,
                        'chainId': 4
                    })
                signed_tx = self.web3.eth.account.signTransaction(tx_dict, self.sender_private_key)
                tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
                success = True
            except SchemaError as e:
                print(e.message)
                retry = 0
                raise SdkError(e.message)

            except ThirdPartyRequestError as e:
                print(e.message)
                nonce += 1
                retry -= 1

            except Exception as ex:
                print(ex.args[0])
                nonce += 1
                retry -= 1
        return (self.web3.toHex(tx_hash))


    def update_farmer(self, farmer_id, name, task_id):
        nonce = self.web3.eth.getTransactionCount(self.sender_address)
        retry = 10
        while retry > 0 and success == False:
            try:
                
                
                _farmer = { 
                    'farmer_id': farmer_id, 
                    'name': name, 
                    'task_id': task_id
                }
                tx_dict = self.contract.functions.updateFarmer(_farmer)\
                    .buildTransaction({
                        'from': self.sender_address,
                        'gas': 800000,
                        'gasPrice': self.web3.toWei('200', 'gwei'),
                        'nonce': nonce,
                        'chainId': 4
                    })
                signed_tx = self.web3.eth.account.signTransaction(tx_dict, self.sender_private_key)
                tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
                success = True
            except SchemaError as e:
                print(e.message)
                retry = 0
                raise SdkError(e.message)

            except ThirdPartyRequestError as e:
                print(e.message)
                nonce += 1
                retry -= 1

            except Exception as ex:
                print(ex.args[0])
                nonce += 1
                retry -= 1
        return (self.web3.toHex(tx_hash))

    def get_tree(self, tree_id, block_id='latest'):
        tree_infor = self.contract.functions.getTree(tree_id).call(block_identifier=block_id)
        return tree_infor

    def create_tree(self, tree_id, name, description, season_id):
        nonce = self.web3.eth.getTransactionCount(self.sender_address)
        retry = 10
        while retry > 0 and success == False:
            try:
                
                
                _tree = { 
                    'tree_id': tree_id, 
                    'name': name, 
                    'description': description, 
                    'season_id': season_id
                }
                tx_dict = self.contract.functions.createTree(_tree)\
                    .buildTransaction({
                        'from': self.sender_address,
                        'gas': 800000,
                        'gasPrice': self.web3.toWei('200', 'gwei'),
                        'nonce': nonce,
                        'chainId': 4
                    })
                signed_tx = self.web3.eth.account.signTransaction(tx_dict, self.sender_private_key)
                tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
                success = True
            except SchemaError as e:
                print(e.message)
                retry = 0
                raise SdkError(e.message)

            except ThirdPartyRequestError as e:
                print(e.message)
                nonce += 1
                retry -= 1

            except Exception as ex:
                print(ex.args[0])
                nonce += 1
                retry -= 1
        return (self.web3.toHex(tx_hash))


    def update_tree(self, tree_id, name, description, season_id):
        nonce = self.web3.eth.getTransactionCount(self.sender_address)
        retry = 10
        while retry > 0 and success == False:
            try:
                
                
                _tree = { 
                    'tree_id': tree_id, 
                    'name': name, 
                    'description': description, 
                    'season_id': season_id
                }
                tx_dict = self.contract.functions.updateTree(_tree)\
                    .buildTransaction({
                        'from': self.sender_address,
                        'gas': 800000,
                        'gasPrice': self.web3.toWei('200', 'gwei'),
                        'nonce': nonce,
                        'chainId': 4
                    })
                signed_tx = self.web3.eth.account.signTransaction(tx_dict, self.sender_private_key)
                tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
                success = True
            except SchemaError as e:
                print(e.message)
                retry = 0
                raise SdkError(e.message)

            except ThirdPartyRequestError as e:
                print(e.message)
                nonce += 1
                retry -= 1

            except Exception as ex:
                print(ex.args[0])
                nonce += 1
                retry -= 1
        return (self.web3.toHex(tx_hash))
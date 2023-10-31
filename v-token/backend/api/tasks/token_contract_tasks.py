import json
import os
import re
import shutil
import string
from pathlib import Path
from uuid import uuid4

from api.models import (FTContract, NFTContract, TokenSmartContract,
                        UnrecognizedTokenStandardError)
from django.conf import settings
from django.core.files.base import ContentFile
from jinja2 import Environment, FileSystemLoader
from solcx import compile_source
from web3 import Web3
from web3.auto import w3
from web3.exceptions import ContractLogicError
from web3.middleware import geth_poa_middleware

rinkeby_web3 = Web3(Web3.HTTPProvider(settings.INFURA_RINKEBY_HTTP_URL))
goerli_web3 = Web3(Web3.HTTPProvider(settings.INFURA_GOERLI_HTTP_URL))
goerli_web3.middleware_onion.inject(geth_poa_middleware, layer=0)

class UnrecognizedTokenTypeError(Exception):
    pass

def get_contract_class_from_type(token_type):
    if token_type == 'fungible':
        model_class = FTContract
    elif token_type == 'non_fungible':
        model_class = NFTContract
    else:
        raise UnrecognizedTokenTypeError(f"Unrecognized token type.")
    return model_class


def compile_token_contract(contract, content, name=''):
    debug = True
    if not name:
        name = str(uuid4())

    if debug:
        Path(os.path.join(settings.MEDIA_ROOT, 'contracts', f'{name}.sol')).unlink(missing_ok=True)

    contract.contract_file.save(f'{name}.sol', ContentFile(content))
    abi, bin = compile_contract(content)
    contract.compiled_code.save(f'{name}.bin', ContentFile(bin))
    contract.abi.save(f'{name}.json', ContentFile(json.dumps(abi)))

    return contract


def _format_statements(statements, level=2):
    """Formate statements with indentation"""

    res = ''
    for _ in statements:
        res += '    ' * level + _ + '\n'
    return res


def generate_smart_contract_code_v2(contract_id, token_type):
    """Generate the token contract based on configuration

    :param contract_id: the id of the contract
    :type contract_id: str
    :param token_type: fungible or non_fungible
    :type token_type: str
    :raises UnrecognizedTokenTypeError: raise if the token_type is unrecognized
    :return: content
    :rtype: str
    """

    model_class = get_contract_class_from_type(token_type)

    pragma_version = '^0.8.11'
    header = '// SPDX-License-Identifier: MIT\n'

    import_list = [
        "@openzeppelin/contracts/token/ERC20/ERC20.sol",
        "@openzeppelin/contracts/access/AccessControlEnumerable.sol",
        "@openzeppelin/contracts/utils/Context.sol",
    ]
    attribute_statements = []
    mint_guards = []
    mint_statements = []
    _mint_guards = []
    _mint_statements = []
    constructor_statements = []
    constructor_arguments = ['string memory name', 'string memory symbol']
    constructor_guards = []
    burn_from_statements = []

    contract = model_class.objects.filter(id=contract_id).prefetch_related('network').first()
    if not contract:
        return None

    contract_name = ''.join([x.capitalize() for x in contract.token_name.replace('-', ' ').translate(str.maketrans('', '', string.punctuation)).split() if x])
    if not contract_name:
        contract_name = 'CustomizedERC20'
    
    if contract.token_standard == TokenSmartContract.TOKEN_STANDARDS.ERC_20:
        parent_list = ['Context', 'AccessControlEnumerable']
        
        if contract.pausable:
            parent_list.append('ERC20')
            parent_list.append('ERC20Pausable')
        else:
            parent_list.append('ERC20')
        
        
        contract_body = ''

        attribute_statements.append('bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");')
        attribute_statements.append('bytes32 public constant PAUSER_ROLE = keccak256("PAUSER_ROLE");')
    
        # if contract.pausable or contract.mintable:
        #     constructor_statements.append('address owner = _msgSender();')

        if contract.pausable:
            # parent_list.append('Pausable')
            # parent_list.append('ERC20Pausable')
            # import_list.append('@openzeppelin/contracts/security/Pausable.sol')
            import_list.append('@openzeppelin/contracts/token/ERC20/extensions/ERC20Pausable.sol')

            # before_token_transfer_guards = [f'require(!paused(), "{contract_name}: token transfer while paused");']

            constructor_statements.append('_setupRole(PAUSER_ROLE, _msgSender());')

        if contract.burnable:

            burn_statements = ['_burn(_msgSender(), amount);']
            burn_from_statements = [
                'uint256 currentAllowance = allowance(account, _msgSender());',
                f'require(currentAllowance >= amount, "{contract_name}: burn amount exceeds allowance");',
                'unchecked {',
                '    _approve(account, _msgSender(), currentAllowance - amount);',
                '}',
                '_burn(account, amount);'
            ]
        
        if contract.mintable:
            # attribute_statements.append('address public admin;')
            # constructor_statements.append('admin = msg.sender;')
            # TODO: add bridge as the minter
            constructor_statements.append('_setupRole(DEFAULT_ADMIN_ROLE, _msgSender());')
            constructor_statements.append('_setupRole(MINTER_ROLE, _msgSender());')

            network = contract.network 
            if network:
                bridge_address = ''
                # if network.network_id == 1:
                #     bridge_address = settings.ETHEREUM_BRIDGE_CONTRACT_ADDRESS
                if network.network_id == 4:
                    bridge_address = settings.RINKEBY_BRIDGE_CONTRACT_ADDRESS_V2
                elif network.network_id == 5:
                    bridge_address = settings.GOERLI_BRIDGE_CONTRACT_ADDRESS_V2

                if bridge_address:
                    constructor_statements.append(f'address bridge = {bridge_address};')
                    constructor_statements.append('_setupRole(MINTER_ROLE, bridge);')

                    constructor_statements.append('_approve(_msgSender(), bridge, 2**256 - 1);')


            # mint_guards.append('require(msg.sender == admin, "only admin");')
            mint_guards.append(f'require(hasRole(MINTER_ROLE, _msgSender()), "{contract_name}: must have minter role to mint");')
            mint_statements.append('_mint(to, amount);')
        
        if contract.max_supply is not None:
            attribute_statements.append('uint256 private immutable _cap;')
            _mint_guards.append(f'require(totalSupply() + amount <= cap(), "{contract_name}: cap exceeded");')
            _mint_statements.append('super._mint(account, amount);')
            
            constructor_arguments.append('uint256 cap_')
            constructor_guards.append(f'require(cap_ > 0, "{contract_name}: cap is 0");')
            constructor_statements.append('_cap = cap_;')
        
        if contract.initial_supply > 0:
            constructor_arguments.append('uint256 initialSupply_')
            constructor_guards.append(f'require(initialSupply_ > 0, "{contract_name}: initialSupply is less than 1");')
            constructor_statements.append(f'_mint(_msgSender(), {contract.initial_supply}{"0" * contract.decimal});')
            
        # build constructor
        constructor_content = f'    constructor({", ".join(constructor_arguments)}) ERC20(name, symbol) {{\n'
        constructor_content += _format_statements(constructor_guards) + '\n'
        constructor_content += _format_statements(constructor_statements)
        constructor_content += '    }\n\n'
    
        # build contract content
        if attribute_statements:
            for _ in attribute_statements:
                contract_body += f'    {_}\n'
            contract_body += '\n'    

        # if len(constructor_arguments) > 2 or constructor_guards or constructor_statements:
        #     contract_body += constructor_content
        
        contract_body += constructor_content

        if contract.pausable:
            pause_content = '    function pause() public virtual {\n'
            pause_content += f'        require(hasRole(PAUSER_ROLE, _msgSender()), "{contract_name}: must have pauser role to pause");\n'
            pause_content += '        _pause();\n'
            pause_content += '    }\n\n'

            unpause_content = '    function unpause() public virtual {\n'
            unpause_content += f'        require(hasRole(PAUSER_ROLE, _msgSender()), "{contract_name}: must have pauser role to unpause");\n'
            unpause_content += '        _unpause();\n'
            unpause_content += '    }\n\n'

            _before_token_transfer_content = '    function _beforeTokenTransfer(address from, address to, uint256 amount) internal virtual override(ERC20, ERC20Pausable) {\n'
            _before_token_transfer_content += '        super._beforeTokenTransfer(from, to, amount);\n'
            _before_token_transfer_content += '    }\n\n'

            contract_body += pause_content + unpause_content + _before_token_transfer_content 
        
        if contract.burnable:
            burn_content = '    function burn(uint256 amount) public virtual {\n'
            burn_content += _format_statements(burn_statements)
            burn_content += '    }\n\n'
            
            contract_body += burn_content

            burn_from_content = '    function burnFrom(address account, uint256 amount) public virtual {\n'
            burn_from_content += _format_statements(burn_from_statements)
            burn_from_content += '    }\n\n'

            contract_body += burn_from_content
        
        if contract.mintable:
            mint_content = '    function mint(address to, uint amount) external {\n'
            mint_content += _format_statements(mint_guards)
            mint_content += _format_statements(mint_statements)
            mint_content += '    }\n\n'

            contract_body += mint_content
        
        if contract.max_supply is not None:
            cap_content = '    function cap() public view virtual returns (uint256) {\n'
            cap_content += '        return _cap;\n'
            cap_content += '    }\n\n'

            contract_body += cap_content

            _mint_content = '    function _mint(address account, uint256 amount) internal virtual override {\n'
            _mint_content += _format_statements(_mint_guards)
            _mint_content += _format_statements(_mint_statements)
            _mint_content += '    }\n\n'

            contract_body += _mint_content
        
        if contract.decimal != 18:
            decimal_content = '    function totalSupply() public view virtual override returns (uint256) {\n'
            decimal_content += '        return _totalSupply;\n'
            decimal_content += '    }\n\n'

            contract_body += decimal_content

        # build final content
        content = f'{header}\npragma solidity {pragma_version};\n\n'
        for _ in import_list:
            content += f"import \"{_}\";\n"
        
        content += "\n" + f"contract {contract_name} is {', '.join(parent_list)} {{\n" + contract_body + '}'

    elif contract.token_standard == TokenSmartContract.TOKEN_STANDARDS.ERC_1155:
        pass
    elif contract.token_standard == TokenSmartContract.TOKEN_STANDARDS.ERC_721:
        pass
    elif contract.token_standard == TokenSmartContract.TOKEN_STANDARDS.ERC_777:
        pass

    return content


def compile_contract(content):
    """Compile smart contract
    
    Return abi and binary code
    """

    compiled = compile_source(content, allow_paths=os.path.join(settings.BASE_DIR, 'data'), import_remappings=f"@openzeppelin={os.path.join(settings.BASE_DIR, 'data', 'node_modules', '@openzeppelin')}", output_values=["abi", "bin"])
    contract_id, contract_interface = compiled.popitem()
    
    return contract_interface['abi'], contract_interface['bin']


def get_contract_arguments(contract):
    """Get the arguments for contract constructor"""

    # TODO: fix this or overflow will happen
    
    args = [contract.token_name, contract.token_symbol]

    if contract.max_supply is not None:
        args.append(contract.max_supply)

    if contract.initial_supply > 0:
        args.append(contract.initial_supply)
    return args


def _gen_file(data, dst, template):
    """Generate file from jinja2 template and metadata

    :param data: the metadata for generating
    :type data: dict
    :param dst: the destination path
    :type dst: str
    :param template: jinja2 template
    :type template: ???
    """

    with open(dst, 'w') as f:
        f.write(template.render(data=data))


class GenerateContractSDKError(Exception):
    pass


def _format_snake_case(s):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower() if not s.isupper() else s


def generate_rendering_data(contract):
    contract.abi.seek(0)
    abi_data = json.load(contract.abi)

    functions = []

    for d in abi_data:
        if d['type'] == 'function':

            for inp in d['inputs']:
                if inp['name'] == 'from':
                    inp['name'] = 'from_account'

            functions.append({
                'python_name': _format_snake_case(d['name']),
                **d
            })

    res = {
        'token': {
            'address': contract.address,
        },
        'network': {
            'url': contract.network.url,
        },
        'abi': {
            # 'filename': os.path.basename(contract.abi.name),
            'filename': 'Token.json',
            'functions': functions,
        },
    }

    return res


def generate_token_contract_sdk(contract_id, token_type):
    """Generate SDK for token contract

    :param contract_id: id of the contract
    :type contract_id: str
    :param token_type: token type (fungible|non_fungible)
    :type token_type: str
    :return: result object
    :rtype: dict
    """

    res = {
        'status': 0,
        'output_path': '',
        'detail': ''
    }

    model_class = get_contract_class_from_type(token_type)

    contract = model_class.objects.filter(id=contract_id).prefetch_related('network').first()
    if not contract:
        return None

    if not contract.contract_file:
        raise GenerateContractSDKError("Contract file is None")
    if not contract.abi:
        raise GenerateContractSDKError("Contract abi is None")
    if len(contract.contract_file.name) <= 4 or not contract.contract_file.name.endswith('.sol'):
        raise GenerateContractSDKError("Contract file name is invalid")

    folder_id = os.path.basename(contract.contract_file.name)[:-4]
    output_dir = os.path.join(settings.BASE_DIR, 'data', 'media', 'sdk', folder_id)
    token_output_dir = os.path.join(output_dir, 'token_sdk')
    shutil.rmtree(output_dir, ignore_errors=True)
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    Path(token_output_dir).mkdir(parents=True, exist_ok=True)
    build_dir = os.path.join(token_output_dir, 'build')
    Path(build_dir).mkdir(parents=True, exist_ok=True)
    Path(os.path.join(build_dir, 'abi')).mkdir(parents=True, exist_ok=True)
    Path(os.path.join(token_output_dir, 'contracts')).mkdir(parents=True, exist_ok=True)

    file_loader = FileSystemLoader(os.path.join(settings.BASE_DIR, 'templates', 'sdk'))
    rendering_data = generate_rendering_data(contract)

    env = Environment(loader=file_loader, autoescape=True, trim_blocks=True, lstrip_blocks=True)

    files = (
        ('exceptions.py', 'exceptions.jinja2'),
        ('handler.py', 'sdk_python.jinja2'),
    )

    for t in files:
        if t[1].endswith('.py'):
            shutil.copyfile(os.path.join(settings.BASE_DIR, 'templates', 'sdk', t[1]), os.path.join(token_output_dir, t[0]))
        else:
            _gen_file(rendering_data, os.path.join(token_output_dir, t[0]), env.get_template(t[1]))

    files = (
        ('requirements.txt', 'requirements.jinja2'),
        ('example.py', 'sdk_example.py'),
    )

    for t in files:
        if t[1].endswith('.py'):
            shutil.copyfile(os.path.join(settings.BASE_DIR, 'templates', 'sdk', t[1]), os.path.join(output_dir, t[0]))
        else:
            _gen_file(rendering_data, os.path.join(output_dir, t[0]), env.get_template(t[1]))

    # copy contract code and abi to build folder
    with open(os.path.join(build_dir, 'abi', 'Token.json'), 'wb') as f:
        contract.abi.seek(0)
        f.write(contract.abi.read())

    with open(os.path.join(token_output_dir, 'contracts', 'Token.sol'), 'wb') as f:
        contract.contract_file.seek(0)
        f.write(contract.contract_file.read())

    res['output_path'] = output_dir

    return res


def inspect_fungible_token(token_contract, func_data):
    """Call view method of a token

    :param func_data: dict object contain metadata of func to call
    :type func_data: dict
    :return: result
    :rtype: dict
    """

    web3_client = None
    if token_contract.network.name == "Rinkeby Test Network":
        web3_client = rinkeby_web3
    elif token_contract.network.name == "Goerli Test Network":
        web3_client = goerli_web3

    abi = json.loads(token_contract.abi.read())
    
    token = web3_client.eth.contract(address=token_contract.address, abi=abi)

    func_to_call = getattr(token.functions, func_data['name'])

    res = func_to_call().call(block_identifier='latest')

    output = {
        'value': res,
        'type': 'undefined',
    }

    if isinstance(res, bool):
        output['type'] = 'bool'
    elif isinstance(res, bytes):
        output['type'] = 'bytes'
        output['value'] = res.hex()
    elif isinstance(res, int):
        output['type'] = 'int'
        output['value'] = str(res)
    elif isinstance(res, str):
        if len(res) == 42 and res.startswith('0x'):
            output['type'] = 'address'
        else:
            output['type'] = 'string'
    
    return [output]



'''
Here is the example script demonstrating how to use the token SDK

'''
from token_sdk.handler import TokenContractHandler

# DEFINE ACCOUNTS
# Please change these accounts before running the example !
# Also, make sure ACC1 has at least 20 tokens in balance.
ACC1 = ''
ACC1_PRIVATE_KEY = ''
ACC2 = ''
ACC2_PRIVATE_KEY = ''
ACC3 = ''

def main():
    def has_method(obj, method_name):
        return hasattr(obj.__class__, method_name) and callable(getattr(obj.__class__, method_name))

    # Create token handler for account 1
    handler = TokenContractHandler(sender_address=ACC1, sender_private_key=ACC1_PRIVATE_KEY)

    # Create token handler for account 2
    handler2 = TokenContractHandler(sender_address=ACC2, sender_private_key=ACC2_PRIVATE_KEY)

    # GET BASIC INFORMATION
    name = handler.name()
    symbol = handler.symbol()
    try:
        cap = handler.cap()
    except Exception:
        cap = None
    total_supply = handler.total_supply()
    decimals = handler.decimals()

    print('[*] Basic information:')
    print(f'  - Token: {name}')
    print(f'  - Symbol: {symbol}')
    if cap is not None:
        print(f'  - Total Capacity: {cap}')
    
    print(f'  - Total Supply: {total_supply}')
    print(f'  - Decimals: {decimals}')


    # TRANSFER TOKEN
    # e.g: transfer token directly from account 1 to account 2
    b1, b2 = handler.balance_of(ACC1), handler.balance_of(ACC2)

    print('\n[*] Transfer token')
    print(f'  - Before transferring 20 tokens from ACC1 to ACC2:')
    print(f'      Balance of {ACC1}: {b1}')
    print(f'      Balance of {ACC2}: {b2}')

    tx_hash = handler.transfer(ACC2, 20)
    handler.wait_for_receipt(tx_hash)
    b1, b2 = handler.balance_of(ACC1), handler.balance_of(ACC2)

    print(f'  - After:')
    print(f'      Balance of {ACC1}: {b1}')
    print(f'      Balance of {ACC2}: {b2}')


    # 3RD PARTY TRANSFER TOKEN
    # e.g: account 1 allows account 2 to transfer 10 tokens to account 3
    print('\n[*] 3rd-party Transfer token')
    print(f'  - ACC1 approve ACC2 to use 10 tokens')
    tx_hash = handler.approve(ACC2, 10)
    handler.wait_for_receipt(tx_hash)

    print(f'  - ACC2 send 10 tokens to ACC3')

    tx_hash = handler2.transfer_from(ACC1, ACC3, 10)
    handler.wait_for_receipt(tx_hash)



    # EXTENSIONS
    # Note:
    #   some methods are not available
    #   if the corresponding extensions are not enabled.

    # Burnable
    if has_method(handler, 'burn'):
        print('\n[*] Extension: Burnable')
        print('  - Burn 10 tokens from account 2:')
        print(f'      Before: {handler.balance_of(ACC2)}')
        tx_hash = handler2.burn(10)
        handler.wait_for_receipt(tx_hash)
        print(f'      After: {handler.balance_of(ACC2)}')

    # Mintable
    if has_method(handler, 'mint'):
        print('\n[*] Extension: Mintable')
        b3 = handler.balance_of(ACC3)
        tx_hash = handler.mint(ACC3, 1000)
        handler.wait_for_receipt(tx_hash)
        print('  - 1000 tokens has been minted for account 3')
        print(f'    - Balance of account 3:')
        print(f'      Before: {b3}')
        print(f'      After:  {handler.balance_of(ACC3)}')

    # Pausable
    if has_method(handler, 'pause') and has_method(handler, 'unpause'):
        print('\n[*] Extension: Pausable')

        tx_hash = handler.pause()
        handler.wait_for_receipt(tx_hash)

        print('  - PAUSER has paused the token')
        try:
            tx_hash = handler2.transfer(ACC3, 10)
            handler.wait_for_receipt(tx_hash)
        except:
            print('      Should raise exception when token is paused')

        tx_hash = handler.unpause()
        handler.wait_for_receipt(tx_hash)

        print('  - PAUSER has unpaused the token')

        try:
            tx_hash = handler2.transfer(ACC3, 10)
            handler.wait_for_receipt(tx_hash)
            print('      Should not raise exception when token is unpaused')
        except Exception as e:
            pass


if __name__ == '__main__':
    main()

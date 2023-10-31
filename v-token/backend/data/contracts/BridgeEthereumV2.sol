// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import '@openzeppelin/contracts/token/ERC20/IERC20.sol';
import './IToken.sol';

contract BridgeBase {
    address public admin;
    // IToken public token;
    uint public nonce;
    mapping(uint => bool) public processedNonces;

    enum Step { Burn, Mint }
    event Transfer(
        address from,
        address to,
        address token,
        uint amount,
        uint date,
        uint nonce,
        Step indexed step
    );

    constructor(){
        admin = msg.sender;
        // token = IToken(_token);
    }

    function burn(address _token, address to, uint amount) external {
        IToken token = IToken(_token);
        
        token.burnFrom(msg.sender, amount);

        emit Transfer(
            msg.sender,
            to,
            _token,
            amount,
            block.timestamp,
            nonce,
            Step.Burn
        );
        nonce++;
    }

    function mint(address _token, address to, uint amount, uint otherChainNonce) external {
        // require(msg.sender == admin, 'only admin');
        require(processedNonces[otherChainNonce] == false, 'transfer already processed');
        processedNonces[otherChainNonce] = true;
        IToken token = IToken(_token);
        token.mint(to, amount);

        emit Transfer(
            msg.sender,
            to,
            _token,
            amount,
            block.timestamp,
            otherChainNonce,
            Step.Mint
        );
    }
}
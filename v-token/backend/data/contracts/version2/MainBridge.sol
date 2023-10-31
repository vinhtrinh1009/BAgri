// SPDX-License-Identifier: MIT

pragma solidity ^0.8.11;

import { IToken } from './IMainToken.sol';


contract MainBridge {
    address public admin;
    uint public nonce;
    mapping(uint => bool) public processedNonces;

    event TokensLocked(address indexed requester, uint256 amount, uint256 timestamp, uint256 nonce);
    event TokensUnlocked(address indexed requester, uint256 amount, uint256 timestamp, uint256 nonce);

    constructor() {
        admin = msg.sender;
    }

    function lock(address _token, uint256 amount) external {
        IToken token = IToken(_token);
        token.transfer(address(this), amount);
        // token.transferFrom(_requester, address(this), amount);
        emit TokensLocked(msg.sender, amount, block.timestamp, nonce);
        nonce++;
    }

    function unlock(address _token, address _requester, uint256 amount, uint256 _nonce) onlyAdmin external {
        require(processedNonces[_nonce] == false, "transfer already processed");
        processedNonces[_nonce] = true;

        IToken token = IToken(_token);
        token.transferFrom(address(this), _requester, amount);
        emit TokensUnlocked(_requester, amount, block.timestamp, _nonce);
    }

    modifier onlyAdmin {
      require(msg.sender == admin, "only admin can execute this function");
      _;
    }
}
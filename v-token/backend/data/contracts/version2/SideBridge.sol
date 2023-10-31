// SPDX-License-Identifier: MIT

pragma solidity ^0.8.11;

import { IToken } from "./ISideToken.sol";

contract SideBridge {
    // event BridgeInitialized(uint256 indexed timestamp);
    // event TokensBridged(address indexed requester, bytes32 indexed mainDepositHash, uint256 amount, uint256 timestamp);
    // event TokensReturned(address indexed requester, bytes32 indexed sideDepositHash, uint256 amount, uint256 timestamp);
    event TokensBridged(address indexed _requester, uint256 amount, uint256 timestamp, uint256 nonce);
    event TokensReturned(address indexed _requester, uint256 amount, uint256 timestamp, uint256 nonce);


    // IToken private sideToken;
    address public admin;
    // bool bridgeInitState;
    // address owner;
    // address gateway;
    
    

    constructor () {
        admin = msg.sender;
    }

    // constructor (address _gateway) {
        // gateway = _gateway;
        // owner = msg.sender;
    // }

    // function initializeBridge (address _childTokenAddress) onlyOwner external {
    //     sideToken = IToken(_childTokenAddress);
    //     // bridgeInitState = true;
    // }

    function bridgeTokens (address _token, address _requester, uint256 amount, uint256 _nonce) onlyAdmin  external {
        IToken sideToken = IToken(_token);
        sideToken.mint(_requester, amount);
        emit TokensBridged(_requester, amount, block.timestamp, _nonce);
    }

    function returnTokens (address _token, address _requester, uint256 amount, uint256 _nonce) onlyAdmin external {
        IToken sideToken = IToken(_token);
        sideToken.burnFrom(_requester, amount);
        emit TokensReturned(_requester, amount, block.timestamp, _nonce);
    }

    // modifier verifyInitialization {
    //   require(bridgeInitState, "Bridge has not been initialized");
    //   _;
    // }
    
    // modifier onlyAdmin {
    //   require(msg.sender == gateway, "Only gateway can execute this function");
    //   _;
    // }

    // modifier onlyOwner {
    //   require(msg.sender == owner, "Only owner can execute this function");
    //   _;
    // }

    modifier onlyAdmin {
      require(msg.sender == admin, "Only admin can execute this function");
      _;
    }
    

}

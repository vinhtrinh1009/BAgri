pragma solidity ^0.8.11;

interface IToken {
    // function mint(address to, uint amount) external;
    // function burnFrom(address owner, uint amount) external;
    function transfer(address recipient, uint256 amount) external returns (bool);
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
}
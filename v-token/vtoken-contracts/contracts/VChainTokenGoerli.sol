// SPDX-License-Identifier: MIT

pragma solidity ^0.8.11;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/AccessControlEnumerable.sol";
import "@openzeppelin/contracts/utils/Context.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Pausable.sol";

contract VchainTokenGoerli is Context, AccessControlEnumerable, ERC20, ERC20Pausable {
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    bytes32 public constant PAUSER_ROLE = keccak256("PAUSER_ROLE");
    uint256 private immutable _cap;

    constructor(string memory name, string memory symbol, uint256 cap_, uint256 initialSupply_) ERC20(name, symbol) {
        require(cap_ > 0, "VchainTokenGoerli: cap is 0");
        require(initialSupply_ > 0, "VchainTokenGoerli: initialSupply is less than 1");

        _setupRole(PAUSER_ROLE, _msgSender());
        _setupRole(DEFAULT_ADMIN_ROLE, _msgSender());
        _setupRole(MINTER_ROLE, _msgSender());
        address bridge = 0x4b4E91159E41d614294d8f2EEcC700d13C342528;
        _setupRole(MINTER_ROLE, bridge);
        _approve(_msgSender(), bridge, 2**256 - 1);
        _cap = cap_;
        _mint(_msgSender(), 100000000000000000000);
    }

    function pause() public virtual {
        require(hasRole(PAUSER_ROLE, _msgSender()), "VchainTokenGoerli: must have pauser role to pause");
        _pause();
    }

    function unpause() public virtual {
        require(hasRole(PAUSER_ROLE, _msgSender()), "VchainTokenGoerli: must have pauser role to unpause");
        _unpause();
    }

    function _beforeTokenTransfer(address from, address to, uint256 amount) internal virtual override(ERC20, ERC20Pausable) {
        super._beforeTokenTransfer(from, to, amount);
    }

    function burn(uint256 amount) public virtual {
        _burn(_msgSender(), amount);
    }

    function burnFrom(address account, uint256 amount) public virtual {
        uint256 currentAllowance = allowance(account, _msgSender());
        require(currentAllowance >= amount, "VchainTokenGoerli: burn amount exceeds allowance");
        unchecked {
            _approve(account, _msgSender(), currentAllowance - amount);
        }
        _burn(account, amount);
    }

    function mint(address to, uint amount) external {
        require(hasRole(MINTER_ROLE, _msgSender()), "VchainTokenGoerli: must have minter role to mint");
        _mint(to, amount);
    }

    function cap() public view virtual returns (uint256) {
        return _cap;
    }

    function _mint(address account, uint256 amount) internal virtual override {
        require(ERC20.totalSupply() + amount <= cap(), "VchainTokenGoerli: cap exceeded");
        super._mint(account, amount);
    }

}
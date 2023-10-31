const { expect, assert } = require("chai");
const { BigNumber } = require("ethers");
const { ethers } = require("hardhat");


describe("CrossChainBridge", () => {
  let deployer;
  let account1;
  let account2;
  let rinkebyBridge;
  let goerliBridge;
  let token;

  beforeEach(async () => {
    const signers = await ethers.getSigners();
    deployer = signers[0];
    account1 = signers[1];
    account2 = signers[2];

    const factory = await ethers.getContractFactory("Bridge");
    rinkebyBridge = await factory.deploy();
    await rinkebyBridge.deployed();

    const tokenFactory1 = await ethers.getContractFactory("VchainTokenRinkeby");
    token = await tokenFactory1.connect(account1).deploy("VChain Token", "VCHAIN", BigNumber.from(1000000).mul(BigNumber.from(10).pow(18)), BigNumber.from(100).mul(BigNumber.from(10).pow(18)));
    await token.deployed();
  });

  if("Should has cap")

  it("Should emit event when burn token", async () => {
    await token.connect(account1).approve(rinkebyBridge.address, BigNumber.from(2).pow(256).sub(1));
    const tx = await rinkebyBridge.connect(account1).burn(token.address, account2.address, 1);

    const receipt = await tx.wait();

    const eventArgs = receipt.events[2].args;

    assert.equal(eventArgs.token, token.address);
  });

  it("Should not be able to burn token if not approved", async () => {
    await expect(rinkebyBridge.connect(account1).burn(token.address, account2.address, 1)).to.be.revertedWith("VchainTokenRinkeby: burn amount exceeds allowance");
  });

  it("Should be able to mint token", async () => {
    await token.connect(account1).grantRole(ethers.utils.keccak256(ethers.utils.toUtf8Bytes("MINTER_ROLE")), rinkebyBridge.address);

    await rinkebyBridge.mint(token.address, account2.address, BigNumber.from(1000000).mul(BigNumber.from(10).pow(18)), 1);
  })
});

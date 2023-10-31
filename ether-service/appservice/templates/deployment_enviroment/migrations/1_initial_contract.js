const Contracts = artifacts.require("contract");

module.exports = function (deployer) {
  deployer.deploy(Contracts);
};

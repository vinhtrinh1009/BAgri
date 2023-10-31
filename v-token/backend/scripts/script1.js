const hre = require("hardhat");

async function main() {
    const network = await hre.ethers.getDefaultProvider().getNetwork();
    console.log("Network name=", network.name);
    console.log("Network chain id=", network.chainId);
}


// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
});

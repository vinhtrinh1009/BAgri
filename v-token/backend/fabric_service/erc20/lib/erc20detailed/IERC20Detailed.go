package erc20detailed

import "github.com/hyperledger/fabric-chaincode-go/shim"

/*DetailedTokenInterface implements Name, Symbol & Decimal*/
type DetailedTokenInterface interface {
	GetName(stub shim.ChaincodeStubInterface) (string, error)

	GetSymbol(stub shim.ChaincodeStubInterface) (string, error)

	GetDecimals(stub shim.ChaincodeStubInterface) (string, error)
}

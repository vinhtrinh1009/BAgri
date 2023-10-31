import { Link } from "@material-ui/core";

function getHost() {
  const url = process.env.REACT_APP_BACKEND_URL;
  const parts = url.split(":");
  parts.pop();
  const host = parts.join(":");
  //  console.log(host);
  return host;
}

function getLinkFromTxid(txid, length = 20) {
  return (
    <Link target="_blank" href={`${process.env.REACT_APP_EXPLORER_URL}/#/transactions/${txid}`}>
      {txid.slice(0, length)}...
    </Link>
  );
}

export { getHost, getLinkFromTxid };

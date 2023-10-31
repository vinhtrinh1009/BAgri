import { Link } from "@material-ui/core";

function getHost() {
  const url = process.env.REACT_APP_BACKEND_URL;
  const parts = url.split(":");
  parts.pop();
  const host = parts.join(":");
  //  console.log(host);
  return host;
}

function getLinkFromTxid(txid, length) {
  if (!length) length = 30;
  return (
    <Link target="_blank" href={`${process.env.REACT_APP_EXPLORER_URL}/#/transactions/${txid}`}>
      {txid.slice(0, length)}...
    </Link>
  );
}

function toDateTimeString(timestamp) {
  return ` ${new Date(timestamp).toISOString().split("T")[0]}, ${new Date(timestamp).toISOString().split("T")[1].split(".")[0]}`;
}

export { getHost, getLinkFromTxid, toDateTimeString };

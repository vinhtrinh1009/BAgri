import { makeStyles } from "@material-ui/core";
import { useEffect, useState } from "react";
import { useParams } from "react-router";
import View from "../../shared/View";
import DecryptedCertInfo from "./DecryptedCertInfo";
import axios from "axios";
import DecryptedResult from "./DecryptedResult";
import { ERR_TOP_CENTER } from "../../utils/snackbar-utils";
import { useSnackbar } from "notistack";

const useStyles = makeStyles((theme) => ({
    root: {
        "& > *": {
            marginBottom: theme.spacing(3),
        },
        marginLeft: "-32px",
        marginRight: "-32px",
    },
}));

export default function VerifyDataResult(props) {
    const cls = useStyles();
    const { token } = useParams();
    const [dataTxId, setDataTxID] = useState({ certificate: "", result: [] });
    const { enqueueSnackbar } = useSnackbar();

    useEffect(() => {
        checkTocken(token);
    }, []);
    async function checkTocken(token) {
        try {
            const decodeTokenResponse = await axios.get(`${process.env.REACT_APP_SCHOOL_BACKEND_URL}/api/v1/student/decode-token/?token=${token}`);
            console.log(decodeTokenResponse.data);
            setDataTxID(decodeTokenResponse.data.data);
        } catch (error) {
            console.error(error);
            error.response && enqueueSnackbar("Token không hợp lệ: " + JSON.stringify(error.response.data), ERR_TOP_CENTER);
        }
    }
    return (
        <View title="Kết quả xác thực">
            <div className={cls.root}>
                <DecryptedCertInfo cert_txid={dataTxId.certificate}></DecryptedCertInfo>
                <DecryptedResult results_txid={dataTxId.result}></DecryptedResult>
            </div>
        </View>
    );
}

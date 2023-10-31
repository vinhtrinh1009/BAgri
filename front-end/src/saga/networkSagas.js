import { takeEvery, put, call } from 'redux-saga/effects';
import { DELETE_NETWORK } from 'src/redux/User/Networks/actionTypes';
import { GET_NETWORK_BY_ID } from 'src/redux/User/Networks/actionTypes';
import { GET_NETWORK } from 'src/redux/User/Networks/actionTypes';
import { networkActions } from 'src/redux/User/Networks/reducer';
import { getNetworkById } from 'src/services/User/networks';
import { deleteNetwork, getNetwork } from 'src/services/User/networks';


function* getRecomnendNetwork({ payload }) {
    // const { params } = payload
    try {
        const response = yield call(getNetwork, payload)
        yield put(networkActions.getNetworkSuccessful(response.data.data))
    } catch (err) {
        const error = err.response ? err.response.data.msg : err.stack
        // yield put(networkActions.fail(error));
    }
}
function* getRecomnendNetworkById({ payload }) {
    // const { params } = payload
    try {
        const response = yield call(getNetworkById, payload)
        yield put(networkActions.getNetworkByIdSuccessful(response.data.data))
    } catch (err) {
        const error = err.response ? err.response.data.msg : err.stack
        // yield put(networkActions.fail(error));
    }
}
function* deleteRecomnendNetwork({ payload }) {
    const { params } = payload
    try {
        const response = yield call(deleteNetwork, payload)
        yield put(networkActions.deleteNetworkSuccessful(response.data.data))
    } catch (err) {
        const error = err.response ? err.response.data.msg : err.stack
        // yield put(networkActions.fail(error));
    }
}

function* networkSagas() {
    yield takeEvery(GET_NETWORK, getRecomnendNetwork)
    yield takeEvery(GET_NETWORK_BY_ID, getRecomnendNetworkById)
    yield takeEvery(DELETE_NETWORK, deleteRecomnendNetwork)
}

export default networkSagas
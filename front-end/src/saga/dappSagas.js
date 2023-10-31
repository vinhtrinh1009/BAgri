import { takeEvery, put, call } from 'redux-saga/effects';
import { 
    GET_DAPPS,
    CREATE_DAPP
} from 'src/redux/User/DApps/actionTypes';

import { dappActions } from 'src/redux/User/DApps/reducer';
import { getDApps, createDApp } from "src/services/User/dapps"


function* getUserDapps() {
    try {
        const response = yield call(getDApps)
        if (response.data.status == 'success') {
            yield put(dappActions.getDAppsSuccessful(response.data.data))
        } else {

        }
    } catch (error) {

    }
}

function* createNewDApp({ payload }) {
    try {
        const response = yield call(createDApp, payload.body)
        if (response.data.status == 'success') {
            yield put(dappActions.createDAppsSuccessful(response.data.data))
        } else {

        }
    } catch (error) {

    }
}

function* dappSagas() {
    yield takeEvery(GET_DAPPS, getUserDapps)
    yield takeEvery(CREATE_DAPP, createNewDApp)
}

export default dappSagas
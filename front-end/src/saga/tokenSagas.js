import { takeEvery, put, call } from 'redux-saga/effects';
import { 
    GET_FT_TOKENS, GET_NFT_TOKENS
} from 'src/redux/User/Tokens/actionTypes';

import { tokensActions } from 'src/redux/User/Tokens/reducer';
import { getFTTokens, getNFTTokens } from "src/services/User/tokens"


function* getUserFTTokens(action) {
    try {
        const response = yield call(getFTTokens, action.params)
        if (response) {
            console.log(response.data)
            yield put(tokensActions.getFTTokensSuccessful(response.data))
        } else {

        }
    } catch (error) {

    }
}

function* getUserNFTTokens() {
    try {
        const response = yield call(getNFTTokens)
        if (response) {
            console.log(response.data)
            yield put(tokensActions.getNFTTokensSuccessful(response.data))
        } else {

        }
    } catch (error) {

    }
}

// function* createDApp({ payload }) {

// }

function* tokenSagas() {
    yield takeEvery(GET_FT_TOKENS, getUserFTTokens)
    yield takeEvery(GET_NFT_TOKENS, getUserNFTTokens)
}

export default tokenSagas
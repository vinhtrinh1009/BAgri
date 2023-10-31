import { combineReducers } from "redux";
import { all } from "redux-saga/effects";

import DApp from "src/redux/User/DApps/reducer";
import dappSagas from "src/saga/dappSagas";

import Network from "src/redux/User/Networks/reducer";
import networkSagas from "src/saga/networkSagas";

import Storage from "src/redux/User/Storages/reducer";
// import storageSagas from "src/saga/storageSagas";

import User from "src/redux/Guest/reducer";
import userSagas from "src/saga/userSagas";

import Token from "src/redux/User/Tokens/reducer";
import tokenSagas from "src/saga/tokenSagas";

import Setting from "src/redux/User/Settings/reducer";
import settingSagas from "src/saga/settingSagas";

import Alert from "src/redux/User/Alerts/reducer";

export const reducers = combineReducers({
    DApp,
    Network,
    Storage,
    User,
    Token,
    Setting,
    Alert,
});

export function* rootSaga() {
    yield all([dappSagas(), networkSagas(), userSagas(), tokenSagas(), settingSagas()]);
}

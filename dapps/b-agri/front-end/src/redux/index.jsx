import { combineReducers } from "redux";
import { all } from "redux-saga/effects";
import seasonSagas from "src/saga/seasonSagas";
import Season from "src/redux/Season/reducer";

export const reducers = combineReducers({
    Season,
});

export function* rootSaga() {
    yield all([seasonSagas()]);
}

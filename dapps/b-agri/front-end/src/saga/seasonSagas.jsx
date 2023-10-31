import { GET_SEASON_BY_ID } from "src/redux/Season/actionTypes";
import { seasonActions } from "src/redux/Season/reducer";
import { getSeasonByID } from "src/services/season";
import { takeEvery, put, call } from "redux-saga/effects";

function* getSeasonById({ payload }) {
    try {
        const response = yield call(getSeasonByID, payload);
        if (response) {
            console.log(response.data);
            yield put(seasonActions.getSeasonSuccessful(response.data.season));
        } else {
        }
    } catch (error) {
        console.error(error);
    }
}
function* seasonSagas() {
    yield takeEvery(GET_SEASON_BY_ID, getSeasonById);
}

export default seasonSagas;

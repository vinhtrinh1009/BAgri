import { ADD, GET_SEASON_BY_ID, GET_SEASON_BY_ID_FAIL, GET_SEASON_BY_ID_SUCCESSFUL, START_DATE } from "./actionTypes";

const initial_state = {
    season: "",
    start_date: null,
};

export default (state = initial_state, action) => {
    switch (action.type) {
        case GET_SEASON_BY_ID_SUCCESSFUL:
            return { ...state, season: action.payload };
        case START_DATE:
            return { ...state, start_date: action.payload };

        default:
            return { ...state };
    }
};

export const seasonActions = {
    getSeason: (params) => ({ type: GET_SEASON_BY_ID, payload: params }),
    getSeasonSuccessful: (params) => ({ type: GET_SEASON_BY_ID_SUCCESSFUL, payload: params }),
    getSeasonFail: (params) => ({ type: GET_SEASON_BY_ID_FAIL, payload: params }),
};

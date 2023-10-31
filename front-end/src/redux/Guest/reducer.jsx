import {
    GET_PROFILE,
    GET_PROFILE_SUCCESS,
    GET_PROFILE_FAIL,
    UPDATE_PROFILE,
    UPDATE_PROFILE_SUCCESS,
    UPDATE_PROFILE_FAIL
} from "./actionTypes"
const initial_state = {
    user: {
        folder_id: ""
    }
}

export default (state = initial_state, action) => {

    switch (action.type) {
        case GET_PROFILE_SUCCESS:
            return { ...state, user: action.payload }
        case UPDATE_PROFILE_SUCCESS:
            return {}
        default: return { ...state };
    }
}

export const userActions = {
    getProfile: (params) => ({ type: GET_PROFILE, payload: params }),
    getProfileSuccessful: (payload) => ({ type: GET_PROFILE_SUCCESS, payload: payload }),
    updateProfile: (payload) => ({ type: UPDATE_PROFILE, payload: payload }),
    updateProfileSuccessful: (payload) => ({ type: UPDATE_PROFILE_SUCCESS, payload: payload })
}
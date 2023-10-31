import { GET_FT_TOKENS, GET_FT_TOKENS_SUCCESSFUL, GET_NFT_TOKENS, GET_NFT_TOKENS_SUCCESSFUL, DISPLAY_TOKEN } from "./actionTypes";

const initial_state = {
    list_ft_tokens: [],
    list_nft_tokens: [],
    display_token: null
}

export default (state = initial_state, action) => {
    switch (action.type) {
        case GET_FT_TOKENS_SUCCESSFUL:
            return { ...state, list_ft_tokens: action.payload }
        case GET_NFT_TOKENS_SUCCESSFUL:
            return { ...state, list_nft_tokens: action.payload}  
        case DISPLAY_TOKEN:
            return { ...state, display_token: action.payload }
        default:
            return { ...state }
    }
}

export const tokensActions = {
    getFTTokens: (params) => ({ type: GET_FT_TOKENS, params }),
    getNFTTokens: () => ({ type: GET_NFT_TOKENS }),
    getFTTokensSuccessful: (params) => ({ type: GET_FT_TOKENS_SUCCESSFUL, payload: params }),
    getNFTTokensSuccessful: (params) => ({ type: GET_NFT_TOKENS_SUCCESSFUL, payload: params })
}
import { GET_NETWORK_SUCCESSFUL } from "./actionTypes";
import { DELETE_NETWORK } from "./actionTypes";
import { GET_NETWORK_BY_ID } from "./actionTypes";
import { NAVIGATE } from "./actionTypes";
import { GET_NETWORK_BY_ID_SUCCESSFUL } from "./actionTypes";
import { DELETE_NETWORK_SUCCESSFUL } from "./actionTypes";
import { VIEW_MORE } from "./actionTypes";
import { GET_NETWORK } from "./actionTypes";
import { CLUSTER_NAME, CONSENSUS, ENGINE_BLOCKCHAIN, NUMBER_NODES, NUMBER_OF_PEERS, ADD_ORGANIZATIONS, UPDATE_ORGANIZATIONS, DELETE_ORGANIZATIONS, NODE_PLAN } from "./actionTypes";

const initial_state = {
    list_network: [],
    engineBlockchain: "",
    consensus: "",
    clusterName: "",
    numberNodes: "",
    numberOfPeers: 1,
    organizations: [{ name: "", number_peer: 1 }],
    nodePlan: null,
    viewMore: null,
    dappInNetwork: null,
    navigate: false,
};

export default (state = initial_state, action) => {
    switch (action.type) {
        case NAVIGATE:
            return { ...state, navigate: action.payload };
        case ENGINE_BLOCKCHAIN:
            return { ...state, engineBlockchain: action.payload };
        case CONSENSUS:
            return { ...state, consensus: action.payload };
        case NUMBER_NODES:
            return { ...state, numberNodes: action.payload };
        case NUMBER_OF_PEERS:
            return { ...state, numberOfPeers: action.payload };
        case CLUSTER_NAME:
            return { ...state, clusterName: action.payload };
        case ADD_ORGANIZATIONS:
            return { ...state, organizations: [...state.organizations, action.payload] };
        case UPDATE_ORGANIZATIONS:
            return { ...state, organizations: action.payload };
        case DELETE_ORGANIZATIONS:
            return { ...state, organizations: action.payload };
        case NODE_PLAN:
            return { ...state, nodePlan: action.payload };
        case VIEW_MORE:
            return { ...state, viewMore: action.payload };
        case GET_NETWORK_SUCCESSFUL:
            return { ...state, list_network: action.payload };
        case GET_NETWORK_BY_ID_SUCCESSFUL:
            return { ...state, dappInNetwork: action.payload };
        default:
            return { ...state };
    }
};

export const networkActions = {
    getNetwork: (params) => ({ type: GET_NETWORK, payload: params }),
    getNetworkSuccessful: (params) => ({ type: GET_NETWORK_SUCCESSFUL, payload: params }),
    deleteNetwork: (params) => ({ type: DELETE_NETWORK, payload: params }),
    deleteNetworkSuccessful: (params) => ({ type: DELETE_NETWORK_SUCCESSFUL, payload: params }),
    getNetworkById: (params) => ({ type: GET_NETWORK_BY_ID, payload: params }),
    getNetworkByIdSuccessful: (params) => ({ type: GET_NETWORK_BY_ID_SUCCESSFUL, payload: params }),
};

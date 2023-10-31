export const initialAttribute = {
    name: "",
    type: "string",
    encrypt: false,
    description: "",
    idAttr: "",
};

export const initialEntity = {
    name: "",
    attributes: [],
    primary_key: null,
    relationships: [],
    color: "",
    description: "",
};

export const initialNode = {
    id: "",
    position: {},
    type: "customNode",
    data: initialEntity,
};

export const colors = ["#b8c2cc", "#5db0b9", "#84cc16", "#23d3ee", "#4dc0b5", "#3490dc", "#f66d9b", "#6574cd", "#9561e2", "#ffed4a", "#f6993f", "#e3342f"];

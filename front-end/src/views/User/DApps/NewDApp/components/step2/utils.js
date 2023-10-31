export const checkNameEntityUnique = (arrObj, lengtharr, name, idEntity) => {
    for (let i = 0; i < lengtharr; i++) {
        if (arrObj[i].data.name === name && arrObj[i].id != idEntity) {
            return false;
        }
    }
    return true;
};

export const checkNameAttrUnique = (arrObj, lengtharr, name, idAttr) => {
    for (let i = 0; i < lengtharr; i++) {
        if (arrObj[i].name === name && arrObj[i].idAttr != idAttr) {
            return false;
        }
    }
    return true;
};

export const findNodeById = (listNode, lengthList, idNode) => {
    const length = lengthList || listNode.length;
    for (let i = 0; i < length; i++) {
        if (listNode[i].id === idNode) {
            return listNode[i];
        }
    }
    return null;
};

export const swapSourceTarget = (params) => {
    return {
        source: params.target,
        sourceHandle: params.target + "sright",
        target: params.source,
        targetHandle: params.source + "tleft",
    };
};

export const reverseString = (str) => {
    var newString = "";
    for (var i = str.length - 1; i >= 0; i--) {
        newString += str[i];
    }
    return newString;
};

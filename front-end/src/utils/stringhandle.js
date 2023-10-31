export const isPositiveNumber = (str) => {
    // return /^\+?(0|[1-9]\d*)$/.test(str);
    if (/^\+?([0-9]\d*)$/.test(str)) {
        if (Number(str) > 0) return true;
    } else {
        return false;
    }
};

export const isStringNumber = (str) => {
    return /^[\+\-]?\d*\.?\d+(?:[Ee][\+\-]?\d+)?$/.test(str);
};

export const isOnlyLetterAndNumber = (str) => {
    return !/[^A-Za-z0-9]+/g.test(str);
};

export const isOnlyLowerLetterAndNumber = (str) => {
    return !/[^a-z0-9]+/g.test(str);
};

export const isStringOnlyNumberNotSign = (str) => {
    return /^\d+$/.test(str);
};

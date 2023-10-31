export const exchangeSizeValue = (num) => {
    if (num == 0) return "0 Kb";
    if (num < 1024) return `${Math.round(num)} Byte`;
    if (num < 1048576) return `${Math.round(num / 1024)} Kb`;
    if (num < 1073741824) return `${Math.round(num / (1024 * 1024))} Mb`;
    return `${Math.round(num / (1024 * 1024 * 1024))} Gb`;
};

import { format, formatDistanceToNow } from "date-fns";

// ----------------------------------------------------------------------

export function diffTime(date1, date2) {
    let timediff = new Date(Number(date1) || 0) - new Date(Number(date2) || 0);
    if (timediff < 360000) {
        return `${Math.ceil(timediff / 60000)} phút`;
    }
    if (timediff >= 3600000 && timediff < 86400000) {
        return `${Math.floor(timediff / 3600000)} giờ ${timediff % 3600000 ? (timediff % 3600000) + " phút" : ""}`;
    }
    return new Date(date1) - new Date(date2);
}

export function fDate(date) {
    return format(new Date(Number(date) || 0), "HH:mm dd-MM-yyyy");
}

export function fDateTime(date) {
    return format(new Date(date), "dd MMM yyyy HH:mm");
}

export function fDateTimeSuffix(date) {
    return format(new Date(date), "dd/MM/yyyy hh:mm p");
}

export function fToNow(date) {
    return formatDistanceToNow(new Date(date), {
        addSuffix: true,
    });
}

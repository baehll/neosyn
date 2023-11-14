function formatNumbers(i) {
    return i.toString().padStart(2, "0")
}

const utils = {
    dateFormatter: (d) => {
        return `${formatNumbers(d.getDay())}.${formatNumbers(d.getMonth())}.${d.getFullYear()}, ${formatNumbers(d.getHours())}:${formatNumbers(d.getMinutes())} Uhr`
    }
}

export default utils;
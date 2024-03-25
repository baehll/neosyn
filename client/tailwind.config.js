/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,vue}",
    ],
    theme: {
        extend: {
            colors: {
                primary: '#ACED84',
                black: '#1E1E1E',
                lightgray: '#4F4F4F',
                'lightgray-90': '#6f6f6f',
                'lightgray-80': '#494949',
                'lightgray-60': '#BFBFBF',
                'lightgray-10': '#BBBBBB',
                darkgray: '#2C2C2C',
                'darkgray-80': '#6F6F6F',

            },
            fontFamily: {
                'neuebit': ['PP NeueBit', 'sans-serif'],
                'archimoto': ['Archimoto V01', 'sans-serif'],
                'mondwest': ['PP Mondwest', 'sans-serif'],
                'nimbus': ['Nimbus', 'sans-serif'],
            },
        },
    },
    plugins: [],
}


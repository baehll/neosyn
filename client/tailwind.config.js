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
                'primary-10': '#D9FFC1',
                black: '#1E1E1E',
                lightgray: '#4F4F4F',
                'lightgray-90': '#6f6f6f',
                'lightgray-80': '#494949',
                'lightgray-70': '#444',
                'lightgray-60': '#BFBFBF',
                'lightgray-40': '#3e3e3e',
                'lightgray-30': '#3c3c3c',
                'lightgray-20': '#3a3a3a',
                'lightgray-10': '#BBBBBB',
                darkgray: '#2C2C2C',
                'darkgray-10': '#212121',
                'darkgray-20': '#1e1e1e',
                'darkgray-80': '#6F6F6F',

            },
            fontFamily: {
                'roboto': ['Roboto', 'sans-serif'],
                'neuebit': ['PP NeueBit', 'sans-serif'],
                'archimoto': ['Archimoto V01', 'sans-serif'],
                'mondwest': ['PP Mondwest', 'sans-serif'],
                'nimbus': ['Nimbus', 'sans-serif'],
            },
        },
    },
    plugins: [],
}


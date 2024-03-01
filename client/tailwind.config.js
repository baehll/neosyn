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
        'lightgray-80': '#494949',
        'lightgray-10': '#BBBBBB',
        darkgray: '#2C2C2C',

      }
    },
  },
  plugins: [],
}


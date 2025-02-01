/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./templates/**/*.html', './static/css/input.css'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: '#232D3F',
        secondary: '#008170',
        accent: '#005B41',
      },
    },
  },
  plugins: [],
}

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {},
    screens: {
      'sm': '300px',
      'md': '700px',
      'lg': '1000px',
      'xl': '1300px',
      '2xl': '1900px'
    }
  },
  plugins: [],
}


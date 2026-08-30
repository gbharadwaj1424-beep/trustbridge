/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,jsx}",
    "./components/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        teal: {
          DEFAULT: "#028090",
          dark: "#014F58",
        },
        seafoam: "#00A896",
        mint: "#02C39A",
        sand: "#F7F5F0",
        ink: "#0E2A2E",
      },
    },
  },
  plugins: [],
};

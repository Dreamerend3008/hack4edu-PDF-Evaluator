// tailwind.config.js
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx,html}", // Alpine leerá HTML
  ],
  theme: {
    extend: {
      colors: {
        solarized: {
          base03: '#002b36',
          base02: '#073642',
          base01: '#586e75',
          base00: '#657b83',
          base0:  '#839496',
          base1:  '#93a1a1',
          yellow: '#b58900',
          orange: '#cb4b16',
          red:    '#dc322f',
          magenta:'#d33682',
          violet: '#6c71c4',
          blue:   '#268bd2',
          cyan:   '#2aa198',
          green:  '#859900',
        },
      },
      fontFamily: {
        nerd: ['"FiraCode Nerd"', 'monospace'],
      },
    },
  },
  plugins: [],
}

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./pages/**/*.{html,js}", "./src/**/*.{html,js}"],
  theme: {
    extend: {
      fontFamily: {
        mono: ['CaskaydiaMono', 'monospace'],
      },
    },
  },
  plugins: [],
};


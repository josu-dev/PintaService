/* eslint-env node */
/** @type {import('tailwindcss/plugin')} */
const plugin = require('tailwindcss/plugin');

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      screens: {
        xs: '360px'
      }
    }
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
    require('@tailwindcss/aspect-ratio'),
    require('@tailwindcss/container-queries'),
    require('daisyui'),
    plugin(function ({ addUtilities }) {
      addUtilities({
        '.text-balance': {
          'text-wrap': 'balance'
        },
        '.text-pretty': {
          'text-wrap': 'pretty'
        }
      });
    })
  ],
  daisyui: {
    themes: [
      {
        pintaservice: {
          primary: '#fb923c',
          secondary: '#84cc16',
          accent: '#fb7185',
          neutral: '#1c1917',
          'base-100': '#FFF8EF',
          info: '#60a5fa',
          success: '#34d399',
          warning: '#facc15',
          error: '#f87171'
        }
      }
    ]
  }
};

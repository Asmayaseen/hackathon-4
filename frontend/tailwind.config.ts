import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50:  '#f0f4ff',
          100: '#e0eaff',
          200: '#c7d5ff',
          300: '#9db1ff',
          400: '#7389f5',
          500: '#4f63d2',
          600: '#3d4fc4',
          700: '#2d3db0',
          800: '#1e2e9e',
          900: '#1a237e',
        },
      },
    },
  },
  plugins: [],
}
export default config

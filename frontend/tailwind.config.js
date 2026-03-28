/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive) / <alpha-value>)",
          foreground: "hsl(var(--destructive-foreground) / <alpha-value>)",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
        // io-gita Parchment Theme — Light + Warm
        cosmic: {
          bg: '#F5F0E8',
          'bg-light': '#E8E0D4',
          surface: '#F5F0E8',
          card: 'rgba(245, 240, 232, 0.6)',
          'card-hover': 'rgba(245, 240, 232, 0.8)',
          text: '#1a1a2e',
          'text-secondary': '#4a4a5e',
          'text-muted': '#8B7355',
        },
        sacred: {
          cream: '#F5F0E8',
          gold: {
            DEFAULT: '#B8860B',
            dark: '#9A7B0A',
            light: '#D4A052',
          },
          saffron: {
            DEFAULT: '#B8860B',
            dark: '#9A7B0A',
            light: '#D4A052',
          },
          maroon: '#8B2332',
          brown: '#8B7355',
          text: {
            DEFAULT: '#1a1a2e',
            secondary: '#4a4a5e',
          },
          purple: {
            DEFAULT: '#F5F0E8',
            light: '#E8E0D4',
          },
          violet: '#B8860B',
        },
        minimal: {
          white: '#F5F0E8',
          gray: {
            50: '#F5F0E8',
            100: '#E8E0D4',
            200: 'rgba(139, 115, 85, 0.15)',
            300: 'rgba(139, 115, 85, 0.25)',
            400: '#8B7355',
            500: '#6B5B45',
            600: '#4a4a5e',
            700: '#3a3a4e',
            800: '#2a2a3e',
            900: '#1a1a2e',
          },
          indigo: '#B8860B',
          violet: '#8B2332',
          blue: '#B8860B',
        },
      },
      fontFamily: {
        display: ['Cormorant Garamond', 'IM Fell English', 'Georgia', 'serif'],
        body: ['-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        sacred: ['Cormorant Garamond', 'IM Fell English', 'Georgia', 'serif'],
        decorative: ['IM Fell English', 'Cormorant Garamond', 'serif'],
        cinzel: ['Cormorant Garamond', 'serif'],
        mantra: ['Laila', 'Noto Serif Devanagari', 'Georgia', 'serif'],
        mono: ['JetBrains Mono', 'monospace'],
        handwritten: ['IM Fell English', 'serif'],
      },
      borderRadius: {
        xl: "calc(var(--radius) + 4px)",
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
        xs: "calc(var(--radius) - 6px)",
      },
      boxShadow: {
        xs: "0 1px 2px 0 rgb(0 0 0 / 0.05)",
        soft: "0 4px 20px rgba(0, 0, 0, 0.08), 0 0 10px rgba(184, 134, 11, 0.03)",
        'soft-lg': "0 10px 40px rgba(0, 0, 0, 0.1), 0 0 20px rgba(184, 134, 11, 0.05)",
        'sacred': "inset 0 0 60px rgba(139, 69, 19, 0.1), 0 4px 20px rgba(0, 0, 0, 0.1)",
        'sacred-lg': "inset 0 0 80px rgba(139, 69, 19, 0.12), 0 8px 30px rgba(0, 0, 0, 0.12)",
        'glow-gold': "0 0 20px rgba(184, 134, 11, 0.15), 0 0 40px rgba(184, 134, 11, 0.05)",
        'glow-saffron': "0 0 20px rgba(184, 134, 11, 0.15), 0 0 40px rgba(184, 134, 11, 0.05)",
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
        "caret-blink": {
          "0%,70%,100%": { opacity: "1" },
          "20%,50%": { opacity: "0" },
        },
        "float": {
          "0%, 100%": { transform: "translateY(0px)" },
          "50%": { transform: "translateY(-6px)" },
        },
        "pulse-gold": {
          "0%, 100%": { boxShadow: "0 0 0 0 rgba(184, 134, 11, 0.3)" },
          "50%": { boxShadow: "0 0 0 15px rgba(184, 134, 11, 0)" },
        },
        "shimmer": {
          "0%": { backgroundPosition: "-200% 0" },
          "100%": { backgroundPosition: "200% 0" },
        },
        "fadeIn": {
          from: { opacity: "0", transform: "translateY(8px)" },
          to: { opacity: "1", transform: "translateY(0)" },
        },
        "scrollHint": {
          "0%, 100%": { transform: "translateY(0)", opacity: "0.5" },
          "50%": { transform: "translateY(8px)", opacity: "1" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
        "caret-blink": "caret-blink 1.25s ease-out infinite",
        "float": "float 5s ease-in-out infinite",
        "pulse-gold": "pulse-gold 2s ease-in-out infinite",
        "shimmer": "shimmer 3s ease-in-out infinite",
        "fadeIn": "fadeIn 0.4s ease-out",
        "scrollHint": "scrollHint 2s ease-in-out infinite",
      },
      backgroundImage: {
        'sacred-gradient': 'linear-gradient(135deg, #F5F0E8 0%, #E8E0D4 50%, #F5F0E8 100%)',
        'gold-gradient': 'linear-gradient(135deg, #D4A052 0%, #B8860B 50%, #9A7B0A 100%)',
        'saffron-gradient': 'linear-gradient(135deg, #D4A052 0%, #B8860B 100%)',
        'cosmic-gradient': 'linear-gradient(135deg, #F5F0E8 0%, #E8E0D4 50%, #F5F0E8 100%)',
        'wax-gradient': 'linear-gradient(145deg, #A52A2A 0%, #8B0000 100%)',
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}

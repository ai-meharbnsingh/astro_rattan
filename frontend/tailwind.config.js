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
        // io-gita Dark Theme — Rich & Mystical
        cosmic: {
          bg: '#1a1a2e',
          'bg-light': '#22223a',
          surface: '#22223a',
          card: 'rgba(34, 34, 58, 0.8)',
          'card-hover': 'rgba(40, 40, 68, 0.9)',
          text: '#e8e0d4',
          'text-secondary': '#b8b0a4',
          'text-muted': '#8B7355',
        },
        sacred: {
          cream: '#22223a',
          gold: {
            DEFAULT: '#D4A052',
            dark: '#B8860B',
            light: '#E8C078',
          },
          saffron: {
            DEFAULT: '#D4A052',
            dark: '#B8860B',
            light: '#E8C078',
          },
          maroon: '#C43E4E',
          brown: '#D4A052',
          text: {
            DEFAULT: '#e8e0d4',
            secondary: '#b8b0a4',
          },
          purple: {
            DEFAULT: '#2a2a4e',
            light: '#22223a',
          },
          violet: '#D4A052',
        },
        minimal: {
          white: '#1a1a2e',
          gray: {
            50: '#22223a',
            100: '#2a2a4e',
            200: 'rgba(184, 134, 11, 0.15)',
            300: 'rgba(184, 134, 11, 0.25)',
            400: '#8B7355',
            500: '#A08060',
            600: '#b8b0a4',
            700: '#d4ccc0',
            800: '#e8e0d4',
            900: '#f5f0e8',
          },
          indigo: '#D4A052',
          violet: '#C43E4E',
          blue: '#D4A052',
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

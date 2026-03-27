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
        // Cosmic Dark Theme Colors
        cosmic: {
          bg: '#0a0a1a',
          'bg-light': '#0d0d2b',
          surface: '#111133',
          card: '#0f0f2e',
          'card-hover': '#151540',
          text: '#f0e6d3',
          'text-secondary': '#a89b8c',
          'text-muted': '#6b5f52',
        },
        // Sacred theme mapped to dark cosmic
        sacred: {
          cream: '#0a0a1a',
          gold: {
            DEFAULT: '#D4AF37',
            dark: '#B8860B',
            light: '#F4D03F',
          },
          saffron: {
            DEFAULT: '#FF9933',
            dark: '#E67300',
            light: '#FFB366',
          },
          maroon: '#2d1b69',
          brown: '#f0e6d3',
          text: {
            DEFAULT: '#f0e6d3',
            secondary: '#a89b8c',
          },
          purple: {
            DEFAULT: '#2d1b69',
            light: '#4a2c8a',
          },
          violet: '#7c3aed',
        },
        // Minimal colors mapped to dark cosmic
        minimal: {
          white: '#0a0a1a',
          gray: {
            50: '#0f0f2e',
            100: '#111133',
            200: 'rgba(212, 175, 55, 0.15)',
            300: 'rgba(212, 175, 55, 0.25)',
            400: '#6b5f52',
            500: '#a89b8c',
            600: '#c4b8a8',
            700: '#d4c8b8',
            800: '#e8ddd0',
            900: '#f0e6d3',
          },
          indigo: '#D4AF37',
          violet: '#B8860B',
          blue: '#D4AF37',
        },
      },
      fontFamily: {
        display: ['Cinzel', 'Playfair Display', 'Georgia', 'serif'],
        body: ['Barlow', 'Inter', 'sans-serif'],
        sacred: ['Cinzel', 'Playfair Display', 'Georgia', 'serif'],
        decorative: ['Cinzel Decorative', 'Cinzel', 'serif'],
        cinzel: ['Cinzel', 'serif'],
        mantra: ['Sanskrit Text', 'Noto Serif Devanagari', 'Georgia', 'serif'],
      },
      borderRadius: {
        xl: "calc(var(--radius) + 4px)",
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
        xs: "calc(var(--radius) - 6px)",
      },
      boxShadow: {
        xs: "0 1px 2px 0 rgb(0 0 0 / 0.2)",
        soft: "0 4px 20px rgba(0, 0, 0, 0.3), 0 0 10px rgba(212, 175, 55, 0.05)",
        'soft-lg': "0 10px 40px rgba(0, 0, 0, 0.4), 0 0 20px rgba(212, 175, 55, 0.08)",
        'sacred': "0 4px 20px rgba(0, 0, 0, 0.3), 0 0 15px rgba(212, 175, 55, 0.15)",
        'sacred-lg': "0 8px 30px rgba(0, 0, 0, 0.4), 0 0 25px rgba(212, 175, 55, 0.2)",
        'glow-gold': "0 0 20px rgba(212, 175, 55, 0.3), 0 0 40px rgba(212, 175, 55, 0.1)",
        'glow-saffron': "0 0 20px rgba(255, 153, 51, 0.3), 0 0 40px rgba(255, 153, 51, 0.1)",
        'glow-purple': "0 0 20px rgba(124, 58, 237, 0.3), 0 0 40px rgba(124, 58, 237, 0.1)",
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
          "0%, 100%": { boxShadow: "0 0 0 0 rgba(212, 175, 55, 0.4)" },
          "50%": { boxShadow: "0 0 0 15px rgba(212, 175, 55, 0)" },
        },
        "shimmer": {
          "0%": { backgroundPosition: "-200% 0" },
          "100%": { backgroundPosition: "200% 0" },
        },
        "twinkle": {
          "0%, 100%": { opacity: "0.3" },
          "50%": { opacity: "1" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
        "caret-blink": "caret-blink 1.25s ease-out infinite",
        "float": "float 5s ease-in-out infinite",
        "pulse-gold": "pulse-gold 2s ease-in-out infinite",
        "shimmer": "shimmer 3s ease-in-out infinite",
        "twinkle": "twinkle 3s ease-in-out infinite",
      },
      backgroundImage: {
        'sacred-gradient': 'linear-gradient(135deg, #0a0a1a 0%, #0d0d2b 50%, #0a0a1a 100%)',
        'gold-gradient': 'linear-gradient(135deg, #D4AF37 0%, #FF9933 50%, #B8860B 100%)',
        'saffron-gradient': 'linear-gradient(135deg, #FFB366 0%, #FF9933 50%, #E67300 100%)',
        'cosmic-gradient': 'linear-gradient(135deg, #0a0a1a 0%, #2d1b69 50%, #0a0a1a 100%)',
        'nebula': 'radial-gradient(ellipse at 30% 50%, rgba(45, 27, 105, 0.4) 0%, transparent 60%), radial-gradient(ellipse at 70% 40%, rgba(128, 0, 80, 0.2) 0%, transparent 50%)',
        'mandala': 'radial-gradient(circle at 20% 80%, rgba(45, 27, 105, 0.3) 0%, transparent 50%), radial-gradient(circle at 80% 20%, rgba(212, 175, 55, 0.08) 0%, transparent 50%)',
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}

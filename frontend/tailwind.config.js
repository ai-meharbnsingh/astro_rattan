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
        // Observatory Theme - Pure Black + Gold
        cosmic: {
          bg: '#000000',
          'bg-light': '#050505',
          surface: '#0a0a0a',
          card: '#0a0a0a',
          'card-hover': '#111111',
          text: '#ffffff',
          'text-secondary': 'rgba(255, 255, 255, 0.85)',
          'text-muted': 'rgba(255, 255, 255, 0.5)',
        },
        // Sacred theme - Black + Gold only
        sacred: {
          cream: '#000000',
          gold: {
            DEFAULT: '#ffd700',
            dark: '#d4af37',
            light: '#ffec8b',
          },
          saffron: {
            DEFAULT: '#ffaa33',
            dark: '#e67e22',
            light: '#ffb366',
          },
          maroon: '#0a0a0a',
          brown: '#ffffff',
          text: {
            DEFAULT: '#ffffff',
            secondary: 'rgba(255, 255, 255, 0.85)',
          },
          purple: {
            DEFAULT: '#000000',
            light: '#0a0a0a',
          },
          violet: '#d4af37',
        },
        // Minimal colors - Black based
        minimal: {
          white: '#000000',
          gray: {
            50: '#000000',
            100: '#050505',
            200: 'rgba(212, 175, 55, 0.15)',
            300: 'rgba(212, 175, 55, 0.25)',
            400: 'rgba(255, 255, 255, 0.4)',
            500: 'rgba(255, 255, 255, 0.5)',
            600: 'rgba(255, 255, 255, 0.6)',
            700: 'rgba(255, 255, 255, 0.7)',
            800: 'rgba(255, 255, 255, 0.8)',
            900: '#ffffff',
          },
          indigo: '#ffd700',
          violet: '#d4af37',
          blue: '#d4af37',
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
        soft: "0 4px 20px rgba(0, 0, 0, 0.5), 0 0 10px rgba(212, 175, 55, 0.05)",
        'soft-lg': "0 10px 40px rgba(0, 0, 0, 0.6), 0 0 20px rgba(212, 175, 55, 0.08)",
        'sacred': "0 4px 20px rgba(0, 0, 0, 0.5), 0 0 15px rgba(212, 175, 55, 0.15)",
        'sacred-lg': "0 8px 30px rgba(0, 0, 0, 0.6), 0 0 25px rgba(212, 175, 55, 0.2)",
        'glow-gold': "0 0 20px rgba(255, 215, 0, 0.3), 0 0 40px rgba(255, 215, 0, 0.1)",
        'glow-saffron': "0 0 20px rgba(255, 170, 51, 0.3), 0 0 40px rgba(255, 170, 51, 0.1)",
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
          "0%, 100%": { boxShadow: "0 0 0 0 rgba(255, 215, 0, 0.4)" },
          "50%": { boxShadow: "0 0 0 15px rgba(255, 215, 0, 0)" },
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
        'sacred-gradient': 'linear-gradient(135deg, #000000 0%, #050505 50%, #000000 100%)',
        'gold-gradient': 'linear-gradient(135deg, #ffd700 0%, #d4af37 50%, #b8941d 100%)',
        'saffron-gradient': 'linear-gradient(135deg, #ffb366 0%, #ffaa33 50%, #e67e22 100%)',
        'cosmic-gradient': 'linear-gradient(135deg, #000000 0%, #050505 50%, #000000 100%)',
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}

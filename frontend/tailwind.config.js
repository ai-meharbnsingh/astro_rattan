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
        // Sacred Gold Theme Colors
        sacred: {
          cream: '#FAF6F0',
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
          maroon: '#800000',
          brown: '#4A3728',
          text: {
            DEFAULT: '#2C1810',
            secondary: '#5C4033',
          },
        },
        // Legacy minimal colors (keeping for compatibility)
        minimal: {
          white: '#FFFFFF',
          gray: {
            50: '#F8FAFC',
            100: '#F1F5F9',
            200: '#E2E8F0',
            300: '#CBD5E1',
            400: '#94A3B8',
            500: '#64748B',
            600: '#475569',
            700: '#334155',
            800: '#1E293B',
            900: '#0F172A',
          },
          indigo: '#6366F1',
          violet: '#8B5CF6',
          blue: '#3B82F6',
        },
      },
      fontFamily: {
        display: ['Space Grotesk', 'sans-serif'],
        body: ['Inter', 'sans-serif'],
        sacred: ['Cinzel', 'Playfair Display', 'Georgia', 'serif'],
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
        xs: "0 1px 2px 0 rgb(0 0 0 / 0.05)",
        soft: "0 4px 20px rgba(0, 0, 0, 0.05), 0 1px 3px rgba(0, 0, 0, 0.02)",
        'soft-lg': "0 10px 40px rgba(0, 0, 0, 0.08), 0 2px 8px rgba(0, 0, 0, 0.03)",
        'sacred': "0 4px 20px rgba(74, 55, 40, 0.08), 0 1px 3px rgba(212, 175, 55, 0.1)",
        'sacred-lg': "0 8px 30px rgba(74, 55, 40, 0.12), 0 2px 8px rgba(212, 175, 55, 0.15)",
        'glow-gold': "0 0 20px rgba(212, 175, 55, 0.3), 0 0 40px rgba(212, 175, 55, 0.1)",
        'glow-saffron': "0 0 20px rgba(255, 153, 51, 0.3), 0 0 40px rgba(255, 153, 51, 0.1)",
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
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
        "caret-blink": "caret-blink 1.25s ease-out infinite",
        "float": "float 5s ease-in-out infinite",
        "pulse-gold": "pulse-gold 2s ease-in-out infinite",
        "shimmer": "shimmer 3s ease-in-out infinite",
      },
      backgroundImage: {
        'sacred-gradient': 'linear-gradient(135deg, #FAF6F0 0%, #F5EFE6 50%, #FAF6F0 100%)',
        'gold-gradient': 'linear-gradient(135deg, #D4AF37 0%, #FF9933 50%, #B8860B 100%)',
        'saffron-gradient': 'linear-gradient(135deg, #FFB366 0%, #FF9933 50%, #E67300 100%)',
        'mandala': 'radial-gradient(circle at 20% 80%, rgba(212, 175, 55, 0.05) 0%, transparent 50%), radial-gradient(circle at 80% 20%, rgba(255, 153, 51, 0.05) 0%, transparent 50%)',
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}

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
        // Digital Patra & Prismatic Light
        cosmic: {
          bg: '#FAFAFA',
          'bg-light': '#FFFFFF',
          surface: '#FFFFFF',
          card: 'rgba(255, 255, 255, 0.95)',
          'card-hover': 'rgba(255, 255, 255, 1)',
          text: '#1e293b',
          'text-secondary': '#64748b',
          'text-muted': '#94a3b8',
        },
        sacred: {
          cream: '#F8FAFC',
          gold: {
            DEFAULT: '#FF9933',
            dark: '#B45309',
            light: '#FFD700',
          },
          saffron: {
            DEFAULT: '#FF9933',
            dark: '#B45309',
            light: '#FFD700',
          },
          maroon: '#dc2626',
          brown: '#78716c',
          text: {
            DEFAULT: '#1e293b',
            secondary: '#64748b',
          },
          purple: {
            DEFAULT: '#e2e8f0',
            light: '#f1f5f9',
          },
          violet: '#FF9933',
        },
        minimal: {
          white: '#FFFFFF',
          gray: {
            50: '#f8fafc',
            100: '#f1f5f9',
            200: '#e2e8f0',
            300: '#cbd5e1',
            400: '#94a3b8',
            500: '#64748b',
            600: '#475569',
            700: '#334155',
            800: '#1e293b',
            900: '#0f172a',
          },
          indigo: '#FF9933',
          violet: '#dc2626',
          blue: '#2563eb',
        },
      },
      fontSize: {
        // Standardized typography scale — replace ALL arbitrary text-[Npx]
        'micro': ['0.5rem', { lineHeight: '1.2' }],     // 8px — legends, fine print
        'data': ['0.6875rem', { lineHeight: '1.4' }],    // 11px — dense data tables
        'label': ['0.625rem', { lineHeight: '1.3' }],    // 10px — small labels
      },
      fontFamily: {
        // Primary: clean geometric sans for UI and data
        display: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'sans-serif'],
        body: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        // Vedic/scripture: regal serif for headings and sacred text
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
        soft: "0 4px 20px rgba(0, 0, 0, 0.04), 0 1px 3px rgba(0, 0, 0, 0.06)",
        'soft-lg': "0 10px 40px rgba(0, 0, 0, 0.06), 0 4px 6px rgba(0, 0, 0, 0.04)",
        'sacred': "0 1px 3px rgba(0, 0, 0, 0.06), 0 4px 20px rgba(0, 0, 0, 0.04)",
        'sacred-lg': "0 4px 6px rgba(0, 0, 0, 0.04), 0 8px 30px rgba(0, 0, 0, 0.06)",
        'glow-gold': "0 0 20px rgba(255, 153, 51, 0.1), 0 0 40px rgba(255, 153, 51, 0.04)",
        'glow-saffron': "0 0 20px rgba(255, 153, 51, 0.1), 0 0 40px rgba(255, 153, 51, 0.04)",
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
        'sacred-gradient': 'linear-gradient(135deg, #FAFAFA 0%, #F8FAFC 50%, #FAFAFA 100%)',
        'gold-gradient': 'linear-gradient(135deg, #FFD700 0%, #FF9933 50%, #B45309 100%)',
        'saffron-gradient': 'linear-gradient(135deg, #FFD700 0%, #FF9933 100%)',
        'cosmic-gradient': 'linear-gradient(135deg, #FAFAFA 0%, #F8FAFC 50%, #FAFAFA 100%)',
        'wax-gradient': 'linear-gradient(145deg, #dc2626 0%, #991b1b 100%)',
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}

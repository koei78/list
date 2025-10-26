/**
 * Tailwind preset for the Dark Luxury UI
 * Add to your tailwind.config.js:
 *   presets: [require('./src/styles/lux.preset')]
 */

/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  theme: {
    container: {
      center: true,
      padding: {
        DEFAULT: "1.5rem", // px-6
        md: "2rem",
      },
      screens: {
        "2xl": "1280px",
      },
    },
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        border: "var(--border)",
        input: "var(--input)",
        ring: "var(--ring)",
        muted: {
          DEFAULT: "var(--muted)",
          foreground: "var(--muted-foreground)",
        },
        card: {
          DEFAULT: "var(--card)",
          foreground: "var(--card-foreground)",
        },
        primary: {
          DEFAULT: "var(--primary)",
          foreground: "var(--primary-foreground)",
        },
        secondary: {
          DEFAULT: "var(--secondary)",
          foreground: "var(--secondary-foreground)",
        },
        lux: {
          bg: "var(--lux-bg)",
          bgSubtle: "var(--lux-bg-subtle)",
          border: "var(--lux-border)",
          fg: "var(--lux-fg)",
          muted: "var(--lux-muted)",
          gold: "var(--lux-gold)",
          violet: "var(--lux-violet)",
        },
      },
      boxShadow: {
        lux: "var(--shadow-lux)",
      },
      borderRadius: {
        "2xl": "var(--radius-2xl)",
      },
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "-apple-system", "Segoe UI", "Roboto", "Helvetica", "Arial", "Apple Color Emoji", "Segoe UI Emoji"],
        display: ["Poppins", "ui-sans-serif", "system-ui", "-apple-system", "Segoe UI", "Roboto", "Helvetica", "Arial", "Apple Color Emoji", "Segoe UI Emoji"],
      },
      lineHeight: {
        relaxed: "1.65",
      },
      transitionTimingFunction: {
        lux: "cubic-bezier(0.16, 1, 0.3, 1)", // ease-out like
      },
      transitionDuration: {
        150: "150ms",
        200: "200ms",
      },
    },
  },
  plugins: (() => {
    try { return [require('tailwindcss-animate')]; } catch { return []; }
  })(),
};

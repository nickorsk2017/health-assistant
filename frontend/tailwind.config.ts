import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      keyframes: {
        breathe: {
          "0%, 100%": { transform: "scale(1)", boxShadow: "0 1px 3px 0 rgb(139 92 246 / 0.3)" },
          "50%": { transform: "scale(1.05)", boxShadow: "0 4px 14px 0 rgb(139 92 246 / 0.5)" },
        },
      },
      animation: {
        breathe: "breathe 2.4s ease-in-out infinite",
      },
    },
  },
  plugins: [],
};

export default config;

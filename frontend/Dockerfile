FROM node:20-slim AS builder
# Устанавливаем pnpm глобально
RUN corepack enable && corepack prepare pnpm@latest --activate

WORKDIR /app

COPY package.json pnpm-lock.yaml* ./


RUN pnpm install

ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

COPY . .
RUN pnpm run build

FROM node:20-slim AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Копируем standalone сборку (она всегда есть, если build прошел успешно)
COPY --from=builder /app/.next/standalone ./

# Мягкое копирование статики и публичных файлов (не упадет, если их нет)
COPY --from=builder /app/.next/static* ./.next/static/
COPY --from=builder /app/public* ./public/

EXPOSE 3000
CMD ["node", "server.js"]
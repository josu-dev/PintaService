FROM node:20-alpine AS base

ARG VITE_BACKEND_BASE_URL
ENV VITE_BACKEND_BASE_URL=$VITE_BACKEND_BASE_URL

WORKDIR /tmp/app

COPY package*.json ./

RUN npm ci --ignore-scripts

COPY public ./public
COPY src ./src
COPY index.html .
COPY postcss.config.js .
COPY tailwind.config.js .
COPY vite.config.js .

RUN npm run build


FROM node:20-alpine AS prod

WORKDIR /app

COPY --from=base /tmp/app/package*.json .

RUN npm i --omit=dev --ignore-scripts

COPY --from=base /tmp/app/dist ./dist

RUN npm i serve

EXPOSE 4173

USER node

CMD ["npx", "serve", "-s", "dist", "-l", "4173"]

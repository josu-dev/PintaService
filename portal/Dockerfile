FROM node:22.8-alpine AS base

ARG BACKEND_BASE_URL
ENV VITE_BACKEND_BASE_URL=$BACKEND_BASE_URL

WORKDIR /tmp/app

COPY package*.json ./

RUN npm ci --ignore-scripts

COPY public ./public
COPY src ./src
COPY index.html .
COPY postcss.config.cjs .
COPY tailwind.config.cjs .
COPY vite.config.js .

RUN npm run build


FROM node:22.8-alpine AS prod

WORKDIR /app

COPY --from=base /tmp/app/package*.json .

RUN npm i --omit=dev --ignore-scripts

COPY --from=base /tmp/app/dist ./dist

RUN npm i -g serve

EXPOSE 4173

USER node

CMD ["serve", "-s", "dist", "-l", "4173"]

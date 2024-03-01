# Base image
FROM node:20-alpine as base

ARG VITE_BACKEND_BASE_URL
ENV VITE_BACKEND_BASE_URL=$VITE_BACKEND_BASE_URL

WORKDIR /tmp/app

COPY package.json package-lock.json ./

# Can't use npm ci because breaks because of pinia
# RUN npm i --ignore-scripts
RUN npm ci --ignore-scripts

COPY public ./public
COPY src ./src
COPY index.html ./index.html
COPY vite.config.js ./vite.config.js
COPY postcss.config.js ./postcss.config.js
COPY tailwind.config.js ./tailwind.config.js

RUN npm run build


# Prod image
FROM node:20-alpine as prod

WORKDIR /app

COPY --from=base /tmp/app/package.json ./

RUN npm i --omit=dev --ignore-scripts

COPY --from=base /tmp/app/dist ./dist

RUN npm i serve

EXPOSE 4173

USER node

# Start the app
CMD ["npx", "serve", "-s", "dist", "-l", "4173"]

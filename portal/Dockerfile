FROM node:14.21.3-bullseye

WORKDIR /app

COPY package.json ./
RUN npm i

COPY public ./public
COPY src ./src
COPY index.html ./index.html
COPY vite.config.js ./vite.config.js
COPY postcss.config.js ./postcss.config.js
COPY tailwind.config.js ./tailwind.config.js


EXPOSE 5173


CMD ["npm", "run", "dev", "--", "--host"]

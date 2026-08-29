# Serve the static board UI (npm run build → out/) on port 8275.
FROM node:22-alpine
WORKDIR /board

COPY package.json package-lock.json* ./
RUN npm install

COPY . .
RUN npm run build

ENV HOSTNAME=0.0.0.0
ENV PORT=8275
ENV TASKMARK_BOARD=/board
EXPOSE 8275

CMD ["npx", "taskmark", "preview", "--no-open"]

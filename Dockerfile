ARG node=node:8.9.1-alpine
ARG target=node:8.9.1-alpine

FROM $node

WORKDIR /code

COPY package.json package.json
RUN npm install --production

COPY . .

FROM $target
COPY --from=0 /code /code

ENTRYPOINT ["node", "/code/index.js"]

ARG node=node:10.6.0-alpine
ARG target=node:10.6.0-alpine

FROM $node

WORKDIR /code

COPY package.json package.json
RUN npm install --production

COPY . .

FROM $target
COPY --from=0 /code /code

ENTRYPOINT ["node", "/code/index.js"]

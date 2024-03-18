FROM node:14

WORKDIR /usr/src/read_posts
COPY ./complex/read_posts/package*.json ./
RUN npm install

COPY ./complex/read_posts/*.js .

CMD [ "node", "read_posts.js" ]


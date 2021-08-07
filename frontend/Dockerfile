FROM node:14.4.0-alpine3.10

# to chage localhost to API_URL
WORKDIR /frontend

# add `/app/node_modules/.bin` to $PATH
ENV PATH /frontend/node_modules/.bin:$PATH

COPY package*.json ./
RUN npm i

COPY . ./

CMD ["npm", "start"]

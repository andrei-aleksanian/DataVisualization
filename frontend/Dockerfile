FROM node:14.4.0-alpine3.10

USER root
ARG API_URL
# to chage localhost to API_URL
ENV REACT_APP_HOST_IP_ADDRESS API_URL
WORKDIR /frontend
# add `/frontend/node_modules/.bin` to $PATH
# ENV PATH /frontend/node_modules/.bin:$PATH

COPY package*.json ./
RUN npm i

COPY . .

CMD ["npm", "start"]

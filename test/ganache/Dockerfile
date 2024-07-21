FROM node:alpine


RUN npm install -g ganache-cli@latest

EXPOSE 8545

CMD ["ganache-cli", "-h", "0.0.0.0", "-e", "1000", "--db", "/ganache/data"]

#Ow$"f9qV0&*HN`VA
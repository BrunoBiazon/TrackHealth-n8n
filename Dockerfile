FROM docker.n8n.io/n8nio/n8n:latest

WORKDIR /home/node
USER node

CMD ["n8n", "start"]

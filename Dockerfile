FROM n8nio/n8n:latest

WORKDIR /home/node
USER node

CMD ["n8n", "start"]

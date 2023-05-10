FROM mongo:latest

COPY ./Event_Manager /data/db

EXPOSE 27017

CMD ["mongod", "--bind_ip_all"]
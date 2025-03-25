up:
	docker compose up --build

down:
	docker compose down

re: down up

logs: logs-rabbitmq logs-server-u2f

logs-rabbitmq:
	docker logs -f rabbitmq

logs-u2f:
	docker logs -f server-u2f

bash-rabbitmq:
	docker exec -it rabbitmq bash

bash-u2f:
	docker exec -it server-u2f bash

.PHONY: up down re logs logs-rabbitmq logs-u2f bash-rabbitmq bash-u2f
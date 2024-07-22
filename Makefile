# Makefile

all:
	@if [ ! -f .env ]; then \
		echo "Error: .env file not found. Please add it to the root of this project."; \
	else \
		docker compose up -d --build; \
	fi

clean:
	@echo "Taking down the containers"
	@docker compose down

re: fclean all

fclean: clean
	@docker system prune -f
	@docker system prune -a -f --volumes
	@if [ "$(docker ps -aq)" ]; then docker stop $(docker ps -aq); fi
	@docker volume ls -q | xargs -r docker volume rm
	@docker network prune -f
	@docker-compose down --rmi all -v --remove-orphans

.PHONY: all clean re fclean check-env

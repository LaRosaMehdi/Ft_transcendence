DOCKER_COMPOSE := docker-compose
.DEFAULT_GOAL := help
RESET := \033[0m
BOLD := \033[1m
GREEN := \033[32m
YELLOW := \033[33m
BLUE := \033[34m
CYAN := \033[36m


.PHONY: help
help:
	@echo "${CYAN}Usage: make [target]${RESET}"
	@echo "${CYAN}Targets:${RESET}"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "${CYAN}  %-20s ${BLUE} %s\n${RESET}", $$1, $$2}'


.PHONY: build
build:
	$(DOCKER_COMPOSE) build

.PHONY: up
up:
	$(DOCKER_COMPOSE) up -d

.PHONY: down
down:
	$(DOCKER_COMPOSE) down

.PHONY: restart
restart: down up

.PHONY: logs
logs:
	$(DOCKER_COMPOSE) logs -f

.PHONY: clean
clean:
	$(DOCKER_COMPOSE) down -v
	docker system prune -f

.PHONY: fclean
fclean: clean
	docker system prune -f --all
	docker system prune -a -f --volumes
	docker volume rm test_ft_transcendence_database-data 2> /dev/null || true
	docker network prune -f
	docker-compose down --rmi all -v --remove-orphans

.PHONY: all
all: build up logs 

.PHONY: re
re: fclean all
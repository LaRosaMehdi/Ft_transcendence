all:
	docker-compose up --build -d

clean:
	@echo "Taking down the containers"
	@ docker compose down

re:
	make fclean
	make all

fclean:
	@make clean
	@echo "Removing all the containers, images, and volumes"
	@docker system prune -a -f --volumes
	@docker system prune -a -f --volumes
	@docker network prune -f
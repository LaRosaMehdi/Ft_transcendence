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
	@rm -rf ./backend/blockchain_etherum/build
	@docker system prune -a -f --volumes
	@docker system prune -a -f --volumes
	@docker network prune -f
	@docker volume rm test_ft_transcendence_database-data
	@docker volume rm test_ganache-data



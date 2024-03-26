from django.shortcuts import render, HttpResponse
from web3 import Web3
import json

w3 = Web3(Web3.HTTPProvider('http://container_ganache:8545'))
w3.eth.default_account = w3.eth.accounts[0]  # Use the first account for transactions

def get_contract():
    contract_file_path = "blockchain_etherum/build/contracts/ScoreStorage.json"
    with open(contract_file_path, encoding='utf-8') as deploy_file:
        contract_json = json.load(deploy_file)
        contract_abi = contract_json["abi"]
        network_id = list(contract_json["networks"].keys())[0]
        contract_address = contract_json["networks"][network_id]["address"]
        contract = w3.eth.contract(address=contract_address, abi=contract_abi)
        return contract

def tournament_list_view(request):
    contract = get_contract()

    # Optionally add a tournament and players for testing, if none exist
    tournaments_count = contract.functions.getTournamentsCount().call()
    if tournaments_count == 0:
        # Add a tournament for testing
        tx_hash = contract.functions.addTournament(0, 1625097600, "upcoming").transact()
        w3.eth.wait_for_transaction_receipt(tx_hash)

        # Add players to the newly added tournament
        contract.functions.addPlayerToTournament(0, "floki", 1200).transact()
        contract.functions.addPlayerToTournament(0, "le J", 1300).transact()
        # Re-fetch the tournaments count after adding
        tournaments_count = contract.functions.getTournamentsCount().call()

    tournaments = []
    for i in range(tournaments_count):
        # Fetch tournament details based on your contract's available functions
        tournament_info = {
            'id': i,
            'players': []
            # You can add more details here as needed
        }
        players_count = contract.functions.getTournamentPlayerCount(i).call()
        for j in range(players_count):
            player_info = contract.functions.getTournamentPlayer(i, j).call()
            tournament_info['players'].append({
                'name': player_info[0],
                'eloScore': player_info[1]
            })
        tournaments.append(tournament_info)

    context = {'tournaments': tournaments}
    return render(request, 'tournament.html', context)
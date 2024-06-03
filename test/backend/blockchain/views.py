from django.shortcuts import render, HttpResponse
from web3 import Web3
import json
from aouth.views.jwt import jwt_login_required
from django.template.loader import render_to_string
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

w3 = Web3(Web3.HTTPProvider('http://container_ganache:8545'))
# w3.eth.chainId = 345
w3.eth.default_account = w3.eth.accounts[0]


def get_contract():
    contract_file_path = "blockchain_etherum/build/contracts/ScoreStorage.json"
    with open(contract_file_path, encoding='utf-8') as deploy_file:
        contract_json = json.load(deploy_file)
        contract_abi = contract_json["abi"]
        network_id = list(contract_json["networks"].keys())[0]
        contract_address = contract_json["networks"][network_id]["address"]
        contract = w3.eth.contract(address=contract_address, abi=contract_abi)
        return contract

@jwt_login_required
def blockchain_tournament_list_view(request):
    contract = get_contract()
    tournaments_count = contract.functions.getTournamentsCount().call()
    # Initialize a list to hold transaction hashes and other tournament data
    tournaments = []
    transactions = []
    
    # Example of adding tournaments and capturing transaction hashes
    if tournaments_count == 0:
        # Create a new tournament and capture the transaction hash
        tx_hash = contract.functions.addTournament(0, 1625097600, "upcoming").transact()
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        transactions.append(tx_hash.hex())  # Store the transaction hash

        # Add players and capture transaction hashes
        tx_hash = contract.functions.addPlayerToTournament(0, "floki", 1200).transact()
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        transactions.append(tx_hash.hex())  # Store the transaction hash

        tx_hash = contract.functions.addPlayerToTournament(0, "larosa le J", 1300).transact()
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        transactions.append(tx_hash.hex())  # Store the transaction hash

        # Update tournament count after changes
        tournaments_count = contract.functions.getTournamentsCount().call()

    # Retrieve tournament details
    for i in range(tournaments_count):
        tournament_info = {'id': i, 'players': [], 'hashes': []}
        players_count = contract.functions.getTournamentPlayerCount(i).call()
        for j in range(players_count):
            player_info = contract.functions.getTournamentPlayer(i, j).call()
            tournament_info['players'].append({
                'name': player_info[0],
                'eloScore': player_info[1]
            })
        # Store the transaction hashes associated with each tournament
        tournament_info['hashes'].extend(transactions)
        tournaments.append(tournament_info)
    context = {'tournaments': tournaments}
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('spa_scoreTournament.html', context, request=request)
        return JsonResponse({'html': html})
    else:
        return render(request, 'scoreTournament.html', context)
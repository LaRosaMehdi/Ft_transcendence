from django.shortcuts import render
from web3 import Web3
import json
from aouth.views.jwt import jwt_login_required
from django.template.loader import render_to_string
from django.http import JsonResponse
import logging
from tournaments.models import Tournament

logger = logging.getLogger(__name__)

w3 = Web3(Web3.HTTPProvider('http://container_ganache:8545'))
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
    tournaments = Tournament.objects.all()

    for t in tournaments:
        if t.is_finished and not t.blockchain_stored:  # Check if the tournament is finished and not already stored
            # Prepare player names and rankings for the top 4 positions
            player_names = []
            rankings = []

            # Collecting player names based on their positions
            positions = [t.first_place, t.second_place, t.third_place, t.fourth_place]
            
            for player in positions:
                if player:
                    player_names.append(player.username)
                    rankings.append(player.username)  # Since rankings are in the same order as positions

            # Add tournament, players, and rankings in a single transaction
            tx_hashes = []
            tx_hash = contract.functions.addTournament(t.id, t.name, player_names).transact()
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            tx_hashes.append(tx_hash.hex())

            # Mark the tournament as stored and save transaction hashes
            t.blockchain_stored = True
            t.transaction_hashes = tx_hashes
            t.save()

    context = {'tournaments': tournaments}
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('spa_scoreTournament.html', context, request=request)
        return JsonResponse({'html': html})
    else:
        return render(request, 'scoreTournament.html', context)

// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;
pragma experimental ABIEncoderV2;

contract ScoreStorage {
    struct Player {
        string name;
    }

    struct Tournament {
        uint id;
        string name;
        Player[] players;
        string[] rankings; // Store player names according to their ranks
    }

    Tournament[] public tournaments;

    function addTournament(uint _id, string memory _name, string[] memory _playerNames) public {
        Tournament storage newTournament = tournaments.push();
        newTournament.id = _id;
        newTournament.name = _name;

        // Add players and rankings in a single transaction
        for (uint i = 0; i < _playerNames.length; i++) {
            newTournament.players.push(Player(_playerNames[i]));
            newTournament.rankings.push(_playerNames[i]);
        }
    }

    function getTournamentPlayerCount(uint _tournamentId) public view returns (uint) {
        require(_tournamentId < tournaments.length, "Tournament does not exist.");
        return tournaments[_tournamentId].players.length;
    }

    function getTournamentPlayer(uint _tournamentId, uint _playerIndex) public view returns (string memory name) {
        require(_tournamentId < tournaments.length, "Tournament does not exist.");
        require(_playerIndex < tournaments[_tournamentId].players.length, "Player does not exist.");
        Player storage player = tournaments[_tournamentId].players[_playerIndex];
        return player.name;
    }

    function getTournamentsCount() public view returns (uint) {
        return tournaments.length;
    }

    function getRankings(uint _tournamentId) public view returns (string[] memory) {
        require(_tournamentId < tournaments.length, "Tournament does not exist.");
        return tournaments[_tournamentId].rankings;
    }
}

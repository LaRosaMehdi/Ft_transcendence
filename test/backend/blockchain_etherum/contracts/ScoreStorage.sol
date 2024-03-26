// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract ScoreStorage {
    struct Player {
        string name;
        uint eloScore;
    }

    struct Tournament {
        uint id;
        Player[] players;
        uint startTime;
        string status; // "upcoming", "ongoing", "completed"
    }

    Tournament[] public tournaments;

    function addTournament(uint _id, uint _startTime, string memory _status) public {
        Tournament storage newTournament = tournaments.push();
        newTournament.id = _id;
        newTournament.startTime = _startTime;
        newTournament.status = _status;
    }

    function addPlayerToTournament(uint _tournamentId, string memory _name, uint _eloScore) public {
        require(_tournamentId < tournaments.length, "Tournament does not exist.");
        tournaments[_tournamentId].players.push(Player(_name, _eloScore));
    }

    function getTournamentPlayerCount(uint _tournamentId) public view returns (uint) {
        require(_tournamentId < tournaments.length, "Tournament does not exist.");
        return tournaments[_tournamentId].players.length;
    }

    function getTournamentPlayer(uint _tournamentId, uint _playerIndex) public view returns (string memory name, uint eloScore) {
        require(_tournamentId < tournaments.length, "Tournament does not exist.");
        require(_playerIndex < tournaments[_tournamentId].players.length, "Player does not exist.");
        Player storage player = tournaments[_tournamentId].players[_playerIndex];
        return (player.name, player.eloScore);
    }

    function getTournamentsCount() public view returns (uint) {
    return tournaments.length;
}
}


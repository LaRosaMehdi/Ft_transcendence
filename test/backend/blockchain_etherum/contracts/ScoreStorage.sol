// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract ScoreStorage {
    // Mapping from player ID (address) to their score
    mapping(address => uint256) public scores;

    // Event to emit when a score is updated
    event ScoreUpdated(address player, uint256 score);

    // Function to add or update a player's score
    function setScore(address player, uint256 score) public {
        scores[player] = score;
        emit ScoreUpdated(player, score);
    }

    // Function to get a player's score
    function getScore(address player) public view returns (uint256) {
        return scores[player];
    }
}

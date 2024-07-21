const ScoreStorage = artifacts.require("ScoreStorage");

contract("ScoreStorage", accounts => {
    it("should allow a score to be set for a player", async () => {
        const scoreStorageInstance = await ScoreStorage.deployed(); // Changed variable name

        await scoreStorageInstance.setScore(accounts[0], 10); // Use the new variable name
        const score = await scoreStorageInstance.getScore(accounts[0]); // Use the new variable name

        assert.equal(score.toNumber(), 10, "The score was not correctly set");
    });

    it("should update a player's score", async () => {
        const scoreStorageInstance = await ScoreStorage.deployed(); // Reuse the same pattern

        await scoreStorageInstance.setScore(accounts[0], 20); // Use the new variable name
        const score = await scoreStorageInstance.getScore(accounts[0]); // Use the new variable name

        assert.equal(score.toNumber(), 20, "The score was not correctly updated");
    });
});

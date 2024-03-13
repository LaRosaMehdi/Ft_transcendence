const ScoreStorage = artifacts.require("ScoreStorage");

module.exports = function (deployer) {
  deployer.deploy(ScoreStorage);
};

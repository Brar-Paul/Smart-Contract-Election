from brownie import Elections, accounts, config, network, exceptions
import py
from scripts.deploy import deployElection, getAccount
from web3 import Web3
import pytest

# Test election voting
def test_election_voting():
    # Arrange
    if network.show_active() != "development":
        pytest.skip()
    account = getAccount()
    election = Elections.deploy("CEO", ["Paul", "Peter"], 2, {"from": account})
    # Act
    election.castVote("Paul", {"from": account})
    # Assert
    assert election.Voted(account) == True


# Test can't vote more than once
def test_election_valid_voter():
    # Arrange
    if network.show_active() != "development":
        pytest.skip()
    account = getAccount()
    election = Elections.deploy("CEO", ["Paul", "Peter"], 2, {"from": account})
    # Act
    election.castVote("Paul", {"from": account})
    # Assert
    with pytest.raises(exceptions.VirtualMachineError):
        election.castVote("Paul", {"from": account})


# test valid vote
def test_valid_vote():
    # Arrange
    if network.show_active() != "development":
        pytest.skip()
    account = getAccount()
    election = Elections.deploy("CEO", ["Paul", "Peter"], 2, {"from": account})
    # Act/Assert
    with pytest.raises(exceptions.VirtualMachineError):
        election.castVote("Mary", {"from": account})


# test can't close before end of deadline
def test_cannot_close_election_early():
    # Arrange
    if network.show_active() != "development":
        pytest.skip()
    account = getAccount()
    election = Elections.deploy("CEO", ["Paul", "Peter"], 2, {"from": account})
    # Act/Assert
    with pytest.raises(exceptions.VirtualMachineError):
        election.closeElection({"from": account})


# test election chooses right winner
def test_election_winner():
    # Arrange
    if network.show_active() != "development":
        pytest.skip()
    account = getAccount()
    election = Elections.deploy("CEO", ["Paul", "Peter"], 2, {"from": account})
    # Act
    election.castVote("Paul", {"from": account})
    # Override deadline requirement for testing
    if network.show_active() == "development":
        w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    currentTime = w3.eth.get_block("latest").timestamp
    election.setDeadlineForTesting(currentTime)
    election.closeElection({"from": account})
    # Assert
    assert election.winner() == "Paul"

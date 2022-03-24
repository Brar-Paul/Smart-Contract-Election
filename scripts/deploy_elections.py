from email.header import decode_header
from brownie import Elections, accounts, network, config
from web3 import Web3


def getAccount():
    if network.show_active() == "development":
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def deployElection():
    account = getAccount()
    election = Elections.deploy(
        "CEO",
        ["Peter", "Paul", "Mary"],
        2,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print(f"Election deployed to {election.address}")
    return election


def voteInElection():
    account = getAccount()
    election = Elections[-1]
    vote = election.castVote("Mary", {"from": account})
    account1 = accounts[1]
    election.castVote("Peter", {"from": account1})
    account2 = accounts[2]
    election.castVote("Mary", {"from": account2})
    print(f"You have successfully cast your vote!")


def endElection():
    if network.show_active() == "development":
        w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    currentTime = w3.eth.get_block("latest").timestamp
    account = getAccount()
    election = Elections[-1]
    election.setDeadlineForTesting(currentTime)
    election.closeElection({"from": account})
    print(f"{election.winner()} is the winner of the election!")


def main():
    deployElection()
    voteInElection()
    endElection()

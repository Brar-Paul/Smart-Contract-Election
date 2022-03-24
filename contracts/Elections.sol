// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";

contract Elections is Ownable {
    string public title;
    uint256 public deadline;
    string[] public candidateList;
    string public winner;
    mapping(string => bool) public ValidCanditate;
    mapping(string => uint256) public VoteCount;
    struct Voter {
        address voterId;
        string vote;
        bool voted;
    }
    Voter[] public voters;
    mapping(address => bool) public Voted;
    enum ELECTION_STATE {
        OPEN,
        CLOSED
    }
    ELECTION_STATE public election_state;

    constructor(
        string memory _electionTitle,
        string[] memory _candidateList,
        uint256 _votingTime
    ) {
        for (uint256 i = 0; i < _candidateList.length; i++) {
            candidateList.push(_candidateList[i]);
        }
        title = _electionTitle;
        deadline = block.timestamp + (_votingTime * 1 days);
        election_state = ELECTION_STATE.OPEN;
        for (uint256 i = 0; i < candidateList.length; i++) {
            ValidCanditate[candidateList[i]] = true;
        }
    }

    function castVote(string memory _candidate) public {
        require(
            election_state == ELECTION_STATE.OPEN,
            "This election is closed"
        );
        require(Voted[msg.sender] == false, "You have already cast your vote");
        require(
            block.timestamp < deadline,
            "This election is no longer open for voting"
        );
        require(
            ValidCanditate[_candidate] == true,
            "Invalid candidate selection"
        );
        voters.push(Voter(msg.sender, _candidate, true));
        VoteCount[_candidate] += 1;
        Voted[msg.sender] = true;
    }

    function closeElection() public onlyOwner returns (string memory) {
        require(block.timestamp >= deadline, "Cannot close election yet");
        election_state = ELECTION_STATE.CLOSED;
        uint256 voteLead = 0;
        for (uint256 i = 0; i < candidateList.length; i++) {
            uint256 candidateVotes = VoteCount[candidateList[i]];
            if (candidateVotes > voteLead) {
                voteLead = candidateVotes;
                winner = candidateList[i];
            }
        }
        return winner;
    }

    function setDeadlineForTesting(uint256 time) public {
        deadline = time;
    }
}

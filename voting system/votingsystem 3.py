import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class Voter:
    def __init__(self, voter_id: str, name: str, email: str):
        self.voter_id = voter_id
        self.name = name
        self.email = email
        self.has_voted = False
        self.vote_timestamp = None

class Candidate:
    def __init__(self, candidate_id: str, name: str, party: str, description: str = ""):
        self.candidate_id = candidate_id
        self.name = name
        self.party = party
        self.description = description
        self.votes = 0

class Election:
    def __init__(self, title: str, description: str = ""):
        self.title = title
        self.description = description
        self.candidates: Dict[str, Candidate] = {}
        self.voters: Dict[str, Voter] = {}
        self.votes: List[Dict] = []
        self.is_active = True
        self.created_at = datetime.now().isoformat()

class VotingSystem:
    def __init__(self, data_file: str = "voting_data.json"):
        self.data_file = data_file
        self.elections: Dict[str, Election] = {}
        self.current_election_id: Optional[str] = None
        self.load_data()

    def create_election(self, election_id: str, title: str, description: str = "") -> bool:
        """Create a new election"""
        if election_id in self.elections:
            print(f"Election '{election_id}' already exists!")
            return False
        
        self.elections[election_id] = Election(title, description)
        self.current_election_id = election_id
        print(f"Election '{title}' created successfully!")
        return True

    def set_current_election(self, election_id: str) -> bool:
        """Set the active election"""
        if election_id not in self.elections:
            print(f"Election '{election_id}' not found!")
            return False
        
        self.current_election_id = election_id
        print(f"Current election set to: {self.elections[election_id].title}")
        return True

    def add_candidate(self, candidate_id: str, name: str, party: str, description: str = "") -> bool:
        """Add a candidate to the current election"""
        if not self.current_election_id:
            print("No active election! Create or select an election first.")
            return False
        
        election = self.elections[self.current_election_id]
        
        if candidate_id in election.candidates:
            print(f"Candidate '{candidate_id}' already exists!")
            return False
        
        election.candidates[candidate_id] = Candidate(candidate_id, name, party, description)
        print(f"Candidate '{name}' added successfully!")
        return True

    def register_voter(self, voter_id: str, name: str, email: str) -> bool:
        """Register a new voter"""
        if not self.current_election_id:
            print("No active election! Create or select an election first.")
            return False
        
        election = self.elections[self.current_election_id]
        
        if voter_id in election.voters:
            print(f"Voter '{voter_id}' is already registered!")
            return False
        
        election.voters[voter_id] = Voter(voter_id, name, email)
        print(f"Voter '{name}' registered successfully!")
        return True

    def cast_vote(self, voter_id: str, candidate_id: str) -> bool:
        """Cast a vote for a candidate"""
        if not self.current_election_id:
            print("No active election!")
            return False
        
        election = self.elections[self.current_election_id]
        
        if not election.is_active:
            print("This election is not active!")
            return False
        
        if voter_id not in election.voters:
            print(f"Voter '{voter_id}' is not registered!")
            return False
        
        if candidate_id not in election.candidates:
            print(f"Candidate '{candidate_id}' not found!")
            return False
        
        voter = election.voters[voter_id]
        if voter.has_voted:
            print(f"Voter '{voter_id}' has already voted!")
            return False
        
        # Record the vote
        candidate = election.candidates[candidate_id]
        candidate.votes += 1
        voter.has_voted = True
        voter.vote_timestamp = datetime.now().isoformat()
        
        # Store vote record (anonymous)
        election.votes.append({
            "candidate_id": candidate_id,
            "timestamp": voter.vote_timestamp
        })
        
        print(f"Vote cast successfully for {candidate.name}!")
        return True

    def get_results(self) -> Dict:
        """Get election results"""
        if not self.current_election_id:
            print("No active election!")
            return {}
        
        election = self.elections[self.current_election_id]
        results = []
        total_votes = len(election.votes)
        
        for candidate in election.candidates.values():
            percentage = (candidate.votes / total_votes * 100) if total_votes > 0 else 0
            results.append({
                "name": candidate.name,
                "party": candidate.party,
                "votes": candidate.votes,
                "percentage": round(percentage, 2)
            })
        
        # Sort by votes (descending)
        results.sort(key=lambda x: x["votes"], reverse=True)
        
        return {
            "election_title": election.title,
            "total_votes": total_votes,
            "total_registered": len(election.voters),
            "turnout_percentage": round((total_votes / len(election.voters) * 100) if len(election.voters) > 0 else 0, 2),
            "results": results
        }

    def display_results(self):
        """Display formatted election results"""
        results = self.get_results()
        if not results:
            return
        
        print(f"\n{'='*50}")
        print(f"ELECTION RESULTS: {results['election_title']}")
        print(f"{'='*50}")
        print(f"Total Votes Cast: {results['total_votes']}")
        print(f"Total Registered Voters: {results['total_registered']}")
        print(f"Voter Turnout: {results['turnout_percentage']}%")
        print(f"{'='*50}")
        
        for i, candidate in enumerate(results['results'], 1):
            print(f"{i}. {candidate['name']} ({candidate['party']})")
            print(f"   Votes: {candidate['votes']} ({candidate['percentage']}%)")
            print(f"   {'█' * int(candidate['percentage'] // 2)}")
            print()

    def list_elections(self):
        """List all elections"""
        if not self.elections:
            print("No elections found.")
            return
        
        print("\nElections:")
        print("-" * 40)
        for election_id, election in self.elections.items():
            status = "ACTIVE" if election.is_active else "CLOSED"
            current = " (CURRENT)" if election_id == self.current_election_id else ""
            print(f"ID: {election_id}")
            print(f"Title: {election.title}")
            print(f"Status: {status}{current}")
            print(f"Candidates: {len(election.candidates)}")
            print(f"Voters: {len(election.voters)}")
            print(f"Votes Cast: {len(election.votes)}")
            print("-" * 40)

    def close_election(self) -> bool:
        """Close the current election"""
        if not self.current_election_id:
            print("No active election!")
            return False
        
        election = self.elections[self.current_election_id]
        election.is_active = False
        print(f"Election '{election.title}' has been closed.")
        return True

    def save_data(self):
        """Save data to file"""
        data = {}
        for election_id, election in self.elections.items():
            data[election_id] = {
                "title": election.title,
                "description": election.description,
                "is_active": election.is_active,
                "created_at": election.created_at,
                "candidates": {
                    cid: {
                        "name": c.name,
                        "party": c.party,
                        "description": c.description,
                        "votes": c.votes
                    } for cid, c in election.candidates.items()
                },
                "voters": {
                    vid: {
                        "name": v.name,
                        "email": v.email,
                        "has_voted": v.has_voted,
                        "vote_timestamp": v.vote_timestamp
                    } for vid, v in election.voters.items()
                },
                "votes": election.votes
            }
        
        with open(self.data_file, 'w') as f:
            json.dump({
                "elections": data,
                "current_election_id": self.current_election_id
            }, f, indent=2)

    def load_data(self):
        """Load data from file"""
        if not os.path.exists(self.data_file):
            return
        
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
            
            self.current_election_id = data.get("current_election_id")
            
            for election_id, election_data in data.get("elections", {}).items():
                election = Election(election_data["title"], election_data["description"])
                election.is_active = election_data["is_active"]
                election.created_at = election_data["created_at"]
                election.votes = election_data["votes"]
                
                # Load candidates
                for cid, cdata in election_data["candidates"].items():
                    candidate = Candidate(cid, cdata["name"], cdata["party"], cdata["description"])
                    candidate.votes = cdata["votes"]
                    election.candidates[cid] = candidate
                
                # Load voters
                for vid, vdata in election_data["voters"].items():
                    voter = Voter(vid, vdata["name"], vdata["email"])
                    voter.has_voted = vdata["has_voted"]
                    voter.vote_timestamp = vdata["vote_timestamp"]
                    election.voters[vid] = voter
                
                self.elections[election_id] = election
        
        except Exception as e:
            print(f"Error loading data: {e}")

def main():
    """Main interactive menu"""
    voting_system = VotingSystem()
    
    while True:
        print("\n" + "="*50)
        print("           VOTING SYSTEM MENU")
        print("="*50)
        print("1. Create Election")
        print("2. Set Current Election")
        print("3. Add Candidate")
        print("4. Register Voter")
        print("5. Cast Vote")
        print("6. View Results")
        print("7. List Elections")
        print("8. Close Election")
        print("9. Save Data")
        print("0. Exit")
        print("="*50)
        
        choice = input("Enter your choice (0-9): ").strip()
        
        if choice == "1":
            election_id = input("Enter election ID: ").strip()
            title = input("Enter election title: ").strip()
            description = input("Enter description (optional): ").strip()
            voting_system.create_election(election_id, title, description)
        
        elif choice == "2":
            voting_system.list_elections()
            election_id = input("Enter election ID to select: ").strip()
            voting_system.set_current_election(election_id)
        
        elif choice == "3":
            candidate_id = input("Enter candidate ID: ").strip()
            name = input("Enter candidate name: ").strip()
            party = input("Enter party: ").strip()
            description = input("Enter description (optional): ").strip()
            voting_system.add_candidate(candidate_id, name, party, description)
        
        elif choice == "4":
            voter_id = input("Enter voter ID: ").strip()
            name = input("Enter voter name: ").strip()
            email = input("Enter voter email: ").strip()
            voting_system.register_voter(voter_id, name, email)
        
        elif choice == "5":
            voter_id = input("Enter your voter ID: ").strip()
            
            # Show candidates
            if voting_system.current_election_id:
                election = voting_system.elections[voting_system.current_election_id]
                print("\nAvailable candidates:")
                for cid, candidate in election.candidates.items():
                    print(f"ID: {cid} - {candidate.name} ({candidate.party})")
            
            candidate_id = input("Enter candidate ID to vote for: ").strip()
            voting_system.cast_vote(voter_id, candidate_id)
        
        elif choice == "6":
            voting_system.display_results()
        
        elif choice == "7":
            voting_system.list_elections()
        
        elif choice == "8":
            voting_system.close_election()
        
        elif choice == "9":
            voting_system.save_data()
            print("Data saved successfully!")
        
        elif choice == "0":
            voting_system.save_data()
            print("Thank you for using the Voting System!")
            break
        
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
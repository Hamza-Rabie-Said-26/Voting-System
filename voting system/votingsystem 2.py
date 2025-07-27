class VotingSystem:
    def __init__(self):
        self.candidates = {}
        self.voters = set()
    
    def add_candidate(self, name):
        """Add a new candidate to the voting system."""
        if name not in self.candidates:
            self.candidates[name] = 0
            print(f"Candidate '{name}' added successfully.")
        else:
            print(f"Candidate '{name}' already exists.")
    
    def cast_vote(self, voter_id, candidate_name):
        """Cast a vote for a candidate."""
        if voter_id in self.voters:
            print(f"Voter {voter_id} has already voted.")
            return False
        
        if candidate_name not in self.candidates:
            print(f"Candidate '{candidate_name}' does not exist.")
            return False
        
        self.candidates[candidate_name] += 1
        self.voters.add(voter_id)
        print(f"Vote cast successfully for {candidate_name}.")
        return True
    
    def display_results(self):
        """Display the voting results."""
        if not self.candidates:
            print("No candidates available.")
            return
        
        print("\nVoting Results:")
        print("----------------")
        for candidate, votes in self.candidates.items():
            print(f"{candidate}: {votes} votes")
        
        winner = max(self.candidates.items(), key=lambda x: x[1])
        print(f"\nWinner: {winner[0]} with {winner[1]} votes!")
    
    def run(self):
        """Run the voting system interface."""
        print("Welcome to the Voting System!")
        
        # Add some initial candidates
        self.add_candidate("Dad Rabie")
        self.add_candidate("Mom Noura")
        self.add_candidate("Grandma Fardous")
        
        while True:
            print("\nOptions:")
            print("1. Add Candidate")
            print("2. Cast Vote")
            print("3. View Results")
            print("4. Exit")
            
            choice = input("Enter your choice (1-4): ")
            
            if choice == "1":
                name = input("Enter candidate name: ")
                self.add_candidate(name)
            elif choice == "2":
                voter_id = input("Enter your voter ID: ")
                candidate = input("Enter candidate name to vote for: ")
                self.cast_vote(voter_id, candidate)
            elif choice == "3":
                self.display_results()
            elif choice == "4":
                print("Thank you for using the Voting System!")
                break
            else:
                print("Invalid choice. Please try again.")

# Run the voting system
if __name__ == "__main__":
    vs = VotingSystem()
    vs.run()
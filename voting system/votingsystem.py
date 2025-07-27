class VotingSystem:
    def __init__(self):
        self.candidates = {}
        self.voted_ids = set()
    
    def add_candidate(self, name):
        if name not in self.candidates:
            self.candidates[name] = 0
            print(f"Candidate '{name}' added.")
        else:
            print(f"Candidate '{name}' already exists.")
    
    def vote(self, voter_id, candidate_name):
        if voter_id in self.voted_ids:
            print("You have already voted!")
            return
        
        if candidate_name in self.candidates:
            self.candidates[candidate_name] += 1
            self.voted_ids.add(voter_id)
            print(f"Vote for '{candidate_name}' recorded. Thank you!")
        else:
            print(f"Candidate '{candidate_name}' not found.")
    
    def show_results(self):
        if not self.candidates:
            print("No candidates available.")
            return
        
        print("\n--- VOTING RESULTS ---")
        sorted_results = sorted(self.candidates.items(), key=lambda x: x[1], reverse=True)
        for name, votes in sorted_results:
            print(f"{name}: {votes} vote(s)")
        
        winner = sorted_results[0][0]
        max_votes = sorted_results[0][1]
        print(f"\nWinner: {winner} with {max_votes} vote(s)!")
    
    def show_candidates(self):
        if not self.candidates:
            print("No candidates available.")
            return
        
        print("\n--- CANDIDATES ---")
        for name in self.candidates:
            print(f"- {name}")

def main():
    system = VotingSystem()
    
    # Add some default candidates
    system.add_candidate("Alice")
    system.add_candidate("Bob")
    system.add_candidate("Charlie")
    
    while True:
        print("\n=== VOTING SYSTEM ===")
        print("1. Vote")
        print("2. View Candidates")
        print("3. View Results")
        print("4. Add Candidate")
        print("5. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == "1":
            voter_id = input("Enter your voter ID: ")
            system.show_candidates()
            candidate = input("Enter candidate name to vote for: ")
            system.vote(voter_id, candidate)
        
        elif choice == "2":
            system.show_candidates()
        
        elif choice == "3":
            system.show_results()
        
        elif choice == "4":
            name = input("Enter new candidate name: ")
            system.add_candidate(name)
        
        elif choice == "5":
            print("Exiting...")
            break
        
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
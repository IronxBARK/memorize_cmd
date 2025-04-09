import json
import os

class Player:
    def __init__(self):
        self.username = None
        self.score_file = os.path.join(os.path.dirname(__file__), 'score.json')  # Use absolute path

    def initialize_player(self):
        ''' Initializes the player '''
        self.username = input("Enter your name: ").lower()
        scores = {}

        # Check if the score file exists and load it safely
        if os.path.exists(self.score_file):
            try:
                with open(self.score_file, 'r') as file:
                    scores = json.load(file)
            except (json.JSONDecodeError, ValueError):
                print("Score file is corrupted or empty. Resetting scores.")
                scores = {}

        if self.username in scores:
            status = "yes"
        else:
            # Reset scores for the new player with default lengths
            scores[self.username] = [5, 8]  # Default lengths for Easy and Hard levels
            status = "no"
        
        # Always write the updated scores back to the file
        with open(self.score_file, 'w') as file:
            json.dump(scores, file, indent=4)

        print(f"-----------------Welcome {self.username}!--------------------------------------- ")
        return self.username, status

    def write_score(self, score):
        ''' Writes the score to the json file '''
        scores = {}

        # Safely load the existing scores
        if os.path.exists(self.score_file):
            try:
                with open(self.score_file, 'r') as file:
                    scores = json.load(file)
            except (json.JSONDecodeError, ValueError):
                print("Score file is corrupted. Resetting scores.")
                scores = {}

        # Append the new score for the user
        if self.username not in scores:
            scores[self.username] = []
        scores[self.username].append(score)

        # Write the updated scores back to the file
        with open(self.score_file, 'w') as file:
            json.dump(scores, file, indent=4)
            file.flush()  # Ensure data is written to disk

    def get_score(self):
        ''' Get overall percentage of player's scores '''
        scores = {}

        # Safely load the existing scores
        if os.path.exists(self.score_file):
            try:
                with open(self.score_file, 'r') as file:
                    scores = json.load(file)
            except (json.JSONDecodeError, ValueError):
                return None

        # Get the scores of the current user
        user_scores = scores.get(self.username, [])

        # Check if there are enough scores to calculate an average
        if len(user_scores) <= 2:  # Only default lengths exist, no actual scores
            return None

        # Calculate the average percentage
        average_score = (sum(user_scores) - user_scores[0] - user_scores[1]) / (len(user_scores) - 2)  # Exclude lengths
        return average_score

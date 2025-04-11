from player import Player
import time
import keyboard  # Requires the 'keyboard' library to detect key presses
from levels import EasyLevel, MediumLevel, HardLevel
import threading  # Import threading for quit functionality
import os  # Import os for forceful exit
import json


class Game:
    def __init__(self):
        self.username = None
        self.quit_thread = threading.Thread(target=self._quit, daemon=True)
        self.quit_thread.start()  # Start the thread to monitor 'esc' key in init to avoid delay
    
    def _quit(self):
        ''' Monitors the 'esc' key press in a separate thread '''
        while True:
            if keyboard.is_pressed('esc'):
                average = self.player.get_score()
                if average:
                    print(f"\nYour overall percentage is: {average}%")
                print("Thanks for playing! See you again")
                os._exit(0)  # Forcefully terminate the program
    
    def start_game(self):
        ''' Initializes the game and welcomes the user '''
        self.player = Player()
        self.username, status = self.player.initialize_player()
        
        print("-----------------MEMORY BOOSTER-------------------------------------")
        time.sleep(3)
        # if player is new give instructions
        if status == 'no':
            self._give_instructions()
            
        # start new game    
        self._play_game()
        
    
    def _play_game(self):
        ''' Main game loop '''
        while True:
            self._level_start()  # Start the selected level

    def _give_instructions(self):
        ''' Gives instructions to the player '''
        print("In this game you will be given a set of numbers, numbers with alphabets or mixtures to memorize")
        print("Then you will be asked to recall them in the same order (lower case only)")
        print("You can press 'esc' to exit the game at any time")
        print("This game has three levels of difficulty")
        print("1. Easy: Only numbers")
        print("2. Medium: Numbers with alphabets")
        print("3. Hard: Mixture of numbers,alphabets and symbols")
        print("You can type l to choose the length of number (otherwise default)")
        print("You will be given 10 seconds to recall the numbers")
        input("Press Enter to proceed...")
        print("Starting in:")
   
    def _level_selector(self):
        ''' Select the level and start it'''
        print("Select the level of difficulty:")
        
        while True:
            level = input("1 - Easy, 2 - Medium, 3 - Hard or l to set length : ").strip()
            
            if level == '1' or level.lower() == 'easy':
                return EasyLevel(self.player)  # Pass self.player
                
            elif level == '2' or level.lower() == 'medium':
                return MediumLevel(self.player)  # Pass self.player
                
            elif level == '3' or level.lower() == 'hard':
                return HardLevel(self.player)  # Pass self.player
            
            elif level.lower() == 'l':
                self._length_selector()  # Function to select length
                
            else:
                print("Invalid selection. Please choose again.")

        
    def _level_start(self):
        ''' Start the selected level '''
        level = self._level_selector()
        if not level:  # Exit if quit_thread terminates the program
            return 0

        print(level.get_instructions())
        time.sleep(2)
        percentage = level.start()
        if percentage == None:
            percentage = 0
        self.player.write_score(score=percentage)  # Write score to file
        print(f"{percentage}% correct")  # Print correct percentage
        print(f"The correct answer was: {level.random_number}")  # Print correct answer
        
    def _length_selector(self):
        ''' Method that selects length of levels '''
        print("You can customize the length of numbers for Easy and Hard levels.")
        print("Note: Medium level length is fixed and length cannot be ZERO.")
        
        # Load existing lengths from score.json or initialize default
        try:
            with open('score.json', 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        # Ensure the current player has default lengths if not already set
        if self.username not in data:
            data[self.username] = [5, 8]

        # Get input for Easy level length
        while True:
            easy_length = input("Enter the length for Easy level (press Enter to keep default): ").strip()
            try:
                if easy_length:
                    data[self.username][0] = int(easy_length)  # Update Easy level length
                    break
                elif easy_length == '':
                    break
            except ValueError:
                print("Invalid input for Easy level. Length must be a number.")
        
        # Get input for Hard level length
        while True:
            hard_length = input("Enter the length for Hard level (press Enter to keep default): ").strip()
            try:
                if hard_length:
                    data[self.username][1] = int(hard_length)  # Update Hard level length
                    break
                elif hard_length == '':
                    break
            except ValueError:
                print("Invalid input for Hard level. Length must be a number.")
        
        # Save updated lengths back to score.json
        with open('score.json', 'w') as file:
            json.dump(data, file, indent=4)
            
game = Game()
game.start_game()
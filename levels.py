import sys
import time
import random  # Add this import for generating random numbers
import threading  # Add this import for threading
import json

class Level:
    '''Base class for game levels'''
    def __init__(self, player):
        self.difficulty = None
        self.time_to_memorize = 5  # Default time to memorize
        self.time_to_recall = 10  # Default time to recall
        self.length = 0           # Default length of the number/sequence
        self.percentage = 0  # percentage of each win
        self.player = player  # Store the player object
        
    def get_instructions(self):
        '''Returns instructions specific to the level'''
        raise NotImplementedError("This method should be implemented by subclasses")
    
    def _countdown(self, seconds):
        ''' Displays a countdown at the end of the line '''
        for i in range(seconds, 0, -1):
            sys.stdout.write(f" {i}")  # Append countdown at the end
            sys.stdout.flush()
            time.sleep(1)
            sys.stdout.write("\b" * len(f" {i}"))  # Erase the countdown
        

class EasyLevel(Level):
    '''Easy level: Only numbers'''
    def __init__(self, player):
        super().__init__(player)  # Pass player to the base class
        self.difficulty = "Easy"
        self.length = int(self._get_length())

    def get_instructions(self):
        return "Memorize numbers only."

    def _get_length(self):
        ''' Get the length of the number from the json file '''
        try:
            with open('score.json', 'r') as file:
                data = json.load(file)
                if self.player.username in data:
                    return int(data[self.player.username][0])  # Easy level length
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return 5  # Default length for Easy level
        
    def start(self):
        ''' Method that starts the level'''
        self.random_number = self._guess() #  all guess handling
        time.sleep(1) # Sleep for 1 second before writing
        answer = self._memorize() # all memorize handling
        
        return self._check_answer(self.random_number, answer) # check answer and return percentage
        
    def _guess(self):
        ''' All guess functionary '''
        random_number = random.randint(10**(self.length-1), 10**self.length - 1)  # Generate a random number 
        sys.stdout.write(f"\nMemorize this number: {random_number}") 
        sys.stdout.flush()  # Flush the output buffer to ensure the message is displayed immediately
        self._countdown(self.time_to_memorize)  # Use the countdown method
        sys.stdout.write('\r' + ' '* (len(f"Memorize this number: {random_number}") + 2) + '\r') # Clear the line
        sys.stdout.flush()

        return random_number
    
    def _memorize(self):
        answer = [None]  # Use a list to allow modification within the thread

        def get_input():
            '''Thread function to get user input'''
            answer[0] = input("\nEnter the number you memorized: ")
            
        print(f" You have {self.time_to_recall} seconds to write")
        input_thread = threading.Thread(target=get_input)
        input_thread.start()
        input_thread.join(timeout=self.time_to_recall)  # Wait for the thread or timeout

        if input_thread.is_alive():
            print("\nTime's up!")
            input_thread.join()  # Ensure the thread is cleaned up
            return answer[0].strip()
            
        return answer[0].strip() 
     
    def _check_answer(self, random_number, answer):
        # Calculate percentage of correct digits
        for x, y in zip(str(random_number), answer):
            if x == y:
                self.percentage += 1 
        self.percentage = (self.percentage / self.length) * 100

        if self.percentage == 0:
            return 
        
        return self.percentage
     
        
class MediumLevel(Level):
    '''Medium level: Numbers with alphabets (indian vehicle number plate)'''
    def __init__(self, player):
        super().__init__(player)  # Pass player to the base class
        self.difficulty = "Medium"
        self.time_to_memorize = 4
        self.length = 9  # length is fixed for medium level
        
    def get_instructions(self):
        return "Memorize numbers with alphabets."
    
    def start(self):
        ''' Method that starts the level'''
        self.random_number = self._guess() #  all guess handling
        time.sleep(1)  # Sleep for 1 second before writing
        answer = self._memorize() # all memorize handling
        
        return self._check_answer(self.random_number, answer) # check answer and return percentage
        
    def _guess(self):
        ''' All guess functionary '''
        random_number = (
            ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=2)) +  # 2 alphabets
            ''.join(random.choices('0123456789', k=2)) +                 # 2 integers
            ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=1)) +  # 1 alphabet
            ''.join(random.choices('0123456789', k=4))                  # 4 integers
        )
        sys.stdout.write(f"\nMemorize this number: {random_number}") 
        sys.stdout.flush()  # Flush the output buffer to ensure the message is displayed immediately
        self._countdown(self.time_to_memorize)  # Use the countdown method
        sys.stdout.write('\r' + ' '* (len(f"Memorize this number: {random_number}") + 2) + '\r') # Clear the line
        sys.stdout.flush()

        return random_number
    
    def _memorize(self):
        answer = [None]  # Use a list to allow modification within the thread

        def get_input():
            '''Thread function to get user input'''
            answer[0] = input("\nEnter the number you memorized: ")

        print(f" You have {self.time_to_recall} seconds to write")
        input_thread = threading.Thread(target=get_input)
        input_thread.start()
        input_thread.join(timeout=self.time_to_recall)  # Wait for the thread or timeout

        if input_thread.is_alive():
            print("\nTime's up!")
            input_thread.join()  # Ensure the thread is cleaned up

        return answer[0].strip() if answer[0] else "0"
     
    def _check_answer(self, random_number, answer):
        # Calculate percentage of correct digits
        for x, y in zip(str(random_number), answer):
            if x == y:
                self.percentage += 1 
        self.percentage = (self.percentage / self.length) * 100

        if self.percentage == 0:
            return 0
        
        return self.percentage

class HardLevel(Level):
    '''Hard level: Mixture of numbers, alphabets, and symbols'''
    def __init__(self, player):
        super().__init__(player)  # Pass player to the base class
        self.difficulty = "Hard"
        self.time_to_memorize = 4
        # Remove self.length here to rely on the class attribute
    
    def get_instructions(self):
        return "Memorize a mixture of numbers, alphabets, and symbols."

    def _get_length(self):
        ''' Get the length of the number from the json file '''
        try:
            with open('score.json', 'r') as file:
                data = json.load(file)
                if self.player.username in data:
                    return int(data[self.player.username][1])  # Hard level length
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return 8  # Default length for Hard level
    
    
    def start(self):
        ''' Method that starts the level'''
        self.random_number = self._guess() #  all guess handling
        time.sleep(1)  # Sleep for 1 second before writing
        answer = self._memorize() # all memorize handling
        
        return self._check_answer(self.random_number, answer) # check answer and return percentage
        
    def _guess(self):
        ''' All guess functionary '''
        random_number = ''.join(random.choices(
            '0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()_+',
            k=self.length  # Generate a random sequence of the specified length
        ))
        sys.stdout.write(f"\nMemorize this number: {random_number}") 
        sys.stdout.flush()  # Flush the output buffer to ensure the message is displayed immediately
        self._countdown(self.time_to_memorize)  # Use the countdown method
        sys.stdout.write('\r' + ' '* (len(f"Memorize this number: {random_number}") + 2) + '\r') # Clear the line
        sys.stdout.flush()

        return random_number
    
    def _memorize(self):
        answer = [None]  # Use a list to allow modification within the thread

        def get_input():
            '''Thread function to get user input'''
            answer[0] = input("\nEnter the number you memorized: ")

        start_time = time.time()
        print(f" You have {self.time_to_recall} seconds to write")
        input_thread = threading.Thread(target=get_input)
        input_thread.start()
        input_thread.join(timeout=self.time_to_recall)  # Wait for the thread or timeout

        if input_thread.is_alive():
            print("\nTime's up!")
            input_thread.join()  # Ensure the thread is cleaned up

        return answer[0].strip() if answer[0] else "0"
     
    def _check_answer(self, random_number, answer):
        # Calculate percentage of correct digits
        for x, y in zip(str(random_number), answer):
            if x == y:
                self.percentage += 1 
        self.percentage = (self.percentage / self.length) * 100

        if self.percentage == 0:
            return 
        
        return self.percentage
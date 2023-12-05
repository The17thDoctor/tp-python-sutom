from enum import Enum
from io import TextIOWrapper
import random
import re
import time
from sutom import DICTIONARY_PATH

class LetterPlacement(Enum):
    """Enum representing the position of a letter inside the guess"""
    WRONG = '\033[91m'
    RIGHT = '\033[92m'
    MISPLACED = '\033[93m'

class Sutom():
    __word_to_find: str
    __attemptLimit: int
    __attemptsLeft: int

    __attempts: list[str] = []

    def __init__(self, attemptLimit: int = 5) -> None:
        """Creates a new sutom game with the defined number of attempts"""
        self.__word_to_find = Sutom.__get_random_word()
        self.__attemptLimit = attemptLimit
        self.__attemptsLeft = attemptLimit

    def run(self) -> bool:
        """Runs the game, returns true while the game can still be played."""
        
        while True:
            print("\033[2J")
            print(f"{len(self.__word_to_find)} LETTERS WORD TO FIND.")
            print(f"{self.attempts_left()} ATTEMPTS LEFT.")

            for attempt in self.__attempts:
                print(attempt)

            user_input: str = input("YOUR GUESS : ").strip()

            if (len(user_input) != len(self.__word_to_find)):
                print("\033[91mINVALID WORLD LENGTH\033[00m")
                time.sleep(1.5)
                continue
            
            if (re.search(r"[^a-zA-Z]", user_input)):
                print("\033[91mILLEGAL CHARACTERS FOUND.\033[00m")
                time.sleep(1.5)
                continue

            break

        if self.__try_guess(user_input):
            print("\033[92mYOU WON\033[00m")
            return False
        
        self.__attemptsLeft -= 1

        if self.__attemptsLeft == 0:
            print("\033[91mGAME OVER.\033[00m")
            print(f"THE CORRECT WORD WAS : {self.__word_to_find}")
            return False

        return True

    def __try_guess(self, guess: str) -> bool:
        """Compares the guess to the word to find and prints out the result"""
        guess = guess.upper()
        find_dict: dict[str, int] = Sutom.__letter_dict(self.__word_to_find)

        # By default all letters are wrongly placed, then apply algorithm to
        # fix this.
        placement_list: list[LetterPlacement] = [LetterPlacement.WRONG 
                                                 for i in range(len(guess))]

        correctly_placed: int = 0
        # First pass for correctly placed letters
        for index, letter in enumerate([*guess]):
            if self.__word_to_find[index] == letter:
                placement_list[index] = LetterPlacement.RIGHT
                correctly_placed += 1
                find_dict[letter] -= 1

        # Second pass for misplaced letters
        for index, letter in enumerate([*guess]):
            if letter in find_dict and self.__word_to_find[index] != letter:
                if find_dict[letter] > 0:
                    placement_list[index] = LetterPlacement.MISPLACED
                    find_dict[letter] -= 1

        self.__attempts.append(self.__get_guess_result(guess, placement_list))

        return guess == self.__word_to_find
    
    def get_attempt_limit(self) -> int:
        """Returns the maximum amount of attempts before the game ends"""
        return self.__attemptLimit

    def attempts_left(self) -> int:
        """Returns the amount of attempts left before the game ends"""
        return self.__attemptsLeft
    
    def __get_guess_result(self, guess: str, 
                             placement_list: list[LetterPlacement]) -> str:
        """Returns the result of a guess as a formatted string"""
        
        attempt_string: str = ""
        for index, letter in enumerate([*guess]):
            attempt_string += placement_list[index].value + letter

        attempt_string += "\033[00m"
        return attempt_string
            

    @staticmethod
    def __get_random_word() -> str:
        """Returns a random word from the dictionary"""
        dictionary_file: TextIOWrapper = open(DICTIONARY_PATH, "r")
        words: list[str] = dictionary_file.readlines()

        return random.choice(words).strip()
    
    @staticmethod
    def __letter_dict(word: str) -> dict[str, int]:
        """
        Turns a word into a dictionary containing the number of occurences of
        each letter in that word.
        Example : beer -> {b: 1, e: 2, r: 1}
        """
        result_dict: dict[str, int] = {}

        for letter in [*word]:
            if letter in result_dict:
                result_dict[letter] += 1
            else:
                result_dict[letter] = 1

        return result_dict


    
'''target game'''
from typing import List
import string
import random


def generate_grid() -> List[List[str]]:
    """
    Generates list of lists of letters - i.e. grid for the game.
    e.g. [['I', 'G', 'E'], ['P', 'I', 'S'], ['W', 'M', 'G']]
    >>> print('Doctests will not work because the order of the words differs every time')
    Doctests will not work because the order of the words differs every time
    """
    alphabet = string.ascii_lowercase
    grid = []
    for r in range(3):
        row = []
        for c in range(3):
            row.append(random.choice(alphabet))
        grid.append(row)
    print('\n'.join(list(map(' '.join, grid))))
    return grid


def get_words(f: str, letters: List[str]) -> List[str]:
    """
    Reads the file f. Checks the words with rules and returns a list of words.
    >>> print('Doctests will not work because the order of the words differs every time')
    Doctests will not work because the order of the words differs every time
    """
    with open(f, 'r') as words_file:  # '#en: English'
        possible_words = set()
        lines_words = words_file.readlines()
        for word in lines_words:
            word = word[:-1].lower()
            if len(word) >= 4 and letters[4] in word:
                possible_words.add(word)
        letters_tuple = tuple((letter, letters.count(letter)) for letter in letters)
        words_matching = []
        for word in possible_words:
            letter_matches = 0
            for letter in word:
                count = word.count(letter)
                for key_letter in letters_tuple:
                    if letter == key_letter[0] and count <= key_letter[1]:
                        letter_matches += 1
                        break
                if letter_matches == 0:
                    break
            if letter_matches == len(word):
                words_matching.append(word)
        return words_matching


def get_user_words() -> List[str]:
    """
    Gets words from user input and returns a list with these words.
    Usage: enter a word or press ctrl+d to finish.
    >>> print('Doctests will not work because the order of the words differs every time')
    Doctests will not work because the order of the words differs every time
    """
    words = []
    while True:
        try:
            x = input('Введіть слово:')
            if x:
                words.append(x)
            else:
                return words
        except EOFError or KeyboardInterrupt:  # pressing CTRL+D
            return words


def get_pure_user_words(user_words: List[str], letters: List[str], words_from_dict: List[str]) -> List[str]:
    """
    (list, list, list) -> list

    Checks user words with the rules and returns list of those words
    that are not in dictionary.
    >>> print('Doctests will not work because the order of the words differs every time')
    Doctests will not work because the order of the words differs every time
    """
    passed_user_words = set()
    for word in user_words:
        if len(word) >= 4 and letters[4] in word:
            passed_user_words.add(word)
    letters_tuple = tuple(set(((letter, letters.count(letter)) for letter in letters)))
    words_matching = []
    words_not_in_dict = []
    for word in passed_user_words:
        letter_matches = 0
        for letter in word:
            count = word.count(letter)
            for key_letter in letters_tuple:
                if letter == key_letter[0] and count == key_letter[1]:
                    letter_matches += 1
                    break
            if letter_matches == 0:
                break
        if letter_matches == len(word):
            words_matching.append(word)
    for word in words_matching:
        if word not in words_from_dict:
            words_not_in_dict.append(word)
    return words_not_in_dict


def results():
    """
    Printing results
    :return: None
    """
    grid_list = ','.join(list(map(','.join, generate_grid()))).split(',')
    possible_words = get_words(r'en.txt', grid_list)
    user_choice = get_user_words()
    pure_words = get_pure_user_words(user_choice, grid_list, possible_words)  # not in dictionary words
    guessed_right = []
    skipped_words = []
    count = 0
    for word in user_choice:
        if word in possible_words:
            guessed_right.append(word)
            count += 1
        else:
            skipped_words = list(set(possible_words).difference(set(guessed_right)))
    with open('result.txt', 'w') as file:
        to_write = f'Guessed right {count} words: {guessed_right}\n' + f'All possible words: {possible_words}\n' + \
                   f'Skipped words: {skipped_words}\n' + f'Words, that are not in dictionary: {pure_words}'
        file.write(to_write)
        print(to_write)

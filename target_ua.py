'''target game'''
from typing import List
import string
import random
import io


def generate_grid() -> List[str]:
    """
    Generates list of lists of letters - i.e. grid for the game.
    e.g. [['I', 'G', 'E'], ['P', 'I', 'S'], ['W', 'M', 'G']]
    >>> print('Doctests will not work because the order of the words differs every time')
    Doctests will not work because the order of the words differs every time
    """
    alphabet = 'а, б, в, г, ґ, д, е, є, ж, з, и, і, ї, й, к, л, м, н, ' \
               'о, п, р, с, т, у, ф, х, ц, ч, ш, щ, ь, ю, я'.split(', ')
    grid = []
    while len(grid) <= 5:
        alpha = random.choice(alphabet)
        if alpha not in grid:
            grid.append(alpha)
    return grid


def get_words(f: str, letters: List[str]) -> List[str]:
    """
    Reads the file f. Checks the words with rules and returns a list of words.
    >>> print('Doctests will not work because the order of the words differs every time')
    Doctests will not work because the order of the words differs every time
    """
    with io.open(f, mode='r', encoding='utf-8') as words_file:
        possible_words = []
        for word in words_file:
            word, *speech_parts = word.lower().split()
            if word[0] in letters and len(word) <= 5:
                if '/n' in speech_parts[0] or 'noun' in speech_parts[0]:
                    possible_words.append((word, 'noun'))
                elif '/adj' in speech_parts[0] or 'adj' in speech_parts[0]:
                    possible_words.append((word, 'adjective'))
                elif '/v' in speech_parts[0] or 'v' in speech_parts[0]:
                    possible_words.append((word, 'verb'))
                elif 'adv' in speech_parts[0] or '/adv' in speech_parts[0]:
                    possible_words.append((word, 'adverb'))
        return possible_words


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


def check_user_words(user_words: List['str'], language_part: str, letters, dict_of_words: list):
    """
    (list, str, list) -> list

    Checks user words with the rules and returns list of those words
    that are not in dictionary.
    >>> print('Doctests will not work because the order of the words differs every time')
    Doctests will not work because the order of the words differs every time
    """
    guessed_right = []
    for word in user_words:
        if word[0].strip() in letters and len(word.strip())<=5:
            for pair in dict_of_words:
                if word.strip() == pair[0] and language_part == pair[1]:
                    guessed_right.append(word.strip())
                    break
    pair = 0
    while pair < len(dict_of_words):
        if language_part != dict_of_words[pair][1]:
            dict_of_words.pop(pair)
            pair -= 1
        pair += 1
    skipped = set(dict_of_words).difference(set(guessed_right))
    return guessed_right, list(skipped)


def results():
    """
    Printing results
    :return: None
    """
    grid_list = generate_grid()
    print(grid_list)
    language_part = random.choice(['noun', 'verb', 'adjective', 'adverb'])
    print(f'Ваша частина мови:{language_part}')
    possible_words = get_words(r'base.txt', grid_list)
    user_choice = get_user_words()
    guessed_right, skipped = check_user_words(user_choice, language_part, grid_list, possible_words)
    with open('result.txt', 'w') as file:
        to_write = f'Guessed right {len(guessed_right)} words: {guessed_right}\n' + f'All possible words: {possible_words}\n' + \
                   f'Skipped words: {skipped}\n'
        file.write(to_write)
        print(to_write)

#get_words('base.txt', ['а', 'б', 'в', 'г', 'д'])
#print(check_user_words(['абаз', 'абая', 'битий', 'бидля'], 'noun', ['а', 'б', 'в', 'г', 'д'], get_words('base.txt', ['а', 'б', 'в', 'г', 'д'])))
results()
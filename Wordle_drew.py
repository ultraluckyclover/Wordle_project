import logging
import os
import math
from scipy.stats import entropy
from wordfreq import word_frequency
import numpy as np
import json
from random import randrange, random, shuffle
from linecache import getline
from itertools import product, count
from tqdm import tqdm as ProgressDisplay

# combining path of program to data files
data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")

short_list = os.path.join(data_dir, "possible_words.txt")
long_list = os.path.join(data_dir, "allowed_words.txt")
freq_list = os.path.join(data_dir, "long_list_freq.txt")
freq_list_map = os.path.join(data_dir, "freq_map.json")
narrowed_down = os.path.join(data_dir, "narrowed_down.txt")
pattern_matrix_file = os.path.join(data_dir, "pattern_matrix.npy")
pattern_grid_data = dict()

print("running...")
def pick_word():

    #picks a random word from the list of possible words

    with open(short_list) as words:
        length = len(words.readlines())
    pick = randrange(1, length)
    line = getline(short_list, pick - 1)
    pieces = line.split(' ')
    return pieces[0]
def guessed_word(guess, answer):

    #This function assigns a pattern to the guessed word
    # based on the letters in the answer

    colors = []
    for i in range(5):
        # if a guessed letter is in the right place
        if guess[i] == answer[i]:
            colors.append("🟩")
        # if a guessed letter is in the wrong place but is in the word
        elif (guess[i] in answer) and (guess[i] != answer[i]):
            colors.append("🟨")
        else:
            colors.append("⬛")
    return colors
def new_possible_words(guess, colors, firstRound=True):

    # This function narrows the list down to words
    # which match the conditions from the previous guess(es)

    new_list = []

    def resize(list):
        resize = []
        for j in range(len(list)):
            if list[j] != "NONE":
                resize.append(list[j])
        return resize

    if firstRound == True:
        # print("here1")
        with open(short_list, 'r') as original, open(narrowed_down, 'w') as copy:
            for line in original.readlines():
                copy.write(line)

    with open(narrowed_down, 'r') as file:
        words = file.readlines()
        for word in words:
            new_list.append(word)

    for i in range(5):
        counter = 0

        # letter guess[i] is green,yellow or grey?
        if (colors[i] == "🟩"):
            # check green letter against words in list
            for j in range(len(new_list)):
                word = new_list[j]

                if guess[i] != word[i]:
                    counter += 1
                    new_list[j] = "NONE"


        if (counter != 0):
            new_list = np.copy(resize(new_list))
            counter = 0


        if (colors[i] == "🟨"):
            for j in range(len(new_list)):
                if (guess[i] not in new_list[j] or guess[i] == new_list[j][i]):
                    # print(guess[i], 'is not in', new_list[j])
                    counter += 1
                    new_list[j] = "NONE"

        if (counter != 0):
            new_list = np.copy(resize(new_list))
            counter = 0


        if (colors[i] == "⬛"):
            # print(guess[i], "is grey")
            for j in range(len(new_list)):
                if (guess[i] in new_list[j]):
                    # print(guess[i], "is in ", new_list[j])
                    counter += 1
                    new_list[j] = "NONE"

        if (counter != 0):
            new_list = np.copy(resize(new_list))
            counter = 0

        # print("after grey list is now", new_list)

        with open(narrowed_down, 'w') as file:
            for j in range(len(new_list)):
                word = new_list[j]
                file.write(word)
def run(firstGuess):
    #answer = pick_word()
    answer = 'aback'
    result = guessed_word(firstGuess, answer)
    print("answer is ", answer)
    print(result)
    new_possible_words(firstGuess, result)

    for i in range(5):
        if result == ['🟩', '🟩', '🟩', '🟩', '🟩']:
            print("Got it in", i + 1, "/6 tries")
            return 0
        else:
            guess = input(str("input another guess:"))

            result = guessed_word(guess, answer)
            print(result)
            new_possible_words(guess, result, firstRound=False)
    return 0

run("train")

# if __name__ == "__main__":
#     first_guess = "crane"
#     results, decision_map = simulate_games(
#         firstGuess = first_guess,
#         priors = get_true_wordle_prior(),
#         shuf = True,
#     )
# answer = pick_word()
# result = guessed_word("salet", answer)
# print(result)
# new_possible_words("salet", result)
# print("answer is ", answer)

# def new_possible_words(guess,colors,possible = False):
#     new_list = []
#
#     # if there is not already a smaller set of words
#     if possible == False:
#         for i in range(5):
#             if (colors[i] == "🟩"):
#                 with open(short_list) as words:
#                     for word in words.readlines():
#                         if guess[i] == word[i]:
#                             new_list.append(word)
#
#     # after the first turn there is a smaller list
#     else:
#         print("passed in a smaller list")
#         for i in range(5):
#             if (colors[i] == "🟩"):
#                 with open(narrowed_down) as words:
#                     for word in words.readlines():
#                         if guess[i] == word[i]:
#                             new_list.append(word)
#
#     # if there were no green letters, start list for yellow letters
#     if new_list == []:
#         print("There are no green letters")
#         for i in range(5):
#             if (colors[i] == "🟨"):
#                 with open(short_list) as words:
#                      for word in words.readlines():
#                         if guess[i] in word:
#                             new_list.append(word)
#
#     # if there were green letters, narrow down the list
#     else:
#         print("there are green letters")
#         for i in range(5):
#             if (colors[i] == "🟨"):
#                 for word in new_list:
#                     if guess[i] not in word:
#                         new_list.remove(word)
#
#     # if there havent been any green or yellow letters
#     if new_list == []:
#         print("there are no green or yellow letters")
#         for i in range(5):
#             if (colors[i] == "⬛"):
#                 with open(short_list) as words:
#                     for word in words.readlines():
#                         if guess[i] not in word:
#                             new_list.append(word)
#
#     # if there have been green and/or yellow letters
#     else:
#         print("there are some yellow and some green")
#         for i in range(5):
#             if (colors[i] == "⬛"):
#                 for word in new_list:
#                     ind = new_list.index(word)
#                     print('index', new_list.index(word))
#                     print('word is ', word)
#                     if guess[i] not in word:
#                         continue
#                     else:
#                         print("answer does not have", guess[i], "so im removing", word)
#                         #new_list.remove(word)
#                         new_list[ind] = 0
#
#     print("length of narrowded", len(new_list))
#     with open(narrowed_down, 'w') as file:
#         for j in range(len(new_list)):
#             word = new_list[j]
#             if ( j < len(new_list) - 1):
#                 file.write(word)


#
#
# print("here2")
# for i in range(5):
#     print("i is ", i)
#         #letter guess[i] is green,yellow or grey?
#     if (colors[i] == "🟩"):
#         with open(narrowed_down,'r') as read:
#             words = read.readlines()
#             for word in words:
#                 with open(narrowed_down,'w') as right:
#                     print("guess[i]", guess[i])
#                     print("word[i]", word[i])
#                     if (guess[i] == word[i]):
#                         right.write("FART")
#                     else:
#                         print(word, 'is not in the list')


# line = read.readline()
# for letter in line:
#      with open(narrowed_down,'w') as right:
#         print('word is ', line)
#         if guess[i] == letter:
#             right.write(line)
#             print("guess[i]", guess[i])
#             print("word[i]",letter)
#         else:
#              print(line, 'is not in the list')


# a = ['a','b','z','H']
# after_removed =[a in ('H' not in a and 'L' not in a and 'C' not in a)] # this is the after removed 'H', 'L', and 'C' from the input_list
#
# print(after_result)


# answer = pick_word()
# result = guessed_word("salet",answer)
# print(result)
# new = new_redo("salet",result)
# print(new)
# print("answer is ", answer)

# def new_redo(guess,colors,possible = False):
#     if possible == False:
#         with
#     else:
#         continue
#
#     for i in range(5):


# run("salet")


# with open(long_list) as file:
#         freq = open("data/long_list_freq.txt", "w")
#         for line in file:
#             word = line.rstrip()
#             p = str(word_frequency(word,'en'))
#             if line != "zymic":
#                 freq.write(word + " " + p + '\n')
#             else:
#                 freq.write(word + " " + p)

# A = os.path.join(os.path.dirname(__file__), '..')
# # A is the parent directory of the directory where program resides.
# B = os.path.dirname(os.path.realpath(__file__))
# # B is the canonicalised (?) directory where the program resides.
# C = os.path.abspath(os.path.dirname(__file__))
# # C is the absolute path of the directory where the program resides.
#
# print('data_dir',data_dir)
# print('A', A)
# print('B', B)
# print('C', C)
# print(__file__)

# for i in range(len(words)):
#     print("i is ", i)
#     print(words[i])
#     for j in range(5):
#         print("j is",j)
#         print(words[i][j])
#         return np.array([ord(words[i][j])],dtype = np.uint8)
# for word in words:
#     print("word is ", words)
#     for letter in word:
#         print("letter is", letter)
#         return np.array([ord(letter)],dtype = np.uint8)

# print('words are', words)
# for word in words:
#     print('word is ', word[0][0])
# for i in range(5):
#     print('letter is ', word[i])
# return np.array( [[ord(letter)for letter in word] for word in words], dtype = np.uint8)
# for words in wordsArr:
#     for word in words:
#         for letter in word:
#             return np.array([ord(letter)], dtype = np.uint8)

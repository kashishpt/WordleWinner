import numpy as np
import pandas as pd


# Eliminates all words taht have a certain character at a specified location
# @param pos - the position that the function should search for the character
# @param let - the character that should be eliminated
# @param dct - the DataFrame that will be searched
# @return dct - returns the modified DataFrame
def indexElimination(pos, let, dct):
    reg = "." * pos + "[^" + let + "]" + "." * (4-pos)
    dct = dct[ dct['word'].str.match( reg) ]
    return dct

# Eliminates all words that do not have a specified number of appearances of a certain letter.
# @param list1 - list of letters that will be compared to the DataFrame. The amount of appearances of the certain
# letter is found by the number of appearances in list1 and list2
# @param list2 - list of letters that will be compared to the DataFrame. Same purpose as list1
# @param let - the letter that should be removed from the words
# @param dct the DataFrame that will be analyzed
# @return - the modified DataFrame
def breadthElimination(list1, list2, let, dct):
    num = list1.count(let) + list2.count(let)
    reg = "\D*"
    for i in range(num):
        reg += let + "\D*"
    return dct[dct['word'].str.match(reg)]

# Displays the message after each guess that shows the remaining possible words and the amount of words left
# @param df - the DataFrame whose details will be printed
def message(df):
    print("--------------------------------------")
    print(df)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("There are %d possible words" % len(df))

# Filters out the DataFrame
# @param guess - the word that was guessed
# @param result - the sequence of letters that represent the colors that resulted from the guess
# @param words - the DataFrame that will be filtered
# @return - the modified DataFrame
def filter(guess, result, words):
    g_letters = []
    y_letters = []

    for j in range(len(result)):
            if result[j] == 'g':
                g_letters.append(guess[j])
                reg_exp = "." * j + guess[j] + "." * (4 - j)
                words = words[ words['word'].str.match( reg_exp ) ]
        
    for j in range(len(result)):
        if result[j] == 'y' or result[j] == 'o':
            y_letters.append(guess[j])
            words = words[ words.word.str.contains( guess[j] ) ]
            words = indexElimination(j, guess[j], words)
            
    for j in range(len(result)):
        if result[j] == 'r' or result[j] == 'b':
            if guess[j] not in g_letters and guess[j] not in y_letters:
                reg = ("[^" + guess[j] + "]") * 5
                words = words[words['word'].str.match(reg)]
            else:
                words = breadthElimination(g_letters, y_letters, guess[j], words)
    
    return words


# Runs the game
def guess():

    words = pd.read_csv('valid_solutions.csv')
    i = 1
    while i < 6:
        y_letters = []
        g_letters = []
        guess = ""
        result = ""
        cont = True
        while cont:
            cont = False
            guess = input("Enter guess %d (or \'stop\' to end the program): " % (i))
            if guess.upper() == 'STOP':
                break
            if len(guess) != 5:
                print("\"%s\" is invalid, try again." % guess)
                cont = True

            else:
                result = input("Enter result for \'%s\': " % (guess))
                if len(result) != 5:
                    print("\"%s\" is invalid, try again." % result)
                    cont = True
                elif result == 'ggggg':
                    print("Congratulations!")
                    break

        if guess.upper() == 'STOP' or result == 'ggggg':
            return i
            break

        words = filter(guess, result, words)

        message(words)

        if len(words) < 2:
            return i
            break

guess()

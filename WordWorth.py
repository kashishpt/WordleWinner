# This program determines which words have the best "weight"
# To determine the weight, the program first finds the number of appearances of each letter in all the words in valid_solutions.csv
# Then, it loops through each word and adds the weight of each of its letters for the word's total weight
# The results are in weights.csv in descending order

import pandas as pd
import numpy as np

words = np.loadtxt('valid_solutions.csv', dtype='str')

letters = {
    'a': 0,
    'b': 0,
    'c': 0,
    'd': 0,
    'e': 0,
    'f': 0,
    'g': 0,
    'h': 0,
    'i': 0,
    'j': 0,
    'k': 0,
    'l': 0,
    'm': 0,
    'n': 0,
    'o': 0,
    'p': 0,
    'q': 0,
    'r': 0,
    's': 0,
    't': 0,
    'u': 0,
    'v': 0,
    'w': 0,
    'x': 0,
    'y': 0,
    'z': 0
}


for word in words:
    for letter in word:
        letters[letter] = letters[letter] + 1

weights = np.array([])

for word in words:
    weight = 0
    used = []
    for letter in word:
        if letter not in used:
            weight += letters[letter]
            used.append(letter)
    weights = np.append(weights, weight)

max = 0
max_index = 0
for i in range(len(weights)):
    if weights[i] > max:
        max = weights[i]
        max_index = i

df = pd.DataFrame()

df['word'] = words
df['weight'] = weights

df = df.sort_values(by='weight', ascending=False)

df = df.set_index('word')
df.to_csv('weights.csv')

print(df.head())

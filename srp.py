#!/usr/bin/env python3

import unicodedata
import csv
import collections
import random
import re

MIN_HSK_LEVEL = 2
MAX_HSK_LEVEL = 2
START_TTL=2
SRP_INCORRECT_DISTANCE = 4
SRP_CORRECT_DISTANCE = 30

VOCAB = collections.deque()

def strip_accents(s):
    # I have no idea what I did in this function
    return ''.join(c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn')

def get_hsk_data():
    hsk_data = []
    with open('data/hsk.csv', 'r') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=';')
        for row in csvreader:
            row['Pinyin'] = row['Pinyin'].replace("\xa0", "")
            row['Ascii'] = strip_accents(row['Pinyin'])
            row['HSK Set'] = int(row['HSK Set'])
            row['TTL'] = START_TTL
            if row['HSK Set'] >= MIN_HSK_LEVEL and row['HSK Set'] <= MAX_HSK_LEVEL:
                hsk_data.append(row)
    return hsk_data

def proc_ans(ans):
    ans = ans.split("｜")[0]
    ans = re.sub(r'\W+', '', ans)
    return ans.replace(" ", "")

def ask_q(vocab):
    result = 0
    print()
    #print(vocab['Character'])
    user_in = proc_ans(input("({}) {}: ".format(vocab['TTL'], vocab['Character'])))

    if user_in == proc_ans(vocab['Ascii']):
        print("Correct!")
        result = 1
    else:
        print("Nope. {}".format(vocab['Ascii']))
    
    print("{} -- {}".format(vocab['Pinyin'], vocab['Meaning']))
    return result

def srp():
    while len(VOCAB) > 0:
        if(len(VOCAB) % 1 == 0):
            print("{} words remaining!".format(len(VOCAB)))
        word = VOCAB.popleft()
        result = ask_q(word) 
        if result: # correct
            # Decrement the TTL
            word['TTL'] = word['TTL']-1
            
            # Re-insert further down
            if word['TTL'] > 0:
                VOCAB.insert(SRP_CORRECT_DISTANCE, word)

        else: # incorrect
            while not ask_q(word):
                ()
            print("Adding spaced repetition practice with TTL {}".format(word['TTL']))
            VOCAB.insert(SRP_INCORRECT_DISTANCE, word) 

def main():
    print("Getting vocab from Level {} to {}".format(MIN_HSK_LEVEL, MAX_HSK_LEVEL))
    hsk_data = get_hsk_data()
    print("Shuffling {} vocabulary words...".format(len(hsk_data)))
    random.shuffle(hsk_data)
    VOCAB.extend(hsk_data)
    srp()

if __name__ == '__main__':
    main()

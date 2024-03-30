import pandas as pd

data_frame = pd.read_csv("nato_phonetic_alphabet.csv")

alphabet_dict = {row.letter: row.code for (index, row) in data_frame.iterrows()}


def generate_phonetic():
    word = input("Word from users: ").upper()
    try:
        new_list = [alphabet_dict[c] for c in word]
    except KeyError:
        print("Sorry, only letters in the alphabet please.")
        generate_phonetic()
    else:
        print(new_list)


generate_phonetic()

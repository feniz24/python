with open("./Input/Names/invited_names.txt") as names:
    invite_names = names.readlines()

with open("./Input/Letters/starting_letter.txt", 'r') as letter:
    letter = letter.read()
    for name in invite_names:
        replaced_letter = letter.replace("[name]", name.strip("\n"))
        with open(f"./Output/ReadyToSend/{name}.txt", "w") as file:
            file.write(replaced_letter)
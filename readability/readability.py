
from cs50 import get_string

# get user input
text = get_string("Text: ")

# initialize variables
letters = 0
words = 1
sentences = 0
length = len(text)

for i in range(length):

    # count the letters
    if (text[i].isalpha()):
        letters += 1

    # count the words
    if (text[i].isspace()):
        words += 1

    # count the sentences
    if (text[i] == '.' or text[i] == '!' or text[i] == '?'):
        sentences += 1

# calculate the Coleman-Liau Index
L = (letters / float(words)) * 100
S = (sentences / float(words)) * 100
grade = round(0.0588 * L - 0.296 * S - 15.8)
# print out the appropriate grade
if grade < 1:
    print("Before Grade 1")
elif grade >= 16:
    print("Grade 16+")
else:
    print(f"Grade: {grade}")
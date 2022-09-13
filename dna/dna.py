from csv import reader, DictReader
from sys import argv, exit


def main():
    # check command-line arguments
    if len(argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        exit()


# file names
database = argv[1]
dna = argv[2]

# open files and read into memory
with open(database, "r") as csvfile:
    reader = DictReader(csvfile)
    dict_list = list(reader)

with open(dna, "r") as file:
    dna_sequence = file.read()

# create an empty array to store the MAX STR sequence
max_count = []

# Loop over the STR in the people dict and count the number of occurrences of each STR
for i in range(1, len(reader.fieldnames)):
    STR = reader.fieldnames[i]
    max_count.append(0)

    for j in range(len(dna_sequence)):
        STR_count = 0

        # if a match is found, start counting
        if dna_sequence[j:(j + len(STR))] == STR:
            k = 0
            while dna_sequence[(j + k):(j + k + len(STR))] == STR:
                STR_count += 1
                k += len(STR)
                # if there is a new max amount of STR repeats, count must be updated
                if STR_count > max_count[i - 1]:
                    max_count[i - 1] = STR_count

# compare against people data to find a match
for i in range(len(dict_list)):
    match = 0
    for j in range(1, len(reader.fieldnames)):
        if int(max_count[j - 1]) == int(dict_list[i][reader.fieldnames[j]]):
            match += 1
            if match == (len(reader.fieldnames) - 1):
                print(dict_list[i]['name'])
                exit()
print("No match")

main()


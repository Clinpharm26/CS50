import cs50
from cs50 import get_float

dollar = 0
# get user input for change needed
while dollar <= 0:
    dollar = get_float("Change needed: ")

# convert dollars to cents
cents = round(dollar * 100)
coins = 0

# while loop for quaters
while cents >= 25:
    cents -= 25
    coins += 1

# while loop for dimes
while cents >= 10:
    cents -= 10
    coins += 1

# while loop for nickels
while cents >= 5:
    cents -= 5
    coins += 1

# while loop for pennies
while cents >= 1:
    cents -= 1
    coins += 1

print("Coins needed:", coins)

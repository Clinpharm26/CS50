import cs50
from cs50 import get_int

# if int is b/w 1-8 the break otherwise, prompt user for int
h = 0
while h < 1 or h > 8:
    h = get_int("Height: ")

# iterate over columns and rows
for i in range(h):
    print((h - i - 1) * " ", end="")
    print((i + 1) * "#")
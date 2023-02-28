
# QUESTION 8: Writee a program that generates random 4 digits number of 0s and 1s and convert the generated number to base 10
import random

# Generate a random 4-digit number of 0s and 1s
binary_num = ""
for i in range(4):
    binary_num += str(random.randint(0, 1))

print("Random binary number:", binary_num)

# Convert the binary number to base 10
decimal_num = int(binary_num, 2)

print("Decimal equivalent:", decimal_num)
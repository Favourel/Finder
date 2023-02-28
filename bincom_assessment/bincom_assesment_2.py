# QUESTION 2: Which color is mostly worn throughout the week?
from collections import Counter

string_list = "GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, BLUE, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN"

# Convert the string to a list of strings
items_list = string_list.split(", ")

# Use Counter to count the occurrences of each item in the list
count_dict = Counter(items_list)

# Find the most common item
most_common = count_dict.most_common(1)

# Print the most common item
print(f"Most common item: {most_common[0][0]}, frequency: {most_common[0][1]}")

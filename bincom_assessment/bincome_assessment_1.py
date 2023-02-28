# QUESTION 1
"""
To calculate the mean of a list of items like the one you provided in Python, you will first need to convert the string into a list of values.
"""
import statistics

string_list = "GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, BLUE, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN"

# Convert the string to a list of strings
items_list = string_list.split(", ")

# Use a dictionary to count the occurrences of each item in the list
count_dict = {}
for item in items_list:
    count_dict[item] = count_dict.get(item, 0) + 1

# Print the counts for each item
for item, count in count_dict.items():
    print(f"{item}: {count}")

# Calculate the mean using the statistics module
mean = statistics.mean(count_dict.values())
print(f"Mean: {mean}")


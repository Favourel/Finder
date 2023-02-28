# QUESTION 4: Get the variance of the colors
import statistics

string_list = "GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, BLUE, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN"

# Convert the string to a list of strings
items_list = string_list.split(", ")

# Use a dictionary to count the occurrences of each item in the list
count_dict = {}
for item in items_list:
    count_dict[item] = count_dict.get(item, 0) + 1

# Calculate the variance using the statistics module
variance = statistics.variance(count_dict.values())
print(f"Variance: {variance}")
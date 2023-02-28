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


# QUESTION 3:
class Solution_Median(object):
    # def findMedianSortedArrays(self, nums1, nums2):

    def findMedianSortedArrays(self, data):
        # Convert the string to a list of strings
        items_list = string_list.split(", ")

        # Use a dictionary to count the occurrences of each item in the list
        count_dict = {}
        for item in items_list:
            count_dict[item] = count_dict.get(item, 0) + 1

        # Convert the dictionary values to a list and sort it
        sorted_counts = sorted(count_dict.values())

        data = sorted(sorted_counts)
        n = len(data)
        if n == 0:
            print("no median for empty data")
        if n % 2 == 1:
            return data[n // 2]
        else:
            i = n // 2
            return (data[i - 1] + data[i]) / 2


string_list = "GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, BLUE, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN"

solution = Solution_Median()
print(solution.findMedianSortedArrays(string_list))

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


# QUESTION 5: if a colour is chosen at random, what is the probability that the color is red?


# QUESTION 7: write a recursive searching algorithm to search for a number entered by user in a list of numbers

class Solution(object):
    def search_range(self, nums, target):
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                if nums[i] == nums[j] == target:
                    print([nums[i], nums[j]])

                    return i, j

                elif nums.count == 1:
                    for k in range(n):
                        if nums[k] == target:
                            return k
                    return 0, 0

        return -1, -1


solution = Solution()
print(solution.search_range([2, 1, 23, 11, 2], 2))

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


# question 9: Write a program to sum the first 50 fibonacci sequence in python
# Function to calculate the nth Fibonacci number
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


# Sum the first 50 Fibonacci numbers
fib_sum = 0
for i in range(50):
    fib_sum += fibonacci(i)

print("Sum of the first 50 Fibonacci numbers:", fib_sum)

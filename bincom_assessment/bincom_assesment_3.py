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
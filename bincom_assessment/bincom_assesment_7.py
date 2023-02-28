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
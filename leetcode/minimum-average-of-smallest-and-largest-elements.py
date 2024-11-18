class Solution:
    def minimumAverage(self, nums: List[int]) -> float:
        result = float("inf")
        nums.sort()
        
        for i in range(len(nums)//2):
            result = min((nums[0] + nums[-1]) / 2, result)
            del nums[0]
            del nums[-1]

        return result

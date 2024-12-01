class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        res = defaultdict(list)

        for word in strs:
            chars = [0] * 26  # lowercase values
            for char in word:
                chars[ord(char) - ord("a")] += 1

            res[tuple(chars)].append(word)

        return res.values()

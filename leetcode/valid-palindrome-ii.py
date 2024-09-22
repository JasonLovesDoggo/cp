# SOL ONE - 119ms - 19.5mb
class Solution:
    def validPalindrome(self, s: str) -> bool:
        def IsPalindrome(l, r, c):
            if c > 1:
                return False
            while l < r:
                if s[l] != s[r]:
                    return IsPalindrome(l + 1, r, c + 1) or IsPalindrome(l, r - 1, c + 1)
                l += 1
                r -= 1
            return True

        return IsPalindrome(0, len(s) - 1, 0)


# SOL TWO - 90ms - 16.9mb
class Solution:
    def validPalindrome(self, s: str) -> bool:
        left, right = 0, len(s) - 1

        while left < right:
            if s[left] != s[right]:
                skipL, skipR = s[left + 1:right + 1], s[left:right]
                return skipL == skipL[::-1] or skipR == skipR[::-1]
            left, right = left + 1, right - 1
        return True

from collections import Counter

def findSubstring(s, words):
    L = len(words[0])
    n = len(words)
    need = Counter(words)
    res = []

    for offset in range(L):
        left = offset
        count = 0
        window = Counter()
        
        right = offset
        while right + L <= len(s):
            word = s[right:right+L]
            right += L
            
            if word not in need:
                # dead window, reset
                window.clear()
                count = 0
                left = right
                continue
            
            window[word] += 1
            count += 1
            
            # too many of this word? shrink from left
            while window[word] > need[word]:
                left_word = s[left:left+L]
                window[left_word] -= 1
                count -= 1
                left += L
            
            if count == n:
                res.append(left)
                # slide left forward by one word to look for next match
                left_word = s[left:left+L]
                window[left_word] -= 1
                count -= 1
                left += L
    
    return res
s = "wordgoodgoodgoodbestword"
words = ["word","good","best"]
print(findSubstring(s,words))
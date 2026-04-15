import random
class RandomizedSet(object):

    def __init__(self):
        self.set = {}

    def insert(self, val):
        if val not in self.set or not self.set[val]:
            self.set[val] = True
            return True

        return False

    def remove(self, val):
        if val in self.set and self.set[val]:
            self.set[val] = False
            return True

        return False
    
    def getRandom(self):
        keys = [x for x in self.set.keys() if self.set[x] == True]
        return random.choice(keys)

randomizedSet = RandomizedSet()
print(randomizedSet.remove(0))
print(randomizedSet.remove(0))
print(randomizedSet.insert(0))
print(randomizedSet.getRandom())
print(randomizedSet.remove(0))
print(randomizedSet.insert(0))
from collections import Counter

counts = Counter()

foo = ['a', 'a', 'a','b', 'c']
bar = [0, 0, 1, 1, 2]

for item in zip(foo, bar):
    counts[item] += 1
    
print(counts)
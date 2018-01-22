from collections import Counter, defaultdict
import itertools

counts = Counter()
finale = defaultdict(list)

list=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
iteration = 200

cutsize = (iteration * 0.05)/2;
print(int(cutsize))

list = list[int(cutsize):] #cut front

list = list[:len(list)-int(cutsize)] #cut back





print(list)


##################################
# foo = ['a', 'a', 'b', 'c']
# bar = ['Agriculture', 'Agriculture', 'Food', 'Sport']

# dic_sector =['Agriculture','Food','Sport','Monza']

# combinations = set(itertools.product(foo, dic_sector))

# for item in combinations:
# 	finale[item].append(counts[item])

# for item in zip(foo, bar):
# 	#key        = value
#     counts[item] += 1


# for item in finale:
# 	if not item in counts:
# 		finale[item].append(0)
# 	else:
# 		finale[item].append(counts[item])

# print(finale)


#############################333
# import random

# permutations = set()

# column = ['Agriculture', 'Agriculture', 'Clothing', 'Food']

# while len(permutations) < 10:
#     random.shuffle(column)
#     permutations.add(tuple(column))
    
# for permutation in permutations:
# 	print(permutation)

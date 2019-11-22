import random

random.seed(5)

locations = []


for i in range(1, 51):
    locations.append("a" + str(i))

#locations
f = open('small.txt','w')

#number of locations and homes
f.write(str(50) + "\n")
f.write(str(25) + "\n")

for i in range(50):
    f.write(locations[i] + " ")

f.write("\n")

#homes
homes = []
for i in range(25):
    rand = random.sample(range(1, 50), 25)
for i in rand:
    homes.append(locations[i])
    f.write(locations[i] + " ")

f.write("\n")

#starting location
set1 = set(locations)
set2 = set(homes)
valid_starts = set1.difference(set2)
f.write(valid_starts.pop())

f.write("\n")




#Adjacency Matrix
x = 1
y = 1
for i in range(50):
    for j in range(50):
        f.write("(" + str(x) + ", " + str(y) + ")")
        y+=1
    y = 1
    f.write("\n")
    x += 1
f.close()

#pick 25 random homes
print(len(valid_starts))
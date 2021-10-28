import matplotlib.pyplot as plt
import random

iterations = 100
drunkmanWalks = 100

#getting input
coords = []
while True:
    inp = input()
    if inp != '':
        coords.append(list(map(int, inp.split(' '))))
    else:
        break

#weight map prep
width = 0
height = 0
for i in coords:
    if width < i[0]:
        width = int(i[0])
    if height < i[1]:
        height = int(i[1])

#making weight map
coords2d = [[[list(filter(lambda x: x[0] == i and x[1] == j, coords))[0][2], True] if len(list(filter(lambda x: x[0] == i and x[1] == j, coords))) > 0 else [-1, False] for i in range(0, width + 1)] for j in range(0, height + 1)]

#drawing edges
coords = [*coords, coords[0]]
for i in range(len(coords) - 1):
    #edges by x
    inter = sorted([int(coords[i][0]), int(coords[i + 1][0])])
    inter[0] += 1
    for x in range(*inter):
        if coords[i + 1][0] - coords[i][0] != 0:
            y = round((x - coords[i][0]) * (coords[i + 1][1] - coords[i][1]) / (coords[i + 1][0] - coords[i][0]) + coords[i][1])
            z = (x - coords[i][0]) * (coords[i + 1][2] - coords[i][2]) / (coords[i + 1][0] - coords[i][0]) + coords[i][2]
            coords2d[y][x] = [z, True]
    #edges by y
    inter = sorted([int(coords[i][1]), int(coords[i + 1][1])])
    inter[0] += 1
    for y in range(*inter):
        if coords[i + 1][1] - coords[i][1] != 0:
            x = round((y - coords[i][1]) * (coords[i + 1][0] - coords[i][0]) / (coords[i + 1][1] - coords[i][1]) + coords[i][0])
            z = (y - coords[i][1]) * (coords[i + 1][2] - coords[i][2]) / (coords[i + 1][1] - coords[i][1]) + coords[i][2]
            coords2d[y][x] = [z, True]

#copy of weight map for drunkman method
coords2d2 = [[[x for x in j] for j in i] for i in coords2d]

#iterative method
for time in range(iterations):
    for i in range(1, len(coords2d) - 1):
        for j in range(1, len(coords2d[0]) - 1):
            if coords2d[i][j - 1][0] != -1 and coords2d[i][j - 1][0] != -1 and not coords2d[i][j][1]:
                coords2d[i][j][0] = (coords2d[i - 1][j][0] + coords2d[i][j + 1][0] + coords2d[i - 1][j][0] + coords2d[i][j - 1][0]) / 4

#drunkman method
for i in range(1, len(coords2d2) - 1):
        for j in range(1, len(coords2d2[0]) - 1):
            if coords2d2[i - 1][j][0] != -1 and coords2d2[i][j - 1][0] != -1 and coords2d2[i][j][0] == -1:
                avgsum = 0
                for time in range(drunkmanWalks):
                    curi, curj = i, j
                    while not coords2d2[curi][curj][1]:
                        dir = random.randint(0, 3)
                        if dir == 0:
                            curi += 1
                        elif dir == 1:
                            curi -= 1
                        elif dir == 2:
                            curj += 1
                        else:
                            curj -= 1
                    avgsum += coords2d2[curi][curj][0]
                coords2d2[i][j][0] = avgsum / drunkmanWalks

#drawing scatters
fig = plt.figure(figsize=(8,4))
ax = fig.add_subplot(121, projection = '3d')
ax.set_title('iterative method')

for idi, i in enumerate(coords2d):
    for idj, j in enumerate(i):
        if j[0] != -1:
            ax.scatter(idj, idi, j[0])

ax2 = fig.add_subplot(122, projection = '3d')
ax2.set_title('drunkman method')

for idi, i in enumerate(coords2d2):
    for idj, j in enumerate(i):
        if j[0] != -1:
            ax2.scatter(idj, idi, j[0])

plt.show()


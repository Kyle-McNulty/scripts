import random
from subprocess import call

target = open('/Users/kyle/Code/scripts/pokemonlist.txt', 'r')
listpokemon = list()
for line in target:
    oneLine = line
    ray = oneLine.split()
    for item in ray:
        if len(item) > 3:
            listpokemon.append(item)
target.close()
listpokemon.remove('mime')
choice = random.randint(0, len(listpokemon))
chosen = listpokemon[choice]

call(["ichooseyou", chosen])

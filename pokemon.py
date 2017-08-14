import random
from subprocess import call

# Run this script on terminal startup:
# python <path to file>; clear

target = open('/Users/kyle/Code/scripts/pokemonlist.txt', 'r')
listpokemon = list()
for line in target:
    oneLine = line
    ray = oneLine.split()
    for item in ray:
        # quick hack for dealing with formatting
        if len(item) > 3:
            listpokemon.append(item)
target.close()
# hack for removing a pokemon with two words, this could be improved
listpokemon.remove('mime')
choice = random.randint(0, len(listpokemon))
chosen = listpokemon[choice]

call(["ichooseyou", chosen])

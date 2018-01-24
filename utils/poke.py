import urllib2, json, random, pokebase, os

#use pokebase package to get info about this pokemon
def findPokemon(num):
    poke = pokebase.pokemon(num) 
    info = {}
    info["Name"] = poke
    info["Height"] = poke.height
    info["Sprite"] = pokebase.pokemon_sprite(num).path
    return info

'''
info = findPokemon(206)
for key in info:
    print key + ": "
    print info[key]
'''

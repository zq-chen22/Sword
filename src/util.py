def bondingPlaces(places):
    for placeI in places:
        for placeJ in places:
            if placeI not in placeJ.neighbors:
                placeJ.neighbors.append(placeI)

import pygame

def getPygameKey():
    keys = ""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            keys += event.unicode
    return keys
 

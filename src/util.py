def bondingPlaces(places):
    for placeI in places:
        for placeJ in places:
            if placeI not in placeJ.neighbors:
                placeJ.neighbors.append(placeI)

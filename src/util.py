def bondingPlaces(places):
    for placeI in places:
        for placeJ in places:
            if placeI not in placeJ.neighbors:
                placeJ.neighbors.append(placeI)



def getPygameKey():
    import pygame
    keys = ""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            keys += event.unicode
    return keys
 
def hex_to_rgb(hex):
  rgb = []
  for i in (0, 2, 4):
    decimal = int(hex[i+1:i+3], 16)
    rgb.append(decimal)
  
  return tuple(rgb)

def hex_to_bgr(hex):
  rgb = []
  for i in (0, 2, 4):
    decimal = int(hex[5-i:7-i], 16)
    rgb.append(decimal)
  
  return tuple(rgb)

from time import time 
  
  
def timer_func(func): 
    # This function shows the execution time of  
    # the function object passed 
    def wrap_func(*args, **kwargs): 
        t1 = time() 
        result = func(*args, **kwargs) 
        t2 = time() 
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s') 
        return result 
    return wrap_func
from source import *



def brute_force(g: Point, h: Point):
    for i in range(2,p-1):
        aux = double_and_add(g, i)
        if aux == h:
            return i
    return -1

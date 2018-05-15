# printer to print a dungeon

char_map = {
    0: ' ', # void
    1: '.', # floor
    2: '#', # wall
    3: '+', # door
    4: '+', # door2
    5: '.', # corridor floor
    6: '#'  # corridor wall

}


def draw(dung):
    '''
        dung - int [][]
    '''
    for row in dung:
        for item in row:
            print(char_map[item], end='')
        print('')
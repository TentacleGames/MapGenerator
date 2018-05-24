# printer to print a dungeon

char_map = {
    0: ' ', # void
    1: '.', # floor
    2: '#', # wall
    3: '+', # door
    4: '+', # door2
    5: '.', # corridor floor
    6: '#', # corridor wall
    7: '0', # portal

}


def draw(dung):
    '''
        dung - int [][]
    '''
    for row in dung:
        for item in row:
            if item >=10:
                print(str(item-10), end='')
            else:
                print(char_map[item], end='')
        print('')
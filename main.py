# main module for MapGenerator

from dungeon import Generator
import printer

params = {
    'transitions_type' : 'both', # corridors/portals/both
    'each_room_transitions': False, # bool. Generate a corridor for each room
    'is_connected': True, # bool. Generate additional corridors, if needed, to connect the dungeon
    'room_size': (3, 4), # min, max
    'rooms_count': 40,
    'max_connections_delta': 5, #max delta: (corridors + portals)-rooms
    'base_connecting': 'random', # closest, farest, random
    'width': 80,
    'height': 80,
    'corridor_curves': 'curve', #straight (as possible), curve, random
    'portals_percent': 10

}

# map generation
dung = Generator(params)
dung.generate() # array[][] of dungeon

# map printing
printer.draw(dung.result)

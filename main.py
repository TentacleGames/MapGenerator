# main module for MapGenerator

from dungeon import Generator
import printer

params = {
    'transitions_type' : 'both', # corridors/portals/both
    'each_room_transitions': True, # bool. Generate a corridor for each room
    'must_conected': True, # bool. Generate additional corridors, if needed, to connect the dungeon
    'room_size': (2, 3), # min, max
    'rooms_count': 8,
    'max_connections_delta': 1, #max delta: (corridors + portals)-rooms
    'base_connecting': 'closest', # closest, farest, random
    'width': 80,
    'height': 20,
    'corridor_curves': 'random', #straight (as possible), curve, random
    'portals_percent': 20

}

# map generation
dung = Generator(params)
dung.generate() # array[][] of dungeon

# map printing
printer.draw(dung.result)

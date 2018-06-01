# MapGenerator
Custom dungeon generation algorithm for roguelike games.

All maps are customizable by parameters.

# Parameters definition

width - maximum width of dungeon

height - maximum height of dungeon

room_size - tuple of min and max size of rooms

rooms_count - maximum number of rooms in dungeon (actual number of rooms could be less in case there is not enough space)

transitions_type - type of transitions between rooms: portals or corridors or both

portals_percent - percentage of portals if transitions_type it 'both'

each_room_transitions - means that each room have at least one connection

must_conected - if it's true, then all rooms should be reachable

base_connecting - if it "closest" or "farest" then rooms will be connected with closest/farest neighbor, and "random" is random.

corridor_curves - style of corridors. Could be straight (as possible), curve (a lots of turnings). In case of random, this parameter sets randomly to "straight" or "curve" for each corridor

max_connections_delta - this parameter needed to delete excess corridors (if it possible, considering "must_connected" parameter)

# dungeon generator class
from random import randint
import copy

DEFAULT_PARAMS = {
    'transitions_type' : 'both', # corridors/portals/both
    'each_room_transitions': True, # bool. Generate a corridor for each room
    'base_connecting': 'random', # closest, farest, random
    'must_conected': True, # bool. Generate additional corridors, if needed, to connect the dungeon
    'room_size': (6, 12), # min, max
    'rooms_count': 10,
    'max_connections_delta': 10, #max delta: (corridors + portals)-rooms
    'width': 120,
    'height': 50,
}


MAX_ATTEMPTS = 10


class Generator():
    def __init__(self, params={}):
        self.rooms = [] # rooms array
        self.corridors = []
        self.portals = []
        self.result = [] # array of int arrays
        self.connections = {} # dict of room connections
        self.not_connected = {}
        self.params = DEFAULT_PARAMS
        self.wave_field = None
        for param in params: # apply user params
            self.params[param] = params[param]

    def generate(self):
        for i in range(0, self.params['rooms_count']):
            new_room = self._generate_room()
            # TODO: here we could dwell a room, place an items, etc.
            self.rooms.append(new_room)
        for room in self.rooms:
            self.connections[room.id]={room.id}

        self._set_connections()

        self.get_result()
        return self.result

    def _generate_room(self):
        #generate the room
        room = None
        collide = True
        attempts = 0
        while collide is not None or attempts < MAX_ATTEMPTS:
            attempts += 1
            x = randint(2, self.params['width'] - self.params['room_size'][0] - 2)
            y = randint(2, self.params['height'] - self.params['room_size'][0] - 2)
            wd = randint(self.params['room_size'][0], self.params['room_size'][1])
            hd = randint(self.params['room_size'][0], self.params['room_size'][1])
            room = Room(x, y, wd, hd)
            # check collisions with existing rooms
            collide = self._check_room_collide(room)
        if not collide:
            room.id = len(self.rooms) + 1
        else:
            # failed to create a new room
            room = None
        return room

    def _get_room(self, id):
        '''get room by id'''
        for room in self.rooms:
            if room.id == id:
                return room
        return None

    def _set_connections(self):
        def _add_connection(roomA, roomB):
            new_corridor = None
            new_portal = None
            if self.params.get('transitions_type') == 'corridors':
                new_corridor = self._generate_corridor(room_A, room_B)
            elif self.params.get('transitions_type') == 'portals':
                # TODO: portals
                new_corridor = self._generate_portal(room_A, room_B)
            elif self.params.get('transitions_type') == 'both':
                # TODO: both corridors and portals
                if randint(0, 1) == 0:
                    new_corridor = self._generate_corridor(room_A, room_B)
                else:
                    new_corridor = self._generate_portal(room_A, room_B)
            if new_corridor:
                self.corridors.append(new_corridor)
            if new_portal:
                self.portals.append(new_portal)
            for r in self.connections[room_B.id]:
                self.connections[r] = self.connections[r] | self.connections[room_A.id]
            for r in self.connections[room_A.id]:
                self.connections[r] = self.connections[r] | self.connections[room_B.id]
            #print('connections: {}'.format(str(self.connections)))

        if self.params.get('each_room_transitions') == True:
            for room in self.rooms:
                room_A = room
                room_B = self._find_room(room_A, self.rooms)
                _add_connection(room_A, room_B)

        if self.params.get('must_conected') == True:
            while not self._is_connected():
                room_A = None
                room_B = None
                for key, val in self.not_connected.items():
                    if val:
                        room_A = self._get_room(key)
                        room_B = self._find_room(room_A, [self._get_room(x) for x in val])
                        break
                _add_connection(room_A, room_B)
        removed = True
        while (len(self.corridors)+len(self.portals))-len(self.rooms) > self.params.get('max_connections_delta') and removed:
            removed = self._remove_connection()
        return

    def _is_connected(self):
        keys = list(self.connections.keys())
        for key, val in self.connections.items():
            self.not_connected[key] = set(keys) - val
        con = set()
        for x in keys:
            con = con | self.not_connected[x]
        return len(con)==0

    def _find_room(self, room, rooms):
        if not rooms:
            return None
        param = self.params.get('base_connecting')
        result = None
        if param == 'random':
            i = randint(0, len(rooms) - 1)
            result = rooms[i]
        else:
            mid = (room.x+(room.wd//2), room.y+(room.hd//2))
            if param == 'closest':
                dist = self.params['width']**2 + self.params['height']**2 #init squared min distance
            else:
                dist = 0 # init max distance
            for check in rooms:
                if check.id == room.id:
                    continue
                mid_c = (check.x+(check.wd//2), check.y+(check.hd//2))
                dist_c = (mid[0]-mid_c[0])**2 + (mid[1]-mid_c[1])**2 #squared distance
                # squared dist is ok. if squared is minimal/maximal, then is't really minimal/maximal
                if dist_c < dist and param=='closest' or dist_c > dist and param=='farest':
                    dist = dist_c
                    result = check
        return result

    def _check_room_collide(self, room):
        collide = None
        # check bonds collide
        if room.x <= 0 or room.x + room.wd + 1 >= self.params['width'] or \
            room.y <= 0 or room.y + room.hd + 1 >= self.params['height']:
            return True

        # check rooms collide
        for check in self.rooms:
            if check.id == room.id:
                is_collide = False
            else:
                is_collide = not (
                        (check.x + check.wd + 1 < room.x - 1) or (check.x - 1 > room.x + room.wd + 1) or
                        (check.y + check.hd + 1 < room.y - 1) or (check.y - 1 > room.y + room.hd + 1)
                )
            if is_collide:
                collide = check.id
                break
        return collide

    def _check_point_collide(self, point):
        collide = None
        x = point[0]
        y = point[1]
        # check bonds collide
        if x <= 0 or x + 1 >= self.params['width'] or y <= 0 or y + 1 >= self.params['height']:
            return True

        # check rooms collide
        for check in self.rooms:
            is_collide = x in range(check.x - 1, check.x + check.wd + 1) and \
                         y in range(check.y - 1, check.y + check.hd + 1)
            if is_collide:
                collide = check.id
                break
        return collide

    def _get_wave_field(self):
        if not self.wave_field:
            self.wave_field = self._set_void_map(value=None)
            for room in self.rooms:  # mark blocking points
                for x in range(room.x - 1, room.x + room.wd + 1):
                    for y in range(room.y - 1, room.y + room.hd + 1):
                        self.wave_field[y][x] = -1
        return copy.deepcopy(self.wave_field) #get clone of wave_field
        #return self.wave_field  # get clone of wave_field

    def _calculate_path(self, startP, destP):
        ''' generating path, using Lee algorithm (wave algorithm)
        '''
        def _mark_point(point, idx=0, needMark = True):
            x = point[0]
            y = point[1]
            if x >= 1 and y >= 1 and y <= len(wave_field) - 2 and x <= len(wave_field[y]) - 2:
                if needMark:
                    if wave_field[y][x] is None:
                        wave_field[y][x] = idx
                        return wave_field[y][x]
                    else:
                        return None
                else:
                    return wave_field[y][x]
            return None

        def _set_distance(points, stop_point):
            new_points = []
            neighborhood = [(0, -1), (0, +1), (-1, 0), (+1, 0)]
            for point in points:
                x = point[0]
                y = point[1]
                idx = wave_field[y][x] + 1
                for neighbor in neighborhood:
                    check = (point[0]+neighbor[0], point[1]+neighbor[1])
                    if _mark_point(check, idx=idx, needMark=True):
                        new_points.append(check)
            if new_points:
                if stop_point in new_points:
                    return True
                else:
                    return _set_distance(new_points, stop_point)
            else:
                return False

        def _get_path(startP, destP):
            path = []
            curP = destP
            path.append(curP)
            neighborhood = [(0, -1), (0, +1), (-1, 0), (+1, 0)]
            while curP != startP:
                cur_idx = wave_field[curP[1]][curP[0]]
                possible_moves = []
                for neighbor in neighborhood:
                    point = (curP[0]+neighbor[0], curP[1]+neighbor[1])
                    idx = _mark_point(point, needMark=False)
                    if idx is not None and idx == cur_idx-1:
                        possible_moves.append(point)
                if possible_moves:
                    curP = possible_moves[randint(0,len(possible_moves)-1)]
                    path.append(curP)
                else:
                    return None
            return path

        wave_field = self._get_wave_field()
        wave_field[startP[1]][startP[0]] = 0
        passible = _set_distance([startP], destP)
        path = None
        if passible:
            path = _get_path(startP, destP)

        return path

    def _generate_corridor(self, roomA, roomB):

        def _get_next_point(point, direction, opposite=False):
            directions = {
                'N': (0, -1),
                'S': (0, +1),
                'E': (+1, 0),
                'W': (-1, 0)
            }
            k = -1 if opposite else 1
            result = (point[0]+k*directions[direction][0], point[1]+k*directions[direction][1])
            return result

        def _get_door_points(room, direction, opposite=False):
            opposition = {'N':'S', 'S':'N', 'E':'W', 'W':'E'}
            direction = direction[randint(0, len(direction) - 1)]
            if opposite:
                direction = opposition[direction]
            directions = {
                'N': (randint(room.x, room.x+room.wd-1), room.y-1), #top
                'S': (randint(room.x, room.x+room.wd-1), room.y+room.hd), #bottom
                'E': (room.x + room.wd, randint(room.y, room.y + room.hd - 1)), # right
                'W': (room.x - 1, randint(room.y, room.y + room.hd - 1))  # left
            }
            result = (directions[direction], opposition[direction] if opposite else direction)
            return result

        #TODO: refine
        corr = Corridor()
        # finding direction from room A to B
        dir = ''
        if roomA.id == roomB.id:
            while not dir:
                dir = '{}{}'.format(' NS'[randint(0, 2)], ' WE'[randint(0, 2)]).strip()
        else:
            if roomA.y != roomB.y:
                dir += 'N' if roomA.y > roomB.y else 'S'
            if roomA.x != roomB.x:
                dir += 'W' if roomA.x > roomB.x else 'E'

        # creating door-points (on the edge of the rooms)
        corr.P1, first_dir = _get_door_points(roomA, dir)
        corr.P2, last_dir = _get_door_points(roomB, dir, opposite=True)
        # generation start and destination points for wave algorithm
        startP = _get_next_point(corr.P1, first_dir)
        destP = _get_next_point(corr.P2, last_dir, opposite=True)
        # generating path
        path = self._calculate_path(startP, destP)

        if path:
            corr.points = path
            corr.rooms = [roomA.id, roomB.id]
            corr.id = len(self.corridors) + 1
            # TODO: here we could define entrance/exit as one of follow: none, door, secret door, trap door, etc.
            # TODO: possible as door class with the states: locked/unlocked, trapped, secret, etc.
            return corr
        else:
            return None

    def _generate_portal(self, roomA, roomB):
        #TODO: make portals great again!
        return self._generate_corridor(roomA, roomB)

    def _set_void_map(self, value = 0):
        result = []
        row = []
        for i in range(0, self.params['width']):
            row.append(value)
        for i in range(0, self.params['height']):
            result.append(list(row))
        return result

    def _remove_connection(self):

        def _find_pair():
            connections = {}
            result = []
            for corr in self.corridors:
                if set(corr.rooms) in connections:
                    connections[set(corr.rooms)].append('C{}'.format(corr.id))
                    result = connections[set(corr.rooms)]
                    break
                else:
                    connections[set(corr.rooms)] = ['C{}'.format(corr.id)]

            for port in self.portals:
                if set(port.rooms) in connections:
                    connections[set(port.rooms)].append('P{}'.format(port.id))
                    result = connections[set(port.rooms)]
                    break
                else:
                    connections[set(port.rooms)] = ['P{}'.format(port.id)]
            return result

        result = False
        if self.params.get('must_conected'):
            pair = _find_pair()
            if len(pair) < 2:
                result = False
            else:
                id = pair[randint(0, 1)]
                if id[0]=='C':
                    for corr in self.corridors:
                        if corr.id == int(id[1:]):
                            self.corridors.remove(corr)
                            result = True
                            break
                elif id[0]=='P':
                    for port in self.portals:
                        if port.id == int(id[1:]):
                            self.portals.remove(port)
                            result = True
                            break
        else:
            result = False
            if (randint(0,1) or not self.portals) and self.corridors:
                del(self.corridors[randint(0, len(self.corridors)-1)])
                result = True
            elif self.portals:
                del(self.portals[randint(0, len(self.portals)-1)])
                result = True
        return result

    def get_result(self):

        self.result = self._set_void_map()
        for room in self.rooms:
            start_x = room.x
            end_x = room.x + room.wd-1
            start_y = room.y
            end_y = room.y + room.hd-1
            print('Room printing: \n {}, {}, {}, {}\n {}, {}, {}, {}'.format(
                room.x, room.y, room.wd, room.hd,
                start_x,end_x,start_y,end_y)
                )
            # printing floor
            for x in range(start_x, end_x+1):
                for y in range(start_y, end_y+1):
                    self.result[y][x] = 1
            # printing walls
            for x in range(start_x-1, end_x+2):
                self.result[start_y-1][x] = 2
                self.result[end_y+1][x] = 2
            for y in range(start_y-1, end_y+2):
                self.result[y][start_x-1] = 2
                self.result[y][end_x+1] = 2

        #makes walls around corridors
        for corr in self.corridors:
            for point in corr.points:
                try:
                    self.result[point[1]][point[0]] = 5
                    if not self.result[point[1]][point[0]-1]:
                        self.result[point[1]][point[0]-1]=6
                    if not self.result[point[1]][point[0]+1]:
                        self.result[point[1]][point[0]+1]=6
                    if not self.result[point[1]-1][point[0]]:
                        self.result[point[1]-1][point[0]]=6
                    if not self.result[point[1]+1][point[0]]:
                        self.result[point[1]+1][point[0]]=6
                    if not self.result[point[1]-1][point[0]+1]:
                        self.result[point[1]-1][point[0]+1]=6
                    if not self.result[point[1]-1][point[0]-1]:
                        self.result[point[1]-1][point[0]-1]=6
                    if not self.result[point[1]+1][point[0]+1]:
                        self.result[point[1]+1][point[0]+1]=6
                    if not self.result[point[1]+1][point[0]-1]:
                        self.result[point[1]+1][point[0]-1]=6
                except:
                    print('Error while handling point: {}'.format(str(point)))
                    raise Exception()
            #TODO: make more door veriants
            self.result[corr.P1[1]][corr.P1[0]] = 3
            self.result[corr.P2[1]][corr.P2[0]] = 4


class Room():
    def __init__(self, x, y, w, h):
        self.id = None
        self.x = x
        self.y = y
        self.wd = w # width
        self.hd = h # height


class Corridor():
    def __init__(self):
        '''
        :param roomA: room class instance
        :param roomB: room class instance
        '''
        self.P1 = (None,None) # tuple (x1,y1) in room[0]
        self.P2 = (None,None) # tuple (x2,y2) in room[0]
        self.points = []
        self.rooms = [] # ids of rooms connected
        self.id = None

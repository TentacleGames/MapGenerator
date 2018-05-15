# dungeon generator class
from random import randint


DEFAULT_PARAMS = {
    'transitions_type' : 'both', # corridors/portals/both
    'each_room_transitions': True, # bool. Generate a corridor for each room
    'base_connecting': 'random', # closest, farest, random
    'must_conected': True, # bool. Generate additional corridors, if needed, to connect the dungeon
    'room_size': (6, 12), # min, max
    'rooms_count': 10,
    'width': 120,
    'height': 50,
    'new_param': None
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

    def _generate_corridor(self, roomA, roomB):
        #TODO: refine
        corr = Corridor()
        corr.rooms.append(roomA.id)
        corr.rooms.append(roomB.id)
        dirx = '' # direction from A to B
        diry = ''  # direction from A to B
        dir = ''
        if roomA.id == roomB.id:
            while not dir:
                dirx = ' WE'[randint(0,2)]
                diry = ' NS'[randint(0, 2)]
                dir = (diry + dirx).strip()
        else:
            if roomA.x != roomB.x:
                dirx = 'W' if roomA.x > roomB.x else 'E'
            if roomA.y != roomB.y:
                diry = 'N' if roomA.y > roomB.y else 'S'
            dir = diry + dirx

        first_dir = ''
        last_dir = ''
        if dir == 'N':
            first_dir = last_dir = 'N'
            corr.P1 = (randint(roomA.x, roomA.x+roomA.wd-1) , roomA.y-1) # top of A
            corr.P2 = (randint(roomB.x, roomB.x+roomB.wd-1) , roomB.y+roomB.hd) # bottom of B
        elif dir == 'NE':
            if randint(0,1)==0:
                first_dir = 'N'
                corr.P1 = (randint(roomA.x+roomA.wd//2, roomA.x+roomA.wd-1), roomA.y-1) # right half of top edge of A
            else:
                first_dir = 'E'
                corr.P1 = (roomA.x+roomA.wd, randint(roomA.y, roomA.y+roomA.hd//2)) # top half of right edge of A
            if randint(0, 1) == 0:
                last_dir = 'N'
                corr.P2 = (randint(roomB.x, roomB.x+roomB.wd//2), roomB.y+roomB.hd) # left half of bottom edge of B
            else:
                last_dir = 'E'
                corr.P2 = (roomB.x-1, randint(roomB.y+roomB.hd//2, roomB.y+roomB.hd-1)) # bottom half of left edge of B
        elif dir == 'E':
            first_dir = last_dir = 'E'
            corr.P1 = (roomA.x+roomA.wd, randint(roomA.y, roomA.y+roomA.hd-1)) # right of A
            corr.P2 = (roomB.x-1, randint(roomB.y, roomB.y+roomB.hd-1)) # left of B
        elif dir == 'SE':
            if randint(0, 1) == 0:
                first_dir = 'E'
                corr.P1 = (roomA.x+roomA.wd, randint(roomA.y+roomA.hd//2, roomA.y+roomA.hd-1)) # bottom half of right edge of A
            else:
                first_dir = 'S'
                corr.P1 = (randint(roomA.x+roomA.wd//2, roomA.x+roomA.wd), roomA.y+roomA.hd) # right half of bottom edge of A
            if randint(0, 1) == 0:
                last_dir = 'S'
                corr.P2 = (randint(roomB.x, roomB.x+roomB.wd//2), roomB.y-1) # left half of top edge of B
            else:
                last_dir = 'E'
                corr.P2 = (roomB.x-1, randint(roomB.y, roomB.y+roomB.hd//2)) # top half of left edge of B
        elif dir == 'S':
            first_dir = last_dir = 'S'
            corr.P1 = (randint(roomA.x, roomA.x + roomA.wd-1), roomA.y + roomA.hd)  # bottom of A
            corr.P2 = (randint(roomB.x, roomB.x + roomB.wd-1), roomB.y-1)  # top of B
        elif dir == 'SW':
            if randint(0, 1) == 0:
                first_dir = 'S'
                corr.P1 = (randint(roomA.x, roomA.x+roomA.wd//2), roomA.y+roomA.hd) # left half of bottom edge of A
            else:
                first_dir = 'W'
                corr.P1 = (roomA.x-1, randint(roomA.y+roomA.hd//2, roomA.y+roomA.hd-1)) # bottom half of left edge of A
            if randint(0,1)==0:
                last_dir = 'S'
                corr.P2 = (randint(roomB.x+roomB.wd//2, roomB.x+roomB.wd-1), roomB.y-1) # right half of top edge of B
            else:
                last_dir = 'W'
                corr.P2 = (roomB.x+roomB.wd, randint(roomB.y, roomB.y+roomB.hd//2)) # top half of right edge of B
        elif dir == 'W':
            first_dir = last_dir = 'W'
            corr.P1 = (roomA.x-1, randint(roomA.y, roomA.y+roomA.hd-1))  # left of A
            corr.P2 = (roomB.x+roomB.wd, randint(roomB.y, roomB.y+roomB.hd-1))  # right of B
        elif dir == 'NW':
            if randint(0, 1) == 0:
                first_dir = 'N'
                corr.P1 = (randint(roomA.x, roomA.x+roomA.wd//2), roomA.y-1) # left half of top edge of A
            else:
                first_dir = 'W'
                corr.P1 = (roomA.x-1, randint(roomA.y, roomA.y+roomA.hd//2)) # top half of left edge of A
            if randint(0, 1) == 0:
                last_dir = 'W'
                corr.P2 = (roomB.x+roomB.wd, randint(roomB.y+roomB.hd//2, roomB.y+roomB.hd-1)) # bottom half of right edge of B
            else:
                last_dir = 'N'
                corr.P2 = (randint(roomB.x+roomB.wd//2, roomB.x+roomB.wd-1), roomB.y+roomB.hd) # right half of bottom edge of B

        startP = destP = None
        if first_dir == 'N':
            startP = (corr.P1[0],corr.P1[1]-1)
        elif first_dir == 'E':
            startP = (corr.P1[0]+1, corr.P1[1])
        elif first_dir == 'S':
            startP = (corr.P1[0], corr.P1[1]+1)
        elif first_dir == 'W':
            startP = (corr.P1[0]-1, corr.P1[1])

        if last_dir == 'N':
            destP = (corr.P2[0],corr.P2[1]+1)
        elif last_dir == 'E':
            destP = (corr.P2[0]-1, corr.P2[1])
        elif last_dir == 'S':
            destP = (corr.P2[0], corr.P2[1]-1)
        elif last_dir == 'W':
            destP = (corr.P2[0]+1, corr.P2[1])

        # TODO: move wave_field to self for reuse each time
        # TODO: move whole wave algorithm to another module
        wave_field = self._set_void_map(value = None)
        for room in self.rooms: #mark blocking points
            for x in range(room.x-1, room.x + room.wd+1):
                for y in range(room.y-1, room.y + room.hd+1):
                    wave_field[y][x] = -1
        wave_field[startP[1]][startP[0]] = 0

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

        passible = _set_distance([startP], destP)
        path = None
        if passible:
            path = _get_path(startP, destP)
        if path:
            corr.points = path
            corr.rooms = [roomA.id, roomB.id]
            # TODO: here we could define entrance/exit as one of follow: none, door, secret door, trap door, etc.
            # TODO: possible as door class with the states: locked/unlocked, trapped, secret, etc.
            return corr
        else:
            return None

    def _old_generate_corridor(self, roomA, roomB):
        #TODO: refine
        corr = Corridor()
        corr.rooms.append(roomA.id)
        corr.rooms.append(roomB.id)
        dirx = '' # direction from A to B
        diry = ''  # direction from A to B
        dir = ''
        if roomA.id == roomB.id:
            while not dir:
                dirx = ' WE'[randint(0,2)]
                diry = ' NS'[randint(0, 2)]
                dir = (diry + dirx).strip()
        else:
            if roomA.x != roomB.x:
                dirx = 'W' if roomA.x > roomB.x else 'E'
            if roomA.y != roomB.y:
                diry = 'N' if roomA.y > roomB.y else 'S'
            dir = diry + dirx

        first_dir = ''
        last_dir = ''
        if dir == 'N':
            first_dir = last_dir = 'N'
            corr.P1 = (randint(roomA.x, roomA.x+roomA.wd-1) , roomA.y-1) # top of A
            corr.P2 = (randint(roomB.x, roomB.x+roomB.wd-1) , roomB.y+roomB.hd) # bottom of B
        elif dir == 'NE':
            if randint(0,1)==0:
                first_dir = 'N'
                corr.P1 = (randint(roomA.x+roomA.wd//2, roomA.x+roomA.wd-1), roomA.y-1) # right half of top edge of A
            else:
                first_dir = 'E'
                corr.P1 = (roomA.x+roomA.wd, randint(roomA.y, roomA.y+roomA.hd//2)) # top half of right edge of A
            if randint(0, 1) == 0:
                last_dir = 'N'
                corr.P2 = (randint(roomB.x, roomB.x+roomB.wd//2), roomB.y+roomB.hd) # left half of bottom edge of B
            else:
                last_dir = 'E'
                corr.P2 = (roomB.x-1, randint(roomB.y+roomB.hd//2, roomB.y+roomB.hd-1)) # bottom half of left edge of B
        elif dir == 'E':
            first_dir = last_dir = 'E'
            corr.P1 = (roomA.x+roomA.wd, randint(roomA.y, roomA.y+roomA.hd-1)) # right of A
            corr.P2 = (roomB.x-1, randint(roomB.y, roomB.y+roomB.hd-1)) # left of B
        elif dir == 'SE':
            if randint(0, 1) == 0:
                first_dir = 'E'
                corr.P1 = (roomA.x+roomA.wd, randint(roomA.y+roomA.hd//2, roomA.y+roomA.hd-1)) # bottom half of right edge of A
            else:
                first_dir = 'S'
                corr.P1 = (randint(roomA.x+roomA.wd//2, roomA.x+roomA.wd), roomA.y+roomA.hd) # right half of bottom edge of A
            if randint(0, 1) == 0:
                last_dir = 'S'
                corr.P2 = (randint(roomB.x, roomB.x+roomB.wd//2), roomB.y-1) # left half of top edge of B
            else:
                last_dir = 'E'
                corr.P2 = (roomB.x-1, randint(roomB.y, roomB.y+roomB.hd//2)) # top half of left edge of B
        elif dir == 'S':
            first_dir = last_dir = 'S'
            corr.P1 = (randint(roomA.x, roomA.x + roomA.wd-1), roomA.y + roomA.hd)  # bottom of A
            corr.P2 = (randint(roomB.x, roomB.x + roomB.wd-1), roomB.y-1)  # top of B
        elif dir == 'SW':
            if randint(0, 1) == 0:
                first_dir = 'S'
                corr.P1 = (randint(roomA.x, roomA.x+roomA.wd//2), roomA.y+roomA.hd) # left half of bottom edge of A
            else:
                first_dir = 'W'
                corr.P1 = (roomA.x-1, randint(roomA.y+roomA.hd//2, roomA.y+roomA.hd-1)) # bottom half of left edge of A
            if randint(0,1)==0:
                last_dir = 'S'
                corr.P2 = (randint(roomB.x+roomB.wd//2, roomB.x+roomB.wd-1), roomB.y-1) # right half of top edge of B
            else:
                last_dir = 'W'
                corr.P2 = (roomB.x+roomB.wd, randint(roomB.y, roomB.y+roomB.hd//2)) # top half of right edge of B
        elif dir == 'W':
            first_dir = last_dir = 'W'
            corr.P1 = (roomA.x-1, randint(roomA.y, roomA.y+roomA.hd-1))  # left of A
            corr.P2 = (roomB.x+roomB.wd, randint(roomB.y, roomB.y+roomB.hd-1))  # right of B
        elif dir == 'NW':
            if randint(0, 1) == 0:
                first_dir = 'N'
                corr.P1 = (randint(roomA.x, roomA.x+roomA.wd//2), roomA.y-1) # left half of top edge of A
            else:
                first_dir = 'W'
                corr.P1 = (roomA.x-1, randint(roomA.y, roomA.y+roomA.hd//2)) # top half of left edge of A
            if randint(0, 1) == 0:
                last_dir = 'W'
                corr.P2 = (roomB.x+roomB.wd, randint(roomB.y+roomB.hd//2, roomB.y+roomB.hd-1)) # bottom half of right edge of B
            else:
                last_dir = 'N'
                corr.P2 = (randint(roomB.x+roomB.wd//2, roomB.x+roomB.wd-1), roomB.y+roomB.hd) # right half of bottom edge of B

        if first_dir == 'N':
            curP = (corr.P1[0],corr.P1[1]-1)
        elif first_dir == 'E':
            curP = (corr.P1[0]+1, corr.P1[1])
        elif first_dir == 'S':
            curP = (corr.P1[0], corr.P1[1]+1)
        elif first_dir == 'W':
            curP = (corr.P1[0]-1, corr.P1[1])
        try:
            corr.points.append(curP)
        except:
            print('dir: {}'.format(dir))
            print('roomA: {}'.format(roomA.id))
            print('roomB: {}'.format(roomB.id))
            raise Exception('')

        if last_dir == 'N':
            destP = (corr.P2[0],corr.P2[1]+1)
        elif last_dir == 'E':
            destP = (corr.P2[0]-1, corr.P2[1])
        elif last_dir == 'S':
            destP = (corr.P2[0], corr.P2[1]-1)
        elif last_dir == 'W':
            destP = (corr.P2[0]+1, corr.P2[1])

        while curP != destP:
            if curP[0] != destP[0]:
                newP = (curP[0]-1, curP[1]) if curP[0] > destP[0] else (curP[0]+1, curP[1])
                print('wanted horizontally')
            elif curP[1] != destP[1]:
                newP = (curP[0], curP[1]-1) if curP[1] > destP[1] else (curP[0], curP[1]+1)
                print('wanted vertically')

            if self._check_point_collide(newP):
                print('collision happened')
                if curP[1] != destP[1]:
                    newP = (curP[0], curP[1] - 1) if curP[1] > destP[1] else (curP[0], curP[1] + 1)
                    print('go vertically')
                elif curP[0] != destP[0]:
                    newP = (curP[0] - 1, curP[1]) if curP[0] > destP[0] else (curP[0] + 1, curP[1])
                    print('go horizontally')
            else:
                print('ok')

            curP = newP
            corr.points.append(curP)

        corr.rooms = [roomA.id, roomB.id]
        # TODO: here we could define entrance/exit as one of follow: none, door, secret door, trap door, etc.
        # TODO: possible as door class with the states: locked/unlocked, trapped, secret, etc.
        return corr

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

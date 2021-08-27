## Builtin Modules
from collections import namedtuple
from functools import wraps
from inspect import signature
import json


MAPSYMBOLS = {
    "": "Empty",
    " ": "Empty",
    "C": "Character",
    "B": "Block",
    "S": "Skeleton",
    "P": "Spikes-Active",
    "p": "Spikes-Inactive",
    "K": "Key",
    "G": "Gate",
    "T": "Target",
    "W": "Wall",
    "E": "Active Terminal",
    "e": "Broken Terminal",
    "0": "Laser Up",
    "1": "Laser Right",
    "2": "Laser Down",
    "3": "Laser Left"
}

## Blocking Entities block the movement of Moveable entities
BLOCKINGENTITIES = ("C", "B", "S", "W", "E", "e", "G", "0", "1", "2", "3")
## Non Blocking allow movement of moveable entities
NONBLOCKINGENTITIES = ("", " ", "P", "p", "K", "T")
## Kickable Entities are kicked if the character moves towards them
KICKABLEENTITIES = ("B", "S", "t", "E", "e")
## Destroyable Entities are destroyed when they are moved into a Blocking Entity or the Edge of the Map
DESTROYABLEENTITIES = ("S", "E")
## Destroyable Entities are convered into their Destroyed State when destroyed (None means remove the entity entirely)
DESTROYEDSTATE = {"S":None, "E":"e"}
## Solid Entities are entities that lasers can't pass through
SOLIDENTITIES = ("B","W","G")

Coordinate = namedtuple("coordinate", ["column", "row"])

SPIKETRANS = {ord(k):ord(v) for k,v in {"P":"p","p":"P"}.items()}

DIRECTIONTRANS = {
    "up":(0,-1),
    "right":(1,0),
    "down":(0,1),
    "left":(-1,0)
}

LASERTRANS = {
    "0":"up",
    "1":"right",
    "2":"down",
    "3":"left",
}

class Map():
    @classmethod
    def validategrid(cls, grid):
        if len(grid) == 0: raise AttributeError("Grid must have rows")
        lengs = [len(row) for row in grid]
        if lengs[0] == 0: raise ValueError("Grid rows must have columns")
        if any(row != lengs[0] for row in lengs):
            raise ValueError("Grid has rows with differing lengths")
        characters = sum(sum(1 if "C" in column else 0 for column in row) for row in grid)
        if 0>=characters or characters>1: raise ValueError("Grid must have exactly 1 Character")
    @classmethod
    def cleangrid(cls, grid):
        """ Sorts the entities in each cell and removes whitespaces """
        return [
            ["".join(sorted(column.replace(" ",""))) for column in row]
            for row in grid
            ]
    @classmethod
    def parsegridstring(cls, gridstring: str):
        return [list(line.split(",")) for line in gridstring.splitlines()]
    @classmethod
    def isblocking(cls, square: str):
        return any(blocking in square for blocking in BLOCKINGENTITIES)
    @classmethod
    def issolid(cls, square: str):
        return any(solid in square for solid in SOLIDENTITIES)
    @classmethod
    def opposingcoord(cls, coorda, coordb):
        """ Given two adjacent coordinates (a and b), return coordinate c which is in the cardinal direction opposite coordinate b from a.
        
            The resulting coordinate may be off the map.
        """
        deltax, deltay = coordb[0]-coorda[0], coordb[1]-coorda[1]
        if (deltax != 0 and deltay != 0) or abs(deltax) > 1 or abs(deltay) > 1: raise ValueError("Coordinates A and B are not adjacent: {coorda}, {coordb}")
        return Coordinate(coordb[0]+deltax, coordb[1]+deltay)
    @classmethod
    def direction_to_coord(cls, direction: str, relativeto: Coordinate):
        """ Returns the coordinate that would be adjacent to the relativeto coordinate in the direction specified.
        
            direction should be one of ["up","right","down","left"].
            May return coordinates outside of the map.
        """
        if (direction := direction.strip().lower()) not in DIRECTIONTRANS:
            raise ValueError("Invalid Direction")
        deltax,deltay = DIRECTIONTRANS[direction]
        return Coordinate(relativeto[0]+deltax, relativeto[1]+deltay)
    @classmethod
    def coord_to_direction(cls, coord: Coordinate, relativeto: Coordinate):
        """ Returns the direction in which the coordinate lays in respect to the relativeto coordinate.

            If coord is not adjacent to relativeto, returns None.
        """
        return {(relativeto[0]+deltax, relativeto[1]+deltay):dire for dire,(deltax,deltay) in DIRECTIONTRANS.items()}.get(tuple(coord))
    @classmethod
    def distance_to_coord(self, start: Coordinate, target: Coordinate):
        """ Returns the number of squares from the start coordinate to the target coordinate (including the target coordinate) """
        start, target = Coordinate(*start), Coordinate(*target)
        return abs(start.column - target.column)+abs(start.row - target.row)


    def __init__(self, grid: list):
        if isinstance(grid, str): grid = Map.parsegridstring(grid)
        Map.validategrid(grid)
        self.grid= Map.cleangrid(grid)

    @property
    def width(self):
        return len(self.grid[0])
    @property
    def height(self):
        return len(self.grid)

    def copy(self):
        return Map([list(row) for row in self.grid])

    def capcoord(self, coordinate: Coordinate):
        try:
            coordinate = Coordinate(*coordinate)
        except Exception as e:
            #print(coordinate)
            raise e
        if self.height > coordinate.row >= 0 and self.width > coordinate.column >= 0: return coordinate
        return None

    def getentities(self, coord: Coordinate):
        """ Returns the entities at the Coordinate """
        c = self.capcoord(coord)
        return self.grid[c.row][c.column]

    def coordcontains(self, coord: Coordinate, entity: str):
        """ Returns whether the given coordinate contains the given entity.
                Raises a ValueError if the coordinate is invalid (outside map)
        """
        c = self.capcoord(coord)
        if c is None: raise ValueError(f"Invalid coordinate: {coord}")
        return entity in self.grid[c.row][c.column]

    def findcharacter(self):
        """ Iterates over the Map, returning the current coordinates of the Character """
        for coord in self:
            if self.coordcontains(coord, "C"): return coord
    
    def findall(self, entity: str):
        """ Returns all coordinates that contain at least one instance of the given entity. """
        return [coord for coord in self if self.coordcontains(coord, entity)]

    def iskickable(self, coord: Coordinate):
        c = self.capcoord(coord)
        if c is None: return False
        return [entity for entity in self.grid[c.row][c.column] if entity in KICKABLEENTITIES]
    
    def getadjacent(self, coord: Coordinate):
        return [self.capcoord((coord.column+deltax, coord.row+deltay)) for (deltax, deltay) in DIRECTIONTRANS.values()]

    def moveentity(self, entity: str, start: Coordinate, target: Coordinate):
        """ Move an entity from the start to the target coordinate.
                If start coord is invalid, raise AttributeError.
                If the entity is not at the start coord, raises a ValueError.
                target can alternatively be a direction: it will be converted to
                    a direction using Map.direction_to_coord with the capped start
                    coord as the relativeto argument.
                If the move cannot be completed for any reason, returns None.
                Otherwise, returns the target coordinate
        """
        ## Verify start
        s = self.capcoord(start)
        if s is None: raise AttributeError(f"Invalid start coordinate: {start}")
        if entity not in self.grid[s.row][s.column]:
            raise ValueError(f'Entity not at start coord: {start}[{s}]->"{self.grid[s.row][s.column]}"')

        ## Check if target needs to be translated
        if isinstance(target, str):
            target = Map.direction_to_coord(target, s)
        ## Verify target
        t = self.capcoord(target)
        if t is None: return None
        if Map.isblocking(self.getentities(t)): return None
        
        ## Move entity to target
        self.grid[t.row][t.column]+=entity
        ## Remove entity from start
        ## TODO: consider replacing with self.removeentity
        self.grid[s.row][s.column] = self.grid[s.row][s.column].replace(entity, "")
        return t

    def kick(self, entity: str, start: Coordinate, target: Coordinate):
        """ Kicks an entity from the start coord to the target coord
                entity must be KICKABLE.
                Uses map.moveentity to move the entity to its new square.
                Destroyable entities are destroyed (removed from the Map) if they cannot be kicked.
                If the target is destroyed, returns None.
                Otherwise, returns the final coordinate of the kicked entity.
        """
        result = self.moveentity(entity, start, target)
        if result is None:
            if entity in DESTROYABLEENTITIES:
                self.removeentity(entity, start)
                ## Replace the entity with it's destroyed state (if it has one)
                if (newentity := DESTROYEDSTATE.get(entity)):
                    self.createentity(newentity, start)
                return None
            ## None means the entity did not move (so it's still at start)
            result = start
        return result

    def removeentity(self, entity: str, coord: Coordinate):
        """ Removes the given entity from the given coordinate.
                Raises a AttributeError if the coordinate is not a valid coordinate.
                Raises a ValueError if the entity is not at the given coordinate.
        """
        c = self.capcoord(coord)
        if c is None: raise AttributeError("Invalid coordinate: {coord}")
        if not self.coordcontains(c, entity): raise ValueError(f"Entity is not at target coordinate: Coord-{c} Entity-{entity} Entities at Coord-{self.grid[c.row][c.column]}")
        self.grid[c.row][c.column] = self.grid[c.row][c.column].replace(entity, "")

    def cyclespikes(self):
        """ Cycles all spikes between Active and Inactive"""
        for r,row in enumerate(self.grid):
            self.grid[r] = [column.translate(SPIKETRANS) for column in row]

    def spikeskeletons(self):
        """ Iterates over the map destroying any Skeleton currently on Active Spikes """
        for coord in self:
            ## This assumes that removeentity removes all of given entity from coord
            if self.coordcontains(coord,"S") and self.coordcontains(coord, "P"):
                self.removeentity("S", coord)

    def generatelaser(self, laser: Coordinate):
        """ Returns a list of coordinates which the laser occupies when active. """
        laser = self.capcoord(laser)
        laserentity = [entity for entity in ["0","1","2","3"] if self.coordcontains(laser,entity)][0]
        offset = DIRECTIONTRANS[LASERTRANS[laserentity]]

        output = []
        nextcoord = self.capcoord((laser.column+offset[0], laser.row+offset[1]))
        while nextcoord and not self.issolid(self.getentities(nextcoord)):
            output.append(nextcoord)
            nextcoord = self.capcoord((nextcoord.column+offset[0], nextcoord.row+offset[1]))
        return output
        

    def createentity(self, entity: str, coord: Coordinate):
        """ Creates the given entity at the given Coordinate.
        
            There are no gameplay uses of this (afaik); this is purely used for debugging.
        """
        c = self.capcoord(coord)
        if c is None: raise RuntimeError("Invalid Coordinate")
        self.grid[c.row][c.column]+= entity

    def nearest_entity(self, coord: Coordinate, entity: str):
        """ Determines the number of squares between the given coord and the nearest entity's square. """
        entities = self.findall(entity)
        if not entities: raise ValueError(f"Grid has no '{entity}' entities")
        return min(entities, key=lambda target: Map.distance_to_coord(coord, target))

    def __iter__(self):
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                yield Coordinate(c,r)

    def __eq__(self,other):
        if isinstance(other, Map):
            return Map.cleangrid(self.grid) == Map.cleangrid(other.grid)
        return NotImplemented
        
    def __str__(self):
        return "\n".join(" ".join(row) for row in self.grid)

    
    
class Character():
    def __init__(self, coord: tuple, willpower: int, _map: Map = None):
        self.haskey = False
        self.map = _map
        self._coord = Coordinate(*coord)
        self.willpower = int(willpower)

    @property
    def coord(self): return self._coord
    @coord.setter
    def coord(self, value):
        self._coord = Coordinate(*value)

    def with_map(func):
        """ Decorator to automatically add self.map to functions if map is set on Character. """
        sig = signature(func)
        ## Return undecorated function if not compatable
        if "_map" not in sig.parameters: return func
        @wraps(func)
        def inner(*args, **kw):
            bargs = sig.bind_partial(*args, **kw)
            bargs.apply_defaults()
            ## _map argument not provided and self.map is not None
            if bargs.arguments.get("_map") is None and bargs.arguments['self'].map:
                bargs.arguments['_map'] = bargs.arguments['self'].map
            return func(**bargs.arguments)
        return inner

    @with_map
    def available_actions(self, _map: Map = None):
        adjacent = _map.getadjacent(self.coord)
        return [_map.coord_to_direction(adj, self.coord) for adj in adjacent if adj]
        
    @with_map
    def move(self, target: Coordinate,  _map: Map = None):
        """ Character.move returns the final location of the character, or None if the character took no action (moved into wall/non-kickable area). """
        if isinstance(target,str):
            target = _map.direction_to_coord(target, self.coord)
        t = _map.moveentity("C", self.coord, target)
        ## Character did not move
        if t is None:
            ## Check if obstacle can be kicked
            if (kickentity := _map.iskickable(target)):
                kickentity = kickentity[0]
                t = self.kick(kickentity, target, _map = _map)
                ## On a kick, the character does not move, but it still takes an action
                t = self.coord
            ## Check if stopped because of gate and we have key
            ## checking haskey first is faster than checking coordcontains
            elif self.haskey and _map.coordcontains(target, "G"):
                ## Unlock Gate and try moving again
                _map.removeentity("G", target)
                return self.move(target, _map = _map)
        else:
            ## Character moved, so update character.coord
            self.coord = t
        ## Check if capturing Key
        if _map.coordcontains(self.coord, "K"):
            ## Remove key from map and set haskey flag
            self.haskey = True
            _map.removeentity("K", self.coord)
        ## Returning result because Not-Moving does not cost willpower/should not be considered an action.
        ## No action == None (only returned from moveentity; kickable targets will always return an action)
        return t

    @with_map
    def kick(self, entity: str, target_to_kick: Coordinate, _map: Map = None):
        """ Returns the result of _map.kick. Generally should not be used for gameplay; move should be used instead. 
        
            Not tested.
        """
        if isinstance(target_to_kick,str):
            target = _map.direction_to_coord(target_to_kick, self.coord)
        if not _map.iskickable(target_to_kick): raise ValueError(f"Cannot kick entity in square: {target_to_kick}")
        return _map.kick(entity, target_to_kick, _map.opposingcoord(self.coord, target_to_kick))

class GameplaySequence():
    """ An effective gameplay loop: provides interfaces to have the character take actions and updates the current gamestate with each action.
    
        A GameOver Exception is raised when an action is attempted with insufficient willpower.
        A Victory Exception is raised if the Character is in a Coordinate with a Target entity at the end of the gameplay_loop.
        The GPS' move action interface only accepts direction keywords in order to prevent illegal movement.
        All action interfaces return the direction of the action taken.
        Actions are recorded on the GPS.actions attribute if they are not expressly illegal. For example,
            the character cannot attempt to move into a wall and therefore attempting to do so does not
            add an action; kicking a Block that cannot be moved, however, still counts as an action even
            though it does not succeed.
        Movement through Active Spikes is recorded with ALL CAPS.
    """
    class GameOver(RuntimeError): pass
    class Victory(RuntimeError): pass

    def loadfromjson(file):
        with open(file, 'r') as f:
            gameplay = json.load(f)
        rules = gameplay.get('rules')
        if rules:
            ## Filter/Validate GameplayRules
            rules = [AVAILABLERULES[rule] for rule in rules if rule in AVAILABLERULES]
        else:
            rules = True
        gp = GameplaySequence(gameplay['grid'], gameplay['willpower'], rulesets= rules)
        gp.actions = list(gameplay.get('actions',[]))
        gp.character.haskey = gameplay.get("haskey", False)
        return gp

    def __init__(self, mapgrid: list, willpower: int, rulesets: list = True):
        self._init_map = Map(mapgrid)
        self.map = self._init_map.copy()
        self.character = Character(self.map.findcharacter(), willpower, _map = self.map)
        ## Lists the actions taken by the character
        self.actions = []
        ## True is the base gamemode which is [StandardRules, TargetSquareRules]
        if rulesets is True: rulesets = [StandardRules, TargetSquareRules]
        for r in rulesets:
            if not issubclass(r, GameplayRule): raise TypeError("rulesets must be a list of GameplayRule classes")
        self.rulesets = list(rulesets)

    def copy(self):
        """ Returns a deepcopy of the GameplaySequence """
        grid = self.map.copy().grid
        gp = GameplaySequence(grid, self.character.willpower, self.rulesets)
        gp.actions = list(self.actions)
        gp.character.haskey = self.character.haskey
        return gp

    def action_length(self):
        """ Helper function to account for spike damage """
        return len(self.actions) + len([action for action in self.actions if action.upper() == action])
        
    def remaining_actions(self):
        return self.character.willpower - self.action_length()

    def premove_checks(self):
        for rule in self.rulesets:
            for condition in rule.PREMOVE:
                condition(self)

    def postmove_checks(self):
        for rule in self.rulesets:
            for condition in rule.POSTMOVE:
                condition(self)

    def unwinnable(self):
        """ Determines whether the distance from the character to the nearest Target is greater than the Character's remaining Willpower """
        return any(rules.unwinnable(self) for rules in self.rulesets)

    def updatemap(self):
        """ Updates the map after each action
        
            Housekeeping performed:
                Cycle Spikes
                Deal Damage to Character and Skeletons
        """
        self.map.cyclespikes()
        self.map.spikeskeletons()
        ## Damage Character by putting action in ALL CAPS
        if self.map.coordcontains(self.character.coord, "P"):
            self.actions[-1] = self.actions[-1].upper()
                
    def gameplay_loop(func):
        sig = signature(func)
        @wraps(func)
        def inner(*args, **kw):
            bargs = sig.bind_partial(*args, **kw)
            bargs.apply_defaults()
            self = bargs.arguments['self']
            self.premove_checks()
            result = func(**bargs.arguments)
            if result:
                self.actions.append(result)
                self.updatemap()
            self.postmove_checks()
            return result
        return inner

    @gameplay_loop
    def move(self, direction):
        """ Attempts to the character in the given direction """
        if (result := self.character.move(direction)): return direction

    def up(self):
        return self.move("up")
    def right(self):
        return self.move("right")
    def down(self):
        return self.move("down")
    def left(self):
        return self.move("left")

class GameplayRule():
    """ GameplayRules contain lists of callbacks to check the gamestate
            and take actions as appropriate (at the moment just Victory/Gameover actions)

        In subclasses, PREMOVE and POSTMOVE should be lists of callback functions which
            accept the GameplaySequence as their only argument.

        unwinnable is a Solver Optimization and should be a function which determines if it's
            possible to still solve the puzzle. For example, TargetSquareRules.unwinnable is a
            naive check to see if the Character has enough actions remaining to move to the nearest
            Target Square.
            
            Unwinnable does not need to be customized and returns False by default.
    """
    def unwinnable(gameplay: GameplaySequence):
        return False
    
    @property
    def PREMOVE(cls):
        raise NotImplementedError(f"Premove Conditions not defined for {cls}")
    
    @property
    def POSTMOVE(cls):
        raise NotImplementedError(f"Postmove Conditions not defined for {cls}")

class StandardRules(GameplayRule):
    """ A Gameplay Ruleset for standard gameplay mechanics """
    def gameover_noactions(gameplay: GameplaySequence):
        """ The Character has run out of willpower"""
        if gameplay.remaining_actions() <= 0:
            raise GameplaySequence.GameOver("No moves remaining!")
    def gameover_lasered(gameplay: GameplaySequence):
        """ The Character has been killed by lasers """
        for lasertype in LASERTRANS:
            for laserentity in gameplay.map.findall(lasertype):
                for laserpathcoord in gameplay.map.generatelaser(laserentity):
                    if gameplay.map.coordcontains(laserpathcoord, "C"):
                        raise GameplaySequence.GameOver("Lasered!")

    PREMOVE = [gameover_noactions]
    POSTMOVE = [gameover_lasered]

class TargetSquareRules(GameplayRule):
    """ A Gameplay Ruleset for the base game mode of Helltaker where the Character attempts to reach a specific square. """
    def unwinnable(gameplay: GameplaySequence):
        nearest = gameplay.map.nearest_entity(gameplay.character.coord, "T")
        return gameplay.map.distance_to_coord(gameplay.character.coord, nearest) > gameplay.remaining_actions()

    def victory_isattarget(gameplay: GameplaySequence):
        """ Character has arrived at the Target Square """
        if gameplay.map.coordcontains(gameplay.character.coord, "T"):
            raise GameplaySequence.Victory("Waifu Getto!")

    PREMOVE = []
    POSTMOVE = [victory_isattarget,]

class DestroyTerminalsRules(GameplayRule):
    """ A Gameplay Ruleset for the EX Mode of the game where the objective is to destroy all Terminals """
    def unwinnable(gameplay: GameplaySequence):
        nearest = gameplay.map.nearest_entity(gameplay.character.coord, "E")
        return gameplay.map.distance_to_coord(gameplay.character.coord, nearest) > gameplay.remaining_actions()

    def victory_noterminals(gameplay: GameplaySequence):
        """ There are no functional Terminals """
        if not gameplay.map.findall("E"):
            raise GameplaySequence.Victory("All Terminals Smashed!")

    PREMOVE = []
    POSTMOVE = [victory_noterminals,]

AVAILABLERULES = {
    "StandardRules":StandardRules,
    "TargetSquareRules": TargetSquareRules,
    "DestroyTerminalsRules": DestroyTerminalsRules
    }
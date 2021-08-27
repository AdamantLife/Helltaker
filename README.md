# Helltaker - A python module to replicate Helltaker game mechanics

## **Installation**
Clone repo, open console and navigate to repo:
```
// Setup an environment using whatever tool you like (optional)
python -m venv .env
.env/scripts/activate

// Install the local package
pip install .
```
#
## **Basic Usage**
Gameplay requires two attributes: a **map** and the amount of **Willpower** available to the player.

The **map** is defined using symbols which represent different ingame entities; a mapping between entities and their symbol representation is available at the top of the file (called ```MAPSYMBOLS```). 

The **map** can be defined in two ways: as a 2d array where each element in the nested arrays is a string represent a cell of the map.
```python
MAP = [
    ["C", "B", " "], ## Empty cells can be represented as a space
    ["B", "",  "T"]  ## or as an empty string
]
```
Alternatively, the array can be converted to a string where the cells are comma-separated and the rows are newline separated.
```python
MAP = "C,B, \nB,,T" ## Like with the array version, the space 
                    ## representing empty cells can be ommitted
```
**Maps** require the Character Symbol be present in order to be valid.

**Willpower** should be an integer.

### <span style="text-decoration: underline">GameplaySequence</span>

The ```GameplaySequence``` class is useful high-level class for simulating Helltaker Gameplay.
```python
gp = GameplaySequence(MAP, 30) ## map and willpower
## Actions can then be taken using GameplaySequence.move or the directional shortcuts
gp.move("right")
gp.right()
```
Gameplay has two terminating states: Victory or Game Over. These are represented by the ```GameplaySequence.Victory``` and ```GameplaySequence.GameOver``` *Exceptions* which are raised when the corresponding state is reached.

The default conditions for these are identical to the main game: in the standard gameplay version, Victory is achieved by moving into a *Target* cell; Game Over is triggered by running out of Willpower or by being killed by a laser.

### Gameplay Notes
* All coordinates outside of the map are considered Walls. This means that attempting to move off the map results in no action being taken (among other implications).
* Each action taken is added to the ```actions``` attribute. These are lowercase strings representing the direction in which the character was moved.
* In normal gameplay, if the character is on an Activated Spike, the action costs an extra point of Willpower; this is indicated in the ```actions``` list by converting the action to all uppercase.
* Only laser generators are represented as Entities on the map. In normal gameplay, the gameplay loop simply checks to see what squares the laser would pass through and then triggers a GameOver if the Character is in one of those squares.
* This module only supports turn-based maps; it would require some modification to accomodate realtime maps.

#
## **Additional Features**

* The arguments for ```GameplaySequence``` can be loaded from a *json* file using ```GameplaySequence.loadfromjson(pathdescriptor)```. The json accepts the following keys:
```json
{
    "name": "A name for the level", // Optional; a string

    "willpower": 10,            // Required; an integer

    "grid": [                   // Required; an array or string with the same
        ["C"," ","T"]           // formatting as described in Basic Usage
    ],

    "rules": [                  // Optional; Strings matching the GameplayRules
        "StandardRules",        // being used. if not provided, the default
        "TargetSquareRules"     // ruleset will be used. GameplayRules are
        ],                      // explained below

    "actions":[]                //Optional; prepopulates GameplaySequence's
                                // action list with the given actions. The grid
                                // should represent a state where these actions
                                // were already taken; willpower should not be
                                // adjusted.
}
```

* Each action taken in ```GameplaySequence``` is performed within the context of the ```gameplay_loop``` function. This function performs pre- and post-move actions (such as updating the map and checking for Victory/Game Over conditions). This can be modified by passing the _rulesets argument_ a list of ```GameplayRules``` objects. For example, to create a ```GameplaySequence``` that replicates the EX-mode gameplay:
```python
MAP = [
    ["C", " ", "E"] ## E is the symbol for a functioning (not destroyed) Terminal
]

## With DestroyTerminalsRules, a Victory Exception will be raised when there are
## no non-destroyed Terminals remaining
gp = GameplaySequence(MAP, 10, rulesets = [StandardRules, DestroyTerminalsRules])
```
* ```GameplayRules``` rules have two required attributes: *PREMOVE* and *POSTMOVE*. These should be lists of callback Functions which accept a ```GameplaySequence``` isntance as its only parameter. Functions in *PREMOVE* will be called before the Character moves and Functions in *POSTMOVE* are called after the character has moved and the map has been updated. As the callback has access to the ```GameplaySequence``` itself, it can affect the Gameplay in virtually any way. ```GameplayRules``` can also have an ```unwinnable(gameplaysequence)``` function: this function is purely an optimization function which can be used to determine if it is still possible for the chacter to win.

* ```GameplaySequence``` is built on top of other lower-level classes: ```Map``` and ```Character```. ```Map``` in particular can be leveraged to manipulate the current gamestate in ways that normally would not be possible (in which a GameplayRules object can raise a GameOver Exception).

* As always, if you are unsure of the functionality of a function or class, the test files can help clarify its uses and limitations.
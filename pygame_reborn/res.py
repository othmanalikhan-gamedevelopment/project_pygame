### Contains all the constants and in-game text (e.g. dialogues) ###


import pygame
import warnings
import os


################################ SETTINGS ######################################



DEFAULTSCREENSIZE = (1024, 768)
SCREENSIZE = DEFAULTSCREENSIZE

# TODO: scaling screen resolution
# SCREENXSCALE = 1
# SCREENYSCALE = 1

SOUNDLEVEL = 10
GAMEFPS = 30
DO = False  # special button ;)

################################## EVENTS ######################################

# custom events
CHANGEMENU = pygame.USEREVENT + 1
CHANGELEVEL = pygame.USEREVENT + 2
CHANGEPLAYER = pygame.USEREVENT + 3

BACKGROUNDUPDATE = pygame.USEREVENT + 4

MOVED = pygame.USEREVENT + 5

################################## FONTS #######################################

# Title text
TITLEFONT = "arial"
TITLEFONTSIZE = 150


TTLTXT = "EXILED"


# Main Screen txt
MENUFONT = "georgia"
MENUFONTSIZE = 30


MSTXT1 = "New Game"
MSTXT2 = "Load"
MSTXT3 = "Options"
MSTXT4 = "Exit"

################################## ARTWORK #####################################

ART_MENU = "artwork/menu"
ART_LEVEL = "artwork/level"
ART_MISC = "artwork/misc"

ART_SPRITE_NAMELESS = "artwork/sprite/nameless"
ART_EVILDOER = "artwork/sprite/evildoer"

###############################################################################

# Main purpose is to omit the declaration of an event in other modules before
# firing it (hence neater code)
def changeState(stateTransition):
    """
    Returns the next state, to transition to on a tree diagram, as an event.
    The argument passed is a stateTransition which should be in the form:
    (stateType, state) where stateType is the type of state diagram and state
    is it's corresponding node.
    """

    stateType, stateNum = stateTransition

    if stateType == "Menu":
        stateEvent = pygame.event.Event(CHANGEMENU, state=stateNum)
    elif stateType == "Level":
        stateEvent = pygame.event.Event(CHANGELEVEL, state=stateNum)
    elif stateType == "Player":
        stateEvent = pygame.event.Event(CHANGEPLAYER, state=stateNum)
    else:
        raise ValueError("'stateType' argument can only be of type 'Menu', "
                         "'Level' or 'Player'. What a noob.")

    return stateEvent


def triggerMoveEvent(spriteName, spriteRect):
    """
    Triggers an event of user defined type MOVED.
    """

    event = pygame.event.Event(MOVED, spriteName=spriteName,
                               spriteRect=spriteRect)
    pygame.event.post(event)


def isFontFound(font):
    """
    Checks if the inputted font exists on the current machine. Returns a
    boolean.
    """

    sysFontsList = pygame.font.get_fonts()

    if font in sysFontsList:
        return True
    else:
        return False


# TODO: os.sep
def loadArtworkFrom(dirPath, *searchQuery):
    """
    The path from the current working directory to the target directory
    needs to be passed as the argument and the artworks first name before the
    "_". Then the function proceeds to store those images into a dictionary.
    For instance to obtain all tile images, the dirPath must be provided and
    artworkName="tile":
    """

    imageDict = {}
    if os.path.exists(dirPath):
        imagesList = os.listdir(dirPath)

        if imagesList:  # Checks if images exist otherwise raises an error
            imageDict = _storeImages(dirPath, imagesList, *searchQuery)
        else:
            raise OSError("No images found in the specified directory.")
    else:
        raise OSError("Specified directory does not exist.")

    return imageDict


def _storeImages(dirPath, imagesList, *searchQuery):
    """
    As specified by the searchQuery, the matched image files are stored
    into a dictionary. The dictionary key is based on the image file's name
    minus the searchQuery.

    For instance, searching for "tile", "blue" in a folder that contains the
    image "tile_blue_03.png" will yield:

    "tile_blue_03.png" -- stored --> imageDict{("03")} = image file
    """

    imageDict = {}
    for imageName in imagesList:
        if not imageName.endswith(".db"):

            imagePath = os.path.join(dirPath, imageName)

            extensionRemovedString = imageName.split(".")[0]
            splitImgName = extensionRemovedString.split("_")    # convention

            if isMatched(searchQuery, splitImgName):
                for query in searchQuery:
                        splitImgName.remove(query)

                # Otherwise with the if, the key stored is of form (item,)
                if len(splitImgName) == 1:
                    imageDict[splitImgName[0]] = pygame.image.load(imagePath)
                else:
                    imageDict[tuple(splitImgName)] = \
                        pygame.image.load(imagePath)

    return imageDict


def isMatched(searchQuery, splitImgName):
    """
    Compares whether all the search keys are within the name of the image.
    Returns true if so otherwise false.
    """
    for query in searchQuery:
        if query not in splitImgName:
            return False
    return True
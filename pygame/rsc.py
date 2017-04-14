### Contains all the constants and in-game text (e.g. dialogues) ###


import pygame
import warnings
import os


################################ SETTINGS ######################################



DEFAULTSCREENSIZE = (1366, 768)
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

LOADINGSCREENARTS = "Artwork/LoadingMenu"
MAINMENUART = "Artwork/MainMenu/Adventure.png"

PLAYERART1 = "Artwork/Player/Standing"
PLAYERART2 = "Artwork/Player/Moving/Right"
PLAYERART3 = "Artwork/Player/Moving/Left"
PLAYERART4 = "Artwork/Player/Jumping"
PLAYERART5 = "Artwork/Player/InAir"
PLAYERART6 = "Artwork/Player/Shooting/Right"
PLAYERART7 = "Artwork/Player/Shooting/Left"
PLAYERART8 = "Artwork/Player/Shooting/Top"
PLAYERART9 = "Artwork/Player/Shooting/Bottom"
PLAYERART10 = "Artwork/Player/Death"

ENEMYART1 = "Artwork/Levels/Enemy/enemy.png"
ENEMYART2 = "Artwork/Levels/Enemy/fireball.png"

LEVEL01ARTS = "Artwork/Levels/Level01/level01.png"
TILEARTS = "Artwork/Levels/TilesBackground"
STRUCTURETILEARTS = "Artwork/Levels/TilesStructure"
DOORART = "Artwork/Levels/Door.png"

MISCART1 = "Artwork/Misc/Arrow.png"
MISCART2 = "Artwork/Misc/Grappling.png"
MISCART3 = "Artwork/Misc/GrapplingEnd.png"

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
def loadArtworkFrom(dirPath):
    """
    The path from the current working directory to the target directory
    needs to be passed as the argument. Then the function proceeds to store
    those images into a dictionary. The image sequence needs to be ordered
    chronologically in order for other methods to work properly.
    """

    imageDict = {}

    if os.path.exists(dirPath):

        imagesList = os.listdir(dirPath)

        # Checks if images exist otherwise raises an error
        if imagesList:
            for index, imageName in enumerate(imagesList, 1):

                if not imageName.endswith(".db"):
                    imagePath = os.path.join(dirPath, imageName)
                    imageDict[index] = pygame.image.load(imagePath)

        else:
            raise OSError("No images found in the specified directory.")
    else:
        raise OSError("Specified directory does not exist.")

    return imageDict
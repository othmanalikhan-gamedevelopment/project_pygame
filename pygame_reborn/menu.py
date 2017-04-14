###
# All in-game menus:
# - Loading Screen
# - main menu
# - ingame shop menu (not implemented yet)
# - escape menu (not implemented yet)
###

import pygame
import time
import random
import res


class Background():
    """
    The blue tiled background that represents mana itself.
    """

    def __init__(self, screen):
        """
        Mainly loads the tiles and initializes their coordinates.
        """

        self.screen = screen
        self.screenWidth, self.screenHeight = self.screen.get_size()

        self.tileDict = res.loadArtworkFrom(res.ART_MISC, "tile")
        self.tileWidth, self.tileHeight = \
            self.tileDict[("blue", "01")].get_size()
        self.amountTilesInX = (self.screenWidth // self.tileWidth) + 1
        self.amountTilesInY = (self.screenHeight // self.tileHeight) + 1

        self.coordList = self.initializeCoord()


    def initializeCoord(self):
        """
        The list of all possible coordinates of the tiles on the background
        coordinate system.
        """
        coordList = []
        for x in range(self.amountTilesInX):
            for y in range(self.amountTilesInY):
                coord = (x, y)
                coordList.append(coord)

        return coordList


    def drawTileAt(self, coord, *tile):
        """
        The interface to convert between the background tile coordinate system
        into pixel coordinates.

        coord is of form (x, y) which is the amount of tiles in the x, y
        direction respectively.
        *tile is of form "colour", "number" (following the naming convention
        of the file names).
        """
        self.screen.blit(self.tileDict[tile],
                         (coord[0]*self.tileWidth, coord[1]*self.tileHeight))


    def drawRandomTile(self, coord=None, colour=None):
        """
        Draws a tile random coloured tile at a random location onto the
        background if no arguments are supplied. By passing arguments, the
        passed arguments are not randomized.
        """

        if not coord:
            coord = random.sample(self.coordList, 1)[0]

        if not colour:
            tile = random.sample(list(self.tileDict), 1)[0]
        else:
            colouredTileList = [key for key in self.tileDict
                                if key[0] == colour]
            tile = random.sample(colouredTileList, 1)[0]

        colour, num = tile[0], tile[1]
        self.drawTileAt(coord, colour, num)


# Makes it easier to identify where the exceptions stem from
class MenuError(Exception):
    pass


class Menu():
    """
    This is a superclass that is passed to all menus so that every menu's
    structure is compatible with the clear, draw & update, event handler
    pygame cycle. As such, all methods are dummy methods.
    """

    def __init__(self, screen):
        """
        Creates instantiated variables of all the menus that are in this file
        and their associated node number as a dictionary. This is done to
        ease transitions between menus. Additionally, contains an
        instance variable of the currentMenu being used.
        """

        self.screen = screen
        self.blankMenu = BlankMenu()
        self.splashMenu = SplashMenu(self.screen)
        self.mainMenu = MainMenu(self.screen)
        self.exitMenu = ExitMenu(self.screen)

        # state "blank" is the blank menu for event handling
        self.state = {"blank": self.blankMenu,
                      "splash": None,
                      "loading": None,
                      "main": None,
                      "exit": None}

        self.stateGenerator = {"blank": BlankMenu,
                               "splash": SplashMenu,
                               "main": MainMenu,
                               "exit": ExitMenu}  # self.exitLevel

        self.currentMenu = self.state["blank"]  # Starting menu = blankMenu


    def changeState(self, label):
        """
        Changes the state of the current menu (i.e. changes menus).
        Checks whether the menu has already been generated and if not,
        generates the menu.
        """

        if not isinstance(self.state[label], self.stateGenerator[label]):
            self.currentMenu = self.stateGenerator[label](self.screen)
        else:
            self.currentMenu = self.state[label]


    def handleEvent(self, event):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def clear(self):
        pass


# Only used to control flow of logic in main game file
class BlankMenu(Menu):
    """
    A blank menu used for event handling
    """

    # Dummy consturctor (otherwise superclass constructor is invoked
    # if omittited)
    def __init__(self):
        pass



class TileEffect():
    """
    Combines multiple tiles into a single one.
    """

    def __init__(self, screen, background):
        """
        """

        self.screen = screen
        self.background = background

    def draw(self):
        """
        """




class SplashMenu(Menu):
    """
    The first screen that runs when the game launches
    """


    def __init__(self, screen):
        """
        Initializes methods in the SplashMenu
        """

        self.screen = screen
        self.background = Background(self.screen)

        self.tileDict = res.loadArtworkFrom(res.ART_MISC, "tile")
        self.drawTileList = []

        self.isEffectOne = False
        self.isEffectTwo = False
        self.isEffectThree = False

        # To draw the blue background & the red/black emblem symbol
        self.initializeEffectOne()
        self.initializeEffectTwo()
        self.initializeEffectThree()


    def update(self):
        """
        The core logic of how the two effects are executed.
        X ---> Y
        This method updates the effect being executed.
        """

        data1 = ("blue", 5, self.blueCoordItr)
        data2 = ("red", 1, self.redCoordItr)
        data3 = ("black", 1, self.blackCoordItr)


        if self.updateEffect(*data1):
            self.isEffectOne = True

        elif self.updateEffect(*data2):
            self.isEffectTwo = True

        elif self.updateEffect(*data3):
            self.isEffectThree = True



    def updateEffect(self, tileColour, drawTileRate, tileCoordItr):
        """

        """

        del self.drawTileList[:]

        time.sleep(0.035)

        try:
            for _ in range(drawTileRate):
                data = (next(tileCoordItr), tileColour)
                self.drawTileList.append(data)
            return True
        except StopIteration:
            return False



    def draw(self):
        """
        Draws either a slideShowEffect or a flashEffect on the screen
        specified by effectNum
        """

        for tileData in self.drawTileList:
            if self.isEffectOne:
                self.background.drawRandomTile(*tileData)

            if self.isEffectTwo or self.isEffectThree:
                self.background.drawTileAt(tileData[0], tileData[1], "01")











    def initializeEffectOne(self):
        """
        Initializes effect one by generating the coordinates for the blue tiles
        for the mana background. The coordinates are randomized.
        """

        self.blueCoordList = self.background.coordList

        random.shuffle(self.blueCoordList)
        self.blueCoordItr = iter(self.blueCoordList)


    def initializeEffectTwo(self):
        """
        Initializes effect two by generating the red tiles used for drawing the
        emblem.
        """

        # The -1 to remove fractional tiles since for instance amountTilesInX
        # takes into account fractional tiles by adding +1
        centerX = (self.background.amountTilesInX // 2) - 1
        centerY = (self.background.amountTilesInY // 2) - 1
        offsetX = 10
        offsetY = 6

        # rect object simplifies drawing of emblem
        rect = pygame.Rect(0, 0, offsetX, offsetY)
        rect.center = (centerX, centerY)

        self.redCoordList = []

        # draws the two columns of the emblem
        for i in range(offsetY):
            self.redCoordList.append((rect.topleft[0],
                                      rect.topleft[1] + i))
            self.redCoordList.append((rect.bottomright[0],
                                      rect.bottomright[1] - i))

        # draws the topright and bottomleft "\" symbol
        for i in range((offsetX // 2) + 1):
            self.redCoordList.append((rect.topright[0] - i,
                                      rect.topright[1] - i))
            self.redCoordList.append((rect.bottomleft[0] + i,
                                      rect.bottomleft[1] + i))

        # draws the bottomright and topleft "/" symbol but in reverse order
        for i in range((offsetX // 2), -1, -1):
            self.redCoordList.append((rect.bottomright[0] - i,
                                      rect.bottomright[1] + i))
            self.redCoordList.append((rect.topleft[0] + i,
                                      rect.topleft[1] - i))

        self.redCoordItr = iter(self.redCoordList)


    def initializeEffectThree(self):
        """
        Initializes effect three by generating the black tiles used for
        drawing the emblem.
        """

        # The -1 to remove fractional tiles since for instance amountTilesInX
        # takes into account fractional tiles by adding +1
        centerX = (self.background.amountTilesInX // 2) - 1
        centerY = (self.background.amountTilesInY // 2) - 1
        offsetX = 2
        offsetY = 0

        self.blackCoordList = []

        for i in range(5):
            self.blackCoordList.append((centerX - offsetX + i,
                                        centerY - offsetY))

        self.blackCoordList.append((centerX - offsetX + 4,
                                    centerY - offsetY + 1))

        self.blackCoordList.append((centerX - offsetX,
                                    centerY - offsetY + 1))

        self.blackCoordList.append((centerX - offsetX + 4,
                                    centerY - offsetY + 1))

        for i in range(4):
            self.blackCoordList.append((centerX + offsetX + - 2,
                                       centerY - offsetY - 2 + i))


        self.blackCoordItr = iter(self.blackCoordList)









    def endSafely(self):
        """
        Triggers an event that indicates to end loading screen and also resets
        only it's necessary variables to allow to run again
        """

        pygame.event.post(res.changeState(("Menu", "main")))

        self.effectNum = 0
        self.frameNum = 1
        self.flashesDone = 0




# class LoadingMenu(Menu):
#     """
#     The main booting screen before the main menu of the game loads
#     """
#
#     def __init__(self, screen):
#         """
#         Initializes methods in the LoadingMenu
#         """
#
#         self.screen = screen
#
#         self.effectNum = 0
#
#         self.initializeSlideShowEffect(slideFPS=0.3)
#         self.initializeFlashEffect(flashesThreshold=6, flashFPS=0.3)
#
#
#     def update(self):
#         """
#         The core logic of how the two effects are executed.
#         slideShowEffect --> flashEffect
#         This method updates the effect being executed.
#         """
#
#         # if effect 1 running
#         if self.effectNum == 1:
#             time.sleep(self.slideFPS)
#
#         # check if transition possible: effect 1 to effect 2
#         if self.frameNum > len(self.artworkDict):
#             self.effectNum = 2
#
#         # if effect 2 running
#         if self.effectNum == 2:
#             time.sleep(self.flashFPS)
#
#             if self.flashesDone > self.flashesThreshold:
#                 self.endSafely()
#
#
#     def draw(self):
#         """
#         Draws either a slideShowEffect or a flashEffect on the screen
#         specified by effectNum
#         """
#         # For initialization purposes (otherwise re-running of loading screen
#         #  skips out the first first)
#         if self.effectNum == 0:
#             self.effectNum = 1
#
#         elif self.effectNum == 1:
#             self.applySlideShowEffect()
#
#         elif self.effectNum == 2:
#             self.applyFlashEffect()
#
#
#     def applyFlashEffect(self):
#         """
#         Draws a black or white background on the screen to imitate a flashing
#         effect then increments flashesDone variable.
#         """
#
#         if self.flashesDone % 2 == 0:
#             self.screen.blit(self.blackBackground, (0,0))
#         else:
#             self.screen.blit(self.whiteBackground, (0,0))
#
#         self.flashesDone += 1
#
#
#     def applySlideShowEffect(self):
#         """
#         Draws an image on the screen from images stored in a dictionary then
#         increments the key of the dictionary.
#         """
#
#         frame = self.artworkDict[self.frameNum].convert()
#         frame = pygame.transform.scale(frame, self.screen.get_size())
#
#         self.screen.blit(frame, (0,0))
#
#         self.frameNum += 1
#
#
#     def initializeFlashEffect(self, flashesThreshold=4, flashFPS=1):
#         """
#         Initializes the variables for the flashEffect method
#         """
#
#         # one flash = either white or black
#         self.flashesThreshold = flashesThreshold
#         self.flashesDone = 0
#         self.flashFPS = flashFPS
#
#         self.whiteBackground = pygame.Surface(self.screen.get_size()).convert()
#         self.whiteBackground.fill((255,255,255))
#
#         self.blackBackground = pygame.Surface(self.screen.get_size()).convert()
#         self.blackBackground.fill((0,0,0))
#
#
#     def initializeSlideShowEffect(self, slideFPS=1):
#         """
#         Initializes the variables for the slideShow method
#         """
#
#         self.slideFPS = slideFPS  # Frames Per Second
#         self.frameNum = 1
#         self.artworkDict = res.loadArtworkFrom(res.LOADINGSCREENARTS)
#
#
#     def endSafely(self):
#         """
#         Triggers an event that indicates to end loading screen and also resets
#         only it's necessary variables to allow to run again
#         """
#
#         pygame.event.post(res.changeState(("Menu", "main")))
#
#         self.effectNum = 0
#         self.frameNum = 1
#         self.flashesDone = 0



class MainMenu(Menu):
    """
    The main menu of the game after the Loading Screen ends
    """

    def __init__(self, screen):
        """
        Constructs all the text in MainMenu as instances of class Buttons
        """

        self.screen = screen

        artworkDict = res.loadArtworkFrom(res.ART_MENU, "artwork")
        self.artwork = artworkDict["01"]
        self.background = pygame.transform.scale(self.artwork,
                                                 self.screen.get_size())

        self.initializeButtons()


    def handleEvent(self, event):
        """
        Local event handler for MainMenu that triggers methods depending on
        the event type.
        """

        # Easter egg occurs when title is clicked on
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (event.button == 1 and
                    self.buttonsDict[0].buttonRect.collidepoint(event.pos)):
                pygame.event.post(
                    res.changeState(self.buttonsDict[0].linkedToState))

        # Uses arrow keys to navigate menu
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.changeHighlight(direction="down")

            if event.key == pygame.K_UP:
                self.changeHighlight(direction="up")

            if event.key == pygame.K_RETURN:
                for button in self.buttonsDict.values():
                    if button.isHighlighted and button.linkedToState != None:
                        pygame.event.post(res.changeState(button.linkedToState))


    def changeHighlight(self, direction):

        if direction == "up":
            increment = -1
        elif direction == "down":
            increment = 1
        else:
            raise ValueError("Direction can only be 'up' or 'down'!")

        for id, currentButton in sorted(self.buttonsDict.items()):

            if currentButton.isHighlighted:
                nextButtonNum = id + increment
                if nextButtonNum in self.buttonsDict:

                    nextButton = self.buttonsDict[nextButtonNum]

                    if nextButton.highlightEnabled:
                        currentButton.isHighlighted = False
                        nextButton.isHighlighted = True
                        break


    def draw(self):
        """
        Draws the button objects onto the screen (does not draw background)
        """

        for num, button in self.buttonsDict.items():
            button.draw(self.coordsList[num], center=True)


    def clear(self):
        """
        Draws only the background onto the screen (does not draw buttons)
        """

        self.screen.blit(self.background, (0,0))


    def initializeButtons(self):
        """
        Constructs a list of instantiated variables of the button class and
        their respective coordinates
        """

        self.buttonsDict = {}

        buttonsData = [
            (res.TTLTXT, res.TITLEFONT, res.TITLEFONTSIZE,
             (255,255,255), ("Menu", 1)),
            (res.MSTXT1, res.MENUFONT, res.MENUFONTSIZE,
             (200,0,0), ("Level", 1)),
            (res.MSTXT2, res.MENUFONT, res.MENUFONTSIZE,
             (0,0,255), ("Menu", 2)),
            (res.MSTXT3, res.MENUFONT, res.MENUFONTSIZE,
             (100,100,0), ("Menu", 2)),
            (res.MSTXT4, res.MENUFONT, res.MENUFONTSIZE,
             (0,128,128), ("Menu", 6))]

        for id, (text, font, fontSize, colour, (stateType, stateNum)) in \
                enumerate(buttonsData):

            button = Button(screen=self.screen,
                            text=text,
                            textFont=font,
                            textFontSize=fontSize,
                            textColour=colour,
                            textItalic=True,
                            textBold=True,
                            linkedToState=(stateType, stateNum))

            self.buttonsDict[id] = button

        # Disables highlighting of title text
        self.buttonsDict[0].highlightEnabled = False
        # Causes first non-title button to be highlighted (displays an arrow)
        self.buttonsDict[1].isHighlighted = True

        self.initializeCoords(amount=len(self.buttonsDict), spacing=80)


    def initializeCoords(self, amount, offsetx=0, offsety=0, spacing=50):
        """
        Generates coordinates of where the buttons will be drawn. 'offsetx' &
        'offsety' refer to the offset of each coordinate in pixels. 'spacing'
        refers to the gap between each set of coordinates generated in pixels.
        """

        self.coordsList = []
        screenWidth, screenHeight = self.screen.get_size()

        for i in range(amount):

            x = screenWidth/2 + offsetx
            y = screenHeight/2.1 + i*spacing + offsety
            coord = (x, y)

            self.coordsList.append(coord)

        # Title text has a different layout
        self.coordsList[0] = (screenWidth/2, 120)


class ExitMenu(Menu):
    """
    The menu that is displayed before the game exits
    """

    def __init__(self, screen):
        """
        Initializes the exit menu
        """

        self.screen = screen


    def update(self):
        """
        Triggers a pygame.QUIT event
        """

        pygame.event.post(pygame.event.Event(pygame.QUIT))


    # def draw(self):
    #     """
    #     Draws the exit effect before quiting the game
    #     """
    #
    #     self.applyExitEffect()


    # def applyExitEffect(self):
    #     """
    #     Draws a special exit effect
    #     """
    #     pass



class Button():
    """
    Creates a button that is a component of a menu
    """

    def __init__(self, screen,
                 text="uninitialized",
                 textFont="monospace",
                 textFontSize=12,
                 textBold=False,
                 textItalic=False,
                 textColour=(255,255,255),
                 textAA=False,
                 backgroundColour=None,
                 hightlightEnabled=True,
                 isHighlighted=False,
                 linkedToState=None):
        """
        Constructs a button where the fonts are retrieved by pygame, 'text'
        refers to the literal text to be drawn, 'textAA' refers to anti-aliasing
        of text and is of type boolean, 'isHighlighted' is boolean and when
        true it draws an adjacent arrow, 'linkedToState' refers to the next
        state in a given state diagram to transition to (of the form
        (stateType, state)).
        """

        self.screen = screen

        self.text = text
        self.textFont = textFont
        self.textFontSize = textFontSize
        self.textBold = textBold
        self.textItalic = textItalic
        self.textColour = textColour
        self.textAA = textAA

        self.backgroundColour = backgroundColour
        self.highlightEnabled = hightlightEnabled
        self.isHighlighted = isHighlighted
        self.initializeHighlightSurface()

        self.linkedToState = linkedToState

        # Merges text formatting information into a single font object
        self.buttonFont = pygame.font.SysFont(self.textFont, self.textFontSize,
                                              self.textBold, self.textItalic)

        # Converts 'buttonFont' into a surface
        self.buttonSurface = self.buttonFont.render(self.text,
                                                    self.textAA,
                                                    self.textColour,
                                                    self.backgroundColour)
        self.buttonSurface = self.buttonSurface.convert()
        self.buttonRect = self.buttonSurface.get_rect()


    def draw(self, coord, center=False):
        """
        Draws the button surface on the given coordinate. The last argument
        is to specify whether to draw from the centre or the default (top-left)
        of the surface.
        """

        if center:
            x, y = coord
            self.buttonRect.center = (x, y)
            self.screen.blit(self.buttonSurface, self.buttonRect)
        else:
            self.buttonRect = self.screen.blit(self.buttonSurface, coord)

        if self.highlightEnabled and self.isHighlighted:
            self.drawHighlight(offset=-20)


    def drawHighlight(self, offset=0):
        """
        Draws the highlight effect next to the button. 'offset' refers to
        the gap between the arrow and the button in pixels.
        """

        highlightedWidth, _ = self.highlightedSurface.get_size()

        highlightedCoordx = -highlightedWidth + self.buttonRect.left - offset
        highlightedCoordy = self.buttonRect.center[1]   # y-coordinate retrieved

        self.highlightedRect.center = (highlightedCoordx, highlightedCoordy)

        self.screen.blit(self.highlightedSurface, self.highlightedRect)


    def initializeHighlightSurface(self):
        """
        Loads an image for the highlight effect and sets the color of
        the top-left corner of that image to the transparent colour (alpha
        colour)
        """

        artwork = res.loadArtworkFrom(res.ART_MENU, "arrow")

        self.highlightedSurface = artwork["01"].convert()
        self.highlightedRect = self.highlightedSurface.get_rect()

        color = self.highlightedSurface.get_at((0,0))
        self.highlightedSurface.set_colorkey(color)

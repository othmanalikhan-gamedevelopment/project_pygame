###
# All in-game menus:
# - Loading Screen
# - main menu
# - ingame shop menu (not implemented yet)
# - escape menu (not implemented yet)
###

import pygame
import time
import rsc



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
        self.loadingMenu = LoadingMenu(self.screen)
        self.mainMenu = MainMenu(self.screen)
        self.exitMenu = ExitMenu(self.screen)

        self.state = {0: self.blankMenu,    # blank menu for event handling
                      1: "loadingMenu",
                      2: "mainMenu",
                      3: None,
                      4: None,
                      5: None,
                      6: "exitMenu"}

        self.stateGenerator = {0: BlankMenu,
                               1: LoadingMenu,
                               2: MainMenu,
                               3: None,
                               4: None,
                               5: None,
                               3: ExitMenu}  # self.exitLevel

        self.currentMenu = self.state[0]  # Starting menu = blankMenu


    def changeState(self, stateNum):
        """
        Changes the state of the current menu (i.e. changes menus).
        Checks whether the menu has already been generated and if not,
        generates the menu.
        """

        if not isinstance(self.state[stateNum], self.stateGenerator[stateNum]):
            self.currentMenu = self.stateGenerator[stateNum](self.screen)
        else:
            self.currentMenu = self.state[stateNum]


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





class LoadingMenu(Menu):
    """
    The main booting screen before the main menu of the game loads
    """

    def __init__(self, screen):
        """
        Initializes methods in the LoadingMenu
        """

        self.screen = screen

        self.effectNum = 0

        self.initializeSlideShowEffect(slideFPS=0.3)
        self.initializeFlashEffect(flashesThreshold=6, flashFPS=0.3)


    def update(self):
        """
        The core logic of how the two effects are executed. 
        slideShowEffect --> flashEffect
        This method updates the effect being executed.  
        """

        # if effect 1 running
        if self.effectNum == 1:
            time.sleep(self.slideFPS)

        # check if transition possible: effect 1 to effect 2
        if self.frameNum > len(self.artworkDict):
            self.effectNum = 2

        # if effect 2 running
        if self.effectNum == 2:
            time.sleep(self.flashFPS)

            if self.flashesDone > self.flashesThreshold:
                self.safelyEnd()


    def draw(self):
        """
        Draws either a slideShowEffect or a flashEffect on the screen
        specified by effectNum
        """
        # For initialization purposes (otherwise re-running of loading screen
        #  skips out the first first)
        if self.effectNum == 0:
            self.effectNum = 1

        elif self.effectNum == 1:
            self.applySlideShowEffect()

        elif self.effectNum == 2:
            self.applyFlashEffect()


    def applyFlashEffect(self):
        """
        Draws a black or white background on the screen to imitate a flashing
        effect then increments flashesDone variable.
        """

        if self.flashesDone % 2 == 0:
            self.screen.blit(self.blackBackground, (0,0))
        else:
            self.screen.blit(self.whiteBackground, (0,0))

        self.flashesDone += 1


    def applySlideShowEffect(self):
        """
        Draws an image on the screen from images stored in a dictionary then
        increments the key of the dictionary.
        """

        frame = self.artworkDict[self.frameNum].convert()
        frame = pygame.transform.scale(frame, self.screen.get_size())

        self.screen.blit(frame, (0,0))

        self.frameNum += 1


    def initializeFlashEffect(self, flashesThreshold=4, flashFPS=1):
        """
        Initializes the variables for the flashEffect method
        """

        # one flash = either white or black
        self.flashesThreshold = flashesThreshold
        self.flashesDone = 0
        self.flashFPS = flashFPS

        self.whiteBackground = pygame.Surface(self.screen.get_size()).convert()
        self.whiteBackground.fill((255,255,255))

        self.blackBackground = pygame.Surface(self.screen.get_size()).convert()
        self.blackBackground.fill((0,0,0))


    def initializeSlideShowEffect(self, slideFPS=1):
        """
        Initializes the variables for the slideShow method
        """

        self.slideFPS = slideFPS  # Frames Per Second
        self.frameNum = 1
        self.artworkDict = rsc.loadArtworkFrom(rsc.LOADINGSCREENARTS)


    def safelyEnd(self):
        """
        Triggers an event that indicates to end loading screen and also resets
        only it's necessary variables to allow to run again
        """

        pygame.event.post(rsc.changeState(("Menu", 2)))

        self.effectNum = 0
        self.frameNum = 1
        self.flashesDone = 0



class MainMenu(Menu):
    """
    The main menu of the game after the Loading Screen ends
    """

    def __init__(self, screen):
        """
        Constructs all the text in MainMenu as instances of class Buttons
        """

        self.screen = screen
        self.artwork = pygame.image.load(rsc.MAINMENUART).convert()
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
                    rsc.changeState(self.buttonsDict[0].linkedToState))

        # Uses arrow keys to navigate menu
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.changeHighlight(direction="down")

            if event.key == pygame.K_UP:
                self.changeHighlight(direction="up")

            if event.key == pygame.K_RETURN:
                for button in self.buttonsDict.values():
                    if button.isHighlighted and button.linkedToState != None:
                        pygame.event.post(rsc.changeState(button.linkedToState))


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
            (rsc.TTLTXT, rsc.TITLEFONT, rsc.TITLEFONTSIZE,
             (255,255,255), ("Menu", 1)),
            (rsc.MSTXT1, rsc.MENUFONT, rsc.MENUFONTSIZE,
             (200,0,0), ("Level", 1)),
            (rsc.MSTXT2, rsc.MENUFONT, rsc.MENUFONTSIZE,
             (0,0,255), ("Menu", 2)),
            (rsc.MSTXT3, rsc.MENUFONT, rsc.MENUFONTSIZE,
             (100,100,0), ("Menu", 2)),
            (rsc.MSTXT4, rsc.MENUFONT, rsc.MENUFONTSIZE,
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

        self.highlightedSurface = pygame.image.load(rsc.MISCART1).convert()
        self.highlightedRect = self.highlightedSurface.get_rect()

        color = self.highlightedSurface.get_at((0,0))
        self.highlightedSurface.set_colorkey(color)

### The moduel that contains all the levels of the game: superclass Level,
### Main level, and Level 01

import pygame
import random
import sprites
import rsc



# Makes it easier to identify where the exceptions stem from
class levelError(Exception):
    pass



class Level():
    """
    This is a superclass that is passed to all levels so that every level's
    structure is compatible with the clear, draw & update, event handler
    pygame cycle. As such, some methods are dummy methods.
    """

    def __init__(self, screen, player):
        """
        Creates instantiated variables of all the levels that are in this file
        and their associated node number as a dictionary. This is done to
        ease transitions between levels. Additionally, contains an
        instance variable of the currentLevel being used.
        """

        self.screen = screen
        self.player = player
        self.blankLevel = BlankLevel()

        self.state = {0: self.blankLevel,    # blank level for event handling
                      1: "mainLevel",
                      2: "Level01",
                      3: None}  # self.exitLevel

        self.stateGenerator = {0: BlankLevel,
                               1: MainLevel,
                               2: Level01,
                               3: None}  # self.exitLevel

        self.currentLevel = self.state[0]  # Starting level = blankLevel


    def changeState(self, stateNum):
        """
        Changes the state of the current level (i.e. changes levels).
        Checks whether the level has already been generated and if not,
        generates the level.
        """

        if not isinstance(self.state[stateNum], self.stateGenerator[stateNum]):
            self.currentLevel = self.stateGenerator[stateNum](self.screen,
                                                              self.player)
        else:
            self.currentLevel = self.state[stateNum]


    def handleEvent(self, event):
        pass


    def update(self):
        pass


    def draw(self):
        pass


    def clear(self):
        pass


    def updateBackground(self):
        """
        Blits random tile types on random locations on the background surface.
        The method must first be initialized via "initializeBackground".
        """

        for _ in range(self.updateTileAmount):

            x = random.randint(0, self.amountTilesx - 1) * self.tileWidth
            y = random.randint(0, self.amountTilesy - 1) * self.tileHeight
            coord = (x, y)

            tileNum = random.randint(1, len(self.tileDict))
            tile = self.tileDict[tileNum].convert()

            self.backgroundSurface.blit(tile, coord)


    def initializeUpdateBackground(self, tileAmount=1, tileDelay=0):
        """
        Initializes the 'updateBackground' method. 'tileDelay' argument is in
        milliseconds while 'tileAmount' is the number of tiles to blit onto the
        background surface.
        """

        self.updateTileAmount = tileAmount
        pygame.time.set_timer(rsc.BACKGROUNDUPDATE, tileDelay)


    def initializeBackground(self, tileOffsetx=2, tileOffsety=2):
        """
        Draws an entire randomly generated tiles background onto a surface
        and also initializes the rect of that background.  The last two
        arguments refer to the amount of tiles to remove in each direction
        respectively.
        """

        self.tileDict = rsc.loadArtworkFrom(rsc.TILEARTS)

        # All tiles have the same width & height
        self.tileWidth, self.tileHeight = self.tileDict[1].get_size()

        self.amountTilesx = (self.screenWidth // self.tileWidth) - tileOffsetx
        self.amountTilesy = (self.screenHeight // self.tileHeight) - tileOffsety

        allTilesPixelx = self.amountTilesx * self.tileWidth
        allTilesPixely = self.amountTilesy * self.tileHeight

        centerPixelOffsetx = (self.screenWidth - allTilesPixelx) / 2
        centerPixelOffsety = (self.screenHeight - allTilesPixely) / 2

        self.backgroundOffsetx = centerPixelOffsetx
        self.backgroundOffsety = centerPixelOffsety
        self.backgroundWidth = allTilesPixelx
        self.backgroundHeight = allTilesPixely

        self.backgroundSurface = pygame.Surface((self.backgroundWidth,
                                                 self.backgroundHeight))

        for y in range(self.amountTilesy):
            for x in range(self.amountTilesx):

                coordx = x * self.tileWidth
                coordy = y * self.tileHeight
                coord = (coordx, coordy)

                tileNum = random.randint(1, len(self.tileDict))
                tile = self.tileDict[tileNum]

                self.backgroundSurface.blit(tile, coord)

        self.backgroundRect = pygame.Rect(self.backgroundOffsetx,
                                          self.backgroundOffsety,
                                          self.backgroundWidth,
                                          self.backgroundHeight)




# Only used to control flow of logic in main game file
class BlankLevel(Level):
    """
    A blank level used for event handling
    """

    # Dummy constructor (otherwise superclass constructor is invoked
    # if omittited)
    def __init__(self):
        pass



class MainLevel(Level):
    """
    The main hub level used to access other levels
    """

    def __init__(self, screen, player):
        """
        Initializes the main level by generating the background, player and
        doors.
        """

        self.screen = screen
        self.screenWidth, self.screenHeight = self.screen.get_size()

        self.initializeBackground()
        self.initializeUpdateBackground(tileAmount=10, tileDelay=1000)
        self.initializeDoors()

        self.player = player
        self.player.currentState = self.player.state[1]     # spawns player
        self.player.rect.center = (200, 200)     # spawn location
        self.player.initalize(areaBounded=self.backgroundRect)


    def handleEvent(self, event):
        """
        When a UPDATEBACKGROUND event is caught, then the updateBackground()
        function is called. Also, when the player is near a door and presses
        the enter key (triggering a key event), the player transitions levels.
        """

        if event.type == rsc.BACKGROUNDUPDATE:
            self.updateBackground()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.player.nearDoorNum in self.doorDict:
                    door = self.doorDict[self.player.nearDoorNum]
                    if not door.isDisabled:
                        pygame.event.post(rsc.changeState(door.linkedToNode))
                        self.player.rect.center = door.spawnPlayerLocation


    def draw(self):
        """
        Draws the background surface and doors of the level onto the screen.
        """

        # Everything that isn't within the background Surface area is black
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.backgroundSurface, self.backgroundRect)

        for door in self.doorDict.values():
            door.draw(self.screen)


    def clear(self):
        """
        Clears the current background by drawing the background surface only
        (which is constantly changing) onto the screen.
        """

        self.screen.blit(self.backgroundSurface, self.backgroundRect)


    def initializeDoors(self, doorSpacing=20):
        """
        Creates door objects and specifies their locations on screen.
        """

        self.doorDict = {}

        self.doorDict[1] = Door(linkedToNode=("Level", 2),
                                spawnPlayerLocation=(100, 100))
        self.doorDict[2] = Door(linkedToNode=("Level", 1), isDisabled=True,
                                alphaColour=100)
        self.doorDict[3] = Door(linkedToNode=("Level", 1), isDisabled=True,
                                alphaColour=100)

        doorWidth, _ = self.doorDict[1].surface.get_size()

        # All the doors should touch the background's bottom
        for num, door in sorted(self.doorDict.items()):
            door.rect.bottom = (self.backgroundHeight +
                                    self.backgroundOffsety)

            door.rect.right = (self.backgroundWidth/1.5 +
                               self.backgroundOffsetx +
                               (doorWidth + doorSpacing)*num)

            rsc.triggerMoveEvent(spriteName="Door" + str(num),
                                 spriteRect=door.rect)



class Level01(Level):
    """
    The first level of the game.
    """

    def __init__(self, screen, player):
        """
        """
        self.platformRectsDict = {}

        self.screen = screen
        self.screenWidth, self.screenHeight = self.screen.get_size()

        self.initializeBackground()
        self.initializeUpdateBackground(tileAmount=10, tileDelay=1000)
        self.initializeDoors()
        self.initializePlatforms()
        self.initializeEnemies()

        self.player = player
        self.player.currentState = self.player.state[1]     # spawns player
        self.player.rect.center = (100, 100)     # spawn location
        self.player.initalize(areaBounded=self.backgroundRect)


    def handleEvent(self, event):
        """
        When a UPDATEBACKGROUND event is caught, then the updateBackground()
        function is called. Also, when the player is near a door and presses
        the enter key (triggering a key event), the player transitions levels.
        """

        for enemy in self.enemiesDict.values():
            enemy.handleEvent(event)

        if event.type == rsc.BACKGROUNDUPDATE:
            self.updateBackground()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.player.nearDoorNum in self.doorDict:
                    door = self.doorDict[self.player.nearDoorNum]
                    if not door.isDisabled:
                        pygame.event.post(rsc.changeState(door.linkedToNode))
                        pygame.event.post(pygame.event.Event(pygame.QUIT))


    def update(self):
        """
        Updates the sprites in the level (in this case enemies).
        """

        for enemy in self.enemiesDict.values():
            enemy.update()


    def draw(self):
        """
        Draws the background surface and doors of the level onto the screen.
        """

        # Everything that isn't within the background Surface area is black
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.backgroundSurface, self.backgroundRect)
        self.drawLevelStructure()

        for enemy in self.enemiesDict.values():
            enemy.draw()

        for door in self.doorDict.values():
            door.draw(self.screen)


    def clear(self):
        """
        Clears the current background by drawing the background surface only
        (which is constantly changing) onto the screen.
        """

        self.screen.blit(self.backgroundSurface, self.backgroundRect)


    def drawLevelStructure(self):
        """
        Draws the platforms in the level.
        """

        for platform in self.platformRectsDict.values():
            platform.draw()


    def initializeDoors(self, doorSpacing=20):
        """
        Creates door objects and specifies their locations on screen.
        """

        self.doorDict = {}

        self.doorDict[1] = Door(linkedToNode=("Menu", 1),
                                spawnPlayerLocation=(100, 100))

        doorWidth, _ = self.doorDict[1].surface.get_size()

        # All the doors should touch the background's bottom
        for num, door in sorted(self.doorDict.items()):
            door.rect.bottom = (self.backgroundHeight +
                                    self.backgroundOffsety)

            door.rect.right = (self.backgroundWidth/1.5 +
                               self.backgroundOffsetx +
                               (doorWidth + doorSpacing)*3)

            rsc.triggerMoveEvent(spriteName="Door" + str(num),
                                 spriteRect=door.rect)



    def initializePlatforms(self):
        """
        Generates the platform sprites in the level.
        """

        for i in range(8):
            for j in range(1, 4):
                num = 3*i + j

                platform = Platform(self.screen, self.backgroundRect,
                                    2, 1, 2 + 4*i, 5*j)
                rsc.triggerMoveEvent("Platform" + str(num), platform.rect)

                self.platformRectsDict[num] = platform


    def initializeEnemies(self):
        """
        Generates the enemies in the level.
        """
        self.enemiesDict = {}

        self.enemiesDict[1] = sprites.Enemy(self.screen, 300, 205)
        self.enemiesDict[2] = sprites.Enemy(self.screen, 300, 385)
        self.enemiesDict[3] = sprites.Enemy(self.screen, 445, 565)
        self.enemiesDict[4] = sprites.Enemy(self.screen, 590, 205)
        self.enemiesDict[5] = sprites.Enemy(self.screen, 590, 565)
        self.enemiesDict[6] = sprites.Enemy(self.screen, 878, 565)




class Platform():
    """
    A class from platform sprites.
    """

    def __init__(self, screen, coordinateRect, width, height, x, y):
        """
        Constructs a platform that is made out of smaller tiles. The platform
        must be provided with a backgroundRect which is used as a coordinate
        system to draw the tiles neatly onto the background. Consequently, all
        arguments are relative to that (e.g. width of 3 is 3 tiles)
        """

        self.screen = screen
        self.structureTileDict = rsc.loadArtworkFrom(rsc.STRUCTURETILEARTS)
        # All tiles have the same width and height
        self.tileWidth, self.tileHeight = self.structureTileDict[1].get_size()


        self.coordinateRect = coordinateRect
        self.originx, self.originy = self.coordinateRect.topleft

        self.width = width
        self.height = height
        self.x = x
        self.y = y

        widthPixel = width * self.tileWidth
        heightPixel = height * self.tileHeight

        self.rect = pygame.Rect(self.originx + x * self.tileWidth,
                                self.originy + y * self.tileHeight,
                                widthPixel, heightPixel)


    def draw(self):
        """
        Draws a platform sprite. It is generated via blitting mulitple single
        tiles.
        """

        for col in range(self.width):
            for row in range(self.height):

                xblock = self.originx + (col + self.x) * self.tileWidth
                yblock = self.originy + (row + self.y) * self.tileHeight

                tileNum = random.randint(1, len(self.structureTileDict))
                tile = self.structureTileDict[tileNum].convert()

                self.screen.blit(tile, (xblock, yblock))


















class Door():
    """
    Creates a door that is a component of a level
    """

    def __init__(self,
                 linkedToNode=None,
                 spawnPlayerLocation = (500,500),
                 isDisabled = False,
                 alphaColour=230):
        """
        Loads the door image and sets the color of the top-left corner of that
        image to the transparent colour (alpha colour).
        """

        self.linkedToNode = linkedToNode
        self.spawnPlayerLocation = spawnPlayerLocation
        self.isDisabled = isDisabled
        self.alphaColour = alphaColour

        self.surface = pygame.image.load(rsc.DOORART).convert()
        self.rect = self.surface.get_rect()

        # Sets the top-left pixel of the door as the transparent colour
        color = self.surface.get_at((0, 0))
        self.surface.set_colorkey(color)
        self.surface.set_alpha(self.alphaColour)



    def draw(self, screen):
        """
        Draws the door onto the screen.
        """

        screen.blit(self.surface, self.rect)

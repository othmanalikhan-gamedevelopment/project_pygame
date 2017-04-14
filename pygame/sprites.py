### The module that contains all the sprites: base class sprite, player, enemy
### grappling hook, fireball.

import pygame
import rsc
import math


# Makes it easier to identify where the exceptions stem from
class spriteError(Exception):
    pass



class Sprite():
    """
    A base class for in-game enemies and players.
    """


    def __init__(self):
        """
        Initializes all the instance variables needed for the methods in this
        class.
        """

        self.stateAction = {"Standing": True,
                            "MovingLeft": False,
                            "MovingRight": False,
                            "Death": False}


        self.isLevelCollidedDict = {"Top": False,
                                    "Bottom": False,
                                    "Right": False,
                                    "Left": False}

        self.spritesCollidedDict = {}
        self.levelSpritesRectDict = {}

        self.currentActionState = self.stateAction["Standing"]

        # Variables initialized for animation purposes
        self.animationNum = 1
        self.gameFrameCounter = 0
        self.repeatAnimation = False
        self.animatedActionState = self.currentActionState

       # Displacement
        self.dx = 0
        self.dy = 0
        # Velocity
        self.vx = 0
        self.vy = 0
        # Acceleration
        self.ax = 0
        self.ay = 0

        self.overrideDisplacement = False
        self.disableGravity = False
        self.disableFriction = False

        self.timeStep = 1   # unit of time in mathematical equations

        self.gForce = 1/3
        self.molecularForce = 5     # the gap between two surfaces in pixels
        self.coefficientFriction = 0.1
        self.walkingSpeed = 1
        self.maxWalkingSpeed = 3
        self.terminalVelocity = 10


    def draw(self):
        """
        Draws the animation for the action that is true in stateAction. It
        synchronizes the amount of frames available for an animation with the
        in-game frame rate hence allowing speeding up or slowing down of
        animation.
        """

        if self.currentActionState != self.animatedActionState:
            self.animatedActionState = self.currentActionState
            self.gameFrameCounter = 0
            self.animationNum = 1

        animationDict, animationFPS = (
            self.stateAnimation[self.currentActionState])

        # The rate at which an animation frame plays for every
        # in-game frame (causes animations to play at a rate independent
        # of the in-game FPS).
        self.playFrame = rsc.GAMEFPS // animationFPS
        self.gameFrameCounter += 1

        # Increments the animation frame to be played next every time
        # the in-game FPS counter reaches the playFrame threshold
        if self.gameFrameCounter % self.playFrame == 0:
            self.animationNum += 1

        # Resets gameFrameCounter so that the modulus calculation above
        # always involve small numbers.
        if self.gameFrameCounter == rsc.GAMEFPS:
            self.gameFrameCounter = 0

        if self.animationNum > len(animationDict):
            if self.repeatAnimation:
                self.animationNum = 1
            else:
                self.animationNum = len(animationDict)

        self.screen.blit(animationDict[self.animationNum], self.rect)

        self.drawProjectiles()


    # Method to be overridden by subclass
    def drawProjectiles(self):
        pass


    # Dummy method to keep pygame logical structure in main file consistent
    def clear(self):
        pass


    def applyGravity(self):
        """
        Creates gravity, pulling the sprite down via increasing acceleration in
        the y-direction. If the self.disableGravity flag is triggered, then
        the influence of gravity is cancelled and the flag is reset for next
        calculation.
        """

        if not self.disableGravity:
            self.ay += self.gForce
        else:
             self.disableGravity = False


    def applyFriction(self):
        """
        Slows the sprite's velocity in the x and y direction hence slows the
        sprite down to imitate friction (a simple model only).
        f the self.disableFriction flag is triggered, then friction
        is not calculated and the flag is reset for next calculation
        """

        if not self.disableFriction:

            # Halts the sprite completely otherwise the velocity would be just
            # very small but non-zero (since velocity change above is discrete).
            if (math.fabs(self.vx) - self.coefficientFriction <
                    self.coefficientFriction):
                self.vx = 0
            elif self.vx > 0:
                self.vx -= self.coefficientFriction
            elif self.vx < 0:
                self.vx += self.coefficientFriction

            # Halts the sprite completely otherwise the velocity would be just
            # very small but non-zero (since velocity change above is discrete).
            if (math.fabs(self.vy) - self.coefficientFriction <
                    self.coefficientFriction):
                self.vy = 0
            elif self.vy > 0:
                self.vy -= self.coefficientFriction
            elif self.vy < 0:
                self.vy += self.coefficientFriction
        else:
            self.disableFriction = False


    def calculateVelocity(self):
        """
        Calculates the velocity of the sprite in the x and y direction.
        """

        # v = u + at
        self.vx = self.vx + self.ax * self.timeStep
        self.vy = self.vy + self.ay * self.timeStep


    def calculateDisplacement(self):
        """
        Calculates the displacement of the sprite in the x and y direction.
        If the self.overrideDisplacement flag is triggered, then displacement
        is not calculated and the flag is reset for next calculation
        """

        if not self.overrideDisplacement:
            # s = ut + 0.5at^2
            self.dx = (self.vx * self.timeStep) + \
                      0.5 * self.ax * (self.timeStep ** 2)
            self.dy = (self.vy * self.timeStep) + \
                      0.5 * self.ay * (self.timeStep ** 2)
        else:
            self.overrideDisplacement = False


    def checkLevelSpritesCollision(self):
        """
        Upon a sprite collision, stores the collided sprite's name along with
        its direction of collision and rect in self.spritesCollidedDict. So of
        form:
        self.spritesCollidedDict[spriteName] = (isCollidedDict, spriteRect)
        """

        for spriteName, spriteRect in self.levelSpritesRectDict.items():
            isCollidedDict = {}
            if self.rect.colliderect(spriteRect):



                # Calculating x and y components of the position vector
                # between the two objects from their centers
                x = self.rect.centerx - spriteRect.centerx
                y = self.rect.centery - spriteRect.centery

                # Rotating the coordinate system by 45 degrees (derived from
                # complex number manipulation) so that inequalities below are
                # revolve around being greater or less than zero.
                rotatedx = (y + x) / 1.4142
                rotatedy = (y - x) / 1.4142

                if rotatedx > 0 and rotatedy < 0:
                    isCollidedDict["Left"] = True
                else:
                    isCollidedDict["Left"] = False

                if rotatedx < 0 and rotatedy > 0:
                    isCollidedDict["Right"] = True
                else:
                    isCollidedDict["Right"] = False

                if rotatedx < 0 and rotatedy < 0:
                    isCollidedDict["Bottom"] = True
                else:
                    isCollidedDict["Bottom"] = False

                if rotatedx > 0 and rotatedy > 0:
                    isCollidedDict["Top"] = True
                else:
                    isCollidedDict["Top"] = False

                self.spritesCollidedDict[spriteName] = (isCollidedDict,
                                                        spriteRect)


    def applyLevelSpritesNormalReaction(self):
        """
        Applies a normal reaction force by the level on the sprite hence
        causing the sprite either to bounce or stand on the ground only if
        the ocllided object is not a door.
        """

        for spriteName, (isCollidedDict, spriteRect) in \
                self.spritesCollidedDict.items():
            if not spriteName.startswith("Door"):


                if isCollidedDict["Top"]:
                    self.vy = -self.vy // 3
                    self.dy = 0
                    self.rect.top = spriteRect.bottom


                if isCollidedDict["Bottom"]:
                    if self.rect.bottom - spriteRect.top < self.molecularForce:
                        self.vy = 0
                    else:
                        self.vy = -self.vy // 3

                    self.dy = 1     # pygame '.collidedrect' ignores boundaries
                    self.rect.bottom = spriteRect.top


                if isCollidedDict["Right"]:
                    if self.rect.right - spriteRect.left < self.molecularForce:
                        self.vx = 0
                    else:
                        self.vx = -self.vx // 3

                    self.dx = 0
                    self.rect.right = spriteRect.left


                if isCollidedDict["Left"]:
                    if self.rect.left - spriteRect.right < self.molecularForce:
                        self.vx = 0
                    else:
                        self.vx = -self.vx // 3

                    self.dx = 0
                    self.rect.left = spriteRect.right


    def predictLevelCollision(self):
        """
        Triggers a collide flag in isLevelCollidedDict upon level collision for
        the sprites next calculated (and yet to be drawn) rect.
        """

        futureRect = self.rect
        futureRect.centerx += self.dx
        futureRect.centery += self.dy

        if futureRect.left <= self.areaBounded.left:
            self.isLevelCollidedDict["Left"] = True

        if futureRect.right >= self.areaBounded.right:
            self.isLevelCollidedDict["Right"] = True

        if futureRect.bottom >= self.areaBounded.bottom:
            self.isLevelCollidedDict["Bottom"] = True

        if futureRect.top <= self.areaBounded.top:
            self.isLevelCollidedDict["Top"] = True


    def applyLevelNormalReaction(self):
        """
        Applies a normal reaction force by the level sprites on the sprite hence
        causing the sprite either to bounce or stand on the ground.
        """

        if self.isLevelCollidedDict["Top"]:
            self.vy = -self.vy // 3
            self.dy = 1
            self.rect.top = self.areaBounded.top


        if self.isLevelCollidedDict["Bottom"]:
            if self.rect.bottom - self.areaBounded.bottom < self.molecularForce:
                self.vy = 0
            else:
                self.vy = -self.vy // 3

            self.dy = 0
            self.rect.bottom = self.areaBounded.bottom


        if self.isLevelCollidedDict["Right"]:
            if self.rect.right - self.areaBounded.right < self.molecularForce:
                self.vx = 0
            else:
                self.vx = -self.vx // 3

            self.dx = 0
            self.rect.right = self.areaBounded.right


        if self.isLevelCollidedDict["Left"]:
            if self.rect.left - self.areaBounded.left > self.molecularForce:
                self.vx = 0
            else:
                self.vx = -self.vx // 3

            self.dx = 1     # Bugged Behaviour
            self.rect.left = self.areaBounded.left


    def moveRight(self):
        """
        Increases the sprites velocity in the right direction by the given rate
        only if it doesn't exceed the maxWalkingSpeed.
        """

        if self.vx < self.maxWalkingSpeed:
            self.vx += self.walkingSpeed

        self.changeStateActionTo("MovingRight")
        self.repeatAnimation = True


    def moveLeft(self):
        """
        Increases the sprites velocity in the left direction by the given rate
        only if it doesn't exceed the maxWalkingSpeed.
        """

        if -self.vx < self.maxWalkingSpeed:
            self.vx -= self.walkingSpeed

        self.changeStateActionTo("MovingLeft")
        self.repeatAnimation = True


    def checkVelocity(self):
        """
        Checks whether the sprite has reached the predefined maximum vx.
        If so, prevents the sprite from exceeding the maximum vx.
        """

        if self.vx > self.terminalVelocity:
            self.vx = self.terminalVelocity
        if self.vx < -self.terminalVelocity:
            self.vx = -self.terminalVelocity

        if self.vy > self.terminalVelocity:
            self.vy = self.terminalVelocity
        if self.vy < -self.terminalVelocity:
            self.vy = -self.terminalVelocity


    def resetLevelCollisions(self):
        """
        Sets all the values in isLevelCollidedDict to False.
        """
        self.isLevelCollidedDict = {direction: False for direction in
                                    self.isLevelCollidedDict}


    def resetSpritesCollisions(self):
        """
        Empties spritesCollidedDict.
        """
        self.spritesCollidedDict = {}


    def changeStateActionTo(self, actionToChange):
        """
        Used for transitioning between action states; sets all the actions in
        stateAction to False except the given argument action.
        """

        for action in self.stateAction:
            self.stateAction[action] = False

        self.stateAction[actionToChange] = True



class Player(Sprite):
    """
    The main character of the game that the user controls.
    """

    def __init__(self, screen):
        """
        Initializes the player.
        """

        super().__init__()

        self.screen = screen

        self.standingArtworkDict = rsc.loadArtworkFrom(rsc.PLAYERART1)
        self.movingRightArtworkDict = rsc.loadArtworkFrom(rsc.PLAYERART2)
        self.movingLeftArtworkDict = rsc.loadArtworkFrom(rsc.PLAYERART3)
        self.jumpingArtworkDict = rsc.loadArtworkFrom(rsc.PLAYERART4)
        self.inAirArtworkDict = rsc.loadArtworkFrom(rsc.PLAYERART5)
        self.shootingRightArtworkDict = rsc.loadArtworkFrom(rsc.PLAYERART6)
        self.shootingLeftArtworkDict = rsc.loadArtworkFrom(rsc.PLAYERART7)
        self.shootingTopArtworkDict = rsc.loadArtworkFrom(rsc.PLAYERART8)
        self.shootingBottomArtworkDict = rsc.loadArtworkFrom(rsc.PLAYERART9)
        self.deathArtworkDict = rsc.loadArtworkFrom(rsc.PLAYERART10)

        self.blankPlayer = BlankPlayer()
        self.state = {0: self.blankPlayer,
                      1: self}

        self.stateAction = {"Standing": True,
                            "MovingLeft": False,
                            "MovingRight": False,
                            "Jumping": False,
                            "InAir": False,
                            "ShootRight": False,
                            "ShootLeft": False,
                            "ShootTop": False,
                            "ShootBottom": False,
                            "Death": False}

        # 2nd index in the tuple is the animationFPS (independent of ingame FPS)
        self.stateAnimation = {"Standing": (self.standingArtworkDict, 2),
                               "MovingRight": (self.movingRightArtworkDict, 5),
                               "MovingLeft": (self.movingLeftArtworkDict, 5),
                               "Jumping": (self.jumpingArtworkDict, 3),
                               "InAir": (self.inAirArtworkDict, 1),
                               "ShootRight": (self.shootingRightArtworkDict, 3),
                               "ShootLeft": (self.shootingLeftArtworkDict, 3),
                               "ShootTop": (self.shootingTopArtworkDict, 3),
                               "ShootBottom": (self.shootingBottomArtworkDict,
                                              3),
                               "Death": (self.deathArtworkDict, 3)}

        self.bindingsStanding = {pygame.K_RIGHT: self.moveRight,
                                 pygame.K_LEFT: self.moveLeft,
                                 pygame.K_UP: self.jump}

        self.bindingsMoving = {pygame.K_RIGHT: self.moveRight,
                               pygame.K_LEFT: self.moveLeft,
                               pygame.K_UP: self.jump}

        self.bindingsJumping = {pygame.K_RIGHT: self.moveRight,
                                pygame.K_LEFT: self.moveLeft,
                                pygame.K_UP: self.jump}

        self.bindingsInAir = {pygame.K_RIGHT: self.moveRight,
                              pygame.K_LEFT: self.moveLeft,
                              pygame.K_UP: self.airJump}

        self.bindingsShooting = {pygame.K_UP: self.moveUpGrapplingHook,
                                 pygame.K_DOWN: self.moveDownGrapplingHook}

        self.bindingsDeath = {}

        self.stateBindings = {"Standing": self.bindingsStanding,
                              "MovingRight": self.bindingsMoving,
                              "MovingLeft": self.bindingsMoving,
                              "Jumping": self.bindingsJumping,
                              "InAir": self.bindingsInAir,
                              "ShootRight": self.bindingsShooting,
                              "ShootLeft": self.bindingsShooting,
                              "ShootTop": self.bindingsShooting,
                              "ShootBottom": self.bindingsShooting,
                              "Death": self.bindingsDeath}

        self.hooksFiredList = []
        self.levelSpritesRectDict = {}

        # Starting player = blankPlayer until summoned by level
        self.currentState = self.state[0]
        self.nearDoorNum = None
        self.isDead = False

        # All the artwork have a constant rect size
        self.rect = self.standingArtworkDict[1].get_rect()
        # player artwork has an extra 6 pixel width
        self.rect.width -= 8


        self.defaultTicker = rsc.GAMEFPS  # ticker is timer of 1 second
        self.discreteTicker = self.defaultTicker * 2
        self.jumpTicker = self.defaultTicker * 0.5
        self.stillJumpingTicker = self.defaultTicker * 0.2
        self.stillShootingTicker = self.defaultTicker * 0.2
        self.dyingTicker = self.defaultTicker * 2.2
        self.jumpVelocity = 2
        self.jumpsUsed = 0
        self.maxJumps = 3


    def handleEvent(self, event):
        """
        For left button mouse clicks, creates and calculates a hook object and
        it's direction, stores it in self.hooksFiredList. For right clicks, if
        the player is in any shooting action state, it changes state to
        standing. MOVED events are also picked up here and stored.
        """

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                clickedx, clickedy = event.pos
                centerx, centery = self.rect.center
                transformedVector = (centery - clickedy, clickedx - centerx)

                angleRadians = math.atan2(*transformedVector)
                angleDegrees = 180*angleRadians/math.pi
                origin = self.rect.center

                hook = GrapplingHook(self.screen, origin, angleDegrees,
                                     self.areaBounded,
                                     self.levelSpritesRectDict)
                self.hooksFiredList = [hook]    # To be changed in the future

            if event.button == 3 and self.isShootingActionState():
                self.changeStateActionTo("Standing")
                self.hooksFiredList = []

        if event.type == rsc.MOVED:
            spriteName = event.spriteName
            spriteRect = event.spriteRect
            self.levelSpritesRectDict[spriteName] = spriteRect

            if self.hooksFiredList:
                for hook in self.hooksFiredList:
                    hook.handleEvent(event)

        if event.type == rsc.CHANGELEVEL:
            self.levelSpritesRectDict = {}


    def update(self):
        """
        Executes the actions that each binding does in the current action state
        of the player. Additionally, applies physics on the player (e.g.
        gravity, friction, etc) and then updates players position.
        """

        if not self.isDead:
            self.updateProjectiles()
            self.updateJumpTicker()
            self.updateStillJumpingTicker()

            self.checkDoorCollision()
            self.checkCurrentActionState()
            self.checkCurrentBindings()
            self.executeCurrentBindings()

            self.applyGravity()
            self.applyFriction()

            self.calculateVelocity()
            self.checkVelocity()    # Restricts maximum velocity
            self.calculateDisplacement()

            self.predictLevelCollision()    # sees into the future :o
            if True in self.isLevelCollidedDict.values():
                self.applyLevelNormalReaction()

            self.checkLevelSpritesCollision()
            if self.spritesCollidedDict:
                self.applyLevelSpritesNormalReaction()

            self.checkDoorCollision()

            self.checkDeathActionState()
            self.checkInAirActionState()
            self.checkStandingActionState()
            self.checkShootingActionState()

            self.resetLevelCollisions()
            self.resetSpritesCollisions()

            # Updates the players position
            self.rect.centerx += self.dx
            self.rect.centery += self.dy
            rsc.triggerMoveEvent(spriteName="Player", spriteRect=self.rect)

            # Reset forces acted upon player
            self.ax = 0
            self.ay = 0
        else:
            self.currentActionState = "Death"
            self.updateDyingTicker()
            self.applyDeathEffect()


    def drawProjectiles(self):
        """
        Draws the hooks fired by the player. The actual screen blitting is done
        through the draw method inherited from the superclass.
        """

        if self.hooksFiredList:
            for hook in self.hooksFiredList:
                hook.draw()


    def updateProjectiles(self):
        """
        Updates the positions of the fired hooks by the player.
        """

        if self.hooksFiredList:
            for hook in self.hooksFiredList:
                hook.update()


    def updateDiscreteTicker(self):
        """
        Updates the self.discreteTicker.
        """

        if self.discreteTicker > 0:
            self.discreteTicker -= 1


    def updateJumpTicker(self):
        """
        Updates the self.jumpTicker.
        """

        if self.jumpTicker > 0:
            self.jumpTicker -= 1


    def updateStillJumpingTicker(self):
        """
        Updates the self.stillJumpingTicker.
        """

        if self.stateAction["Jumping"]:
            if self.stillJumpingTicker > 0:
                self.stillJumpingTicker -= 1
        else:
            self.stillJumpingTicker = self.defaultTicker * 0.8


    def updateDyingTicker(self):
        """
        Updates the self.discreteTicker which is not discrete itself but rather
        is used to exhibit discrete animation.
        """

        if self.dyingTicker > 0:
            self.dyingTicker -= 1


    def checkCurrentActionState(self):
        """
        Checks which action state the player is currently in and then assigns it
        to self.currentActionState.
        """

        for action, isActive in self.stateAction.items():
            if isActive:
                self.currentActionState = action
                return   # Only one action state can be present at a time


    def checkCurrentBindings(self):
        """
        Checks the bindings for the current action state then assigns it to
        self.currentBindings
        """

        self.currentBindings = self.stateBindings[self.currentActionState]


    def executeCurrentBindings(self):
        """
        Retrieves the keys pressed by the player currently then executes them.
        """

        keys = pygame.key.get_pressed()
        self.keysHit = [keyNum for keyNum, isKeyPressed in enumerate(keys)
                        if isKeyPressed]

        for key in self.keysHit:
            if key in self.currentBindings:
                # Executes the action of each binding
                self.currentBindings[key]()


    def checkDoorCollision(self):
        """
        Checks whether the player has collided with an door. If so, triggers
        the self.isNearDoor flag to true.
        """

        if self.spritesCollidedDict:
            for spriteName in self.spritesCollidedDict:
                if spriteName.startswith("Door"):
                    self.nearDoorNum = int(spriteName.strip("Door"))
        else:
            self.nearDoorNum = None


    def checkDeathActionState(self):
        """
        Checks whether the player has collided with an enemy. If so, triggers
        the self.dead flag to true.
        """

        if self.spritesCollidedDict:
            for spriteName in self.spritesCollidedDict:
                if spriteName.startswith("Enemy"):
                    self.isDead = True


    def checkStandingActionState(self):
        """
        Checks whether the player should transition to the standing action
        state. The player transitions only if the x and y velocities are zero.
        """

        if not self.keysHit and self.vx == 0 and self.vy == 0 \
            and not self.stateAction["Death"]:
            self.changeStateActionTo("Standing")


    def applyDeathEffect(self):
        """
        Causes the player to exponentially to fall down the screen.
        """

        self.repeatAnimation = False

        if not self.dyingTicker:
            self.dyingTicker = self.defaultTicker * 0.2
            self.rect.centery *= 1.1

        if self.rect.bottom > self.areaBounded.bottom:
            # Changes the player to a blank player
            self.currentState = self.state[0]


    def airJump(self):
        """
        Causes the player to jump in air only if the self.jumpTicker has reached
        zero. The amount of jumps in air is restricted by self.maxJumps.
        """

        if self.jumpTicker == 0:
            if self.stateAction["InAir"] and self.jumpsUsed <= self.maxJumps:

                if self.vy > 0:
                    self.vy = -2*self.jumpVelocity
                else:
                    self.vy -= 1.5*self.jumpVelocity

                self.jumpsUsed += 1
                self.jumpTicker = self.defaultTicker * 0.5


    def checkInAirActionState(self):
        """
        Checks whether the player should transition in or out of the in air
        action state. This is done by checking whether he is currently or not
        shooting or colliding with any sprites or level
        """

        isShooting = self.isShootingActionState()
        isLevelCollided = self.isLevelCollidedDict["Bottom"]
        isSpriteCollided = False   # Assume no collision then check

        for isCollided, _ in self.spritesCollidedDict.values():
            if isCollided["Bottom"]:
                isSpriteCollided = True
                break

        if not isLevelCollided and not isSpriteCollided and not isShooting:
            self.changeStateActionTo("InAir")
        else:
            self.jumpsUsed = 0

        if self.stateAction["InAir"] and isLevelCollided or \
                self.stateAction["InAir"] and isSpriteCollided:
            self.changeStateActionTo("Standing")
            self.jumpsUsed = 0


    def jump(self):
        """
        Changes the player into the jumping action state. Also, causes the
        player to jump after the self.stillJumping ticker reaches zero--
        increasing the players velocity up.
        """

        self.changeStateActionTo("Jumping")

        if not self.stillJumpingTicker:
            self.vy = -self.jumpVelocity
            self.jumpsUsed = 1
            self.changeStateActionTo("InAir")


    def checkShootingActionState(self):
        """
        Checks whether the player should transition to a direction specific
        shooting action state. This is done by checking whether the player has
        fired any projectiles and their respective directions. If so, then
        disables gravity, friction and stops the player's movement.
        """

        if self.hooksFiredList:

            self.updateDiscreteTicker()

            self.disableFriction = True
            self.disableGravity = True
            self.overrideDisplacement = True
            self.dx = 0
            self.dy = 0

            for hook in self.hooksFiredList:

                if 45 > hook.angleDegrees > -45:
                    self.changeStateActionTo("ShootRight")

                if 135 > hook.angleDegrees > 45:
                    self.changeStateActionTo("ShootTop")

                if -135 < hook.angleDegrees < -45:
                    self.changeStateActionTo("ShootBottom")

                if 180 > hook.angleDegrees > 135 or \
                        -180 < hook.angleDegrees < -135:
                    self.changeStateActionTo("ShootLeft")


    def isShootingActionState(self):
        """
        Checks whether the player is in any of the four shooting action states.
        Returns True if so otherwise False.
        """

        shootingStates = [isActive for action, isActive in
                          self.stateAction.items() if
                          action.startswith("Shoot")]

        if True in shootingStates:
            isShooting = True
        else:
            isShooting = False

        return isShooting


    def moveUpGrapplingHook(self):
        """
        Moves the player up the grappling hook. This is done in discrete steps
        hence the player moves discretely.
        """

        self.overrideDisplacement = True

        if self.hooksFiredList and not self.discreteTicker:
            self.discreteTicker = self.defaultTicker
            hook = self.hooksFiredList[0]


            self.dx = hook.initialvx * 10
            self.dy = hook.initialvy * 10
            self.rect.centerx += self.dx
            self.rect.centery += self.dy


    def moveDownGrapplingHook(self):
        """
        Moves the player up the grappling hook. This is done in discrete steps
        hence the player moves discretely.
        """

        self.overrideDisplacement = True

        if self.hooksFiredList and not self.discreteTicker:
            self.discreteTicker = self.defaultTicker
            hook = self.hooksFiredList[0]

            self.dx = -hook.initialvx * 10
            self.dy = -hook.initialvy * 10
            self.rect.centerx += self.dx
            self.rect.centery += self.dy


    def initalize(self, areaBounded):
        """
        Initializes the player. Creates an instance variable of the region where
        the player is bounded to.
        """

        self.areaBounded = areaBounded



class BlankPlayer():
    """
    A blank player used for event handling and as a dead player when playing
    multiplayer.
    """

    def handleEvent(self):
        pass


    def update(self):
        pass


    def draw(self):
        pass


    def clear(self):
        pass



class Enemy(Sprite):
    """
    The main evil doer of the game.
    """

    def __init__(self, screen, x, y):
        """
        Initializes the evil doer.
        """

        super().__init__()

        self.screen = screen

        self.standingArtwork = pygame.image.load(rsc.ENEMYART1)
        # All the artwork have a constant rect size
        self.rect = self.standingArtwork.get_rect()
        self.rect.width -= 10
        self.rect.height -= 10
        self.rect.center = (x, y)

        self.aggroRect = self.rect.copy()
        self.aggroRect.width += 300
        self.aggroRect.height += 300
        self.aggroRect.center = self.rect.center
        self.isTargetInRange = False
        self.playerDirection = (0, 0)

        self.isDead = False
        self.fireballsList = []
        self.levelSpritesRectDict = {}

        self.defaultTicker = rsc.GAMEFPS
        self.fireballTicker = self.defaultTicker * 3

        rsc.triggerMoveEvent(spriteName="Enemy" + str(id(self)),
                             spriteRect=self.rect)


    def handleEvent(self, event):
        """
        MOVED events are also picked up here and stored.
        """

        if event.type == rsc.MOVED:
            spriteName = event.spriteName
            spriteRect = event.spriteRect
            self.levelSpritesRectDict[spriteName] = spriteRect

            if self.fireballsList:
                for fireball in self.fireballsList:
                    fireball.handleEvent(event)


    def update(self):
        """
        Updates the evil doer, unleashing further evil.
        """

        if not self.isDead:
            self.updateFireballTicker()

            self.checkLevelSpritesCollision()
            self.checkAggro()

            if self.isTargetInRange:
                self.shootFireball()
                self.updateFireballs()

            self.resetSpritesCollisions()
        else:
            pass


    def draw(self):
        """
        Draws the enemy.
        """

        if not self.isDead:
            self.screen.blit(self.standingArtwork, self.rect)

            if self.fireballsList:
                for fireball in self.fireballsList:
                    fireball.draw()
        else:
            pass


    def shootFireball(self):
        """
        Generates a fireball.
        """

        if self.fireballTicker == 0:

            (x, y) = self.playerDirection
            fireball = Fireball(self.screen, x, y, self.rect.center)
            self.fireballsList.append(fireball)

            if len(self.fireballsList) > 5:
                del self.fireballsList[0]

            self.fireballTicker = self.defaultTicker * 3


    def updateFireballs(self):
        """
        Updates the positions of the fired hooks by the player.
        """

        for fireball in self.fireballsList:
            fireball.update()


    def updateFireballTicker(self):
        """
        Updates the self.fireballTicker.
        """

        if self.fireballTicker > 0:
            self.fireballTicker -= 1


    def checkAggro(self):
        """
        Checks whether the player is close enough to be scorched. If so,
        triggers a flag and and calculates the displacement vector.
        """

        for spriteName, spriteRect in self.levelSpritesRectDict.items():
            if spriteName.startswith("Player"):
                if self.aggroRect.collidepoint(spriteRect.center):
                    self.isTargetInRange = True

                    x1, y1 = spriteRect.center
                    x2, y2 = self.rect.center
                    self.playerDirection = (x1 - x2, y1 - y2)


    def checkDeathActionState(self):
        """
        """


    def checkLevelSpritesCollision(self):
        """
        Upon a sprite collision, sets the self.isSpriteCollide flag to true.
        """

        for spriteName, spriteRect in self.levelSpritesRectDict.items():
            if self.rect.colliderect(spriteRect) and \
                    spriteName.startswith("Hook"):
                self.isDead = True



class Fireball():
    """
    A class for the fireball spell.
    """

    def __init__(self, screen, directionx, directiony, origin):
        """
        Initializes the fireball
        """

        self.screen = screen

        self.x = directionx
        self.y = directiony

        self.fireballArtwork = pygame.image.load(rsc.ENEMYART2)
        self.rect = self.fireballArtwork.get_rect()
        self.rect.center = origin

        self.levelSpriteRectDict = {}


    def handleEvent(self, event):
        """
        Catches MOVED events fired by any sprite that can be collided into.
        """

        if event.type == rsc.MOVED:
            spriteName = event.spriteName
            spriteRect = event.spriteRect

            if spriteName.startswith("Player"):
                self.levelSpriteRectDict[spriteName] = spriteRect


    def draw(self):
        """
        Draws the fireball.
        """

        self.screen.blit(self.fireballArtwork, self.rect)


    def update(self):
        """
        Updates the fireball's coordinates
        """

        self.rect.centerx += self.x / 100
        self.rect.centery += self.y / 100
        rsc.triggerMoveEvent("Enemy" + str(id(self)), self.rect)





class GrapplingHook():
    """
    The projectiles the main player shoots: grappling hook.
    """

    def __init__(self, screen, origin, angle, areaBounded,
                 levelSpritesRectDict):
        """
        """

        # .convert() is omitted as it renders the images completely black
        self.grapplingEndArtwork = pygame.image.load(rsc.MISCART3)
        self.grapplingArtwork = pygame.image.load(rsc.MISCART2)

        self.screen = screen
        self.areaBounded = areaBounded

        self.origin = origin
        self.finale = origin
        self.angleDegrees = angle
        self.angleRadians = math.pi * angle / 180
        self.vx = math.cos(self.angleRadians) * 10
        self.vy = -math.sin(self.angleRadians) * 10    # y-axis is reversed
        self.initialvx = self.vx
        self.initialvy = self.vy
        self.timeStep = 1

        # Initial origin offset
        self.dx = self.vx * 3
        self.dy = self.vy * 3

        self.grapplingEndSurface = pygame.transform.rotate(
            self.grapplingEndArtwork, self.angleDegrees)
        self.grapplingSurface = pygame.transform.rotate(
            self.grapplingArtwork, self.angleDegrees)

        # Both artwork images have the same rect size
        self.rect = self.grapplingEndSurface.get_rect()
        self.rect.center = self.origin
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        self.afterImageRect = self.rect.copy()

        self.isLevelCollide = False
        self.isSpriteCollide = False
        self.isFlying = True

        self.amountDrawn = 1
        self.defaultTicker = rsc.GAMEFPS
        self.initialDelayTicker = self.defaultTicker * 1

        self.levelSpritesRectDict = levelSpritesRectDict


    def handleEvent(self, event):
        """
        Catches MOVED events fired by any sprite that can be collided into.
        """

        if event.type == rsc.MOVED:
            spriteName = event.spriteName
            spriteRect = event.spriteRect

            if spriteName.startswith("Enemy") or \
                spriteName.startswith("Platform"):
                self.levelSpritesRectDict[spriteName] = spriteRect


    def draw(self):
        """
        Draws a flying SPEAR on screen that is meant to be a grappling hook.
        """

        if not self.initialDelayTicker:
            if self.isFlying:
                self.screen.blit(self.grapplingEndSurface, self.rect)
            else:
                pygame.draw.line(self.screen, (0,0,0), self.origin,
                                 self.finale, 6)


    def update(self):
        """
        Updates the position of the grappling hook. Also, if the grappling hook
        collides with either the level or a sprite, a straight line is drawn
        from the origin until the finale destination.
        """


        self.updateInitialDelayTicker()
        if not self.isLevelCollide and not self.isSpriteCollide:
            if not self.initialDelayTicker:
                self.checkLevelCollision()
                self.checkLevelSpritesCollision()

                # Allows the grappling hook to accelerate
                self.vx *= 1.05
                self.vy *= 1.05

                self.dx = self.vx * self.timeStep
                self.dy = self.vx * self.timeStep

                self.rect.centerx += self.vx
                self.rect.centery += self.vy
        else:
            self.isFlying = False
            self.finale = self.rect.center
            rsc.triggerMoveEvent("Hook", self.rect)


    def updateInitialDelayTicker(self):
        """
        Updates the self.initialDelayTicker.
        """

        if self.initialDelayTicker > 0:
            self.initialDelayTicker -= 1


    def checkLevelSpritesCollision(self):
        """
        Upon a sprite collision, sets the self.isSpriteCollide flag to true.
        """

        for spriteName, spriteRect in self.levelSpritesRectDict.items():
            if self.rect.colliderect(spriteRect) and \
                    not spriteName.startswith("Player"):
                self.isSpriteCollide = True


    def checkLevelCollision(self):
        """
        Upon level collision, sets the self.iLevelCollide flag to true.
        """

        if self.rect.left <= self.areaBounded.left or \
                        self.rect.right >= self.areaBounded.right or \
                        self.rect.bottom >= self.areaBounded.bottom or \
                        self.rect.top <= self.areaBounded.top:
            self.isLevelCollide = True
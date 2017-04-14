### Author: Othman Alikhan
### SID: 200684094
### All works that are not rightfully owned by Othman Alikhan are credited to
### their rightful owners.

import pygame
import sprites
import levels
import menus
import rsc
import sys
import traceback



class Game():
    """
    Responsible for orchestrating all other classes so that relevant
    information from certain classes are visible to other classes.
    """


    def __init__(self):
        """
        Initializes pygame, in-game classes and sprites
        """

        # pygame initialization
        pygame.init()
        self.running = True
        self.clock = pygame.time.Clock()

        #  screen initialization
        self.screen = pygame.display.set_mode(rsc.DEFAULTSCREENSIZE,
                                              pygame.FULLSCREEN)
        pygame.display.set_caption("Exiled")

        # in-game classes & sprites initialization
        self.player = sprites.Player(self.screen)
        self.menu = menus.Menu(self.screen)
        self.level = levels.Level(self.screen, self.player)


    def eventHandle(self, event):
        """
        Redirects any event occurred in-game to the corresponding class that is
        meant to handle it.
        """

        if event.type == pygame.QUIT:
            self.running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False

        if event.type == rsc.CHANGEPLAYER:
            self.player.currentState = self.player.state[event.state]
        if not isinstance(self.player.currentState, sprites.BlankPlayer):
            self.player.handleEvent(event)

        if event.type == rsc.CHANGELEVEL:
            self.level.changeState(event.state)
            self.menu.changeState(0)    # Shuts menu from listening to events
        if not isinstance(self.level.currentLevel, levels.BlankLevel):
            self.level.currentLevel.handleEvent(event)

        if event.type == rsc.CHANGEMENU:
            self.menu.changeState(event.state)
        if not isinstance(self.menu.currentMenu, menus.BlankMenu):
            self.menu.currentMenu.handleEvent(event)


    def run(self):
        """
        Executes the game
        """

        self.menu.changeState(1)    # Launches the loadingMenu to start the game

        while self.running:

            self.clock.tick(rsc.GAMEFPS)

            for event in pygame.event.get():
                self.eventHandle(event)

            self.menu.currentMenu.clear()
            self.menu.currentMenu.update()
            self.menu.currentMenu.draw()

            self.level.currentLevel.clear()
            self.level.currentLevel.update()
            self.level.currentLevel.draw()

            self.player.currentState.clear()
            self.player.currentState.update()
            self.player.currentState.draw()

            pygame.display.flip()


if __name__ == "__main__":

    try:
        game = Game()
        game.run()
    except Exception:
        print("An unexpected error has occured!")
        sys.exit()
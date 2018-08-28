# -*- coding: utf-8 -*-
"""
    space-whiskey.library
    ~~~~~~~~~~~~~~
    :copyright: © 2018 by the Phillip Royer.
    :license: BSD, see LICENSE for more details.
"""
import pygame
import logging
import utils
import json
from game import *

class Library:
    def __init__(self, screen):
        self.screen = screen
        self.games = []
        self.index = 0

        utils.verifyGamesDirectory()
        self.path = utils.getGamesDirectory()
        self.directories = utils.listDirectories()

    def build(self):

        logging.info("Building library from directories")
        self.buildLibraryFromDirectories()

        logging.info("Building library from file")
        self.buildLibraryFromFile()

        if self.getCount() > 0:
            self.games[self.index].focus()
            if (self.index + 1) <= (self.getCount() - 1):
                pass
                self.games[self.index + 1].unfocusRight()

            # self.setupSlider()

    def buildLibraryFromDirectories(self, folder=utils.getGamesDirectory()):
        directories = utils.listDirectories(folder)
        for directory in directories:
            if utils.verifyMetadata(folder + '/' + directory):
                with open(folder + '/' + directory + '/metadata.json') as f:
                    data = json.load(f)
                    game = Game(
                            directory,
                            data['title'],
                            data['description'],
                            folder + '/' + directory + '/' + data['image'],
                            data['command'])
                    game.create(self.screen)
                    self.games.append(game)

    def buildLibraryFromFile(self):
        if utils.verifyLibraryFile():
            with open(self.path + '/library.json') as f:
                library_file = json.load(f)
                if 'games' in library_file:
                    for item in library_file['games']:
                        game = Game(
                            'Games',
                            item['title'],
                            item['description'],
                            item['image'],
                            item['command'])
                        game.create(self.screen)
                        self.games.append(game)
                if 'directories' in library_file:
                    for directory in library_file['directories']:
                        self.buildLibraryFromDirectories(directory)

    def setupSlider(self):
        self.sliderFrame = tk.Frame(
                master=self.canvas,
                highlightthickness=0, highlightbackground='black',
                bg='black')
        self.slider = Scale(
            self.sliderFrame, from_=1,
            to=self.getCount(), bg="black", fg='white',
            highlightthickness=0, highlightbackground='black',
            troughcolor='white',
            orient=HORIZONTAL, command=self.setFocus)
        self.slider.pack(fill='x')
        self.sliderFrame.pack()
        self.canvas.create_window(self.canvas.winfo_width()/2, self.canvas.winfo_height() - 70, window=self.sliderFrame)

    def nextGame(self):
        if self.index < len(self.games) - 1:
            self.index += 1
            self.setFocus(self.index + 1)
            #self.slider.set(self.index + 1)

    def previousGame(self):
        if self.index > 0:
            self.index -= 1
            self.setFocus(self.index + 1)
            #self.slider.set(self.index + 1)

    def setFocus(self, index):
        self.screen.fill((0,0,0))
        self.index = int(index) - 1
        for game in self.games:
            game.unfocus()
        if self.index > 0:
            self.games[self.index - 1].unfocusLeft()
        self.games[self.index].focus()
        if self.index < self.getCount() - 1:
            self.games[self.index + 1].unfocusRight()
        pygame.display.flip()

    def getCount(self):
        return len(self.games)

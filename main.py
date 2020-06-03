#FishTail! - Tile Race Game

import pygame as pg
import sys
import random as rndm
import os
from os import path
from settings import *
from sprites import *
from tilemap import *

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        os.environ['SDL_VIDEO_WINDOW_POS'] = '400, 25'
        self.DS = pg.display.set_mode((WDTH, HGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(10, 50)
        self.load_data()
        self.running = True

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'Images')
        self.map = Map(path.join(game_folder, 'map.txt'))
        self.player_img = pg.image.load(path.join(img_folder, PLYR_IMG)).convert_alpha()
        self.player_img = pg.transform.rotate(self.player_img, -90)
        self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.bullet_img = pg.transform.scale(self.bullet_img, (5, 5))
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.mob_img = pg.transform.rotate(self.mob_img, -90)
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESZ, TILESZ))

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
        self.camera = Camera(self.map.width, self.map.height)
        self.run()

    def run(self):
        # game loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        # game loop events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if self.playing:
                        self.playing = False
                    self.running = False

    def update(self):
        # game loop update
        self.all_sprites.update()
        self.camera.update(self.player)
        # bulets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.kill()

    def draw_grid(self):
        for x in range(0, WDTH, TILESZ):
            pg.draw.line(self.DS, LIGHTGREY, (x, 0), (x, HGHT))
        for y in range(0, HGHT, TILESZ):
            pg.draw.line(self.DS, LIGHTGREY, (0, y), (WDTH, y))

    def draw(self):
        # game loop draw
        pg.display.set_caption("{:2.0}".format(self.clock.get_fps()))
        self.DS.fill(BGCOLOR)
        #self.draw_grid()
        for sprite in self.all_sprites:
            self.DS.blit(sprite.image, self.camera.apply(sprite))
        # pg.draw.rect(self.DS, WHITE, self.player.hit_rect, 2)
        pg.display.flip()

    def show_start_screen(self):
        # game splash / start screen
        pass

    def show_go_screen(self):
        # game over / continue screen
        pass

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()

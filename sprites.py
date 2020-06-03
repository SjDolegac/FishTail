# Sprite classes for main game
import pygame as pg
import random as rd
from random import uniform
from settings import *
from tilemap import collide_hit_rect
vec = pg.math.Vector2
import numpy as np

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if sprite.vel.x > 0:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if sprite.vel.x < 0:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if sprite.vel.y > 0:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if sprite.vel.y < 0:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #self.image = pg.Surface((TILESZ, TILESZ))
        #self.image.fill(PURPLE)
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.hit_rect = PLYR_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESZ
        self.acc = vec(0, 0)
        self.rot = 0
        self.last_shot = 0

    def get_keys(self):
        self.rot_speed = 0
        self.acc = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.rot_speed = PLYR_ROT_SPD
        if keys[pg.K_RIGHT]:
            self.rot_speed = -PLYR_ROT_SPD
        if keys[pg.K_UP]:
            self.vel = vec(PLYR_ACC, 0).rotate(-self.rot)
        if keys[pg.K_DOWN]:
            self.vel = vec(-PLYR_ACC / 2, 0).rotate(-self.rot)
        if keys[pg.K_SPACE]:
            now = pg.time.get_ticks()
            if now - self.last_shot > BULLET_RATE:
                self.last_shot = now
                dir = vec(1, 0).rotate(-self.rot)
                pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
                Bullet(self.game, pos, dir)
                #self.vel = vec(-KICKBACK, 0).rotate(-self.rot)
        self.acc += self.vel * PLYR_FRCTN
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

    def update(self):
        self.get_keys()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center


class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILESZ
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.pos_UR = vec(WDTH * 2 - TILESZ * 4, 4 * TILESZ)
        self.pos_BR = vec(WDTH * 2 - TILESZ * 4, HGHT * 2 - 4 * TILESZ)
        self.pos_BL = vec(4 * TILESZ, HGHT * 2 - 4 * TILESZ)
        self.pos_UL = vec(4 * TILESZ, 4 * TILESZ)

    def update(self):
        if self.pos.x < WDTH * 2 * 0.20 and self.pos.y < HGHT * 2 * 0.20 + rd.randrange(-15, 15):
            self.rot = (self.pos_UR - self.pos).angle_to(vec(1, 0))
        elif self.pos.x > WDTH * 2 * 0.80 + rd.randrange(-15, 15) and self.pos.y < HGHT * 2 * 0.20:
            self.rot = (self.pos_BR - self.pos).angle_to(vec(1, 0))
        elif self.pos.x > WDTH * 2 * 0.80 and self.pos.y > HGHT * 2 * 0.85 + rd.randrange(-15, 15):
            self.rot = (self.pos_BL - self.pos).angle_to(vec(1, 0))
        elif self.pos.x < WDTH * 2 * 0.20 + rd.randrange(-15, 15) and self.pos.y > HGHT * 2 * 0.80:
            self.rot = (self.pos_UL - self.pos).angle_to(vec(1, 0))
        self.image = pg.transform.rotate(self.game.mob_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.adj_frctn = np.random.random(1)[0]
        self.acc = vec(MOB_SPD, 0).rotate(-self.rot)
        self.acc += self.vel * (MOB_FRCTN - self.adj_frctn)
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center


class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_img
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        spread = uniform(-GUN_SPREAD, GUN_SPREAD)
        self.vec = dir.rotate(spread) * BULLET_SPD
        self.spawn_time = pg.time.get_ticks()
        self.rot = 0

    def update(self):
        self.pos += self.vec * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > BULLET_LFTIME:
            self.kill()


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESZ
        self.rect.y = y * TILESZ

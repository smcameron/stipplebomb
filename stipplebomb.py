#!/usr/bin/python
#
# Copyright (c) 2013 Stephen M. Cameron
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import pygame
import time
import os, sys
import Image
import random
import math

im = Image.open("image.jpg")

x = 3
y = 4

pix = im.load()
print pix[x,y]
image_width = 0.0 + im.size[0];
image_height = 0.0 + im.size[1];
screen_width = 800
screen_height = 700
scaling_factor = (0.0 + screen_height) / (0.0 + image_height);
black = (0, 0, 0)
white = (255, 255, 255)

# origin on screen
osx = (screen_width / 2.0) - (image_width / 2.0) * scaling_factor;
osy = 0.0;

print "w = ", image_width, "h = ", image_height

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.update()

# screen x to image x
def sxtoix(sx):
  return (sx - osx) / scaling_factor;

def sytoiy(sy):
  return (sy - osy) / scaling_factor;

def sampleimg(sx, sy):
   ix = sxtoix(sx)
   iy = sytoiy(sy)
   if ix < 0:
      return 0
   if iy < 0:
      return 0
   if ix >= image_width:
      return 0
   if iy >= image_height:
      return 0
   return pix[ix, iy]

# image intensity to circle radius
def itor(i):
   r = ((0.0 + i) / 255.0) * 7.0;
   if r < 0.01:
	r = 0;
   return r;
    
def circle(x, y, r):
	pygame.draw.circle(screen, white, (x, y), r, 0);

class ball:
   x = 0.0;
   y = 0.0;
   vx = 0.0;
   vy = 0.0;

   def __init__(self, x, y, vx, vy):
      self.x = x;
      self.y = y;
      self.vx = vx;
      self.vy = vy;

   def move(self):
      self.x = self.x + self.vx
      if self.x < 0:
         self.x += 0.0 + screen_width; 
      if self.x > 0.0 + screen_width:
         self.x -= 0.0 + screen_width; 
      if self.y < 0:
         self.y += 0.0 + screen_height; 
      if self.y > 0.0 + screen_height:
         self.y -= 0.0 + screen_height; 
      self.y = self.y + self.vy
      self.vx = 0.95 * self.vx
      self.vy = 0.95 * self.vy
      

   def draw(self):
      r = itor(sampleimg(int(self.x), int(self.y)));
      if (r > 0.01):
          circle(int(self.x), int(self.y), int(r));

balls = [];

def addball(x, y, vx, vy):
  balls.append(ball(x, y, vx, vy))

def drawballs():
   for i in balls:
      i.draw();

def moveballs():
   for i in balls:
      i.move();

def add_a_ball():
  tx = random.randint(0, screen_width);
  ty = random.randint(0, screen_height);
  vx = random.randint(-8, 8);
  vy = random.randint(-8, 8);
  addball(tx, ty, vx, vy);

for i in range(0, 8000):
   for j in range(0, 5):
     add_a_ball()
   moveballs()
   screen.fill(black)
   drawballs()
   pygame.display.update()
   time.sleep(1.0 / 30.0);


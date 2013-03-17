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

starmode = 0;
imagename = "image.jpg";
if (len(sys.argv) >= 2):
  imagename = sys.argv[1];

niterations = 1500;
if (len(sys.argv) >= 3):
  niterations = int(sys.argv[2]);

im = Image.open(imagename)

pix = im.load()
image_width = 0.0 + im.size[0];
image_height = 0.0 + im.size[1];
screen_width = 700 
screen_height = int(screen_width * image_height / image_width);
scaling_factor = (0.8 * screen_height) / (0.0 + image_height);
black = (0, 0, 0)
white = (255, 255, 255)
lightblue = (150, 150, 255);
zone = {}
xzones = 20.0
yzones = 20.0
maxvel = 25.0

# offsets for 8 cardinal directions 
offset = [(0, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)];

# origin on screen
osx = (screen_width / 2.0) - (image_width / 2.0) * scaling_factor;
osy = (screen_height * 0.1);

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
   r = ((0.0 + i) / 255.0) * 10.0;
   if r < 0.01:
	r = 0;
   return r;
    
def star(x, y, r, b):
	mycolor = (b.cr, b.cg, b.cb);
	pygame.draw.line(screen, mycolor, (x - r, y), (x + r, y), 1); 
	pygame.draw.line(screen, mycolor, (x, y - r), (x, y + r), 1); 
	if ((r / 2.0) < 1.0):
		pygame.draw.circle(screen, mycolor, (x, y), r / 2, 0);
	else:
		pygame.draw.circle(screen, mycolor, (x, y), r / 2, 0);
		pygame.draw.circle(screen, white, (x, y), r / 4, 0);

def circle(x, y, r, b):
		pygame.draw.circle(screen, white, (x, y), r);

class ball:
   x = 0.0;
   y = 0.0;
   vx = 0.0;
   vy = 0.0;
   cr = 255.0;
   cb = 255.0;
   cg = 255.0;

   def __init__(self, x, y, vx, vy):
      self.x = x;
      self.y = y;
      self.vx = vx;
      self.vy = vy;
      self.cr -= random.randint(0, 100);
      self.cg -= random.randint(0, 100);
      self.cb -= random.randint(0, 100);

   def reset_zone(self, oldx, oldy):

      # calculate previous current zone
      zx = int(oldx / xzones)
      zy = int(oldy / yzones)

      # calculate new zone
      nzx = int(self.x / xzones)
      nzy = int(self.y / yzones)

      # if the zone hasn't changed, nothing to do.
      if nzx == zx and nzy == zy:
         return;

      # remove ourself from the old zone
      oldlist = zone[(zx, zy)]
      oldlist.remove(self)
      zone[(zx, zy)] = oldlist

      # add ourself to the new zone
      if (nzx, nzy) in zone:
         newlist = zone[(nzx, nzy)]
         newlist.append(self)
      else:
         newlist = [self]
      zone[(nzx, nzy)] = newlist

   def sum_one_force(self, i):
       dist = (self.x - i.x) * (self.x - i.x) + (self.y - i.y) * (self.y - i.y)
       if dist > 400:
          return;
       d = math.sqrt(dist);
       if d <= 0.01:
          d = 0.01;
       r1 = itor(sampleimg(int(self.x), int(self.y))); 
       r2 = itor(sampleimg(int(i.x), int(i.y))); 
       if r1 < 0.01:
          r1 = 0.01;
       if r2 < 0.01:
          r2 = 0.01;
       if dist > 0:
          force = (0.0 + r1) * (0.0 + r2) / dist;
       else:
          force = 8.0;
       force = 4.5 * force
       xforce = ((self.x - i.x) / d) * force;
       yforce = ((self.y - i.y) / d) * force;
       xa = 1.0 * xforce / r1;
       ya = 1.0 * yforce / r1;
       self.vx += xa;
       self.vy += ya;
       if self.vx > maxvel:
	  self.vx = maxvel
       if self.vx < -maxvel:
	  self.vx = -maxvel
       if self.vy > maxvel:
	  self.vy = maxvel
       if self.vy < -maxvel:
	  self.vy = -maxvel

   def sum_zone_forces(self, zx, zy):
      if (zx, zy) in zone:
        blist = zone[(zx, zy)]
        for i in blist:
            self.sum_one_force(i);

   def sum_all_forces(self):
       for o in offset:
           zx = int(self.x / xzones);
           zy = int(self.y / yzones);
           self.sum_zone_forces(zx + o[0], zy + o[1]);

   def move(self):
      # calculate current zone
      oldx = self.x
      oldy = self.y 
      # move
      self.x = self.x + self.vx
      self.y = self.y + self.vy
      if self.x < 0:
         self.x += 0.0 + screen_width; 
      if self.x > 0.0 + screen_width:
         self.x -= 0.0 + screen_width; 
      if self.y < 0:
         self.y += 0.0 + screen_height; 
      if self.y > 0.0 + screen_height:
         self.y -= 0.0 + screen_height; 

      # damp velocity 
      self.vx = 0.90 * self.vx
      self.vy = 0.90 * self.vy
      self.reset_zone(oldx, oldy)

   def draw(self):
      r = itor(sampleimg(int(self.x), int(self.y)));
      if (r > 0.01):
          if (starmode):
              star(int(self.x), int(self.y), int(r), self);
          else:
              circle(int(self.x), int(self.y), int(r), self);

   def printball(self):
      r = itor(sampleimg(int(self.x), int(self.y)));
      if (r > 0.01):
         print "translate(v = [", self.x, ", ", self.y, "]) {";
	 # print "   circle(", r, ", $fn = 50);"; 
	 print "   circle(", r, ");"; 
	 print "}";

balls = [];

def addball(x, y, vx, vy):
  myball = ball(x, y, vx, vy);
  balls.append(myball)
  zx = int(x / xzones)
  zy = int(y / yzones)
  if (zx, zy) in zone:
     blist = zone[(zx, zy)];
     blist.append(myball);
     zone[(zx, zy)] = blist;
  else:
     zone[(zx, zy)] = [myball]

def drawballs():
   for i in balls:
      i.draw();

def moveballs():
   for i in balls:
      i.sum_all_forces();
      i.move();

def add_a_ball():
  # tx = random.randint(0, screen_width);
  # ty = random.randint(0, screen_height);
  # vx = random.randint(-8, 8);
  # vy = random.randint(-8, 8);
  tx = random.randint(screen_width / 2 - 50, screen_width / 2 + 50);
  ty = random.randint(int (screen_height * 0.9 / 2 + screen_height * 0.05) - 50,
				int(screen_height * 0.9 / 2 + screen_height * 0.05) + 50);
  vx = random.randint(-2, 2);
  vy = random.randint(-2, 2);
  addball(tx, ty, vx, vy);

for i in range(0, niterations):
   if i < 85:
     for j in range(0, 20):
       add_a_ball()
   moveballs()
   screen.fill(black)
   drawballs()
   pygame.display.update()
   # time.sleep(1.0 / 30.0);

for i in range(0, int(xzones)):
   for j in range(0, int(yzones)):
      if (i, j) in zone:
         for b in zone[(i, j)]:
		b.printball();


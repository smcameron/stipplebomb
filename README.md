stipplebomb
===========

Stipplebomb renders a grayscale image in a stippling technique via an
interesting method.

The method is as follows:

A rectangular field is mapped to the image so that coordinates in the
lot correspond to coordinates in the image.

"Balls" are introduced into the field.  The radius of the balls is
proportional to the intensity of the image at the corresponding coordinate.
The balls are given some initial velocity, and there is some friction to
slow them down.  The balls also have a repulsive magnetic field which varies in strength that is again proportional to the radius of the ball
(and to the image intensity at the ball's corresponding image coordinate).
The force of this repulsive magnetic field diminishes with the square of
the distance (so very rapidly falls off.)

As the simulation is run, the forces on each ball due to the surrounding
balls are calculated, and the corresponding acceleration is applied to the
balls.

Perhaps surprisingly, the balls eventually settle down to form a stippled
rendering of the underlying image.

I cannot claim to have invented this algorithm, only to have implemented
a simple variant of it in ~200 lines of python.  I got the idea for it
from here: http://roberthodgin.com/stippling/  where you will find  a much
better and faster implementation with more features, done in C++ with the
cinder library.) 


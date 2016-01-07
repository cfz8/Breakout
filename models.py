# models.py
# Christina Zhao, cfz8
# 12/11/15
"""Models module for Breakout

This module contains the model classes for the Breakout game. That is anything that you
interact with on the screen is model: the paddle, the ball, and any of the bricks.

Technically, just because something is a model does not mean there has to be a special 
class for it.  Unless you need something special, both paddle and individual bricks could
just be instances of GRectangle.  However, we do need something special: collision 
detection.  That is why we have custom classes.

You are free to add new models to this module.  You may wish to do this when you add
new features to your game.  If you are unsure about whether to make a new class or 
not, please ask on Piazza."""
import random # To randomly generate the ball velocity
from constants import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything except the module constants.py.
# If you need extra information from Play, then it should be a parameter in your method, 
# and Play should pass it as a argument when it calls the method.

class Paddle(GRectangle):
    """An instance is the game paddle.
    
    This class contains a method to detect collision with the ball, as well as move it
    left and right.  You may wish to add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER TO CREATE A NEW PADDLE
    def __init__(self,x,y,width,height,linecolor,fillcolor):
        """Inititalizes the attributes inherited from GRectangle according to the arguments given by calling the initializer
        of the superclass GRectangle."""
        GRectangle.__init__(self,x=x,y=y,width=width,height=height,linecolor=linecolor,fillcolor=fillcolor)
        
    # METHODS TO MOVE THE PADDLE AND CHECK FOR COLLISIONS
    def collides(self,ball):
        """Returns: True if the ball collides with this paddle

        Parameter ball: The ball to check
        Precondition: ball is of class Ball"""
        if ball._vy > 0:
            return False
        if (self.x - 0.5*self.width)<=(ball.x - 0.5*ball.width)<=(self.x+0.5*self.width):
            if (self.y - 0.5*self.height)<=(ball.y - 0.5*ball.height)<=(self.y+0.5*self.height):
                return True
        if (self.x - 0.5*self.width)<=(ball.x + 0.5*ball.width)<=(self.x+0.5*self.width):
            if (self.y - 0.5*self.height)<=(ball.y - 0.5*ball.height)<=(self.y+0.5*self.height):
                return True
        return False      
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY

class Brick(GRectangle):
    """An instance is the game paddle.
    
    This class contains a method to detect collision with the ball.  You may wish to 
    add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER TO CREATE A BRICK
    def __init__(self,x,y,width,height,linecolor,fillcolor):
         """Inititalizes the attributes inherited from GRectangle according to the arguments given by calling the initializer
         of the superclass GRectangle."""
         GRectangle.__init__(self,x=x,y=y,width=width,height=height,linecolor=linecolor,fillcolor=fillcolor)
        
    # METHOD TO CHECK FOR COLLISION
    def collides(self,ball):
        """Returns: True if the ball collides with this paddle

        Paramter ball: The ball to check
        Precondition: ball is of class Ball"""
        if (self.x - 0.5*self.width)<=(ball.x - 0.5*ball.width)<=(self.x+0.5*self.width):
            if (self.y - 0.5*self.height)<=(ball.y - 0.5*ball.height)<=(self.y+0.5*self.height):
                return True
            if (self.y - 0.5*self.height)<=(ball.y + 0.5*ball.height)<=(self.y+0.5*self.height):
                return True
        if (self.x - 0.5*self.width)<=(ball.x + 0.5*ball.width)<=(self.x+0.5*self.width):
            if (self.y - 0.5*self.height)<=(ball.y - 0.5*ball.height)<=(self.y+0.5*self.height):
                return True
            if (self.y - 0.5*self.height)<=(ball.y + 0.5*ball.height)<=(self.y+0.5*self.height):
                return True
        return False
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY

class Ball(GEllipse):
    """Instance is a game ball.
    
    We extend GEllipse because a ball must have additional attributes for velocity.
    This class adds this attributes and manages them.
    
    INSTANCE ATTRIBUTES:
        _vx [int or float]: Velocity in x direction 
        _vy [int or float]: Velocity in y direction 
    
    The class Play will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with no
    setters for the velocities.
    
    How? The only time the ball can change velocities is if it hits an obstacle
    (paddle or brick) or if it hits a wall.  Why not just write methods for these
    instead of using setters?  This cuts down on the amount of code in Gameplay.
    
    NOTE: The ball does not have to be a GEllipse. It could be an instance
    of GImage (why?). This change is allowed, but you must modify the class
    header up above.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER TO SET RANDOM VELOCITY
    def __init__(self,x,y,width,height,fillcolor):
         """Inititalizes the attributes inherited from GRectangle according to the arguments given by calling the initializer
         of the superclass GRectangle."""
         GEllipse.__init__(self,x=x,y=y,width=width,height=height,fillcolor=fillcolor)
         self._vx = random.uniform(1.0,5.0)
         self._vx = self._vx*random.choice([-1,1])
         self._vy = -3.0
    
    # METHODS TO MOVE AND/OR BOUNCE THE BALL
    def step(self):
        """Moves the ball by adding _vx to x and _vy to y."""
        self.x += self._vx
        self.y += self._vy

    def bounce(self):
        """Detects if the ball hits the wall and if so, then it changes the velocity of the ball."""
        if self.contains(x=self.x,y=GAME_HEIGHT):
            self._vy = -self._vy
        if self.contains(x=GAME_WIDTH,y=self.y) or self.contains(x=0,y=self.y):
            self._vx = -self._vx
           
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY

# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
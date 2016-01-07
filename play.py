# play.py
# Christina Zhao, cfz8
# 12/11/15
"""Subcontroller module for Breakout

This module contains the subcontroller to manage a single game in the Breakout App. 
Instances of Play represent a single game.  If you want to restart a new game, you are 
expected to make a new instance of Play.

The subcontroller Play manages the paddle, ball, and bricks.  These are model objects.  
Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer."""
from constants import *
from game2d import *
from models import *


# PRIMARY RULE: Play can only access attributes in models.py via getters/setters
# Play is NOT allowed to access anything in breakout.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)

class Play(object):
    """An instance controls a single game of breakout.
    
    This subcontroller has a reference to the ball, paddle, and bricks. It animates the 
    ball, removing any bricks as necessary.  When the game is won, it stops animating.  
    You should create a NEW instance of Play (in Breakout) if you want to make a new game.
    
    If you want to pause the game, tell this controller to draw, but do not update.  See 
    subcontrollers.py from Lecture 25 for an example.
    
    INSTANCE ATTRIBUTES:
        _paddle [Paddle]: the paddle to play with 
        _bricks [list of Brick]: the list of bricks still remaining 
        _ball   [Ball, or None if waiting for a serve]:  the ball to animate
        _tries  [int >= 0]: the number of tries left 
    
    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Breakout. It is okay if you do, but you MAY NOT ACCESS 
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that 
    you need to access in Breakout.  Only add the getters and setters that you need for 
    Breakout.
    
    You may change any of the attributes above as you see fit. For example, you may want
    to add new objects on the screen (e.g power-ups).  If you make changes, please list
    the changes with the invariants.
                  
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    _score [int]: keeps track of score, int, >= 0
    _soundeffect [int]: if = 0, plays plate1.wav, if = 1, plays plate2.wav, int, either 0 or 1
    _sound [Sound]: an instance of Sound,sroucemust be a valid sound file
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getTries(self):
        """Returns the number of tries left."""
        return self._tries

    def setTries(self,n):
        """Sets _tries to n.

        Parameter n: number of tries
        Precondition: n is an integer, 0<=n<=3"""
        self._tries = n
        
    def getBricks(self):
        """"Returns the list _bricks."""
        return self._bricks

    def getScore(self):
        """Returns the current score."""
        return self._score

    def getVolume(self):
        """Returns the current volume of _sound."""
        return self._sound.volume

    def setVolume(self, v):
        """Sets the volume of _sound to v.

        Parameter v: the volume to set to
        Precondition: must be a float in the range 0..1"""
        self._sound.volume = v
    
    # INITIALIZER (standard form) TO CREATE PADDLES AND BRICKS
    def __init__(self):
        """Initializes the list _bricks, _paddle, _score, and _tries. Creates BRICK_ROWS rows and BRICKS_IN_ROW bricks in each row."""
        self._bricks = []
        k = 0
        while k < BRICK_ROWS:
            h = 0
            while h < BRICKS_IN_ROW:
                nexth = (BRICK_HEIGHT + BRICK_SEP_V)*k
                nextw = (BRICK_WIDTH + BRICK_SEP_H)*h + BRICK_SEP_H/2+ BRICK_WIDTH/2
                b = Brick(x=nextw,y=GAME_HEIGHT-BRICK_Y_OFFSET-nexth,width=BRICK_WIDTH,height=BRICK_HEIGHT,
                                  linecolor = BRICK_COLORS[k%len(BRICK_COLORS)],fillcolor=BRICK_COLORS[k%len(BRICK_COLORS)])
                if h == 0:
                    b.left = BRICK_SEP_H/2
                self._bricks.append(b)
                h = h+1
            k = k+1
        self._paddle = Paddle(x=GAME_WIDTH/2,y=PADDLE_OFFSET,width=PADDLE_WIDTH,height=PADDLE_HEIGHT,
                              linecolor = colormodel.BLACK, fillcolor = colormodel.BLACK)
        self._tries = 3
        self._score = 0
        self._soundeffects = 0
        self._sound = Sound('bounce.wav')
    #    self._sound.volume = 0.0
    
    # UPDATE METHODS TO MOVE PADDLE, SERVE AND MOVE THE BALL
    def updatePaddle(self,input):
        """Moves the paddle. If user wants to go left, subtracts step from x. If user wants to go right,
        adds step to x. Movement is only horizontal, not vertical.

        Parameter input: the user input, used to control the paddle
        Precondition: the input s an immutable instance of GInput"""
        if input.is_key_down('left'):
            self._paddle.x = max(PADDLE_WIDTH/2,self._paddle.x - PADDLE_STEP)
        if input.is_key_down('right'):
            self._paddle.x = min(GAME_WIDTH-PADDLE_WIDTH/2, self._paddle.x + PADDLE_STEP)

    def makeBall(self):
        """Creates the ball and initializes the _ball attribute."""
        self._ball = Ball(x=GAME_WIDTH/2,y=GAME_HEIGHT/2,width=BALL_DIAMETER,
                          height=BALL_DIAMETER,fillcolor=colormodel.BLACK)

    def updateBall(self):
        """Moves the ball according to step. Calls bounce to bounce the ball off the walls.
        Checks for collisions with the paddle and bricks, and if there is, negates the vertical
        direction of the ball. If a brick is hit, the brick is removed."""
        self._ball.step()
        self._ball.bounce()
        if self._paddle.collides(self._ball):
            if self._sound.volume == 0.0:
                self._sound = Sound('bounce.wav')
                self._sound.volume = 0.0
            if self._sound.volume == 1.0:
                self._sound.play()
            self._ball._vy = -self._ball._vy
        if self._ball._vy > 0:
            k = len(self._bricks) - 1
            while k >= 0:
                if self._bricks[k].collides(self._ball):
                    if self._sound.volume == 1:
                        self.playSound()
                    self._soundeffects = (self._soundeffects + 1)%2
                    self._ball._vy = -self._ball._vy
                    self._bricks.remove(self._bricks[k])
                    self._score += 1
                k = k-1
        elif self._ball._vy < 0:
            k = 0
            while k < len(self._bricks):
                if self._bricks[k].collides(self._ball):
                    if self._sound.volume == 1.0:
                        self.playSound()
                    self.playSound()
                    self._ball._vy = -self._ball._vy
                    self._bricks.remove(self._bricks[k])
                    self._score += 1
                k = k+1
                
    # DRAW METHOD TO DRAW THE PADDLES, BALL, AND BRICKS
    def drawPaddle(self,view):
        """Draw method to draw the paddle.

        Parameter view: the game view
        Precondition: view is an immutable instance of GView"""
        self._paddle.draw(view)

    def drawBall(self,view):
        """Draw method to draw the ball

        Parameter view: the game view
        Precondition: view is an immutable instance of GView"""
        self._ball.draw(view)

    def drawBricks(self,view):
        """Draw method to draw the bricks.

        Parameter view: the game view
        Precondition: view is an immutable instance of GView"""
        for b in self._bricks:
            b.draw(view)
   
    # HELPER METHODS FOR PHYSICS AND COLLISION DETECTION
    def loseBall(self):
        """Checks to see if the ball goes below the paddle, which means the
        ball goes off the screen and the ball is lost."""
        if self._ball.contains(x=self._ball.x,y=0):
            return True
        # ADD ANY ADDITIONAL METHODS (FULLY SPECIFIED) HERE
    def playSound(self):
        """Plays the sound effect (plate1 or plate2) whenever the ball hits a brick."""
        if self._soundeffects == 0:
            sound = Sound('plate1.wav')
            sound.play()
        elif self._soundeffects == 1:
            sound = Sound('plate2.wav')
            sound.play()


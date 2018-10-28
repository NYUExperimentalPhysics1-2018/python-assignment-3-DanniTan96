#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 19:18:02 2018

@author: Daniel E Tanagho
Recitation Instructor: Yiyang Wu
Python Assignment 3
"""
import numpy as np
import matplotlib.pyplot as plt

tank1Color = 'b'
tank2Color = 'r'
obstacleColor = 'k'
tank1box = [10,15,0,5]
tank2box = [90,95,0,5]
obstacleBox = [40,60,0,50]

##### functions you need to implement #####
def trajectory (x0, y0, v, theta, g = 9.8, npts = 1000): ### WORKS

    theta = np.deg2rad(theta)
    v0y = v*np.sin(theta)
    v0x = v*np.cos(theta)
    tfinal = (v0y/g) + np.sqrt(((v0y/g)**2)+(2*(y0/g)))
    t = np.linspace(0.0, tfinal, npts)
    y = y0 + v0y*t - (0.5*g*(t**2))
    x = x0 + v0x*t
    x, y = endTrajectoryAtIntersection(x, y, obstacleBox)

    plt.plot(x, y)
    plt.show()
    
    return x, y

def firstInBox (x,y,box): ### WORKS
    """
    finds first index of x,y inside box
    
    paramaters
    ----------
    x,y : np array type
        positions to check
    box : tuple
        (left,right,bottom,top)
    
    returns
    -------
    int
        the lowest j such that
        x[j] is in [left,right] and 
        y[j] is in [bottom,top]
        -1 if the line x,y does not go through the box
    """
    for j in range(0, len(x)):
        x[j]
        y[j]
        if x[j] >= box[0] and x[j] <= box[1] and y[j] >= box[2] and y[j] <= box[3]:
            return j
    return -1
        
def tankShot (targetBox, obstacleBox, x0, y0, v, theta, g = 9.8): ###WORKS
    """
    executes one tank shot
    
    parameters
    ----------
    targetBox : tuple
        (left,right,bottom,top) location of the target
    obstacleBox : tuple
        (left,right,bottom,top) location of the central obstacle
    x0,y0 :floats
        origin of the shot
    v : float
        velocity of the shot
    theta : float
        angle of the shot
    g : float 
        accel due to gravity (default 9.8)
    returns
    --------
    int
        code: 0 = miss, 1 = hit
        
    hit if trajectory intersects target box before intersecting
    obstacle box
    draws the truncated trajectory in current plot window
    """ 
    x,y = trajectory (x0, y0, v, theta, g = 9.8, npts = 1000)
    hit_obstacle = firstInBox(x, y, obstacleBox)
    hit_opponent = firstInBox(x, y, targetBox)
    if hit_obstacle == -1 and hit_opponent > -1:
        return 1
    else:
        return 0
        
def drawBoard (tank1box, tank2box, obstacleBox, playerNum): ### playerNum!!!
    """
    draws the game board, pre-shot
    parameters
    ----------
    tank1box : tuple
        (left,right,bottom,top) location of player1's tank
    tank2box : tuple
        (left,right,bottom,top) location of player1's tank
    obstacleBox : tuple
        (left,right,bottom,top) location of the central obstacle
    playerNum : int
        1 or 2 -- who's turn it is to shoot
 
    """    
    tank1box = drawBox(tank1box, tank1Color)
    tank2box = drawBox(tank2box, tank2Color)
    obstacleBox = drawBox(obstacleBox, obstacleColor)
    if playerNum == 1:
        plt.title('Player 1\'s Turn')
    else:
        plt.title('Player 2\'s Turn')
    showWindow() #this makes the figure window show up
    return tank1box, tank2box, obstacleBox, playerNum
    
def oneTurn (tank1box, tank2box, obstacleBox, playerNum, g = 9.8):   
    """
    parameters
    ----------
    tank1box : tuple
        (left,right,bottom,top) location of player1's tank
    tank2box : tuple
        (left,right,bottom,top) location of player1's tank
    obstacleBox : tuple
        (left,right,bottom,top) location of the central obstacle
    playerNum : int
        1 or 2 -- who's turn it is to shoot
     g : float 
        accel due to gravity (default 9.8)
    returns
    -------
    int
        code 0 = miss, 1 or 2 -- that player won
    
    clears figure
    draws tanks and obstacles as boxes
    prompts player for velocity and angle
    displays trajectory (shot originates from center of tank)
    returns 0 for miss, 1 or 2 for victory
    """        
    plt.clf()
    drawBoard(tank1box, tank2box, obstacleBox, playerNum)
    v = getNumberInput('Shot Velocity > ', validRange=[-np.Inf, np.Inf])
    theta = getNumberInput('Shot Angle > ', validRange=[-np.Inf, np.Inf])
    if playerNum == 1:
        x0 = tank1box[0]+(tank1box[1]-tank1box[0])/2
        y0 = tank1box[3]
        result = tankShot(tank2box, obstacleBox, x0, y0, v, theta, g=9.8)
    else:
        x0 = tank2box[0]+(tank2box[1]-tank2box[0])/2
        y0 = tank2box[3]
        result = tankShot(tank1box, obstacleBox, x0, y0, v, theta, g=9.8)
    trajectory(x0, y0, v, theta, g=9.8, npts=1000)
    
    return result
    
def playGame(tank1box, tank2box, obstacleBox, g = 9.8):
    """
    parameters
    ----------
    tank1box : tuple
        (left,right,bottom,top) location of player1's tank
    tank2box : tuple
        (left,right,bottom,top) location of player1's tank
    obstacleBox : tuple
        (left,right,bottom,top) location of the central obstacle
    playerNum : int
        1 or 2 -- who's turn it is to shoot
     g : float 
        accel due to gravity (default 9.8)
    """

    playerNum = getNumberInput('Who wants to start? Player 1 or 2? ', validRange=(1, 2))
    result = oneTurn(tank1box, tank2box, obstacleBox, playerNum, g=9.8)

    while True:       
        if result == 0:
            print('Missed :( ... Next Player\'s Turn')
            drawBoard (tank1box, tank2box, obstacleBox, playerNum)           
            playerNum = (3-playerNum)
            result = oneTurn(tank1box, tank2box, obstacleBox, playerNum, g=9.8)
        elif result == 1:
            print('Player ' + str(playerNum) + ' wins!')
            drawBoard (tank1box, tank2box, obstacleBox, playerNum) 
            break
             
##### functions provided to you #####
def getNumberInput (prompt, validRange = [-np.Inf, np.Inf]):
    """displays prompt and converts user input to a number
    
       in case of non-numeric input, re-prompts user for numeric input
       
       Parameters
       ----------
           prompt : str
               prompt displayed to user
           validRange : list, optional
               two element list of form [min, max]
               value entered must be in range [min, max] inclusive
        Returns
        -------
            float
                number entered by user
    """
    while True:
        try:
            num = float(input(prompt))
        except Exception:
            print ("Please enter a number")
        else:
            if (num >= validRange[0] and num <= validRange[1]):
                return num
            else:
                print ("Please enter a value in the range [", validRange[0], ",", validRange[1], "]") #Python 3 sytanx
            
    return num    

def showWindow():
    """
    shows the window -- call at end of drawBoard and tankShot
    """
    plt.draw()
    plt.pause(0.001)
    plt.show()


def drawBox(box, color):
    """
    draws a filled box in the current axis
    parameters
    ----------
    box : tuple
        (left,right,bottom,top) - extents of the box
    color : str
        color to fill the box with, e.g. 'b'
    """    
    x = (box[0], box[0], box[1], box[1])
    y = (box[2], box[3], box[3], box[2])
    ax = plt.gca()
    ax.fill(x,y, c = color)

def endTrajectoryAtIntersection (x,y,box):
    """
    portion of trajectory prior to first intersection with box
    
    paramaters
    ----------
    x,y : np array type
        position to check
    box : tuple
        (left,right,bottom,top)
    
    returns
    ----------
    (x,y) : tuple of np.array of floats
        equal to inputs if (x,y) does not intersect box
        otherwise returns the initial portion of the trajectory
        up until the point of intersection with the box
    """
    i = firstInBox(x,y,box)
    if (i < 0):
        return (x,y)
    return (x[0:i],y[0:i])


##### fmain -- edit box locations for new games #####
def main():
    playGame(tank1box, tank2box, obstacleBox, g=9.8)
    
#don't edit the lines below;
if __name__== "__main__":
    main()  
    
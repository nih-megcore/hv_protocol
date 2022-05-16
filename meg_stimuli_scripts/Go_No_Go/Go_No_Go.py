#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v3.0.0b10),
    on November 13, 2018, at 12:47
If you publish work using this script please cite the PsychoPy publications:
    Peirce, JW (2007) PsychoPy - Psychophysics software in Python.
        Journal of Neuroscience Methods, 162(1-2), 8-13.
    Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy.
        Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from __future__ import absolute_import, division
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding
from psychopy import parallel
from datetime import datetime

#send signals to the MEG
from psychopy import parallel
port = parallel.ParallelPort(address=0x0378)
port.setData(0)

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

def trigger(code):
    port.setData(code)
    core.wait(.025)
    port.setData(0)


# Store info about the experiment session
theDate = datetime.now()
expName = 'Go_No_Go'  # from the Builder filename that created this script
expInfo = {'participant': 'Geraldine', 'session': '001'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK:
    # Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    filename = "data/GoNoGo-s-" + expInfo['participant'] + "-r" + str(expInfo['session']) + "-" + theDate.strftime("%d%b%y")
else:
    core.quit()  # user pressed cancel
expInfo['date'] = theDate  # add a simple timestamp
expInfo['expName'] = expName

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    savePickle=False, saveWideText=False,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', filemode='w', level=logging.DATA)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(
    size=[1344, 768], fullscr=False, screen=0,
    allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=(-.1,-.1,-.1), colorSpace='rgb',
    blendMode='avg', useFBO=True)
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# initialize components for the upper left pixel

upperleft_black = visual.Rect(win,width=1,height=1,lineColor=(0,0,0),fillColor=(0,0,0),opacity=1,pos=(-512,384),units='pix')
upperleft_white = visual.Rect(win,width=1,height=1,lineColor=(1,0,0),fillColor=(1,0,0),opacity=1,pos=(-512,384),units='pix')

# Initialize components for Routine "Instructions"
InstructionsClock = core.Clock()
Timer = core.Clock()
logging.setDefaultClock(Timer)

white_screen = visual.Rect(
    win=win, name='white_screen',
    width=[(2000,2000)[0],(2000,2000)[1]][0], height=[(2000,2000)[0],(2000,2000)[1]][1],
    ori=0, pos=(0, 0),
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor='grey', fillColorSpace='rgb',
    opacity=1, depth=0.0, interpolate=True)
instructions = visual.TextStim(win=win, name='instructions',
    text="In this task, please respond to all the shapes without an X inside. Do not respond to shapes with an X inside them. Respond as quickly and accurately as possible" ,
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    #languageStyle='LTR',
    depth=-1.0);
Localize = visual.TextStim(
    win=win, name='Localize',
    text='Localizing head. Please hold still.',
    font='Arial',
    alignHoriz='center',
    pos=(0, 0), height=0.1, wrapWidth= 1.5, ori=0,
    color='black', colorSpace='rgb', opacity=1)
"""
# Initialize components for Routine "Fixation_Cross"
Fixation_CrossClock = core.Clock()
white_screen_cross = visual.Rect(
    win=win, name='white_screen_cross',
    width=[1000,1000][0], height=[1000,1000][1],
    ori=0, pos=(0, 0),
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb',
    opacity=1, depth=0.0, interpolate=True)
fixation_cross = visual.ShapeStim(
    win=win, name='fixation_cross', vertices='cross',
    size=(0.06, 0.12),
    ori=0, pos=(0, 0),
    lineWidth=.001, lineColor=[-1,-1,-1], lineColorSpace='rgb',
    fillColor=[-1,-1,-1], fillColorSpace='rgb',
    opacity=1, depth=-1.0, interpolate=True)
"""

# Initialize components for Routine "triangle_"
triangle_Clock = core.Clock()
white_screen2 = visual.Rect(
    win=win, name='white_screen2',
    width=[1000,1000][0], height=[1000,1000][1], vertices='cross',
    size=(0.06, 0.12),
    ori=0, pos=(0, 0),
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor='grey', fillColorSpace='rgb',
    opacity=1, depth=0.0, interpolate=True)
triangle = visual.ShapeStim(
    win=win, name='triangle',
    vertices=[[-(.5, .8)[0]/2.0,-(.5, .8)[1]/2.0], [+(.5, .8)[0]/2.0,-(.5, .8)[1]/2.0], [0,(.5, .8)[1]/2.0]],
    ori=0, pos=(0,.1),
    lineWidth=1, lineColor=[-1.000,-1.000,-1.000], lineColorSpace='rgb',
    fillColor=[-1.000,-1.000,-1.000], fillColorSpace='rgb',
    opacity=1, depth=-1.0, interpolate=True)

# Initialize components for Routine "Fixation_Cross"
Fixation_CrossClock = core.Clock()
white_screen_cross = visual.Rect(
    win=win, name='white_screen_cross',
    width=[1000,1000][0], height=[1000,1000][1],
    ori=0, pos=(0, 0),
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor='grey', fillColorSpace='rgb',
    opacity=1, depth=0.0, interpolate=True)
fixation_cross = visual.ShapeStim(
    win=win, name='fixation_cross', vertices='cross',
    size=(0.06, 0.12),
    ori=0, pos=(0, 0),
    lineWidth=.001, lineColor=[-1,-1,-1], lineColorSpace='rgb',
    fillColor=[-1,-1,-1], fillColorSpace='rgb',
    opacity=1, depth=-1.0, interpolate=True)

# Initialize components for Routine "triangleX_2"
triangleX_2Clock = core.Clock()
white_screen2_6 = visual.Rect(
    win=win, name='white_screen2_6',
    width=[1000,1000][0], height=[1000,1000][1],
    ori=0, pos=(0, 0),
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor='grey', fillColorSpace='rgb',
    opacity=1, depth=0.0, interpolate=True)
triangle_2 = visual.ShapeStim(
    win=win, name='triangle_2',
    vertices=[[-(.5, .8)[0]/2.0,-(.5, .8)[1]/2.0], [+(.5, .8)[0]/2.0,-(.5, .8)[1]/2.0], [0,(.5, .8)[1]/2.0]],
    ori=0, pos=(0,.1),
    lineWidth=1, lineColor=[-1.000,-1.000,-1.000], lineColorSpace='rgb',
    fillColor=[-1.000,-1.000,-1.000], fillColorSpace='rgb',
    opacity=1, depth=-1.0, interpolate=True)
line4 = visual.Line(
    win=win, name='line4',
    start=(-(.3,.3)[0]/2.0, 0), end=(+(.3,.3)[0]/2.0, 0),
    ori=60, pos=(0, 0),
    lineWidth=6, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb',
    opacity=1, depth=-2.0, interpolate=True)
line5 = visual.Line(
    win=win, name='line5',
    start=(-(.3,.3)[0]/2.0, 0), end=(+(.3,.3)[0]/2.0, 0),
    ori=-60, pos=(0, 0),
    lineWidth=6, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb',
    opacity=1, depth=-3.0, interpolate=True)


# Initialize components for Routine "pentagon"
pentagonClock = core.Clock()
white_screen2_3 = visual.Rect(
    win=win, name='white_screen2_3',
    width=[1000,1000][0], height=[1000,1000][1],
    ori=0, pos=(0, 0),
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor='grey', fillColorSpace='rgb',
    opacity=1, depth=0.0, interpolate=True)
pentagon_1 = visual.Polygon(
    win=win, name='pentagon_1',units='deg', 
    edges=5, size=(11,11),
    ori=0, pos=(0,0),
    lineWidth=1, lineColor=[-1.000,-1.000,-1.000], lineColorSpace='rgb',
    fillColor=[-1.000,-1.000,-1.000], fillColorSpace='rgb',
    opacity=1, depth=-1.0, interpolate=True)

# Initialize components for Routine "pentagon_X"
pentagon_XClock = core.Clock()
white_screen2_7 = visual.Rect(
    win=win, name='white_screen2_7',
    width=[1000,1000][0], height=[1000,1000][1],
    ori=0, pos=(0, 0),
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor='grey', fillColorSpace='rgb',
    opacity=1, depth=0.0, interpolate=True)
pentagon_2 = visual.Polygon(
    win=win, name='pentagon_2',units='deg', 
    edges=5, size=(11,11),
    ori=0, pos=(0,0),
    lineWidth=1, lineColor=[-1.000,-1.000,-1.000], lineColorSpace='rgb',
    fillColor=[-1.000,-1.000,-1.000], fillColorSpace='rgb',
    opacity=1, depth=-1.0, interpolate=True)
line8 = visual.Line(
    win=win, name='line8',
    start=(-(0.3, 0.3)[0]/2.0, 0), end=(+(0.3, 0.3)[0]/2.0, 0),
    ori=60, pos=(0, 0),
    lineWidth=6, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor='grey', fillColorSpace='rgb',
    opacity=1, depth=-2.0, interpolate=True)
line9 = visual.Line(
    win=win, name='line9',
    start=(-(0.3, 0.3)[0]/2.0, 0), end=(+(0.3, 0.3)[0]/2.0, 0),
    ori=-60, pos=(0, 0),
    lineWidth=6, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor='grey', fillColorSpace='rgb',
    opacity=1, depth=-3.0, interpolate=True)


# Initialize components for Routine "circle_2"
circle_2Clock = core.Clock()
white_screen3 = visual.Rect(
    win=win, name='white_screen3',
    width=[1000,1000][0], height=[1000,1000][1],
    ori=0, pos=(0, 0),
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor='grey', fillColorSpace='rgb',
    opacity=1, depth=0.0, interpolate=True)
circle_3 = visual.Polygon(
    win=win, name='circle_3',
    edges=100, size=(.48,.84),
    ori=0, pos=(0,0),
    lineWidth=1, lineColor=[-1.000,-1.000,-1.000], lineColorSpace='rgb',
    fillColor=[-1.000,-1.000,-1.000], fillColorSpace='rgb',
    opacity=1, depth=-1.0, interpolate=True)


# Initialize components for Routine "circle_X"
circle_XClock = core.Clock()
white_screen3_2 = visual.Rect(
    win=win, name='white_screen3_2',
    width=[1000,1000][0], height=[1000,1000][1],
    ori=0, pos=(0, 0),
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor='grey', fillColorSpace='rgb',
    opacity=1, depth=0.0, interpolate=True)
circle = visual.Polygon(
    win=win, name='circle',
    edges=100, size=(.48,.84),
    ori=0, pos=(0,0),
    lineWidth=1, lineColor=[-1.000,-1.000,-1.000], lineColorSpace='rgb',
    fillColor=[-1.000,-1.000,-1.000], fillColorSpace='rgb',
    opacity=1, depth=-1.0, interpolate=True)
line1 = visual.Line(
    win=win, name='line1',
    start=(-(0.3,0.3)[0]/2.0, 0), end=(+(0.3,0.3)[0]/2.0, 0),
    ori=60, pos=(0,0),
    lineWidth=6, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor='grey', fillColorSpace='rgb',
    opacity=1, depth=-2.0, interpolate=True)
line2 = visual.Line(
    win=win, name='line2',
    start=(-(0.3, 0.3)[0]/2.0, 0), end=(+(0.3, 0.3)[0]/2.0, 0),
    ori=-60, pos=(0,0),
    lineWidth=6, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb',
    opacity=1, depth=-3.0, interpolate=True)

# Initialize components for Routine "diamond"
diamondClock = core.Clock()
white_screen5 = visual.Rect(
    win=win, name='white_screen5',
    width=[1000,1000][0], height=[1000,1000][1],
    ori=0, pos=(0, 0),
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor='grey', fillColorSpace='rgb',
    opacity=1, depth=0.0, interpolate=True)
diamond_1 = visual.Rect(
    win=win, name='diamond_1',units='deg', 
    width=(8,8)[0], height=(8,8)[1],
    ori=45, pos=(0,0),
    lineWidth=1, lineColor=[-1.000,-1.000,-1.000], lineColorSpace='rgb',
    fillColor=[-1.000,-1.000,-1.000], fillColorSpace='rgb',
    opacity=1, depth=-1.0, interpolate=True)

# Initialize components for Routine "diamond_2"
diamond_2Clock = core.Clock()
white_screen2_5 = visual.Rect(
    win=win, name='white_screen2_5',
    width=[1000,1000][0], height=[1000,1000][1],
    ori=0, pos=(0, 0),
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor='grey', fillColorSpace='rgb',
    opacity=1, depth=0.0, interpolate=True)
hexagon_2 = visual.Rect(
    win=win, name='hexagon_2',units='deg', 
    width=(8,8)[0], height=(8,8)[1],
    ori=45, pos=(0,0),
    lineWidth=1, lineColor=[-1.000,-1.000,-1.000], lineColorSpace='rgb',
    fillColor=[-1.000,-1.000,-1.000], fillColorSpace='rgb',
    opacity=1, depth=-1.0, interpolate=True)
line10 = visual.Line(
    win=win, name='line10',
    start=(-(0.3,0.3)[0]/2.0, 0), end=(+(0.3,0.3)[0]/2.0, 0),
    ori=60, pos=(0,0),
    lineWidth=6, lineColor=[1.000,1.000,1.000], lineColorSpace='rgb',
    fillColor=[1.000,1.000,1.000], fillColorSpace='rgb',
    opacity=1, depth=-2.0, interpolate=True)
line11 = visual.Line(
    win=win, name='line11',
    start=(-(0.3,0.3)[0]/2.0, 0), end=(+(0.3,0.3)[0]/2.0, 0),
    ori=-60, pos=(0,0),
    lineWidth=6, lineColor=[1.000,1.000,1.000], lineColorSpace='rgb',
    fillColor=[1.000,1.000,1.000], fillColorSpace='rgb',
    opacity=1, depth=-3.0, interpolate=True)


# Initialize components for Routine "square_5"
square_5Clock = core.Clock()
white_screen5_2 = visual.Rect(
    win=win, name='white_screen5_2',
    width=[1000,1000][0], height=[1000,1000][1],
    ori=0, pos=(0, 0),
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor='grey', fillColorSpace='rgb',
    opacity=1, depth=0.0, interpolate=True)
diamond_3 = visual.Rect(
    win=win, name='diamond_3',units='deg', 
    width=(8,8)[0], height=(8,8)[1],
    ori=0, pos=(0,0),
    lineWidth=1, lineColor=[-1.000,-1.000,-1.000], lineColorSpace='rgb',
    fillColor=[-1.000,-1.000,-1.000], fillColorSpace='rgb',
    opacity=1, depth=-1.0, interpolate=True)



# Initialize components for Routine "square_6X"
square_6XClock = core.Clock()
white_screen2_8 = visual.Rect(
    win=win, name='white_screen2_8',
    width=[1000,1000][0], height=[1000,1000][1],
    ori=0, pos=(0, 0),
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor='grey', fillColorSpace='rgb',
    opacity=1, depth=0.0, interpolate=True)
hexagon = visual.Rect(
    win=win, name='hexagon',units='deg', 
    width=(8,8)[0], height=(8,8)[1],
    ori=0, pos=(0,0),
    lineWidth=1, lineColor=[-1.000,-1.000,-1.000], lineColorSpace='rgb',
    fillColor=[-1.000,-1.000,-1.000], fillColorSpace='rgb',
    opacity=1, depth=-1.0, interpolate=True)
line10_2 = visual.Line(
    win=win, name='line10_2',
    start=(-(0.3,0.3)[0]/2.0, 0), end=(+(0.3,0.3)[0]/2.0, 0),
    ori=60, pos=(0,0),
    lineWidth=6, lineColor=[1.000,1.000,1.000], lineColorSpace='rgb',
    fillColor=[1.000,1.000,1.000], fillColorSpace='rgb',
    opacity=1, depth=-2.0, interpolate=True)
line11_2 = visual.Line(
    win=win, name='line11_2',
    start=(-(0.3,0.3)[0]/2.0, 0), end=(+(0.3,0.3)[0]/2.0, 0),
    ori=-60, pos=(0,0),
    lineWidth=6, lineColor=[1.000,1.000,1.000], lineColorSpace='rgb',
    fillColor=[1.000,1.000,1.000], fillColorSpace='rgb',
    opacity=1, depth=-3.0, interpolate=True)



# ------Prepare to start Routine "Instructions"-------
t = 0
InstructionsClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
response_ready = event.BuilderKeyResponse()
# keep track of which components have finished
InstructionsComponents = [white_screen, instructions, response_ready]
for thisComponent in InstructionsComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "Instructions"-------
while continueRoutine:
    # get current time
    t = InstructionsClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *white_screen* updates
    if t >= 0.0 and white_screen.status == NOT_STARTED:
        # keep track of start time/frame for later
        white_screen.tStart = t
        white_screen.frameNStart = frameN  # exact frame index
        white_screen.setAutoDraw(True)
    
    # *instructions* updates
    if t >= 0.0 and instructions.status == NOT_STARTED:
        # keep track of start time/frame for later
        instructions.tStart = t
        instructions.frameNStart = frameN  # exact frame index
        instructions.setAutoDraw(True)
    
    # *response_ready* updates
    if t >= 0.0 and response_ready.status == NOT_STARTED:
        # keep track of start time/frame for later
        response_ready.tStart = t
        response_ready.frameNStart = frameN  # exact frame index
        response_ready.status = STARTED
        # keyboard checking is just starting
        event.clearEvents(eventType='keyboard')
    if response_ready.status == STARTED:
        theseKeys = event.getKeys(keyList=['y', 'n', 'left', 'right', 'space'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in InstructionsComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "Instructions"-------
for thisComponent in InstructionsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "Instructions" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()
logging.flush()

# ------Prepare to start Routine "Localize"-------
frameN = -1
continueRoutine = True
# update component parameters for each repeat
key_resp_2 = event.BuilderKeyResponse()
# keep track of which components have finished
Localize_Components = [white_screen, Localize, key_resp_2]
for thisComponent in Localize_Components:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# -------Start Routine "Localize"-------
while continueRoutine:
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    if white_screen.status == NOT_STARTED:
        # keep track of start time/frame for later
        white_screen.tStart = t
        white_screen.frameNStart = frameN  # exact frame index
        white_screen.setAutoDraw(True)
        Localize.setAutoDraw(True)
    if key_resp_2.status == NOT_STARTED:
        key_resp_2.tStart = t
        key_resp_2.frameNStart = frameN  # exact frame index
        key_resp_2.status = STARTED
        # keyboard checking is just starting
    if key_resp_2.status == STARTED:
        theseKeys = event.getKeys(keyList=['space', 'up'])
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            Localize.setAutoDraw(False)
            continueRoutine = False
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()
routineTimer.reset()

fixation_time = 1
# ------Prepare to start Routine "Fixation_Cross"-------
def fixation_start ():
    global endExpNow
    t = 0
    Fixation_CrossClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(fixation_time)
    # update component parameters for each repeat
    fixation_cross_response = event.BuilderKeyResponse()
    # keep track of which components have finished
    Fixation_CrossComponents = [white_screen_cross, fixation_cross, upperleft_black, fixation_cross_response]
    for thisComponent in Fixation_CrossComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "Fixation_Cross"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = fixation_time
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        upperleft_black.draw()
        
        # *white_screen_cross* updates
        if t >= 0.0 and white_screen_cross.status == NOT_STARTED:
            # keep track of start time/frame for later
            white_screen_cross.tStart = t
            white_screen_cross.frameNStart = frameN  # exact frame index
            white_screen_cross.setAutoDraw(True)
            upperleft_black.setAutoDraw(True)
        frameRemains = 0.0 + fixation_time- win.monitorFramePeriod * 0.75  # most of one frame period left
        if white_screen_cross.status == STARTED and t >= frameRemains:
            white_screen_cross.setAutoDraw(False)
            upperleft_black.setAutoDraw(False)
        
        # *fixation_cross* updates
        if t >= 0.0 and fixation_cross.status == NOT_STARTED:
            # keep track of start time/frame for later
            fixation_cross.tStart = t
            fixation_cross.frameNStart = frameN  # exact frame index
            fixation_cross.setAutoDraw(True)
        frameRemains = 0.0 + fixation_time- win.monitorFramePeriod * 0.75  # most of one frame period left
        if fixation_cross.status == STARTED and t >= frameRemains:
            fixation_cross.setAutoDraw(False)
        
        # *fixation_cross_response* updates
        if t >= 0.0 and fixation_cross_response.status == NOT_STARTED:
            # keep track of start time/frame for later
            fixation_cross_response.tStart = t
            fixation_cross_response.frameNStart = frameN  # exact frame index
            fixation_cross_response.status = STARTED
            # keyboard checking is just starting
            win.logOnFlip(level=logging.DATA, msg='fixation')
            win.callOnFlip(fixation_cross_response.clock.reset)  # t=0 on next screen flip
        frameRemains = 0.0 + fixation_time- win.monitorFramePeriod * 0.75  # most of one frame period left
        if fixation_cross_response.status == STARTED and t >= frameRemains:
            fixation_cross_response.status = STOPPED
        if fixation_cross_response.status == STARTED:
            theseKeys = event.getKeys(keyList=['y', 'n', 'left', 'right', 'space'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                fixation_cross_response.keys.extend(theseKeys)  # storing all keys
                fixation_cross_response.rt.append(fixation_cross_response.clock.getTime())
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Fixation_CrossComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "Fixation_Cross"-------
    for thisComponent in Fixation_CrossComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if fixation_cross_response.keys in ['', [], None]:  # No response was made
        fixation_cross_response.keys=None
    thisExp.addData('fixation_cross_response.keys',fixation_cross_response.keys)
    if fixation_cross_response.keys != None:  # we had a response
        thisExp.addData('fixation_cross_response.rt', fixation_cross_response.rt)
    thisExp.nextEntry()

# ------Prepare to start Routine "triangle_"-------
def triangle1 (): 
    global endExpNow
    t = 0
    triangle_Clock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(0.200000)
    # update component parameters for each repeat
    triangle_response = event.BuilderKeyResponse()
    # keep track of which components have finished
    triangle_Components = [white_screen2, triangle, upperleft_white, triangle_response]
    for thisComponent in triangle_Components:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # -------Start Routine "triangle_"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = triangle_Clock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *white_screen2* updates
        if t >= 0 and white_screen2.status == NOT_STARTED:
            # keep track of start time/frame for later
            white_screen2.tStart = t
            white_screen2.frameNStart = frameN  # exact frame index
            white_screen2.setAutoDraw(True)
            upperleft_white.setAutoDraw(True)
        frameRemains = .2 - win.monitorFramePeriod * 0.75 - .025  # frameRemans - 0.025 for trigger
        if white_screen2.status == STARTED and t >= frameRemains: 
            white_screen2.setAutoDraw(False)
            upperleft_white.setAutoDraw(False)
        # *triangle* updates
        if t >= 0.0 and triangle.status == NOT_STARTED:
            # keep track of start time/frame for later
            triangle.tStart = t
            triangle.frameNStart = frameN  # exact frame index
            triangle.setAutoDraw(True)
        frameRemains = .2 - win.monitorFramePeriod * 0.75 - .025 # frameRemans - 0.025 for trigger
        if triangle.status == STARTED and t >= frameRemains:
            triangle.setAutoDraw(False)
        
        # *triangle_response* updates
        if t >= 0.0 and triangle_response.status == NOT_STARTED:
            # keep track of start time/frame for later
            triangle_response.tStart = t
            triangle_response.frameNStart = frameN  # exact frame index
            triangle_response.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(triangle_response.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(trigger, code=1)
            win.logOnFlip(level=logging.DATA, msg='triangle')
        frameRemains = 0.0 + .2- win.monitorFramePeriod * 0.75 - 0.025  # frameRemains - 0.025 for trigger
        if triangle_response.status == STARTED and t >= frameRemains:
            triangle_response.status = STOPPED
        if triangle_response.status == STARTED:
            theseKeys = event.getKeys(keyList=['y', 'n', 'left', 'right', 'space'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                triangle_response.keys.extend(theseKeys)  # storing all keys
                triangle_response.rt.append(triangle_response.clock.getTime())
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in triangle_Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "triangle_"-------
    for thisComponent in triangle_Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if triangle_response.keys in ['', [], None]:  # No response was made
        triangle_response.keys=None
    thisExp.addData('triangle_response.keys',triangle_response.keys)
    if triangle_response.keys != None:  # we had a response
        thisExp.addData('triangle_response.rt', triangle_response.rt)
    thisExp.nextEntry()

def fixationcross(): 
    global endExpNow
        # ------Prepare to start Routine "Fixation_Cross"-------
    t = 0
    Fixation_CrossClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(fixation_time)
    upperleft_black.draw()
    # update component parameters for each repeat
    fixation_cross_response = event.BuilderKeyResponse()
    # keep track of which components have finished
    Fixation_CrossComponents = [white_screen_cross, fixation_cross, upperleft_black, fixation_cross_response]
    for thisComponent in Fixation_CrossComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "Fixation_Cross"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = Fixation_CrossClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
       
        # *white_screen_cross* updates
        if t >= 0.0 and white_screen_cross.status == NOT_STARTED:
            # keep track of start time/frame for later
            white_screen_cross.tStart = t
            white_screen_cross.frameNStart = frameN  # exact frame index
            white_screen_cross.setAutoDraw(True)
            upperleft_black.setAutoDraw(True)
        if t >= fixation_time:
            frameRemains = 0.0 + fixation_time - win.monitorFramePeriod * 0.75 - 0.025  # frameRemains - 0.025 for trigger
            if white_screen_cross.status == STARTED and t >= frameRemains:
                white_screen_cross.setAutoDraw(False)
                upperleft_black.setAutoDraw(False)

        # *fixation_cross* updates
        if t >= 0.0 and fixation_cross.status == NOT_STARTED:
            # keep track of start time/frame for later
            fixation_cross.tStart = t
            fixation_cross.frameNStart = frameN  # exact frame index
            fixation_cross.setAutoDraw(True)
        
        frameRemains = 0.0 + fixation_time- win.monitorFramePeriod * 0.75 - 0.025  # frameRemains - 0.025 for trigger
        if fixation_cross.status == STARTED and t >= frameRemains:
            fixation_cross.setAutoDraw(False)
        
        # *fixation_cross_response* updates
        if t >= 0.0 and fixation_cross_response.status == NOT_STARTED:
            # keep track of start time/frame for later
            fixation_cross_response.tStart = t
            fixation_cross_response.frameNStart = frameN  # exact frame index
            fixation_cross_response.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(fixation_cross_response.clock.reset)  # t=0 on next screen flip
        frameRemains = 0.0 + fixation_time- win.monitorFramePeriod * 0.75 - 0.025  # frameRemains - 0.025 for trigger
        if fixation_cross_response.status == STARTED and t >= frameRemains:
            fixation_cross_response.status = STOPPED
            
        if fixation_cross_response.status == STARTED:
            theseKeys = event.getKeys(keyList=['y', 'n', 'left', 'right', 'space'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                fixation_cross_response.keys.extend(theseKeys)  # storing all keys
                fixation_cross_response.rt.append(fixation_cross_response.clock.getTime())
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Fixation_CrossComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "Fixation_Cross"-------
    for thisComponent in Fixation_CrossComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if fixation_cross_response.keys in ['', [], None]:  # No response was made
        fixation_cross_response.keys=None
    thisExp.addData('fixation_cross_response.keys',fixation_cross_response.keys)
    if fixation_cross_response.keys != None:  # we had a response
        thisExp.addData('fixation_cross_response.rt', fixation_cross_response.rt)
    thisExp.nextEntry()

# ------Prepare to start Routine "triangleX_2"-------
def triangle_X ():
    global endExpNow
    t = 0
    triangleX_2Clock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(0.200000)
    # update component parameters for each repeat
    triangle_X_response = event.BuilderKeyResponse()
    upperleft_white.draw()
    # keep track of which components have finished
    triangleX_2Components = [white_screen2_6, triangle_2, upperleft_white, line4, line5, triangle_X_response]
    for thisComponent in triangleX_2Components:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "triangleX_2"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = triangleX_2Clock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *white_screen2_6* updates
        if t >= 0 and white_screen2_6.status == NOT_STARTED:
            # keep track of start time/frame for later
            white_screen2_6.tStart = t
            white_screen2_6.frameNStart = frameN  # exact frame index
            white_screen2_6.setAutoDraw(True)
            upperleft_white.setAutoDraw(True)
        frameRemains = .2 - win.monitorFramePeriod * 0.75 - .025 # frameRemans - 0.025 for trigger
        if white_screen2_6.status == STARTED and t >= frameRemains:
            white_screen2_6.setAutoDraw(False)
            upperleft_white.setAutoDraw(False)
       
        # *triangle_2* updates
        if t >= 0.0 and triangle_2.status == NOT_STARTED:
            # keep track of start time/frame for later
            triangle_2.tStart = t
            triangle_2.frameNStart = frameN  # exact frame index
            triangle_2.setAutoDraw(True)
        frameRemains = .2 - win.monitorFramePeriod * 0.75 - .025 # frameRemans - 0.025 for trigger
        if triangle_2.status == STARTED and t >= frameRemains:
            triangle_2.setAutoDraw(False)
        
        # *line4* updates
        if t >= 0.0 and line4.status == NOT_STARTED:
            # keep track of start time/frame for later
            line4.tStart = t
            line4.frameNStart = frameN  # exact frame index
            line4.setAutoDraw(True)
        frameRemains = .2 - win.monitorFramePeriod * 0.75 - .025 # frameRemans - 0.025 for trigger
        if line4.status == STARTED and t >= frameRemains:
            line4.setAutoDraw(False)
        
        # *line5* updates
        if t >= 0.0 and line5.status == NOT_STARTED:
            # keep track of start time/frame for later
            line5.tStart = t
            line5.frameNStart = frameN  # exact frame index
            line5.setAutoDraw(True)
        frameRemains = 0.0 + .2- win.monitorFramePeriod * 0.75 - 0.025  # frameRemains - 0.025 for trigger
        if line5.status == STARTED and t >= frameRemains:
            line5.setAutoDraw(False)
        
        # *triangle_X_response* updates
        if t >= 0.0 and triangle_X_response.status == NOT_STARTED:
            # keep track of start time/frame for later
            triangle_X_response.tStart = t
            triangle_X_response.frameNStart = frameN  # exact frame index
            triangle_X_response.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(triangle_X_response.clock.reset)  # t=0 on next screen flip
            win.logOnFlip(level=logging.DATA, msg='triangle_x')
            win.callOnFlip(trigger, code=2)
        frameRemains = 0.0 + .2- win.monitorFramePeriod * 0.75 - 0.025  # frameRemains - 0.025 for trigger
        if triangle_X_response.status == STARTED and t >= frameRemains:
            triangle_X_response.status = STOPPED
        if triangle_X_response.status == STARTED:
            theseKeys = event.getKeys(keyList=['y', 'n', 'left', 'right', 'space'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                triangle_X_response.keys.extend(theseKeys)  # storing all keys
                triangle_X_response.rt.append(triangle_X_response.clock.getTime())
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in triangleX_2Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "triangleX_2"-------
    for thisComponent in triangleX_2Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if triangle_X_response.keys in ['', [], None]:  # No response was made
        triangle_X_response.keys=None
    thisExp.addData('triangle_X_response.keys',triangle_X_response.keys)
    if triangle_X_response.keys != None:  # we had a response
        thisExp.addData('triangle_X_response.rt', triangle_X_response.rt)
    thisExp.nextEntry()

# ------Prepare to start Routine "pentagon"-------
def pentagon ():
    global endExpNow
    t = 0
    pentagonClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(0.200000)
    # update component parameters for each repeat
    pentagon_response = event.BuilderKeyResponse()
    upperleft_white.draw()
    # keep track of which components have finished
    pentagonComponents = [white_screen2_3, pentagon_1, upperleft_white, pentagon_response]
    for thisComponent in pentagonComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "pentagon"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = pentagonClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *white_screen2_3* updates
        if t >= 0 and white_screen2_3.status == NOT_STARTED:
            # keep track of start time/frame for later
            white_screen2_3.tStart = t
            white_screen2_3.frameNStart = frameN  # exact frame index
            white_screen2_3.setAutoDraw(True)
            upperleft_white.setAutoDraw(True)
        frameRemains = .2 - win.monitorFramePeriod * 0.75 - 0.025  # frameRemains - 0.025 for trigger
        if white_screen2_3.status == STARTED and t >= frameRemains:
            white_screen2_3.setAutoDraw(False)
            upperleft_white.setAutoDraw(False)
        
        # *pentagon_1* updates
        if t >= 0.0 and pentagon_1.status == NOT_STARTED:
            # keep track of start time/frame for later
            pentagon_1.tStart = t
            pentagon_1.frameNStart = frameN  # exact frame index
            pentagon_1.setAutoDraw(True)
        frameRemains = .2 - win.monitorFramePeriod * 0.75 - 0.025  # frameRemains - 0.025 for trigger
        if pentagon_1.status == STARTED and t >= frameRemains:
            pentagon_1.setAutoDraw(False)
        
        # *pentagon_response* updates
        if t >= 0.0 and pentagon_response.status == NOT_STARTED:
            # keep track of start time/frame for later
            pentagon_response.tStart = t
            pentagon_response.frameNStart = frameN  # exact frame index
            pentagon_response.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(pentagon_response.clock.reset)  # t=0 on next screen flip
            win.logOnFlip(level=logging.DATA, msg='pentagon')
            win.callOnFlip(trigger, code=1)
        frameRemains = 0.0 + .2- win.monitorFramePeriod * 0.75 - 0.025  # frameRemains - 0.025 for trigger
        if pentagon_response.status == STARTED and t >= frameRemains:
            pentagon_response.status = STOPPED
        if pentagon_response.status == STARTED:
            theseKeys = event.getKeys(keyList=['y', 'n', 'left', 'right', 'space'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                pentagon_response.keys.extend(theseKeys)  # storing all keys
                pentagon_response.rt.append(pentagon_response.clock.getTime())
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in pentagonComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "pentagon"-------
    for thisComponent in pentagonComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if pentagon_response.keys in ['', [], None]:  # No response was made
        pentagon_response.keys=None
    thisExp.addData('pentagon_response.keys',pentagon_response.keys)
    if pentagon_response.keys != None:  # we had a response
        thisExp.addData('pentagon_response.rt', pentagon_response.rt)
    thisExp.nextEntry()

# ------Prepare to start Routine "pentagon_X"-------
def pentagon_X (): 
    global endExpNow
    t = 0
    pentagon_XClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(0.200000)
    # update component parameters for each repeat
    pentagon_X_response = event.BuilderKeyResponse()
    upperleft_white.draw()
    # keep track of which components have finished
    pentagon_XComponents = [white_screen2_7, pentagon_2, upperleft_white, line8, line9, pentagon_X_response]
    for thisComponent in pentagon_XComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "pentagon_X"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = pentagon_XClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *white_screen2_7* updates
        if t >= 0 and white_screen2_7.status == NOT_STARTED:
            # keep track of start time/frame for later
            white_screen2_7.tStart = t
            white_screen2_7.frameNStart = frameN  # exact frame index
            white_screen2_7.setAutoDraw(True)
            upperleft_white.setAutoDraw(True)
        frameRemains = .2 - win.monitorFramePeriod * 0.75 - 0.025  # frameRemains - 0.025 for trigger
        if white_screen2_7.status == STARTED and t >= frameRemains:
            white_screen2_7.setAutoDraw(False)
            upperleft_white.setAutoDraw(False)
        
        # *pentagon_2* updates
        if t >= 0.0 and pentagon_2.status == NOT_STARTED:
            # keep track of start time/frame for later
            pentagon_2.tStart = t
            pentagon_2.frameNStart = frameN  # exact frame index
            pentagon_2.setAutoDraw(True)
        frameRemains = .2 - win.monitorFramePeriod * 0.75 - 0.025  # frameRemains - 0.025 for trigger
        if pentagon_2.status == STARTED and t >= frameRemains:
            pentagon_2.setAutoDraw(False)
        
        # *line8* updates
        if t >= 0.0 and line8.status == NOT_STARTED:
            # keep track of start time/frame for later
            line8.tStart = t
            line8.frameNStart = frameN  # exact frame index
            line8.setAutoDraw(True)
        frameRemains = 0.0 + .2- win.monitorFramePeriod * 0.75 - 0.025  # frameRemains - 0.025 for trigger
        if line8.status == STARTED and t >= frameRemains:
            line8.setAutoDraw(False)
        
        # *line9* updates
        if t >= 0.0 and line9.status == NOT_STARTED:
            # keep track of start time/frame for later
            line9.tStart = t
            line9.frameNStart = frameN  # exact frame index
            line9.setAutoDraw(True)
        frameRemains = 0.0 + .2- win.monitorFramePeriod * 0.75 - 0.025  # frameRemains - 0.025 for trigger
        if line9.status == STARTED and t >= frameRemains:
            line9.setAutoDraw(False)
        
        # *pentagon_X_response* updates
        if t >= 0.0 and pentagon_X_response.status == NOT_STARTED:
            # keep track of start time/frame for later
            pentagon_X_response.tStart = t
            pentagon_X_response.frameNStart = frameN  # exact frame index
            pentagon_X_response.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(pentagon_X_response.clock.reset)  # t=0 on next screen flip
            win.logOnFlip(level=logging.DATA, msg='pentagon_x')
            win.callOnFlip(trigger, code=2)
        frameRemains = 0.0 + .2- win.monitorFramePeriod * 0.75 - 0.025  # frameRemains - 0.025 for trigger
        if pentagon_X_response.status == STARTED and t >= frameRemains:
            pentagon_X_response.status = STOPPED
        if pentagon_X_response.status == STARTED:
            theseKeys = event.getKeys(keyList=['y', 'n', 'left', 'right', 'space'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                pentagon_X_response.keys.extend(theseKeys)  # storing all keys
                pentagon_X_response.rt.append(pentagon_X_response.clock.getTime())
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in pentagon_XComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "pentagon_X"-------
    for thisComponent in pentagon_XComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if pentagon_X_response.keys in ['', [], None]:  # No response was made
        pentagon_X_response.keys=None
    thisExp.addData('pentagon_X_response.keys',pentagon_X_response.keys)
    if pentagon_X_response.keys != None:  # we had a response
        thisExp.addData('pentagon_X_response.rt', pentagon_X_response.rt)
    thisExp.nextEntry()
    # ------Prepare to start Routine "Fixation_Cross"------
    t = 0
    Fixation_CrossClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(0.500000)
    # update component parameters for each repeat
    fixation_cross_response = event.BuilderKeyResponse()
    # keep track of which components have finished
    Fixation_CrossComponents = [white_screen_cross, upperleft_black, fixation_cross, fixation_cross_response]
    for thisComponent in Fixation_CrossComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

# ------Prepare to start Routine "circle_2"-------
def circle1 ():
    global endExpNow
    t = 0
    circle_2Clock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(0.200000)
    # update component parameters for each repeat
    circle_response = event.BuilderKeyResponse()
    # keep track of which components have finished
    circle_2Components = [white_screen3, upperleft_white,circle_3, circle_response]
    for thisComponent in circle_2Components:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "circle_2"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = circle_2Clock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *white_screen3* updates
        if t >= 0.0 and white_screen3.status == NOT_STARTED:
            # keep track of start time/frame for later
            white_screen3.tStart = t
            white_screen3.frameNStart = frameN  # exact frame index
            white_screen3.setAutoDraw(True)
            upperleft_white.setAutoDraw(True)
        frameRemains = .2 - win.monitorFramePeriod * 0.75 - 0.025  # frameRemains - 0.025 for trigger
        if white_screen3.status == STARTED and t >= frameRemains:
            white_screen3.setAutoDraw(False)
            upperleft_white.setAutoDraw(False)
        
        # *circle_3* updates
        if t >= 0.0 and circle_3.status == NOT_STARTED:
            # keep track of start time/frame for later
            circle_3.tStart = t
            circle_3.frameNStart = frameN  # exact frame index
            circle_3.setAutoDraw(True)
        frameRemains = .2 - win.monitorFramePeriod * 0.75 - 0.025  # frameRemains - 0.025 for trigger
        if circle_3.status == STARTED and t >= frameRemains:
            circle_3.setAutoDraw(False)
        
        # *circle_response* updates
        if t >= 0.0 and circle_response.status == NOT_STARTED:
            # keep track of start time/frame for later
            circle_response.tStart = t
            circle_response.frameNStart = frameN  # exact frame index
            circle_response.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(circle_response.clock.reset)  # t=0 on next screen flip
            win.logOnFlip(level=logging.DATA, msg='circle')
            win.callOnFlip(trigger, code=1)
        frameRemains = 0.0 + .2- win.monitorFramePeriod * 0.75 - 0.025  # frameRemains - 0.025 for trigger
        if circle_response.status == STARTED and t >= frameRemains:
            circle_response.status = STOPPED
        if circle_response.status == STARTED:
            theseKeys = event.getKeys(keyList=['y', 'n', 'left', 'right', 'space'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                circle_response.keys.extend(theseKeys)  # storing all keys
                circle_response.rt.append(circle_response.clock.getTime())
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in circle_2Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "circle_2"-------
    for thisComponent in circle_2Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if circle_response.keys in ['', [], None]:  # No response was made
        circle_response.keys=None
    thisExp.addData('circle_response.keys',circle_response.keys)
    if circle_response.keys != None:  # we had a response
        thisExp.addData('circle_response.rt', circle_response.rt)
    thisExp.nextEntry()

# ------Prepare to start Routine "circle_X"-------
def circle_X ():
    global endExpNow
    t = 0
    circle_XClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(0.200000)
    # update component parameters for each repeat
    circle_X_response = event.BuilderKeyResponse()
    upperleft_white.draw()
    # keep track of which components have finished
    circle_XComponents = [white_screen3_2, circle, upperleft_white,line1, line2, circle_X_response]
    for thisComponent in circle_XComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "circle_X"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = circle_XClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *white_screen3_2* updates
        if t >= 0.0 and white_screen3_2.status == NOT_STARTED:
            # keep track of start time/frame for later
            white_screen3_2.tStart = t
            white_screen3_2.frameNStart = frameN  # exact frame index
            white_screen3_2.setAutoDraw(True)
            upperleft_white.setAutoDraw(True)
        frameRemains = .2 - win.monitorFramePeriod * 0.75 - 0.025  # frameRemains - 0.025 for trigger
        if white_screen3_2.status == STARTED and t >= frameRemains:
            white_screen3_2.setAutoDraw(False)
            upperleft_white.setAutoDraw(False)
        
        # *circle* updates
        if t >= 0.0 and circle.status == NOT_STARTED:
            # keep track of start time/frame for later
            circle.tStart = t
            circle.frameNStart = frameN  # exact frame index
            circle.setAutoDraw(True)
        frameRemains = .2 - win.monitorFramePeriod * 0.75 - 0.025  # frameRemains - 0.025 for trigger
        if circle.status == STARTED and t >= frameRemains:
            circle.setAutoDraw(False)
        
        # *line1* updates
        if t >= 0.0 and line1.status == NOT_STARTED:
            # keep track of start time/frame for later
            line1.tStart = t
            line1.frameNStart = frameN  # exact frame index
            line1.setAutoDraw(True)
        frameRemains = .2 - win.monitorFramePeriod * 0.75 - 0.025  # frameRemains - 0.025 for trigger
        if line1.status == STARTED and t >= frameRemains:
            line1.setAutoDraw(False)
        
        # *line2* updates
        if t >= 0.0 and line2.status == NOT_STARTED:
            # keep track of start time/frame for later
            line2.tStart = t
            line2.frameNStart = frameN  # exact frame index
            line2.setAutoDraw(True)
        frameRemains = .2 - win.monitorFramePeriod * 0.75 - 0.025  # frameRemains - 0.025 for trigger
        if line2.status == STARTED and t >= frameRemains:
            line2.setAutoDraw(False)
        
        # *circle_X_response* updates
        if t >= 0.0 and circle_X_response.status == NOT_STARTED:
            # keep track of start time/frame for later
            circle_X_response.tStart = t
            circle_X_response.frameNStart = frameN  # exact frame index
            circle_X_response.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(circle_X_response.clock.reset)  # t=0 on next screen flip
            win.logOnFlip(level=logging.DATA, msg='circle_x')
            win.callOnFlip(trigger, code=2)
        frameRemains = 0.0 + .2- win.monitorFramePeriod * 0.75 - 0.025  # frameRemains - 0.025 for trigger
        if circle_X_response.status == STARTED and t >= frameRemains:
            circle_X_response.status = STOPPED
        if circle_X_response.status == STARTED:
            theseKeys = event.getKeys(keyList=['y', 'n', 'left', 'right', 'space'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                circle_X_response.keys.extend(theseKeys)  # storing all keys
                circle_X_response.rt.append(circle_X_response.clock.getTime())
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in circle_XComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "circle_X"-------
    for thisComponent in circle_XComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if circle_X_response.keys in ['', [], None]:  # No response was made
        circle_X_response.keys=None
    thisExp.addData('circle_X_response.keys',circle_X_response.keys)
    if circle_X_response.keys != None:  # we had a response
        thisExp.addData('circle_X_response.rt', circle_X_response.rt)
    thisExp.nextEntry()

# ------Prepare to start Routine "diamond"-------
def diamond ():
    global endExpNow
    t = 0
    diamondClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(0.200000)
    # update component parameters for each repeat
    diamond_response = event.BuilderKeyResponse()
    upperleft_white.draw()
    # keep track of which components have finished
    diamondComponents = [white_screen5, diamond_1, upperleft_white, diamond_response]
    for thisComponent in diamondComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "diamond"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = diamondClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *white_screen5* updates
        if t >= 0.0 and white_screen5.status == NOT_STARTED:
            # keep track of start time/frame for later
            white_screen5.tStart = t
            white_screen5.frameNStart = frameN  # exact frame index
            white_screen5.setAutoDraw(True)
            upperleft_white.setAutoDraw(True)
        frameRemains = 0.0 + .2- win.monitorFramePeriod * 0.75 - 0.025  # frameRemains - 0.025 for trigger
        if white_screen5.status == STARTED and t >= frameRemains:
            white_screen5.setAutoDraw(False)
            upperleft_white.setAutoDraw(False)
        
        # *diamond_1* updates
        if t >= 0.0 and diamond_1.status == NOT_STARTED:
            # keep track of start time/frame for later
            diamond_1.tStart = t
            diamond_1.frameNStart = frameN  # exact frame index
            diamond_1.setAutoDraw(True)
        frameRemains = .2 - win.monitorFramePeriod * 0.75 - 0.025  # frameRemains - 0.025 for trigger
        if diamond_1.status == STARTED and t >= frameRemains:
            diamond_1.setAutoDraw(False)
        
        # *diamond_response* updates
        if t >= 0.0 and diamond_response.status == NOT_STARTED:
            # keep track of start time/frame for later
            diamond_response.tStart = t
            diamond_response.frameNStart = frameN  # exact frame index
            diamond_response.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(diamond_response.clock.reset)  # t=0 on next screen flip
            win.logOnFlip(level=logging.DATA, msg='diamond')
            win.callOnFlip(trigger, code=1)
        frameRemains = 0.0 + .2- win.monitorFramePeriod * 0.75 - 0.025  # frameRemains - 0.025 for trigger
        if diamond_response.status == STARTED and t >= frameRemains:
            diamond_response.status = STOPPED
        if diamond_response.status == STARTED:
            theseKeys = event.getKeys(keyList=['y', 'n', 'left', 'right', 'space'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                diamond_response.keys.extend(theseKeys)  # storing all keys
                diamond_response.rt.append(diamond_response.clock.getTime())
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in diamondComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "diamond"-------
    for thisComponent in diamondComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if diamond_response.keys in ['', [], None]:  # No response was made
        diamond_response.keys=None
    thisExp.addData('diamond_response.keys',diamond_response.keys)
    if diamond_response.keys != None:  # we had a response
        thisExp.addData('diamond_response.rt', diamond_response.rt)
    thisExp.nextEntry()

# ------Prepare to start Routine "diamond_2"-------
def diamond_X (): 
    global endExpNow
    t = 0
    diamond_2Clock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(0.200000)
    # update component parameters for each repeat
    diamond_X_response = event.BuilderKeyResponse()
    upperleft_white.draw()
    # keep track of which components have finished
    diamond_2Components = [white_screen2_5, hexagon_2, upperleft_white, line10, line11, diamond_X_response]
    for thisComponent in diamond_2Components:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "diamond_2"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = diamond_2Clock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *white_screen2_5* updates
        if t >= 0 and white_screen2_5.status == NOT_STARTED:
            # keep track of start time/frame for later
            white_screen2_5.tStart = t
            white_screen2_5.frameNStart = frameN  # exact frame index
            white_screen2_5.setAutoDraw(True)
            upperleft_white.setAutoDraw(True)
        frameRemains = .2 - win.monitorFramePeriod * 0.75 - 0.025  # frameRemains - 0.025 for trigger
        if white_screen2_5.status == STARTED and t >= frameRemains:
            white_screen2_5.setAutoDraw(False)
            upperleft_white.setAutoDraw(False)
        
        # *hexagon_2* updates
        if t >= 0.0 and hexagon_2.status == NOT_STARTED:
            # keep track of start time/frame for later
            hexagon_2.tStart = t
            hexagon_2.frameNStart = frameN  # exact frame index
            hexagon_2.setAutoDraw(True)
        frameRemains = .2 - win.monitorFramePeriod * 0.75 - 0.025  # frameRemains - 0.025 for trigger
        if hexagon_2.status == STARTED and t >= frameRemains:
            hexagon_2.setAutoDraw(False)
        
        # *line10* updates
        if t >= 0.0 and line10.status == NOT_STARTED:
            # keep track of start time/frame for later
            line10.tStart = t
            line10.frameNStart = frameN  # exact frame index
            line10.setAutoDraw(True)
        frameRemains = .2 - win.monitorFramePeriod * 0.75 - 0.025  # frameRemains - 0.025 for trigger
        if line10.status == STARTED and t >= frameRemains:
            line10.setAutoDraw(False)
        
        # *line11* updates
        if t >= 0.0 and line11.status == NOT_STARTED:
            # keep track of start time/frame for later
            line11.tStart = t
            line11.frameNStart = frameN  # exact frame index
            line11.setAutoDraw(True)
        frameRemains = .2 - win.monitorFramePeriod * 0.75 - 0.025  # frameRemains - 0.025 for trigger
        if line11.status == STARTED and t >= frameRemains:
            line11.setAutoDraw(False)
        
        # *diamond_X_response* updates
        if t >= 0.0 and diamond_X_response.status == NOT_STARTED:
            # keep track of start time/frame for later
            diamond_X_response.tStart = t
            diamond_X_response.frameNStart = frameN  # exact frame index
            diamond_X_response.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(diamond_X_response.clock.reset)  # t=0 on next screen flip
            win.logOnFlip(level=logging.DATA, msg='diamond_x')
            win.callOnFlip(trigger, code=2)
        frameRemains = 0.0 + .2- win.monitorFramePeriod * 0.75 - 0.025  # frameRemains - 0.025 for trigger
        if diamond_X_response.status == STARTED and t >= frameRemains:
            diamond_X_response.status = STOPPED
        if diamond_X_response.status == STARTED:
            theseKeys = event.getKeys(keyList=['y', 'n', 'left', 'right', 'space'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                diamond_X_response.keys.extend(theseKeys)  # storing all keys
                diamond_X_response.rt.append(diamond_X_response.clock.getTime())
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in diamond_2Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "diamond_2"-------
    for thisComponent in diamond_2Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if diamond_X_response.keys in ['', [], None]:  # No response was made
        diamond_X_response.keys=None
    thisExp.addData('diamond_X_response.keys',diamond_X_response.keys)
    if diamond_X_response.keys != None:  # we had a response
        thisExp.addData('diamond_X_response.rt', diamond_X_response.rt)
    thisExp.nextEntry()

# ------Prepare to start Routine "square_5"-------
def square ():
    global endExpNow
    t = 0
    square_5Clock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(0.200000)
    # update component parameters for each repeat
    square_response = event.BuilderKeyResponse()
    upperleft_white.draw()
    # keep track of which components have finished
    square_5Components = [white_screen5_2, diamond_3, upperleft_white,square_response]
    for thisComponent in square_5Components:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "square_5"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = square_5Clock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *white_screen5_2* updates
        if t >= 0.0 and white_screen5_2.status == NOT_STARTED:
            # keep track of start time/frame for later
            white_screen5_2.tStart = t
            white_screen5_2.frameNStart = frameN  # exact frame index
            white_screen5_2.setAutoDraw(True)
            upperleft_white.setAutoDraw(True)
        frameRemains = 0.0 + .2- win.monitorFramePeriod * 0.75 - 0.025  # frameRemains - 0.025 for trigger
        if white_screen5_2.status == STARTED and t >= frameRemains:
            white_screen5_2.setAutoDraw(False)
            upperleft_white.setAutoDraw(False)
        
        # *diamond_3* updates
        if t >= 0.0 and diamond_3.status == NOT_STARTED:
            # keep track of start time/frame for later
            diamond_3.tStart = t
            diamond_3.frameNStart = frameN  # exact frame index
            diamond_3.setAutoDraw(True)
        frameRemains = .2 - win.monitorFramePeriod * 0.75 - 0.025  # frameRemains - 0.025 for trigger
        if diamond_3.status == STARTED and t >= frameRemains:
            diamond_3.setAutoDraw(False)
        
        # *square_response* updates
        if t >= 0.0 and square_response.status == NOT_STARTED:
            # keep track of start time/frame for later
            square_response.tStart = t
            square_response.frameNStart = frameN  # exact frame index
            square_response.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(square_response.clock.reset)  # t=0 on next screen flip
            win.logOnFlip(level=logging.DATA, msg='square')
            win.callOnFlip(trigger, code=1)
        frameRemains = 0.0 + .2- win.monitorFramePeriod * 0.75 - 0.025  # frameRemains - 0.025 for trigger
        if square_response.status == STARTED and t >= frameRemains:
            square_response.status = STOPPED
        if square_response.status == STARTED:
            theseKeys = event.getKeys(keyList=['y', 'n', 'left', 'right', 'space'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                square_response.keys.extend(theseKeys)  # storing all keys
                square_response.rt.append(square_response.clock.getTime())
                # a response ends the routine
                continueRoutine = False
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in square_5Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "square_5"-------
    for thisComponent in square_5Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if square_response.keys in ['', [], None]:  # No response was made
        square_response.keys=None
    thisExp.addData('square_response.keys',square_response.keys)
    if square_response.keys != None:  # we had a response
        thisExp.addData('square_response.rt', square_response.rt)
    thisExp.nextEntry()

# ------Prepare to start Routine "square_6X"-------
def square_X ():
    global endExpNow
    t = 0
    square_6XClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(0.200000)
    # update component parameters for each repeat
    square_X_response = event.BuilderKeyResponse()
    upperleft_white.draw()
    # keep track of which components have finished
    square_6XComponents = [white_screen2_8, hexagon, upperleft_white, line10_2, line11_2, square_X_response]
    for thisComponent in square_6XComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "square_6X"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = square_6XClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *white_screen2_8* updates
        if t >= 0 and white_screen2_8.status == NOT_STARTED:
            # keep track of start time/frame for later
            white_screen2_8.tStart = t
            white_screen2_8.frameNStart = frameN  # exact frame index
            white_screen2_8.setAutoDraw(True)
            upperleft_white.setAutoDraw(True)
        frameRemains = .2 - win.monitorFramePeriod * 0.75 - 0.025  # frameRemains - 0.025 for trigger
        if white_screen2_8.status == STARTED and t >= frameRemains:
            white_screen2_8.setAutoDraw(False)
            upperleft_white.setAutoDraw(False)
        
        # *hexagon* updates
        if t >= 0.0 and hexagon.status == NOT_STARTED:
            # keep track of start time/frame for later
            hexagon.tStart = t
            hexagon.frameNStart = frameN  # exact frame index
            hexagon.setAutoDraw(True)
        frameRemains = .2 - win.monitorFramePeriod * 0.75 - 0.025  # frameRemains - 0.025 for trigger
        if hexagon.status == STARTED and t >= frameRemains:
            hexagon.setAutoDraw(False)
        
        # *line10_2* updates
        if t >= 0.0 and line10_2.status == NOT_STARTED:
            # keep track of start time/frame for later
            line10_2.tStart = t
            line10_2.frameNStart = frameN  # exact frame index
            line10_2.setAutoDraw(True)
        frameRemains = .2 - win.monitorFramePeriod * 0.75 - 0.025  # frameRemains - 0.025 for trigger
        if line10_2.status == STARTED and t >= frameRemains:
            line10_2.setAutoDraw(False)
        
        # *line11_2* updates
        if t >= 0.0 and line11_2.status == NOT_STARTED:
            # keep track of start time/frame for later
            line11_2.tStart = t
            line11_2.frameNStart = frameN  # exact frame index
            line11_2.setAutoDraw(True)
        frameRemains = .2 - win.monitorFramePeriod * 0.75 - 0.025  # frameRemains - 0.025 for trigger
        if line11_2.status == STARTED and t >= frameRemains:
            line11_2.setAutoDraw(False)
        
        # *square_X_response* updates
        if t >= 0.0 and square_X_response.status == NOT_STARTED:
            # keep track of start time/frame for later
            square_X_response.tStart = t
            square_X_response.frameNStart = frameN  # exact frame index
            square_X_response.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(square_X_response.clock.reset)  # t=0 on next screen flip
            win.logOnFlip(level=logging.DATA, msg='square_x')
            win.callOnFlip(trigger, code=2)
            event.clearEvents(eventType='keyboard')
        frameRemains = 0.0 + .2- win.monitorFramePeriod * 0.75 - 0.025  # frameRemains - 0.025 for trigger
        if square_X_response.status == STARTED and t >= frameRemains:
            square_X_response.status = STOPPED
        if square_X_response.status == STARTED:
            theseKeys = event.getKeys(keyList=['y', 'n', 'left', 'right', 'space'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                square_X_response.keys.extend(theseKeys)  # storing all keys
                square_X_response.rt.append(square_X_response.clock.getTime())
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in square_6XComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "square_6X"-------
    for thisComponent in square_6XComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if square_X_response.keys in ['', [], None]:  # No response was made
        square_X_response.keys=None
    thisExp.addData('square_X_response.keys',square_X_response.keys)
    if square_X_response.keys != None:  # we had a response
        thisExp.addData('square_X_response.rt', square_X_response.rt)
    thisExp.nextEntry()

shape_list = [triangle1, circle1, pentagon, square, diamond]
shape_list_X = [triangle_X, circle_X, pentagon_X, square_X, diamond_X]

N = 300
randlist = np.zeros((N,),dtype=int)
order = np.empty(N, 'O')

for x in range(N):
    randlist[x]=randint(0,5)
    if x>=2:
        while(randlist[x]==randlist[x-1] and randlist[x]==randlist[x-2]):
            randlist[x]=randint(0,5)

for x in range(N):
    if randint(0, 100) > 33:
        which = shape_list
    else:
        which = shape_list_X
            
    order[x] = which[randlist[x]]

#fixation_start()

trigger(0x80)
Timer.reset()


fixationcross()
for x in order:
    x()
    fixationcross()

Localize.setAutoDraw(True)
Localize.draw()
win.flip()
event.waitKeys(keyList=['s','t','space','escape'])

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
#thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()

#!/usr/bin/python

'''
Implements a Modified Sternberg Working 

- space to trigger the start
- q to quit at most timestamp
- g,a for left response
- b,l for right

expects word lists to be in the directory stim/

ACN c. 2018
'''

from psychopy import visual,core,event,gui,logging
import os,glob
from datetime import datetime
from random import choice as rand_choose
from random import random
from numpy import mod
from re import sub as re_sub
import numpy as np
import egi.simple as egi
from psychopy import parallel
import copy

Trig_time = .025

def trigger(code):
    port.setData(code)
    core.wait(Trig_time)
    port.setData(0)

leftKeys = ['g','a','1']
rightKeys = ['b','l','3']
correctkey = ''

# parallel port for triggering experiment - doesn't work on a mac...

port = parallel.ParallelPort(address=0x0378)
port.setData(0)

# blocks and reps
fix_time = 2
encoding = 2
blocks = 8
reps = 10     #  within the blocks  ISI*reps duration
maintenance = 3  # time difference between target and match faces
probetime = 1       # match face duration
ITI = 1.5  + encoding + maintenance + probetime

theDate = datetime.now()

# annoyingly ask the user something about the experiment
expInfo = {"subject":"Harriet",'run':001}
dlg = gui.DlgFromDict(expInfo, title='simple JND Exp', fixed=['dateStr'])
if dlg.OK:
   logFn = "data/Sternberg-s-" + expInfo['subject'] + "-r-" + str(expInfo['run']) + "-" + theDate.strftime("%d%b%y") + ".log"
   print logFn
else:
    core.quit()  #the user hit cancel so exit

# setup the log file
logging.console.setLevel(logging.CRITICAL)
lastLog=logging.LogFile(logFn,filemode='w', level=logging.DATA)

Timer = core.Clock()
logging.setDefaultClock(Timer)
cdClock = core.CountdownTimer(start=ITI)

with open('stim/wordlist_4.txt', 'r') as f:
    word4 = [line.rstrip() for line in f]
with open('stim/wordlist_6.txt', 'r') as f:
    word6 = [line.rstrip() for line in f]
    
letters=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

win = visual.Window((1024, 768), allowGUI=False, winType='pyglet',
      monitor='MEG', color=(-.1,-.1,-.1), colorSpace='rgb', units='pix', screen=0, fullscr=False)

instruct = visual.TextStim(win, 
           units='norm',
           pos=(0, 0), text='This is a memory task. You will see some letters, followed by a delay. Next, you will see a single letter. Press the left button if the letter was in the previous set, press the right button if it was not.',
           color='BlanchedAlmond')

headlocalization = visual.TextStim(win, 
           units='norm',
           pos=(0, 0), text='Head localization in progress. Please remain still.',
           alignHoriz = 'center',alignVert='center',
           color='BlanchedAlmond')

fixation = visual.TextStim(win, 
           units='norm',
           pos=(0, 0), text='+', height=0.25,
           alignHoriz = 'center',alignVert='center',
           color='BlanchedAlmond')

encode = visual.TextStim(win, 
           units='norm',
           pos=(0, 0), text='ABC', height=0.25,
           alignHoriz = 'center',alignVert='center',
           color='BlanchedAlmond')

probe = visual.TextStim(win, 
           units='norm',
           pos=(0, 0), text='C', height=0.25,
           alignHoriz = 'center',alignVert='center',
           color='BlanchedAlmond')

upperleft_black = visual.Rect(win,width=1,height=1,lineColor=(0,0,0),opacity=1,pos=(-512,384))
upperleft_white = visual.Rect(win,width=1,height=1,lineColor=(1,0,0),opacity=1,pos=(-512,384))

instruct.draw()
win.flip()
event.waitKeys(keyList=['space'])
headlocalization.draw()
win.flip()
event.waitKeys(keyList=['space'])
trigger(0x80)

Timer.reset()
logging.info("Scan triggered start of experiment")
logging.flush()
upperleft_black.draw()
fixation.draw()
msg_string = 'StartFixation'
win.logOnFlip(level=logging.DATA, msg=msg_string)
win.flip()
logging.info("Start Fixation started")
core.wait(fix_time-Trig_time)	# subtract off the time for the trigger
logging.info("Start Fixation ended")
logging.flush()

# shuffle so the word list is different for everyone

np.random.shuffle(word6)
np.random.shuffle(word4)

# increment a counter for moving through the list of words

word6_num=0
word4_num=0

for blocknum in range(blocks):
   
    binlist_inlist_or_not=np.squeeze(np.concatenate((np.ones((reps/2,1)),np.zeros((reps/2,1)))))
    np.random.shuffle(binlist_inlist_or_not)

    for repnum in range(reps):
   
      cdClock.reset()
      
      if mod(blocknum,2):     # every other block should be difficulty 4 or 8
                 
         print '6 letter trial '
         encodetrig=6
         encodetext = word6[word6_num]
         
         if(binlist_inlist_or_not[repnum]==1):          # is the probe in the encoding set?
            index=np.random.randint(0,5)
            probetext = encodetext[index]
            correctkey='left'
         else:                                          # or not?
            probetext = encodetext[0]
            while(probetext in encodetext):
                probetext = np.random.choice(letters)
            correctkey='right'   
         print cdClock.getTime()
         word6_num+=1
      else:
        
         print '4 letter trial begin'
        
         encodetext = word4[word4_num]
         encodetrig=4
         if(binlist_inlist_or_not[repnum]==1):          # is the probe in the encoding set?
            index=np.random.randint(0,3)
            probetext = encodetext[index]
            correctkey='left'
            trigcode_in_out=1
         else:                                          # or not?
            probetext = encodetext[0]
            while(probetext in encodetext):
                probetext = np.random.choice(letters)
            correctkey='right'
            trigcode_in_out=2
         print cdClock.getTime()
         word4_num+=1
      
      print encodetext
      print probetext
      print "correct key: %s" % correctkey
      encode.text = encodetext
      probe.text = probetext
         
      upperleft_white.draw()
      encode.draw()
      msg_string = 'Encode %s' % (encodetext)
      win.callOnFlip(trigger, code=encodetrig)
      win.logOnFlip(level=logging.DATA, msg=msg_string)
      win.flip()
      core.wait(encoding-Trig_time) # subtract off the time for the trigger
      print cdClock.getTime()
      
      upperleft_black.draw()
      fixation.draw()      
      msg_string = 'Maintenance'
      win.logOnFlip(level=logging.DATA, msg=msg_string)
      win.flip()
      core.wait(maintenance)
      print cdClock.getTime()
      
      event.clearEvents()   # clear the event buffer so we can get new keys
      kside = False
      kp = []
      
      upperleft_white.draw()
      msg_string = 'Probe %s' % (probetext)
      win.callOnFlip(trigger, code=trigcode_in_out)
      win.logOnFlip(level=logging.DATA, msg=msg_string)
      probe.draw()
      win.flip()
 
      core.wait(probetime-Trig_time) # subtract off the time for the trigger
      upperleft_black.draw()
      fixation.draw()
      win.flip()
      core.wait(cdClock.getTime()-Trig_time) # leave time for one last trigger

      kp = event.getKeys(leftKeys + rightKeys +['q','escape'])  # fetch all the keys off the event buffer
      print kp
      for key in kp:
            if key in leftKeys:
               kside = "left"
               print "key press: %s" % kside
            elif key in rightKeys:
               kside = "right"
               print "key press: %s" % kside
            else:
               kside = False
               if key in ['q','escape']:
                  win.close()

      if kside == correctkey:
         corr = 1
         trigger(1)
      else:
         corr = 0 
         trigger(2)
      logging.data("Correct key pressed: " + str(corr) )

      logging.flush()

upperleft_black.draw()
fixation.draw()
msg_string = 'EndFixation'
win.logOnFlip(level=logging.DATA, msg=msg_string)
win.flip()
logging.info("End Fixation started")

core.wait(fix_time)
logging.info("End Fixation ended")
logging.flush()
headlocalization.draw()
win.flip()
event.waitKeys(keyList=['s','t','space','escape'])
win.close()
core.quit()

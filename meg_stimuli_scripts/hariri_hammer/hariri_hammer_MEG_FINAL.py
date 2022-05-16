#!/usr/bin/python

'''
Implements Hariri's hammer paradigm

- s,t to trigger the start
- q to quit at most timestamp
- g,a for left response
- b,l for right

expects displayed stim to be in the directory ../stim

JWE c. 2014 

22Jul16 JWE fix issue with lists, probably again...  
12Aug16 JWE add in KDEF faces and such.
15Aug16 JWE add in EGI interface stuff
            add in max face of 1s and ISI of ~3s for mixed-block (emo) er (mot) design
02Sep16 JWE add in the rest of the events to send to the EGI thing
21Oct16 JWE added in different labels for the events to make it easier to tell them apart for analysis...
22Jan16 JWE added in a delay between test and match faces for MEG
06Nov18 ACN modified to correct aspect ratio of shapes
            added jitter to ITIs
            changed so that the top image is never repeated
            changed so that an equal number of male/female top faces shown in both happy and sad
            changed so that bottom images are always one male and one female
            changed so that instead of using the lightbar we can use the propixx upper left pixel on ADC16
            changed trigger code
            changed logging to get event time stamps for every stimulus
            fixed the code for deciding if response was correct so that it works
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

def trigger(code):
    port.setData(code)
    core.wait(.025)
    port.setData(0)

# eeg?
EEG = False
leftKeys = ['g','a','3']
rightKeys = ['b','l','1']

# parallel port for triggering experiment - doesn't work on a mac...

port = parallel.ParallelPort(address=0x0378)
port.setData(0)

# blocks and reps
fix_time = 1
blocks = 10          # We want 5 blocks of each type happy, sad, shape
reps = 15            #  within the blocks  ISI*reps duration
disp_diff = 0.5     # time difference between target and match faces
fdur = 1.           # match face duration
ISI = 1.5 + disp_diff + fdur*2.
jitter = 0.25

theDate = datetime.now()

# annoyingly ask the user something about the experiment
expInfo = {"subject":"Gladys",'run':001}
dlg = gui.DlgFromDict(expInfo, title='simple JND Exp', fixed=['dateStr'])
if dlg.OK:
   logFn = "data/HH-s-" + expInfo['subject'] + "-r-" + str(expInfo['run']) + "-" + theDate.strftime("%d%b%y") + ".log"
   print logFn
else:
    core.quit()#the user hit cancel so exit

# setup the log file
logging.console.setLevel(logging.CRITICAL)
lastLog=logging.LogFile(logFn,filemode='w', level=logging.DATA)

Timer = core.Clock()
logging.setDefaultClock(Timer)
cdClock = core.CountdownTimer(start=ISI)

#logging.info("Hariri's Hammer -- " + theDate.strtime("%a %d %b %y %R"))

# initialize the set of pics

hap_male = glob.glob('./stim/faces/?M*HAS.JPG')         # list of all the faces of each type
hap_female = glob.glob('./stim/faces/?F*HAS.JPG')
sad_male = glob.glob('./stim/faces/?M*SAS.JPG')
sad_female = glob.glob('./stim/faces/?F*SAS.JPG')
len_hap_male = len(hap_male)
len_hap_female = len(hap_female)
len_sad_male = len(sad_male)
len_sad_female = len(sad_female)

total_trials=blocks*reps            # total trials, and trials for each emotion
trials_each_emo=total_trials/3

# set up a binary shuffled list signifying equal sad and happy
# within each emotion, set up a shuffled list of equal male and female

binlist_emo=np.squeeze(np.concatenate((np.ones((trials_each_emo,1)),np.zeros((trials_each_emo,1)))))
np.random.shuffle(binlist_emo)
binlist_gen_hap=np.squeeze(np.concatenate((np.ones((trials_each_emo/2,1)),np.zeros((trials_each_emo/2,1)))))
binlist_gen_sad=copy.deepcopy(binlist_gen_hap)
np.random.shuffle(binlist_gen_hap)
np.random.shuffle(binlist_gen_sad)

# Now that we have those binary lists, so we know which image category to choose from, 
# we'll still want to pick a random image within the category
# so lets make some random shufflings of indices of the image lists

hap_male_index_rand = np.arange(0,len_hap_male)
np.random.shuffle(hap_male_index_rand)
hap_female_index_rand = np.arange(0,len_hap_female)
np.random.shuffle(hap_female_index_rand)
sad_male_index_rand = np.arange(0,len_sad_male)
np.random.shuffle(sad_male_index_rand)
sad_female_index_rand = np.arange(0,len_sad_female)
np.random.shuffle(sad_female_index_rand)

# get the shapes

shape1 = list(np.sort(glob.glob('./stim/shapes/*_v.png')))
shape2 = list(np.sort(glob.glob('./stim/shapes/*_h.png')))

# I'm using units of pixels because its working better for me.  YMMV.

win = visual.Window((1024.0,768.0),allowGUI=False,winType='pyglet',
      monitor='MEG', color=(-0.1,-0.1,-0.1), colorSpace='rgb',units ='pix', screen=1,fullscr=False)

# setup stim
topIm= visual.ImageStim(win,image='./stim/face.jpg',
    mask=None,
    pos=(0,0),
    #pos=(.15,0),
    size=(187,254))

leftIm= visual.ImageStim(win,image='./stim/face.jpg',
    mask=None,
    pos=(-100,0),
    #pos=(-100,0),
    size=(187,254))

rightIm= visual.ImageStim(win,image='./stim/face.jpg',
    mask=None,
    pos=(100,0),
    #pos=(0.5,0),
    size=(187,254))

leftshapeIm= visual.ImageStim(win,image='./stim/shapes/diam_h.png',
    mask=None,
    pos=(-100,0),
    #pos=(-0.25,0),
    size=(187,254))

rightshapeIm= visual.ImageStim(win,image='./stim/shapes/diam_h.png',
    mask=None,
    pos=(100,0),
    #pos=(0.5,0),
    size=(187,254))

headlocalization = visual.TextStim(win, 
           units='norm',
           pos=(0, 0), text='Head localization in progress. Please remain still.',
           alignHoriz = 'center',alignVert='center',
           color='BlanchedAlmond')

instruct = visual.TextStim(win, 
           units='norm',
           pos=(0, 0), text='This is a matching task. You will see an image, followed by a brief delay, then two simultaneous images. Match the first image to the corresponding image in the pair. For faces, match the emotion displayed. For shapes, match the corresponding shape. Press the left or right button to indicate the match.',
           alignHoriz = 'center',alignVert='center', wrapWidth= 1.5,
           color='BlanchedAlmond')

fixation = visual.TextStim(win, 
           units='norm',
           pos=(0, 0), text='+', height=0.25,
           alignHoriz = 'center',alignVert='center',
           color='BlanchedAlmond')

# instead of the lightbar, use the upper left pixel, flipping from white to black

upperleft_black = visual.Rect(win,width=1,height=1,lineColor=(0,0,0),fillColor=(0,0,0),opacity=1,pos=(-512,384))
upperleft_white = visual.Rect(win,width=1,height=1,lineColor=(1,0,0),fillColor=(1,0,0),opacity=1,pos=(-512,384))

# set up EGI stuff
if EEG:
   ns = egi.Netstation()
   ms_localtime = egi.ms_localtime
   ns.connect('10.10.10.42',55513)
   ns.BeginSession()
   ns.sync()

# function to pick the left and right faces

def pickLR(sad_female,hap_male,hap_female,sad_male):
    # pick which is left and which is right by chance
    val_lr_gen = rand_choose((0,1))            # should face on left be male(0) or female(1)
    val_lr_emo = rand_choose((0,1))            # should face on left be happy(0) or sad(1)
    #print 'val_lr_gen: %s val_lr_emo: %s' % (val_lr_gen,val_lr_emo)
    len_sf=len(sad_female)
    len_sm=len(sad_male)
    len_hm=len(hap_male)
    len_hf=len(hap_female)
    #print sad_female
    #print len_sf
    if(val_lr_gen):
        if(val_lr_emo):
            leftFile=sad_female[np.random.choice(len_sf)] # pick L and R faces at random
            rightFile=hap_male[np.random.choice(len_hm)]
        else:
            leftFile=hap_female[np.random.choice(len_hf)]
            rightFile=sad_male[np.random.choice(len_sm)]
    else:
        if(val_lr_emo):
            leftFile=sad_male[np.random.choice(len_sm)]
            rightFile=hap_female[np.random.choice(len_hf)]
        else:
            leftFile=hap_male[np.random.choice(len_hm)]
            rightFile=sad_female[np.random.choice(len_sf)]
    return leftFile, rightFile

def som(list1,list2):
   # randomly select shape
   nlist = range(len(list1))

   topFileType = rand_choose((0,1))
   topInd = rand_choose(nlist)

   if topFileType:
      topFile = list1[topInd]
      match = list2[topInd]
   else:
      topFile = list2[topInd]
      match = list1[topInd]

   del(nlist[topInd])
   remainder = np.concatenate( [np.array(list1)[nlist], np.array(list2)[nlist]])

   val = rand_choose([0,1])

   if val:
      rightFile = match
      leftFile = rand_choose(remainder)
   else:
      rightFile = rand_choose(remainder)
      leftFile = match

   print leftFile[-10:-6]
   if leftFile[-10:-6] == topFile[-10:-6]:      
      side = "left"
   else:
      side = "right"

   return topFile, leftFile, rightFile, side

# show stuff and main loop

instruct.draw()
win.flip()
event.waitKeys(keyList=['space'])
headlocalization.draw()
win.flip()
event.waitKeys(keyList=['space'])

trigger(0x80)

if EEG:
   ns.StartRecording()
Timer.reset()
logging.info("Scan triggered start of experiment")
logging.flush()
upperleft_black.draw()
fixation.draw()      
msg_string = 'StartFixation' 
win.logOnFlip(level=logging.DATA, msg=msg_string)
win.flip()
logging.info("Start Fixation started")
core.wait(fix_time-.025)  # subtract off the time for the trigger
logging.info("Start Fixation ended")
logging.flush()

# initialize the ccounters for selecting images from the shuffled lists

emo_count = 0
gen_hap_count = 0
gen_sad_count = 0
hapm_count = 0
hapf_count = 0
sadm_count = 0
sadf_count = 0 

for bb in range(blocks):

   for rr in range(reps):
     
      cdClock.reset()
      
      if mod(bb,3):     # two out of three blocks should be faces
        
         # determine the emotion and gender of the top face, depending on those shuffled binary lists we made
         # Once we determine which face, choose the index of the face from the shuffled face index lists
         print 'emo block begin'

         if(binlist_emo[emo_count]==0):            # if top face should be happy
            if(binlist_gen_hap[gen_hap_count]==0): # if top face should be male
                topFile = hap_male[hap_male_index_rand[hapm_count]]
                hapm_count+=1
                topStim='HapMale'
                toptrigcode=11      # trig code: first dig=hap/sad second dig=male/fem
            else:                                      # face should be female
                topFile = hap_female[hap_female_index_rand[hapf_count]]
                hapf_count+=1
                topStim='HapFem'
                toptrigcode=12
            gen_hap_count+=1
         else:                                          # top face should be sad
            if(binlist_gen_sad[gen_sad_count]==0): # if top face should be male
                topFile = sad_male[sad_male_index_rand[sadm_count]]
                sadm_count+=1
                topStim='SadMale'
                toptrigcode=21
            else:                                      # face should be female
                topFile = sad_female[sad_female_index_rand[sadf_count]]
                sadf_count+=1
                topStim='SadFem'
                toptrigcode=22
            gen_sad_count+=1 
         emo_count+=1
         
         # get left and right images, initialize as top image then keep picking new ones until no duplicate identity
         
         leftFile=topFile
         rightFile=topFile
         
         while(leftFile[-11:-7]==topFile[-11:-7] or rightFile[-11:-7]==topFile[-11:-7] or leftFile[-11:-7]==rightFile[-11:-7]):
            (leftFile,rightFile)=pickLR(sad_female,hap_male,hap_female,sad_male)
        
         # these loops are just used to set the stimulus type for the log file and triggers
         
         if leftFile[-7]=='H':
            if leftFile[-10]=='F':
                leftStim='HapFem'
                rightStim='SadMale'
                lefttrigcode=12         # trig code: first dig=hap/sad second dig=male/fem
            else: 
                leftStim='HapMale' 
                rightStim='SadFem'
                lefttrigcode=11
         else:
            if leftFile[-10]=='F':
                leftStim='SadFem'
                rightStim='HapMale'
                lefttrigcode=22
            else: 
                leftStim='SadMale'
                rightStim='HapFem'
                lefttrigcode=21
                
        
         # figure out which side is correct
         
         if(topFile[-7:-5]==leftFile[-7:-5]):
            sval='left'
         else:
            sval='right'
            
         print sval
         
         # set final images
         
         trialtype='emo'
         
         topIm.setImage(topFile)
         leftIm.setImage(leftFile)
         rightIm.setImage(rightFile)
         
      # the much easier shape case
      
      else:
         (topFile, leftFile, rightFile, sval) = som(shape1,shape2)
         trialtype='shape'
         topIm.setImage(topFile)
         leftshapeIm.setImage(leftFile)
         rightshapeIm.setImage(rightFile)
         topStim=topFile[-10:-6]
         leftStim=leftFile[-10:-6]
         rightStim=rightFile[-10:-6]
         
         if sval=='left':
            lefttrigcode=1
         elif sval=='right':
            lefttrigcode=2
         
         if topStim=='diam':
            toptrigcode=1
         elif topStim=='moon':
            toptrigcode=2
         elif topStim=='oval':
            toptrigcode=3
         elif topStim=='plus':
            toptrigcode=4
         elif topStim=='rect':
            toptrigcode=5
         elif topStim=='trap':
            toptrigcode=6
         elif topStim=='tria':
            toptrigcode=7
            
      print 'start trial %s' % (cdClock.getTime())
      upperleft_white.draw()
      topIm.draw()
      msg_string = 'TopStim %s' % (topStim)
      win.callOnFlip(trigger, code=toptrigcode)     # send a trigger code for the top stim
      win.logOnFlip(level=logging.DATA, msg=msg_string)
      win.flip()
      core.wait(fdur-.025)   # subtract off the time for the trigger
      upperleft_black.draw()
      fixation.draw()
      msg_string = 'Fixation'
      win.logOnFlip(level=logging.DATA, msg=msg_string)
      win.flip()
      core.wait(disp_diff)
      
      event.clearEvents()   # clear the event buffer so we can get new keys
      kside = False
      kp = []
      
      lefttrigcode=0
      toptrigcode=0

      upperleft_white.draw()
      if trialtype=='shape':
        leftshapeIm.draw()
        rightshapeIm.draw()
      else:
        leftIm.draw()
        rightIm.draw()
        
      # logging 
      msg_string = 'LeftStim %s RightStim %s' % (leftStim,rightStim)
      win.logOnFlip(level=logging.DATA, msg=msg_string)
      win.callOnFlip(trigger, code=lefttrigcode)
      win.flip()
      
      if EEG:
         ns.send_event( 'trial_', label="Trial:" + str(bb*reps+rr) + "=" + trialtype, timestamp=egi.ms_localtime())
       
      core.wait(fdur-.025) # subtract off the time for the trigger
      
      fixation.draw()
      win.flip()
      print cdClock.getTime()
      core.wait(cdClock.getTime()+random()*jitter-0.025)  # wait only long enough to allow one last trigger

      kp = event.getKeys(leftKeys + rightKeys +['q','escape'])  # grab the key presses off the event buffer
    
      for key in kp:
            if key in leftKeys:
               kside = "left"
               print kside
            elif key in rightKeys:
               kside = "right"
               print kside
            else:
               kside = False
               if key in ['q','escape']:
                  win.close()
#                  if EEG:
#                     ns.StopRecording()
#                     ns.EndSession()
#                     ns.disconnect()
#                  core.quit()

#            if EEG:
#               ns.send_event( 'bp_', label="Press=" + key, timestamp=egi.ms_localtime())
      #print topFile + " " + leftFile + " " + rightFile
      #print "key pressed was: " + kside + " correct answer " +  sval

      if kside == sval:
         corr = 1
         #print cdClock.getTime()
         trigger(1)
         #print cdClock.getTime()
      else:
         corr = 0
         #print cdClock.getTime()
         trigger(2)
         #print cdClock.getTime()

#      if EEG:
#         ns.send_event( 'resp_', label="Correct=" + str(corr), timestamp=egi.ms_localtime())

      logging.data("Correct key pressed: " + str(corr) )

      logging.flush()

topIm.setAutoDraw(False)
leftIm.setAutoDraw(False)
rightIm.setAutoDraw(False)

upperleft_black.draw()
fixation.draw()
win.flip()
logging.info("End Fixation started")
if EEG:
   ns.StopRecording()
   ns.EndSession()
   ns.disconnect()
core.wait(fix_time)
logging.info("End Fixation ended")
logging.flush()
headlocalization.draw()
win.flip()
event.waitKeys(keyList=['s','t','space','escape'])
core.quit()

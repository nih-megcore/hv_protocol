'''
Simple task to instruct subjects to make certain movements

Designed to introduce artifacts into the recording

- s,t to trigger the start
- q to quit at most timestamp
- g,a for left response
- b,l for right

expects word lists to be in the directory stim/

ACN c. 2018
'''

from psychopy import visual,core,event,gui,logging
from datetime import datetime
from psychopy import parallel

instructionTime = 2
fixationTime = 2

def trigger(code):
    port.setData(code)
    core.wait(.025)
    port.setData(0)

theDate = datetime.now()

port = parallel.ParallelPort(address=0x0378)
port.setData(0)

# annoyingly ask the user something about the experiment
expInfo = {"subject":"Ophelia",'run':001}
dlg = gui.DlgFromDict(expInfo, title='simple JND Exp', fixed=['dateStr'])
if dlg.OK:
   logFn = "data/Artifacts-s-" + expInfo['subject'] + "-r-" + str(expInfo['run']) + "-" + theDate.strftime("%d%b%y") + ".log"
   print logFn
else:
    core.quit()  #the user hit cancel so exit

# setup the log file
logging.console.setLevel(logging.CRITICAL)
lastLog=logging.LogFile(logFn,filemode='w', level=logging.DATA)

Timer = core.Clock()
logging.setDefaultClock(Timer)
cdClock = core.CountdownTimer(start=0)

win = visual.Window((1024.0,768.0),allowGUI=False,winType='pyglet',
      monitor='MEG', color=(-.1,-.1,-.1), colorSpace='rgb',units ='pix', screen=1,fullscr=False)
      
headlocalization = visual.TextStim(win, 
           units='norm',
           pos=(0, 0), text='Head localization in progress. Please remain still.',
           alignHoriz = 'center',alignVert='center',
           color='BlanchedAlmond')
           
instruct = visual.TextStim(win, 
           units='norm',
           pos=(0, 0), text='InstructionText',
           color='BlanchedAlmond')
           
fixation = visual.TextStim(win, 
           units='norm',
           pos=(0, 0), text='+', height=0.25,
           alignHoriz = 'center',alignVert='center',
           color='BlanchedAlmond')
           
upperleft_black = visual.Rect(win,width=1,height=1,lineColor=(0,0,0),fillColor=(0,0,0),opacity=1,pos=(-512,384))
upperleft_white = visual.Rect(win,width=1,height=1,lineColor=(1,0,0),fillColor=(1,0,0),opacity=1,pos=(-512,384))

headlocalization.draw()
win.flip()
event.waitKeys(keyList=['s','t','space'])

upperleft_black.draw()
fixation.draw()
win.logOnFlip(level=logging.DATA, msg='Fixation')
win.flip()

trigger(0x80)
Timer.reset()
instruct.text = 'Please blink your eyes'
upperleft_white.draw()
instruct.draw()
win.callOnFlip(trigger, code=1)
win.logOnFlip(level=logging.DATA, msg='Blink')
win.flip()
core.wait(instructionTime-0.025)
print cdClock.getTime()

upperleft_black.draw()
fixation.draw()
win.flip()
core.wait(fixationTime)
print cdClock.getTime()

instruct.text = 'Please move your eyes left and right'
upperleft_white.draw()
instruct.draw()
win.callOnFlip(trigger, code=2)
win.logOnFlip(level=logging.DATA, msg='MoveEyesLR')
win.flip()
core.wait(instructionTime-0.025)
print cdClock.getTime()

upperleft_black.draw()
fixation.draw()
win.flip()
core.wait(fixationTime)
print cdClock.getTime()

instruct.text = 'Please move your eyes up and down'
upperleft_white.draw()
instruct.draw()
win.callOnFlip(trigger, code=3)
win.logOnFlip(level=logging.DATA, msg='MoveEyesUD')
win.flip()
core.wait(instructionTime-0.025)
print cdClock.getTime()

upperleft_black.draw()
fixation.draw()
win.flip()
core.wait(fixationTime)
print cdClock.getTime()

instruct.text = 'Please clench your jaw'
upperleft_white.draw()
instruct.draw()
win.callOnFlip(trigger, code=4)
win.logOnFlip(level=logging.DATA, msg='ClenchJaw')
win.flip()
core.wait(instructionTime-0.025)
print cdClock.getTime()

upperleft_black.draw()
fixation.draw()
win.flip()
core.wait(fixationTime)
print cdClock.getTime()

instruct.text = 'Please swallow'
upperleft_white.draw()
instruct.draw()
win.callOnFlip(trigger, code=5)
win.logOnFlip(level=logging.DATA, msg='Swallow')
win.flip()
core.wait(instructionTime-0.025)
print cdClock.getTime()

upperleft_black.draw()
fixation.draw()
win.flip()
core.wait(fixationTime)
print cdClock.getTime()

instruct.text = 'Please take a deep breath'
upperleft_white.draw()
instruct.draw()
win.callOnFlip(trigger, code=6)
win.logOnFlip(level=logging.DATA, msg='breath')
win.flip()
core.wait(instructionTime-0.025)
print cdClock.getTime()

upperleft_black.draw()
fixation.draw()
win.logOnFlip(level=logging.DATA, msg='Fixation')
win.flip()
logging.info("End Fixation started")

core.wait(fixationTime)
logging.info("End Fixation ended")
logging.flush()
headlocalization.draw()
win.flip()
event.waitKeys(keyList=['s','t','space','escape'])
print cdClock.getTime()
core.quit()
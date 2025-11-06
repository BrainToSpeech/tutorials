from psychopy import visual, core, event
import glob

# image directory load
image_files = sorted(glob.glob('topomap_*.png'))

# PsychoPy window setting
win = visual.Window([2560, 1440], fullscr=True, color=(0, 0, 0), colorSpace='rgb', waitBlanking=False, checkTiming=False)
win.mouseVisible = False  # mouse cursor hiding

for stmuli in image_files:
  print("img: ", stmuli)
  img_file = visual.ImageStim(win, image=stmuli,pos=(0, 0))
  img_file.draw()
  win.flip() 
  core.wait(0.1)  # sleep 1 sec.

core.wait(3)

import numpy as np
import cv2
import subprocess
from optparse import OptionParser
import os
from os.path import isfile, join
from PIL import Image


parser=OptionParser()
parser.add_option("-p", "--path", dest="test_video", help="Path for the video to be feed into the neural network.")
parser.add_option("-l", "--live", dest="live", help="define status of live feed", default=False)
(options, args) = parser.parse_args()

try:
    subprocess.run("rm -r incoming_images" ,shell=True)
    subprocess.run("mkdir incoming_images" ,shell=True)
    print("\n completed reseting the input stream")
except:
    pass

if options.live:
    cap = cv2.VideoCapture(0)
elif not options.test_video:
    print(" \n No input method is defind")
else:
    try:
        cap = cv2.VideoCapture(options.test_video)
    except:
        raise ValueError('No such file directory')
        exit()

w=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH ))
h=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT ))
fps=int(cap.get(cv2.CAP_PROP_FPS))
# video recorder
print(w)
print(h)

if not cap.isOpened():
    print(" \n Cannot open camera")
    exit()

i=0
j=0
print("\n converting video and saving")
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        #cv2.rectangle(frame,(100,100),(150,150),(0,200,0),2)
        #frame=np.array([j[::-1] for j in frame])
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.resize(frame,(640,480))
        frame=Image.fromarray(frame)
        if i%5==0:
            frame.save('./incoming_images/{0}kav.png'.format(j))
            j=j+1
        #print(' ** ',frame,' ** ')
        #export(frame)
        #_ = subprocess.call('clear')
        #cv2.imshow('frame',frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break
    i=i+1

# Release everything if job is finished
cap.release()
cv2.destroyAllWindows()

subprocess.run("bash execute.command",shell=True)
subprocess.run("rm -r results_imgs",shell=True)
subprocess.run("mkdir results_imgs",shell=True)
 
def numbers(x):
    print(x)
    y=re.findall(r'\d+', x)
    print(y)
    return(int(y[0]))
 
def convert_frames_to_video(pathIn,pathOut,fps):
    frame_array = []
    files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f)) and f.endswith('.png')]
    #print(files)
    #for sorting the file names properly
    files.sort(key = lambda x: numbers(x))
 
    for i in range(len(files)):
        filename=pathIn + files[i]
        #reading each files
        img = cv2.imread(filename)
        height, width,layer = img.shape
        size = (width,height)
        print(filename)
        #inserting the frames into an image array
        frame_array.append(img)
 
    out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
 
    for i in range(len(frame_array)):
        # writing to a image array
        out.write(frame_array[i])
    out.release()


print("\n receiving video")
pathin="../results_imgs"
pathout="final_output.avi"
convert_frames_to_video(pathin,pathout,fps)

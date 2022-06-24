import threading
from colorthief import ColorThief
from PIL import Image
import cv2
from multiprocessing import Process
import numpy as np
import matplotlib.pyplot as plt

def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)
def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb
def bincount_app(a):
    a2D = a.reshape(-1,a.shape[-1])
    col_range = (256, 256, 256) # generically : a2D.max(0)+1
    a1D = np.ravel_multi_index(a2D.T, col_range)
    return np.unravel_index(np.bincount(a1D).argmax(), col_range)

def plotImg(color):
    plt.figure(facecolor=rgb_to_hex(color))
    plt.show()
    plt.close('all')

def webcamIntegration(perSec):

    cv2.namedWindow("preview")
    vc = cv2.VideoCapture(0)

    if (vc.isOpened() == False):
        print("Error opening the video file")
    else:
        fps = vc.get(5)
        print('Frames per second : ', fps,'FPS')
        rval, frame = vc.read()

    count = 0
    while rval:
        count = count +1
        cv2.imshow("preview", frame)
        rval, frame = vc.read()
        if(count % (fps/perSec) == 0):
            colr = frame.mean(axis=(0,1))
            newColor= bincount_app(frame)
            print(colored(newColor[2],newColor[1],newColor[0], newColor), "  or  ", 
            colored(colr.astype(int)[2], colr.astype(int)[1], colr.astype(int)[0], colr.astype(int)))
            print()
            
        key = cv2.waitKey(20)
        if key == 27: # exit on ESC
            break

    vc.release()
    cv2.destroyWindow("preview")


def vidCaptureToColor(video):
    vid_capture = cv2.VideoCapture(video)

    if (vid_capture.isOpened() == False):
        print("Error opening the video file")
    else:
        fps = vid_capture.get(5)
        print('Frames per second : ', fps,'FPS')

        # Get frame count
        frame_count = vid_capture.get(7)
        print('Frame count : ', frame_count)

    count = 0
    while(vid_capture.isOpened()):
        ret, frame = vid_capture.read()
        if ret == True:
            count = count +1
            cv2.imshow('Frame',frame)

            if(count % fps == 0):
                colr = frame.mean(axis=(0,1))
                print("Color: ",colr)
                
            key = cv2.waitKey(1)
        
            if key == ord('q'):
                break
        else:
            break
        
    vid_capture.release()
    cv2.destroyAllWindows()


def colorFromImage(image):
    color_thief = ColorThief(image)
    dominant_color = color_thief.get_color(quality=100)
    print(dominant_color)
    showImageFromColor(dominant_color)

def showImageFromColor(color):
    img = Image.new('RGB',(400,400),color)
    img.show()





def main():
    perSec=1
    webcamIntegration(perSec)
    

if __name__ == "__main__":
    main()
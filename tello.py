from djitellopy import Tello
import numpy as np
import cv2, PIL
from cv2 import aruco
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import pathlib
import time


def target():
    
       
    target1 = input("ArUco target #1(1-18): \n")
    target2 = input("ArUco target #2(1-18): \n")
    target3 = input("ArUco target #3(1-18): \n")

    target1 = float(target1)
    target2 = float(target2)
    target3 = float(target3)
    
    global li
    li = [target1, target2, target3]
    #print(li)
         
def scan():
    target()
    time.sleep(5)
    #################################################################
    global tello
    tello = Tello()
    tello.connect()
    tello.set_speed(15)
    
    tello.streamon()
    tello.takeoff()
    tello.move_up(110)    
    
    tello.move_forward(100)
    ################################################################
    
    frame_read = tello.get_frame_read()
    
    im = cv2.imwrite(r"C:\\Users\xwzhe\\d10.png", frame_read.frame)
    img = cv2.imread(r"C:\\Users\xwzhe\\d10.png", cv2.IMREAD_GRAYSCALE)
    
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(img, aruco_dict, parameters=parameters)
    frame_markers = aruco.drawDetectedMarkers(img.copy(), corners, ids)
    
    ###############################################################################################   
    tello.move_forward(110)
    ###############################################################################################
    
    plt.figure()
    plt.imshow(frame_markers, origin = "lower")
    plt.xlim([0, 959])
    ax = plt.gca()
    plt.gca().invert_yaxis()
    plt.ylim([718.8,0])
    arrayX = []
    arrayY = []
    arrayFinal= []
    xcoords = []
    ycoords = 0
    if ids is not None:
        for i in range(len(ids)):
            c = corners[i][0]
            plt.plot([c[:, 0].mean()], [c[:, 1].mean()], "+", label = "id={0}".format(ids[i]))
            xcoords = c[:, 0].mean()
            ycoords = c[:, 1].mean()
            intI = float(ids[i])
            arrayFinal1 = arrayFinal
            arrayFinal.append({"idx":intI, "x":xcoords, "y": ycoords})
  
    #plt.show()
    plt.savefig(r"C:\\Users\xwzhe\\dave10.png")
    ##############################################
    
    arrayFinal.append({"idx": "drone", "x": 450, "y": 180})
    
    global dF
    dF = pd.DataFrame(arrayFinal, columns = ["idx", "x", "y"])
    #print(arrayFinal)
    print(dF)
    
    global dF1
    dF1=dF[dF.idx.isin(li)].copy()
    dF1.loc[-1] = ['drone', 450, 180] 
    
    dF1 = dF1.sort_index(ascending=True)  
    dF1.reset_index([0], inplace = True, drop = True)
    
    print(dF1) 
    

def cal():
    
    scan()
    i = 0
    for i in range(len(dF1.index)-1):
        scale1 = 0.22
        scale2 = 0.22

        mxi = dF1['x'].values[i] - dF1['x'].values[i+1]
        dmxi = abs(mxi*scale1)
        if mxi > 0:
            if dmxi < 20:
                ###########################
                tello.move_right(21)
                tello.move_left(int(dmxi)+21)
            elif dmxi > 20:
                ###########################
                tello.move_left(int(dmxi))
        elif mxi < 0:
            if dmxi < 20:
                ##########################
                tello.move_left(21)
                tello.move_right(int(dmxi)+21)
            elif dmxi > 20:
                #########################
                tello.move_right(int(dmxi))  

        myi = dF1['y'].values[i] - dF1['y'].values[i+1]
        dmyi = abs(myi*scale2)
        if myi > 0:
            if dmyi < 20:
                ############################
                tello.move_up(21)
                tello.move_down(int(dmyi)+24)
            elif dmyi > 20:
                ###########################
                tello.move_up(int(dmyi)+3)
        elif myi < 0:
            if dmyi < 20:
                ###########################
                tello.move_down(21)
                tello.move_up(int(dmyi)+24)
            elif dmyi > 20:
                ############################
                tello.move_down(int(dmyi)+3)
        ###################################           
        tello.move_forward(50)
        tello.move_back(50) 
        ###################################
        print(dmxi)
        print(dmyi)
        i += 1
    #######################################
    tello.move_back(140) 
    tello.land()    
    #######################################
    
        



def main():
    cal()

    
if __name__ == "__main__":
    main()

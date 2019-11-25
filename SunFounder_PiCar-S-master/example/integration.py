#!/usr/bin/env python
'''
*****************************************************************
* Filename   : Picar with line_follower and QR Code scanner
* Description: Integration of line follower module with qr code scanner
* Author     : Tejas Morbagal Harish
*****************************************************************
'''

from SunFounder_Line_Follower import Line_Follower
from picar import front_wheels
from picar import back_wheels
import time
import picar

from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2


picar.setup()

REFERENCES = [200, 200, 200, 200, 200]
#calibrate = True
calibrate = False
forward_speed = 60
backward_speed = 70

delay = 0.005

fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels(db='config')
lf = Line_Follower.Line_Follower()

lf.references = REFERENCES
fw.ready()
bw.ready()
fw.turning_max = 45

#global barcode_found
barcode_found = False
counter = 0


   
def main():
    global turning_angle
    off_track_count = 0
    bw.speed = forward_speed

    a_step = 3
    b_step = 10
    c_step = 30
    d_step = 45
    #bw.forward()
    while True:
        '''if barcode_found == True:
           perform_action()
           bw.stop()
           break'''
        lt_status_now = lf.read_digital()
        print(lt_status_now)      
        # Angle calculate
        if  lt_status_now == [1,1,0,1,1]:
            step = 0    
        elif lt_status_now == [1,0,0,1,1] or lt_status_now == [1,1,0,0,1]:
            step = a_step
        elif lt_status_now == [1,0,1,1,1] or lt_status_now == [1,1,1,0,1]:
            step = b_step
        elif lt_status_now == [0,0,1,1,1] or lt_status_now == [1,1,1,0,0]:
            step = c_step
        elif lt_status_now == [0,1,1,1,1] or lt_status_now == [1,1,1,1,0]:
            step = d_step

        # Direction calculate
        if  lt_status_now == [1,1,0,1,1]:
            #off_track_count = 0
            fw.turn(90)
            bw.backward()
            #capture_frame()
        # turn right
        elif lt_status_now in ([1,0,0,1,1],[1,0,1,1,1],[0,0,1,1,1],[0,1,1,1,1]):
            #off_track_count = 0
            turning_angle = int(90 - step)
            fw.turn(turning_angle)
            bw.backward()
            #capture_frame()
        # turn left
        elif lt_status_now in ([1,1,0,0,1],[1,1,1,0,1],[1,1,1,0,0],[1,1,1,1,0]):
            #off_track_count = 0
            turning_angle = int(90 + step)
            fw.turn(turning_angle)
            bw.backward()
            #capture_frame()
        elif lt_status_now == [1,1,1,1,1]:
            fw.turn(90)
            bw.backward()
            #bw.stop()
            #break
            #capture_frame()
        elif lt_status_now == [0,0,0,0,0]:
            fw.turn(90)
            #bw.forward()
            bw.stop()
            capture_frame()
            break
            #capture_frame()
        else:
            off_track_count = 0
    
            #fw.turn(turning_angle)
        time.sleep(delay)
        

def capture_frame():
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    print("video stream started")
    time.sleep(2.0)

    while True:
      #print("creating a frame")
      frame = vs.read()
      frame = imutils.resize(frame, width=400)
      #print("frame resized")
      #global barcodes
      cv2.imshow("scanner", frame)
      #key = cv2.waitKey(1) & 0xFF
      # find the barcodes in the frame and decode each of the barcodes
      #cv2.imshow("Barcode Scanner", frame)
      barcodes = pyzbar.decode(frame)
      print("length of barcodes")
      print(len(barcodes))
      '''if len(barcodes) == 0:
          #cv2.destroyAllWindows()
          #vs.stop()
          print("exiting the loop")
          break
          '''
        #if len(barcodes) > 0:
      for barcode in barcodes:
           print("barcode found")
           (x, y, w, h) = barcode.rect
           cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

           barcodeData = barcode.data.decode("utf-8")
           print("string" + barcodeData)
           barcodeType = barcode.type
           print(barcodeType)
           text = "{} ({})".format(barcodeData, barcodeType)
           cv2.putText(frame, text, (x, y - 10),
           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
           cv2.imshow("Barcode Scanner", frame)
           global barcode_found
           barcode_found = True
    
      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
         break
      if barcode_found == True:
         perform_action() 
         break
    print("[INFO] cleaning up...")
    cv2.destroyAllWindows()
    bw.stop()
    vs.stop()
      
       
    return barcode_found
      
def destroy():
    bw.stop()
    fw.turn(90)
    #vs.stop()
    
def perform_action():
    global counter
    counter = counter + 1
    print("perform some blockchain operation")
    bw.backward()
    print("move ahead")
    #bw.forward()
    if counter < 2:
       print("car moving after qr scan") 
       main()
    '''if counter < 2:
     try:
        try:
            
                #qr_scan()
                print("car moving after qr scan")
                main()
                
                
        except Exception as e:
            print(e)
            print('error try again in 5')
            destroy()
            time.sleep(5)
     except KeyboardInterrupt:
        destroy()
    '''


if __name__ == '__main__':
    try:
        try:
            
                #qr_scan()
                print("HI")
                main()
                
                
        except Exception as e:
            print(e)
            print('error try again in 5')
            destroy()
            time.sleep(5)
    except KeyboardInterrupt:
        destroy()





#!/usr/bin/env python

import warnings
warnings.filterwarnings('ignore')
from picamera import PiCamera
import RPi.GPIO as GPIO
from time import sleep
import time
import datetime
import os



GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT)

pin = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

pwm = GPIO.PWM(pin,100) # 50
pwm.start(0)
camera = PiCamera()
camera.resolution = (1280,853)


MATRIX = 
    [ ?     
        [1,2,3],
? ?     [4,5,6],
? ?     [7,8,9],
? ?     ["*",0,"#"]
? ? ]

ROW ? ? ?= [19,13,6,5]
COL ? ? ?= [27,17,4]

?
for j in range(3):
? ? GPIO.setup(COL[j], GPIO.OUT)
? ? GPIO.output(COL[j],1)

?
for i in range(4):
? ? GPIO.setup(ROW[i],?GPIO.IN, pull_up_down = GPIO.PUD_UP)

############################################################


# �ʱ�ȭ �Լ�
def NFC_Initlized():
    digit = ""
    password = "4444*"
    a = None
    count = 0
    nfc_id = None



# NFC �±� �Լ�
def NFC_Tag():
    if (nfc_id == None):
        # NFC ���̼��� �ҷ�����
        nfc_id = os.system('sudo libnfc-1.7.1/examples/nfc-poll > nfc_data.txt')
? ?     inFile = open('nfc_data.txt')
? ?     lines = inFile.readlines()
? ?     inFile.close()
? ?     buffer = []

        for line in lines:
? ? ?       line_content = line.split()

? ? ? ?     if(not line_content[0] == 'UID'):
                pass

            else:
                buffer.append(line_content)
? ? ? ? ? ?     str1 = buffer[0]
                id_str = str1[2] + str1[3] + str1[4] + str1[5]
                print(id_str)

        # NFC �±� ����
        if(id_str == 'ef1a639e'):
            print('NFC MATCH')
            GPIO.output(22, GPIO.HIGH)
            time.sleep(2)
            GPIO.output(22,GPIO.LOW)
            time.sleep(1)
            return 1

        # NFC �±� ����
        else:
            return 0

    else:
        return 0



# Ű�е� �Է� �Լ�
def Key_Input():
    z = 1
    while(count < 3):
        if (a != '*'):
            while(z == 0):
                for j in range(3):
                    GPIO.output(COL[j],0)

?                   for i in range(4):
                        if (GPIO.input(ROW[i]) == 0):
                            a = (MATRIX[i][j])
                            digit = digit + str(a)
                            print (a)
                            print (digit)

                            while(GPIO.input(ROW[i]) == 0):
                                pass

                    GPIO.output(COL[j],1)

?                   if a == '*':
                        z = 1

           if digit == (password):
                print ("SUCCESS!")
                return 1

        else
            print ("FALSE")
            z = 0
            digit = ""
            count += 1
            a = None

    # ��й�ȣ 3ȸ ����
? ? return 0
    


# ���� ���ư��� �Լ�
def Motor_Rotation(close):
    if (close == 0):
        pwm.ChangeDutyCycle(0)
        print ("degree : stop")
        time.sleep(0.5)
        pwm.ChangeDutyCycle(5) # + degree
        print ("degree : -")
        time.sleep(0.03)
        pwm.ChangeDutyCycle(0)
        print ("degree : stop")
        time.sleep(3)
        pwm.ChangeDutyCycle(24) # - degree
        print ("degree : +")
        time.sleep(0.01)
        pwm.ChangeDutyCycle(0)
        print ("degree : stop")
    else:
        pwm.ChangeDutyCycle(0)
        print ("degree : stop")
        time.sleep(0.5)
        pwm.ChangeDutyCycle(24) # - degree
        print ("degree : +")
        time.sleep(0.01)
        pwm.ChangeDutyCycle(0)
        print ("degree : stop")
        time.sleep(3)
        pwm.ChangeDutyCycle(5) # + degree
        print ("degree : -")
        time.sleep(0.03)
        pwm.ChangeDutyCycle(0)
        print ("degree : stop")



# ���� ��� �Լ�
def Take_Picture():
    print ("Stop: 3s")
    #camera.start_preview() sil_hang_chang
    for num in range(2):#camera~
        d=datetime.datetime.now()
        sleep(1)
        camera.capture('/home/pi/Desktop/camerasave/filename_%s.jpg' % d)
        camera.stop_preview() #~camera

    time.sleep(3)
    count = 0
    NFC_Initlized()

    


######################################################
# Main
try:
? ? while(true):
        NFC_Initlized() # �ʱ�ȭ
? ? ? ? try:
            # �±� ����
            if(NFC_Tag()):
                # Ű �Է� ����
                if(Key_Input()):
                    try :
                        Motor_Rotation(0) # ���� ȸ�� (0�� �� ���� / 1�� �� ����)
                        sleep(60)
                        Motor_Rotation(1) #���� ��ȸ�� �ڵ�(60�� �� �ٽ� ���)

                    except KeyboardInterrupt :
                        pwm.stop()
                        GPIO.cleanup()

                # Ű �Է� 3ȸ ����
                else:
                    Take_Picture() # ���� �Կ�

            # �±� ���� �� 
            else:
                sleep(10) # 10�� �� �ٽ� NFC ���� ����
             ? ? ? ? ? ??
? ? ? ? except KeyboardInterrupt:
? ? ? ? ? ? GPIO.cleanup()
 ? ? ??
except KeyboardInterrupt:
? ? GPIO.cleanup()
######################################################

?


from flask import Flask, app, render_template, request

import socket as sck
import threading as thr
import time
import RPi.GPIO as GPIO
import time as T
import sqlite3 as SQL
import subprocess as sb

class AlphaBot(object):
    
    def __init__(self, in1=13, in2=12, ena=6, in3=21, in4=20, enb=26):
        self.IN1 = in1
        self.IN2 = in2
        self.IN3 = in3
        self.IN4 = in4
        self.ENA = ena
        self.ENB = enb
        self.PA  = 41  #left engine
        self.PB  = 38  #right engine

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)
        self.PWMA = GPIO.PWM(self.ENA,500)
        self.PWMB = GPIO.PWM(self.ENB,500)
        self.PWMA.start(self.PA)
        self.PWMB.start(self.PB)
        self.stop()

    def forward(self, time_ms = 1000):  #that function move the alphabot forward for {time_ms} milliseconds
        print("The Alphabot moves forward...")
        

        self.PWMA.ChangeDutyCycle(self.PA)      #setting the engines
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)

        T.sleep(time_ms/1000)
        self.stop()


    def backward(self, time_ms = 1000):        #this funtion move the alphabot backward for {time_ms} milliseconds
        print("The Alphabot moves backward...")

        self.PWMA.ChangeDutyCycle(self.PA)      #setting the engines
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)

        T.sleep(time_ms/1000)
        self.stop()

    def left(self, time_ms = 1000):        #this function turn the alphabot left for {time_ms} milliseconds
        print("The Alphabot moves left...")
        
        self.PWMA.ChangeDutyCycle(self.PA)      #setting the engines
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)

        T.sleep(time_ms/1000)
        self.stop()

    def right(self, time_ms = 1000):       #this function turn the alphabot right for {time_ms} milliseconds
        print("The Alphabot moves right...")
        
        self.PWMA.ChangeDutyCycle(self.PA)      #setting the engines
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)

        T.sleep(time_ms/1000)
        self.stop()

    def stop(self, time_ms = 0):        #this function stops the alphabot for {time_ms} milliseconds
        print("The Alphabot stops...")

        self.PWMA.ChangeDutyCycle(0)
        self.PWMB.ChangeDutyCycle(0)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

        T.sleep(time_ms/1000)
        
    def set_pwm_a(self, value):
        self.PA = value
        self.PWMA.ChangeDutyCycle(self.PA)

    def set_pwm_b(self, value):
        self.PB = value
        self.PWMB.ChangeDutyCycle(self.PB)    
        
    def set_motor(self, left, right):       #this function sets engines
        if (right >= 0) and (right <= 100):
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
            self.PWMA.ChangeDutyCycle(right)
        elif (right < 0) and (right >= -100):
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            self.PWMA.ChangeDutyCycle(0 - right)
        if (left >= 0) and (left <= 100):
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)
            self.PWMB.ChangeDutyCycle(left)
        elif (left < 0) and (left >= -100):
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)
            self.PWMB.ChangeDutyCycle(0 - left)

alphabot = AlphaBot()

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        if request.form.get('forward') == 'Forward':
            print("Forward")
            alphabot.forward()

        elif request.form.get('backward') == "Backward":
            print("Backward")
            alphabot.backward()
        
        elif request.form.get('left') == "Left":
            print("Left")
            alphabot.left()

        elif request.form.get('right') == "Right":
            print("Right")
            alphabot.right()

        else:
            print("Stop")
            alphabot.stop()

    elif request.method == 'GET':
        return render_template('index.html')
    
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, host='localhost')
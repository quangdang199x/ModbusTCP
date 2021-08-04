# import random

# def guess(x):
#     random_number = random.randint(1, x)
#     guess = 0
#     while guess != random_number:
#         guess = int(input(f'Guess a number between 1 and {x}: '))
#         if guess < random_number:
#             print('Sorry, guess again. Too low.')
#         elif guess > random_number:
#             print('Sorry, guess again. Too high.')
    
#     print(f'Random number is: {random_number}. You win (^.^)')

# guess(10)


import paho.mqtt.client as mqtt
from random import randrange, uniform
import time

mqqtBroker  = "mqtt.eclipseprojects.io"
client = mqtt.Client("Temperature")
client.connect(mqqtBroker) 

while True:
    randNumber = uniform(20.0,21.0)
    client.publish("TEMPERATURE", randNumber)
    print("Just publish "+str(randNumber)+ " to Topic TEMPERATURE" )
    time.sleep(2)
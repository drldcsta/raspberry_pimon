#!/usr/bin/env python3

import RPi.GPIO as GPIO
import random
from time import sleep
GPIO.setwarnings(False)

#Set to true if you want to cheat
DEBUG = False

#TODO - Find out what this actually does
GPIO.setmode(GPIO.BCM)

#Put pin outs in arrays so we don't have to hard code anywhere
#Used for setting up hardware (not app code)
gpio_button_pins = [12, 18, 24, 23]
gpio_led_pins = [17,27,22]

#Set the approppriate pins to handle output
for led in gpio_led_pins:
  GPIO.setup(led,GPIO.OUT)


gpio_button_labels = {  12 : "yellow" ,
                        18 : "red",
                        23 : "start",
                        24 : "green"
}

gpio_button_to_led = {  18 : 17,  
                        12 : 27,
                        24 : 22}



#Set the appropriate pins to handle input
for pin in gpio_button_pins: 
  GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# If I'd done something different this likely could have
# taken "colour" as an arg instead of pin...but I didn't
def blink_light(pin,count):
  print(F"{gpio_button_labels[pin] if DEBUG else '' }")
  for _ in range(count):
    GPIO.output(gpio_button_to_led[pin],True)
    sleep(.5)
    GPIO.output(gpio_button_to_led[pin],False)
    sleep(.25)

def random_light():
  return random.choice(list(gpio_button_to_led.keys()))



print(F"You may start a new game by pressing button 4 at any Time")

#This should probably be a main function but will figure out later
#Spoiler - no I won't
new_game = True
while True:
  if new_game:
    blink_light(18,1)
    blink_light(12,1)
    blink_light(24,1)
    print(F"Starting a new game!")
    new_game = False
    pimons_lights = []
    pimons_lights.append(random_light())
    players_lights = []
    for light in pimons_lights:
      print(F"pimon Says: {gpio_button_labels[light] if DEBUG else '***'}")
      blink_light(light,1)  
    
  #TODO - Find out what this actually does 
  for pin in gpio_button_pins:
    input_state = GPIO.input(pin)

    if input_state == False:
      if pin == 23: #Pin 12 should be button 4 which is the "start new game button"
        new_game = True
      if (pin in gpio_button_to_led):
        print(F"Player Entry: { gpio_button_labels[pin] if  DEBUG else '***'}")
        blink_light(pin,1)
        players_lights.append(pin)
        if len(players_lights) <= len(pimons_lights): 
          for i,v in enumerate(players_lights):
            if players_lights[i] != pimons_lights[i]:
              new_game = True
              print(F"you done messed up")  
              print(F"Correct Sequence {', '.join(list(gpio_button_labels[i] for i in pimons_lights))}")
              print(F"You input {', '.join(list(gpio_button_labels[i] for i in players_lights))} ")
          else: 
            if (len(players_lights) == len(pimons_lights)) and new_game == False:
              pimons_lights.append(random_light())
              players_lights = []
              print(F"Next Sequence: ")
              for light in pimons_lights:
                blink_light(light,1)
                print(F"pimon Says: {gpio_button_labels[light] if DEBUG else '***'}")
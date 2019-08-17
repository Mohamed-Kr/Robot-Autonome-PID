from Robot import *
from sys import exit
from os import _exit
from math import pi

robot = Robot()

def main():
    robot.goTo(-200, -200, 100, 10)


try:
    main()
except KeyboardInterrupt:
    robot.stopMotors()
    try:
        exit(0)
    except SystemExit:
        _exit(0)

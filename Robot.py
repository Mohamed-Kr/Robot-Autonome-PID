from adafruit_crickit import crickit
from PositionWatcher import PositionWatcher
from math import *
from time import sleep


class Robot:
	leftMotor = crickit.dc_motor_1
	rightMotor = crickit.dc_motor_2
	positionWatcher = None
	xR = 0
	yR = 0
	orientation = 0
	erreurPre = 0

	def __init__(self):
		self.positionWatcher = PositionWatcher()
		self.positionWatcher.start()

	def fetch(self):
		self.xR = self.positionWatcher.getPos()[0]
		self.yR = self.positionWatcher.getPos()[1]
		self.orientation = self.positionWatcher.getOrientation()

	def goTo(self, targetX, targetY, p, d):
		vitesseC = 0.6
		threehold=50
		self.xR = self.positionWatcher.getPos()[0]
		self.yR = self.positionWatcher.getPos()[1]
		xC = targetX
		yC = targetY
		running = True
		while running:
			self.fetch()
			distanceCible = sqrt((xC-self.xR)*(xC-self.xR)+(yC-self.yR)*(yC-self.yR))
			cmdG = cmdD = distanceCible + 0.4 * 255

			if cmdD > 255: cmdG = cmdD = 255
			
			cmdD *= vitesseC
			cmdG *= vitesseC

			targetTheta = atan2((targetY - self.yR), (targetX - self.xR))
			erreurOrientation = (targetTheta - self.orientation)
			while abs(erreurOrientation) > pi:
				erreurOrientation += (-2*pi) * (erreurOrientation/abs(erreurOrientation))

			cmd = erreurOrientation*p + self.erreurPre*d

			cmdD += cmd
			cmdG -= cmd
			
			if cmdD > 255: cmdD = 255
			if cmdG > 255: cmdG = 255
			if cmdD < -255: cmdD = -255
			if cmdG < -255: cmdG = -255

			cmdD /= 255
			cmdG /= 255

#			print((('CMD', cmd), ('G', cmdG), ('D', cmdD)))
			self.erreurPre = erreurOrientation
			try:
				self.leftMotor.throttle = -cmdG
				self.rightMotor.throttle = cmdD*0.9
			except:
				print('_____________________ERREUR________________________')
				print(-cmdG, cmdD*0.9)

			if distanceCible < threehold:
				running = False
		self.stopMotors()

	def stopMotors(self):
		self.leftMotor.throttle = self.rightMotor.throttle = 0

	def stopThreads(self):
		self.positionWatcher.stop()

	def logState(self):
		while True:
			self.fetch()
			print(self.xR, self.yR, self.orientation * 180/pi)
			sleep(0.1)

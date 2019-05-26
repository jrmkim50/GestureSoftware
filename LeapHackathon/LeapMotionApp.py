import Leap, sys, thread, time
import pygame
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from Tkinter import *

from twilio.rest import TwilioRestClient


# Twilio phone number goes here. Grab one at https://twilio.com/try-twilio
# and use the E.164 format, for example: "+12025551234"
TWILIO_PHONE_NUMBER = "+1646798-6846"

# list of one or more phone numbers to dial, in "+19732644210" format
DIAL_NUMBERS = ["+19173466036"]

# URL location of TwiML instructions for how to handle the phone call
TWIML_INSTRUCTIONS_URL = \
  "http://static.fullstackpython.com/phone-calls-python.xml"

# replace the placeholder values with your Account SID and Auth Token
# found on the Twilio Console: https://www.twilio.com/console
client = TwilioRestClient("AC97590f59d019ca9325063f865045f706", "93bb9cb394df55e5ccfd31326c818034")


previous_count = -1
delay = 0
message = "Please make a gesture (pop in to pause, pop out to play)"
Color = (0,0,0)

from twilio.rest import TwilioRestClient

TWILIO_PHONE_NUMBER = "+16467986846"

#current
class LeapMotionListener (Leap.Listener):
	finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
	bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
	state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
	
	def on_init(self, controller):
		print "Initialized"
		
	def on_connect(self, controller):
		print "Motion Sensor Connected!"
		
		controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
		controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)
		controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)
		controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
		
		controller.config.set("Gesture.Circle.MinRadius", 10.0)
		controller.config.set("Gesture.Circle.MinArc", .5)
		
		
		
	def on_disconnect(self, controller):
		print "Motion Sensor Disconnected"
		
	def on_exit(self, controller):
		print "Exited"
		
	def on_frame(self, controller):
		frame = controller.frame()
		
		'''
		print "Frame ID: " + str(frame.id) \
			+ " Timestamp: " + str(frame.timestamp) \
			+ " # of Hands " + str(len(frame.hands)) 
		'''
		
		for hand in frame.hands:
			handType = "Left Hand" if hand.is_left else "Right Hand"
			
			#print handType + " Hand ID: " + str(hand.id) + " Palm Position: " + str(hand.palm_position)
			
			normal = hand.palm_normal
			direction = hand.direction
			
			#print "Pitch: " + str(direction.pitch * Leap.RAD_TO_DEG) + "Roll: " + str(normal.roll + Leap.RAD_TO_DEG) + "YAW: " + str(direction.yaw + Leap.RAD_TO_DEG)			
		
			hand_pointables = hand.pointables
				
			global delay
			if delay == 0:
				
				global previous_count

				current_count = 0 
			
			
				for p in hand_pointables:
					if(p.is_finger and p.is_extended):
						current_count += 1
				
				
				#print "Previous Count: " + str(previous_count) + "  |  Current Count: " + str(current_count)
				
				#delay -= 1
			
				if(previous_count - current_count != 0):
				# Alert here 
					
					global message	
					global Color
					if(previous_count - current_count < 0 ):
						#POP UP
						# Accept call
						
						
						print "Pop up"
						message = "RESUMING (and dialing)"
						Color = (0, 255, 0)
						time.sleep(2)
						
						dial_numbers(DIAL_NUMBERS)
							
						
					else:
						#print "POP DOWN"
						# Decline call
						
						print "Pop down"
						message = "PAUSE"
						Color = (255, 0 , 0)
						time.sleep(2)
						
						
			
				previous_count = current_count
			
		
			arm = hand.arm
			
			'''
			print "Arm Direction: " + str(arm.direction) + " Wrist Position: " + str(arm.wrist_position) + " Elbow Position: " + str(arm.elbow_position)
		
			for finger in hand.fingers:
				print "Type: " + self.finger_names[finger.type] + "ID: " + str(finger.id) + " Length (mm): " + str(finger.length) + " Width (mm): " + str(finger.width)
		
				for b in range(0, 4):
					bone = finger.bone(b)
					print"Bone: " + self.bone_names[bone.type] + " Start: " + str(bone.prev_joint) + "End: " + str(bone.next_joint) + " Direction: " + str(bone.direction)

		for gesture in frame.gestures():
			
			if gesture.type == Leap.Gesture.TYPE_CIRCLE:
				circle = CircleGesture(gesture)
				
				if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
					clockwiseness = "clockwise"
					
				else:
					clockwiseness = "counter-clockwise"
					
				swept_angle = 0
				if circle.state != Leap.Gesture.STATE_START:
					previous = CirceGesture(controller.frame(1).gesture(circle.id))
					swept_angle = (circle.progress - previous.progress) * 2 * Leap.PI
					
				print "ID: " + str(circle.id) + "Progress: " + str(circle.progress) + " Radius: " + str(circle.radius) + " Swept Angle: " + str(swept_angle * Leap.RAD_TO_DEG) + clockwiseness 
'''
def main():
	listener = LeapMotionListener()
	controller = Leap.Controller()
	
	controller.add_listener(listener)
	

	'''
	print "Press enter to quit"
	try:
		sys.stdin.readline()
	except KeyboardInterrupt:
		pass
	finally:
		controller.remove_listener(listener)
		'''
		
	background_colour = (255,255,255)
	(width, height) = (300, 200)
	screen = pygame.display.set_mode((width, height))
	pygame.display.set_caption('Demo of Driver Controlled Gestures')
	screen.fill(background_colour)
	pygame.display.flip()
	
	pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
	myfont = pygame.font.SysFont('Comic Sans MS', 30)
	
	global message
	
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		
		screen.fill(background_colour)
		textsurface = myfont.render(message, False, Color)
		screen.blit(textsurface,(0,0))
		pygame.display.flip()
			
	controller.remove_listener(listener)
	
		
def dial_numbers(numbers_list):
    """Dials one or more phone numbers from a Twilio phone number."""
    for number in numbers_list:
        print("Dialing " + number)
        # set the method to "GET" from default POST because Amazon S3 only
        # serves GET requests on files. Typically POST would be used for apps
        client.calls.create(to=number, from_=TWILIO_PHONE_NUMBER, url=TWIML_INSTRUCTIONS_URL, method="GET")		

if __name__ == "__main__":
	main()
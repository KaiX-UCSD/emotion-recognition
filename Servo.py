from multiprocessing import Process, Queue
import time

class Servo:
    """
    Servo Number    GPIO number
    0               4
    1               17
    2               18
    3               21/27 (depends on board revision)
    4               22
    5               23
    6               24
    7               25
    """
    def __init__(self, servoNum, upperlimit, lowerlimit):
        # ServoBlaster is whate we use to control the servo motor
        self.servoBlaster = open('/dev/servoblaster', 'w')
        self.SERVO = servoNum   # servo number: 0,1,2,3...7  (defined in ServoBlaster for GPIO matching)
        self.ul=upperlimit
        self.ll=lowerlimit

        #Self Variables: initialize to arbitrary values
        self.cp = 150    #current position of servo
        self.dp = 151   #desired position of servo
        
        #Queue for communicating with Process thread
        self.servoCp = Queue()
        self.servoDp = Queue()  
        self.servoSpd = Queue()
        self.run()

    def move(self, distance, speed):
        # move servo by desired position by adding to queue
        #check if distance is positive
        if distance >= 0:
            if not self.servoCp.empty():
                self.cp = self.servoCp.get()
            self.dp = self.cp + distance
        
            if self.dp > self.ul:
                self.dp = self.ul
            self.servoDp.put(self.dp)
            self.servoSpd.put(speed)
        #else: distance is negative
        else:
            # move servo to desired position by adding to queue
            if not self.servoCp.empty():
                self.cp = self.servoCp.get()
            self.dp = self.cp + distance
        
            if self.dp < self.ll:
                self.dp = self.ll
            self.servoDp.put(self.dp)
            self.servoSpd.put(speed)
        return;
    
    def moveClockwise(self, distance, speed):
        # move servo clockwise by desired position
        if not self.servoCp.empty():
            self.cp = self.servoCp.get()
        self.dp = self.cp + distance
        
        if self.dp > self.ul:
            self.dp = self.ul
        self.servoDp.put(self.dp)
        self.servoSpd.put(speed)
        return;
    
    def moveCounterClockwise(self, distance, speed):
        # move servo counterclockwise by desired position 
        if not self.servoCp.empty():
            self.cp = self.servoCp.get()
        self.dp = self.cp - distance
        
        if self.dp < self.ll:
            self.dp = self.ll
        self.servoDp.put(self.dp)
        self.servoSpd.put(speed)
        return;
    
    def run (self):
        #start Process on thread
        Process(target=self.Process_servo, args=()).start()
        time.sleep(1)	#allow for the subproccess to start

#   def setDegree ( self, degree ):
#           if degree >= 0 or degree <= 180:
#               width = degree*self.DEGREE + self.MIN_WIDTH
#               self.pi.set_servo_pulsewidth(self.SERVO, width)
#   def setMinWidth( self,min_width ):
#       self.MIN_WIDTH = min_width
# 
#   def setMaxWidth (self,max_width):
#       self.MAX_WIDTH = max_width
#   
#   def rest (self):
#       self.pi.set_servo_pulsewidth(self.SERVO, 0)
    
    def Process_servo(self):
        speed = .1

        # make servo position unequal, so we know where the servo 
        # really is 
        self.cp = 99    
        self.dp = 100
        while True:
            time.sleep(speed)
            """
            Constantly update self.servoCp in case the main process 
            needs to read it
            """
            if self.servoCp.empty():
                self.servoCp.put(self.cp)

            # Constantly read self.servoDp in case the main process
            # has updated it
            if not self.servoDp.empty():
                self.dp = self.servoDp.get()

            # Constantly read self.servoSpd in case the main process 
            # has updated it with the higher speed value, the 
            # shorter the wait between loops will be, so the
            # servo moves faster
            if not self.servoSpd.empty():
                speedChange = self.servoSpd.get()
                speed = .1 / speedChange

            if self.cp < self.dp:
                self.cp += 1    #increment self.servoCp
                self.servoCp.put(self.cp) # move the servo a little bit
                self.servoBlaster.write( str(self.SERVO) + '=' + str(self.cp) + '\n')
                self.servoBlaster.flush() 
            elif self.cp > self.dp:
                self.cp -= 1  # decrement self.servoCp
                # move the servo a little bit
                self.servoCp.put(self.cp) # move the servo a little bit
                self.servoBlaster.write( str(self.SERVO) + '=' + str(self.cp) + '\n')
                self.servoBlaster.flush()

                # throw away the old self.servoCp value.
                if not self.servoCp.empty():
                    trash = self.servoCp.get()
            elif self.cp == self.dp:
                speedChange = 1 # slow the speed; no need to eat CPU just waiting
   
"""
if __name__ == "__main__":
    import Servo

    print "running"
    servoX = Servo.Servo(0, 250,75)
    servoX.run()
    servoX.move(50,3)
"""
    

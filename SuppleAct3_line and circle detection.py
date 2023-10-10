import cv2, numpy as np
from managers import WindowManager, CaptureManager

class Cameo(object):
    def __init__(self):
        self._windowManager = WindowManager('Cameo', self.onkeypress)
        self._captureManager = CaptureManager(cv2.VideoCapture(0), self._windowManager, False)
        
    def run(self):
        """Run the main loop."""
        self._windowManager.createWindow()
        while self._windowManager.isWindowCreated:
            self._captureManager.enterFrame()
            frame = self._captureManager.frame
            
            
            # Line Detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 120)
            minLineLength = 20
            maxLineGap = 5
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength, maxLineGap)
            for x1, y1, x2, y2 in lines[0]:
                cv2.line(frame, (x1,y1), (x2,y2), (0,255,0), 2)
            cv2.imshow('Line Detection' , edges)
            
            
            # Circle Detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame1 = cv2.medianBlur(gray, 25)
            cimg = cv2.cvtColor(frame1, cv2.COLOR_GRAY2BGR)
            circles = cv2.HoughCircles(frame1, cv2.HOUGH_GRADIENT,1,120,
                            param1=100,param2=30,minRadius=0,
                                maxRadius=0)
            
            circles = np.uint16(np.around(circles))
            
            for i in circles[0,:]:
                # draw the outer circle
                cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
                # draw the center of the circle
                cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)
            
            self._captureManager.exitFrame()
            self._windowManager.processEvents()

    def onkeypress(self, keycode):
        """Handle a keypress.
        space -> Take a screenshot.
        tab -> Start/stop recording a screencast.
        escape -> Quit.
        """
      
        if keycode == 32: # space
            self._captureManager.writeImage('screenshot.png')
        elif keycode == 9: # tab
            if not self._captureManager.isWritingVideo:
                self._captureManager.startWritingVideo('screencast.avi')
            else:
                self._captureManager.stopWritingVideo()
        elif keycode == 27: # escape
            self._windowManager.destroyWindow()

if __name__ == "__main__":
  Cameo().run()
  
import cv2
from managers import WindowManager, CaptureManager
import filters

class Cameo(object):
    def __init__(self):
        self._windowManager = WindowManager('Cameo', self.onkeypress)
        self._captureManager = CaptureManager(cv2.VideoCapture(0), self._windowManager, False)
        
        """Filters"""
        self._curveFilter = filters.BGRPortraCurveFilter(filters.BGRkernel) # Initialization of the BGRPortraCurveFilter or the VConvolution Filter
        self._sharpenFilter = filters.Sharpen() # Initialization of the Sharpen Filter
        self._findedgesFilter = filters.FindEdges() # Initialization of the Find Edges Filter
        self._blurFilter = filters.Blur() # Initialization of the Blur Filter
        self._embossFilter = filters.Emboss() # Initialization of the Emboss Filter

    def run(self):
        """Run the main loop."""
        self._windowManager.createWindow()
        while self._windowManager.isWindowCreated:
            self._captureManager.enterFrame()
            frame = self._captureManager.frame
            
            """ TODO: Filter the frame """
            #filters.strokeEdges(frame, frame, blurKsize = 7, edgeKsize = 5) # Stroke Edges Filter
            #self._curveFilter.apply(frame, frame) # Curve Filter 
            #self._sharpenFilter.apply(frame, frame) # Sharpen Filter
            #self._findedgesFilter.apply(frame, frame) # Find Edges Filter
            #self._blurFilter.apply(frame, frame) # Blur Filter
            #self._embossFilter.apply(frame, frame) # Emboss Filter
                       
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
  
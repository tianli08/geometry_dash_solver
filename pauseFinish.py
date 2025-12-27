import pyautogui
import cv2
import numpy as np

class GameRecorder:
    
    def __init__ (self):
        self.screenResolution = (1920, 1080)
        self.screenIsRecording = False

    def startRecording(self):
        self.screenIsRecording = True
        
        # Just for experimentation with window testing
        cv2.namedWindow("Show", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Show", 1080, 590)

        while True:
            # cv2.resizeWindow("Show", 300, 200)
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Need frame resizing, changing for proper config on HiDPI, may not need a non version config.
            frame = cv2.resize(frame, (1080, 590))

            cv2.imshow('Show', frame)
            if cv2.waitKey(1) == ord('q'):
                break
        cv2.destroyAllWindows()


    def pauseButton(self) -> None:
        print("Button here::::::")

        

currGame = GameRecorder()
currGame.startRecording()
# currGame.pauseButton()
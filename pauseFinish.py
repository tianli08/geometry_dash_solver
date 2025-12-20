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
        cv2.namedWindow("Live", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Live", 480, 270)

        while True:
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            cv2.imshow('Live', frame)

            if cv2.waitKey(100) == ord('q'):
                break
        cv2.destroyAllWindows()


    def pauseButton(self) -> None:
        print("Button here::::::")

        

currGame = GameRecorder()
currGame.startRecording()
# currGame.pauseButton()
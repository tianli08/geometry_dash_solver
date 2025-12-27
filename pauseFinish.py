import pyautogui
import cv2
import numpy as np

class GameRecorder:
    
    def __init__ (self):
        self.screenResolution = (1920, 1080)
        self.screenIsRecording = False
        self.playButtomImg = cv2.imread('./images/play_button.jpg', cv2.IMREAD_UNCHANGED)
        self.cursorPos = None

    def startRecording(self): # Starts a recording and automatically starts level based on the pause screen.
        self.screenIsRecording = True
        trueSizeX, trueSizeY = pyautogui.size()

        # Just for experimentation with window testing, need to setup recording software
        cv2.namedWindow("Show", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Show", 1980, 1020)

        while True:
            # cv2.resizeWindow("Show", 300, 200)
            img = pyautogui.screenshot()
            frame = np.array(img)
            ss_h = frame.shape[0]
            ss_w = frame.shape[1]
            scale_h = trueSizeY / ss_h
            scale_w = trueSizeX / ss_w
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = cv2.matchTemplate(frame, self.playButtomImg, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            # Need frame resizing, changing for proper config on HiDPI, may not need a non version config.
            # frame = cv2.resize(frame, (1280, 720))
            if max_val >= 0.97:
                needle_h = self.playButtomImg.shape[0]
                needle_w = self.playButtomImg.shape[1]
                self.cursorPos = ((max_loc[0] + needle_w/2) * scale_w  , (max_loc[1] + needle_h/2) * scale_h) # Center of top left coord, and bottom right coord
                print(max_loc)
                cv2.rectangle(frame, max_loc, (max_loc[0] + needle_w, max_loc[1] + needle_h), (0, 255, 255), 2)
                cv2.imshow('Show', frame)
                pyautogui.click(self.cursorPos) # Clicks when menu button is visible
            else:
                cv2.imshow('Show', frame)
            if cv2.waitKey(1000) == ord('q'): #Lower delay for now
                break
        cv2.destroyAllWindows()
        # pyautogui.moveTo(self.cursorPos)
        # print(self.cursorPos)


    def pauseButton(self) -> None:
        print(pyautogui.size())

        

currGame = GameRecorder()
currGame.startRecording()
# currGame.pauseButton()
import time
import threading
from robot import Robot
from ps4 import PS4Controller, PS4Axis, PS4Button

class Controller(object):

    def __init__(self):
        self.ps4_controller = PS4Controller()

        self.control_thread = threading.Thread(target=self.control_task)
        self.control_thread.start()



    def control_task(self, name="Control thread"):
        print('Starting control thread')

        self.robo1 = Robot()
        self.robo1.initialize(self.ps4_controller)

        while True:
            if self.ps4_controller.get_button(PS4Button.TRIANGLE):
                # close robot
                self.robo1.close()
                break
            elif self.ps4_controller.get_button(PS4Button.SQUARE):
                # restart robot
                self.robo1 = Robot()
                self.robo1.initialize(self.ps4_controller)
            time.sleep(0.01)
        print('Ending control thread')



if __name__ == '__main__':
    robo1 = Controller()

    # start joystick monitoring
    import pyglet
    pyglet.app.run()

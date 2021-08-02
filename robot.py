import time
import threading
from robomaster import robot
from ps4 import PS4Axis, PS4Button

class Robot(robot.Robot):
    def test__init__(self):
        print('Robot init')

    def close(self):
        self.initialized = False
        time.sleep(0.5)
        super().close()

    def initialize(self, controller, conn_type='sta'): # use sta as default
        self.controller = controller
        while True:
            try:
                if super().initialize(conn_type):
                    self.led.set_gimbal_led(comp='all', r=255, g=255, b=255, led_list=[0,1,2,3,4,5,6,7], effect='on')
                    for i in range(1):
                        for led in range(0, 8):
                            self.led.set_gimbal_led(comp='all', r=255, g=255, b=255, led_list=[led], effect='on')
                            time.sleep(0.03)
                    self.led.set_gimbal_led(comp='all', r=255, g=255, b=255, led_list=[0,1,2,3,4,5,6,7], effect='on')

                    break
            except Exception as ex:
                print('Could not connect to robot. Retrying.' + str(ex))
                time.sleep(3)

        #self.gimbal.recenter().wait_for_completed()
        self.set_robot_mode(mode=robot.FREE)
        #self.set_robot_mode(mode=robot.GIMBAL_LEAD)
        #self.set_robot_mode(mode=robot.CHASSIS_LEAD)

        #
        # Start threads
        #
        self.initialized = True

        self.chassis_thread = threading.Thread(target=self.chassis_task)
        self.chassis_thread.start()

        self.gimbal_thread = threading.Thread(target=self.gimbal_task)
        self.gimbal_thread.start()

        #self.uart_listener = threading.Thread(target=self.uart_listen)
        #self.uart_listener.start()


    def chassis_task(self, name="Chassis thread"):
        print('Starting chassis thread')
        while True and self.initialized:
            l2 = (self.controller.get_axis(PS4Axis.L2) + 2) # speed of x,y axis
            r2 = (self.controller.get_axis(PS4Axis.R2) + 2) # speed of z axis

            x_val = self.controller.get_axis(PS4Axis.LEFT_X) * l2           # x axis
            y_val = self.controller.get_axis(PS4Axis.LEFT_Y) * l2           # y axis
            z_val = self.controller.get_axis(PS4Axis.RIGHT_X) * r2 * 200.0  # z azis

            if self.controller.get_button(PS4Button.L1):
                # gimbal moving, keep z axis at 0 to prevent gimbal jitter
                z_val = 0

            self.chassis.drive_speed(x=-y_val, y=x_val, z=z_val, timeout=0.25)

            time.sleep(0.1)
        print('Ending chassis thread')

    def gimbal_task(self, name="Gimbal thread"):
        print('Starting gimbal thread')
        while True and self.initialized:
            try:
                if self.controller.get_button(PS4Button.R1):
                    # quick recenter
                    self.gimbal.moveto(pitch=0, yaw=0, pitch_speed=540, yaw_speed=540).wait_for_completed()
                elif not self.controller.get_button(PS4Button.L1):
                    # chassis turning, keep stationary
                    time.sleep(0.1)
                else:
                    # move gimbal
                    pitch = round(-self.controller.get_axis(PS4Axis.RIGHT_Y) * 30, 2)
                    yaw = round(self.controller.get_axis(PS4Axis.RIGHT_X) * 90, 2)
                    self.gimbal.move(pitch=pitch, yaw=yaw, pitch_speed=30, yaw_speed=90).wait_for_completed()
            except Exception as ex:
                print(ex)
        print('Ending gimbal thread')

    #def uart_listen(self, name="UART Listener"):
    #    self.uart.serial_send_msg('test')
    #    self.uart.sub_serial_msg(self.uart_callback, None, None)

    #def uart_callback(self, data, *args, **kwargs):
    #    print('called')
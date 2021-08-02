import pyglet
import enum

class PS4Axis(enum.Enum):
    LEFT_X      = 'x'
    LEFT_Y      = 'y'
    RIGHT_X     = 'z'
    RIGHT_Y     = 'rz'
    L2          = 'rx'
    R2          = 'ry'

class PS4Button(enum.Enum):
    SQUARE      = 0
    X           = 1
    CIRCLE      = 2
    TRIANGLE    = 3
    L1          = 4
    R1          = 5
    L2          = 6
    R2          = 7
    SHARE       = 8
    OPTIONS     = 9
    STICK_LEFT  = 10
    STICK_RIGHT = 11
    PS          = 12
    PAD         = 13

class PS4Controller(object):
    def __init__(self):
        # initalize axis
        self.axis_data = {}
        for label in PS4Axis:
            self.axis_data[label] = 0.0

        # initialize buttons
        self.button_data = {}
        for label in PS4Button:
            self.button_data[label] = False

            # initialize joystick 0
            joysticks = pyglet.input.get_joysticks()
            if joysticks:
                self.joystick = joysticks[0]
                self.joystick.open()

                # register handlers
                self.joystick.push_handlers(
                    self.on_joybutton_press,
                    self.on_joybutton_release,
                    self.on_joyhat_motion,
                    self.on_joyaxis_motion
                )
            else:
                print('No joystick connected')

    def on_joybutton_press(self, joystick, button):
        self.button_data[PS4Button(button)] = True

    def on_joybutton_release(self, joystick, button):
        self.button_data[PS4Button(button)] = False

    def on_joyhat_motion(self, joystick, hat_x, hat_y):
        #print(hat_x, hat_y)
        pass

    def on_joyaxis_motion(self, joystick, axis, value):
        value = round(value, 2)
        if abs(value) < 0.1:
            value = 0.0
        self.axis_data[PS4Axis(axis)] = value

    def get_axis(self, axis):
        value = 0.0
        if abs(self.axis_data[axis]) > 0.1:
            value = self.axis_data[axis]
        return value

    def get_button(self, button):
        value = False
        if self.button_data[button]:
            value = self.button_data[button]
        return value

# debug
#ps4 = PS4Controller()
#pyglet.app.run()
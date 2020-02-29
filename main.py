import pyfirmata
import time
from audio import audio_controller
from manage_COM_ports import serial_ports



'''
ARDUINO NANO:
LED are hooked up to digital pin 2,3 and 4
button is hooked up to pin 5
rotary encoder is hooked up to pin 6 and 7
'''

class Encoder():
    def __init__(self):
        self.encoder_C = board.digital[5] # button
        self.encoder_A = board.digital[6] # encoder A
        self.encoder_B = board.digital[7] # encoder B
        self.encoder_A.mode = pyfirmata.INPUT
        self.encoder_B.mode = pyfirmata.INPUT
        self.encoder_C.mode = pyfirmata.INPUT
        self.leds = [
            board.digital[2],
            board.digital[3],
            board.digital[4],
        ]
        self.counter = 0
        self.function = 1 #  0 - vol by proccess, 1 - master vol
        self.toggle_mute = False
        self.btn_state = False

        # sequence and state for encoder management
        self.rotation_state =  [False, False]
        self.sequence = [
            [False, False],
            [False, False],
        ]
        self.up_sequence = [[False,False],[False, True]]
        self.down_sequence = [[False,False],[True, False]]

    def manage_state(self):
        # update sequence status
        if self.rotation_state != [self.encoder_A.read(),self.encoder_B.read()]:
            #self.counter += 1
            self.rotation_state = [self.encoder_A.read(),self.encoder_B.read()]
            self.sequence = [
                self.sequence[1],
                self.rotation_state
            ]
            self.react_rotation()

        # manage button press
        if self.encoder_C.read() == 1:
            self.react_button()

    def react_rotation(self):
        # process volume up and down by proccess
        if self.function ==0 :
            if self.sequence == self.up_sequence:
                audio_controller.increase_volume(0.04)
            if self.sequence == self.down_sequence:
                audio_controller.decrease_volume(0.04)
        #master volume up and down
        if self.function == 1:
            if self.sequence == self.up_sequence:
                audio_controller.increase_master_volume(0.4)
            if self.sequence == self.down_sequence:
                audio_controller.decrease_master_volume(0.4)

    def react_button(self):
        # sleep to check if button is pressed and hold down
        time.sleep(.5)
        if self.encoder_C.read() != True:
            #REACT SHORT PRESS
            if self.toggle_mute == False:
                audio_controller.mute()
                self.toggle_mute = True
                time.sleep(.2)
            else:
                audio_controller.unmute()
                self.toggle_mute = False
                time.sleep(.2)
        else:
            #REACT OF LONG PRESS
            self.function = self.function + 1 if self.function < 1 else 0
            self.blink()

    def blink(self, led_nr=None):
        led_nr = self.function if led_nr == None else led_nr
        for temp_led in self.leds:
            temp_led.write(0)
        for i in range(10):
            self.leds[led_nr].write(1)
            time.sleep(.02)
            self.leds[led_nr].write(0)
            time.sleep(.02)

if __name__ == '__main__':
    ports = serial_ports()
    board = None
    for port in ports:
        print(port)
        try:
            board = pyfirmata.Arduino('/{}'.format(port))
            break
        except Exception as e:
            print(e)
    if board == None:
        print('cant find the board')
        exit()

    it = pyfirmata.util.Iterator(board)
    it.start()
    encoder = Encoder()
    print('Volume Controll Ready.')
    while True:
        encoder.manage_state()

from kivy.app import App
from kivy.core.window import Window
try:
    import relay_modbus
    import relay_boards
    from relay_boards.R4D3B16 import NUM_RELAYS as R4D3B16_NUM_RELAYS
    from relay_boards.R4D3B16 import NUM_ADDRESSES as R4D3B16_NUM_ADDRESSES
except:
    R4D3B16_NUM_RELAYS = 16
    pass

from kivy.properties import ListProperty


SERIAL_PORT = '/dev/ttyUSB0'
RELAY_BOARD1_ADDRESS = 1
RELAY_BOARD2_ADDRESS = 2
VERBOSE = True

class MockRelayBoard():
    states = [0] * R4D3B16_NUM_RELAYS
    def __init__(self):
        pass

    def get_status(self, relay):
        return self.states[relay - 1]

    def on(self, relay):
        self.states[relay - 1] = 1

    def off(self, relay):
        self.states[relay - 1] = 0


class OzJigTestApp(App):
    _modbus = None
    relays1 = ListProperty([0] * R4D3B16_NUM_RELAYS)
    relays2 = ListProperty([0] * R4D3B16_NUM_RELAYS)

    def build(self):
        # Create relay_modbus object
        try:
            self._modbus = relay_modbus.Modbus(SERIAL_PORT, verbose=VERBOSE)
            self._modbus.open()
            # Create relay board object
            self._relay_board1 = relay_boards.R4D3B16(self._modbus,
                                                address=RELAY_BOARD1_ADDRESS,
                                                verbose=VERBOSE)
            self._relay_board2 = relay_boards.R4D3B16(self._modbus,
                                                address=RELAY_BOARD2_ADDRESS,
                                                verbose=VERBOSE)
        except Exception as e:
            print('Error: Cannot open serial port: ' + SERIAL_PORT)
            self._relay_board1 = MockRelayBoard()
            self._relay_board2 = MockRelayBoard()

    def on_start(self):
        Window.size = (1024, 600)
        try:
            for i in range(0, R4D3B16_NUM_RELAYS):
                self.relays1[i] = self._relay_board1.get_status(i + 1)
                self.relays2[i] = self._relay_board2.get_status(i + 1)
        except Exception as e:
            print(e)

    def on_stop(self):
        if self._modbus:
            self._modbus.close()

    def state_change(self, relay, channel, state):
        print('Relay {} channel {} state {}'.format(relay, channel, state))
        if relay == 0:
            if state == 'down':
                self._relay_board1.on(channel + 1)
            else:
                self._relay_board1.off(channel + 1)
        else:
            if state == 'down':
                self._relay_board2.on(channel + 1)
            else:
                self._relay_board2.off(channel + 1)


if __name__ == '__main__':
    OzJigTestApp().run()

from entities import Ship
from entities.plane import Plane
from states.state_machine import StateMachine
from states.ship_states import *


class Carrier(Ship, StateMachine):
    PLANES_COUNT = 6
    SEND_INTERVAL = 60  # box2d iterations (hertz) 1 second
    SEND_STATE = 'send_state'
    IDLE_STATE = 'idle_state'

    def __init__(self, game, vertices=None, density=0.1, position=(0, 0)):
        super(Carrier, self).__init__(game, vertices, density, position)
        StateMachine.__init__(self)
        self.planes = []

    def init_states(self):
        self._states[self.SEND_STATE] = CarrierSendState(self)
        self._states[self.IDLE_STATE] = CarrierIdleState(self)

    @property
    def state_on_init(self):
        return self._states[self.SEND_STATE]

    def to_send_state(self):
        self.switch_state_to(self._states[self.SEND_STATE])

    def to_idle_state(self):
        self.switch_state_to(self._states[self.IDLE_STATE])

    def update(self, keys):
        super(Carrier, self).update(keys)
        self._state.update(keys)

    def can_send_plane(self):
        return len(self.planes) < Carrier.PLANES_COUNT

    def send_plane(self):
        plane = Plane(self, self.game)
        self.planes.append(plane)

    def destroy_plane(self, plane):
        self.planes.pop(self.planes.index(plane))
        plane.destroy()

    def destroy(self):
        for plane in self.planes:
            plane.destroy()

        super(Carrier, self).destroy()

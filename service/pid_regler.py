import numpy as np

class PID_regler(object):

    def __init__(self):
        self.p_roll = 2.9
        self.d_roll = 1.9
        self.p_pitch = -1.9
        self.d_pitch = -2

    def innerLoopAileron(self, rollAngle_Reference, rollAngle_Current, rollAngleRateCurrent, AileronCurrent):
        diff_rollAngle = rollAngle_Reference - rollAngle_Current
        AileronCommand = diff_rollAngle * self.p_roll - rollAngleRateCurrent * self.d_roll
        AileronCommand = AileronCommand + AileronCurrent
        AileronCommand = np.clip(AileronCommand, -1, 1)
        return AileronCommand

    def innerLoopElevator(self, pitchAngleReference, pitchAngleCurrent, pitchAngleRateCurrent, elevatorCurrent):
        errorPitchAngle = pitchAngleReference - pitchAngleCurrent
        elevatorCommand = errorPitchAngle * self.p_pitch - pitchAngleRateCurrent * self.d_pitch
        elevatorCommand = elevatorCommand + elevatorCurrent
        elevatorCommand = np.clip(elevatorCommand, -1, 1)
        return elevatorCommand
from core.simulation import Simulation
import numpy as np
import pandas as pd
from bokeh.plotting import figure, output_file, save
from _datetime import datetime

if __name__ == "__main__":
    df = pd.DataFrame(columns=['phi', 'u'])
    #todo: put to toml

    def plot(df):
        TOOLTIPS = [
            ("Name", '$name'),
            ("index", "$index"),
            ("Wert", "$y")]

        p = figure(title="simple line example", x_axis_label='Datapoints', y_axis_label='Data', tooltips=TOOLTIPS)
        p.line(df['phi'].index.values, df['phi'], line_width=2,
               legend_label='phi', name='phi', color="red")
        p.line(df['theta'].index.values, df['theta'], line_width=2,
               legend_label='theta', name='theta', color="green")
        p.line(df['u'].index.values, df['u'], line_width=2,
               legend_label='u', name='u', color="blue")
        output_file("./tests/plot.html")
        save(p)


    p_roll = 2.9
    d_roll = 1.9
    p_pitch = -1.9
    d_pitch = -2

    # innerLoop: heading_roll->Aileron
    def _innerLoopAileron(rollAngle_Reference, rollAngle_Current, rollAngleRateCurrent, AileronCurrent):
        diff_rollAngle = rollAngle_Reference - rollAngle_Current
        AileronCommand = diff_rollAngle * p_roll - rollAngleRateCurrent * d_roll
        AileronCommand = AileronCommand + AileronCurrent
        AileronCommand = np.clip(AileronCommand, -1, 1)
        return AileronCommand

    def _innerLoopElevator(pitchAngleReference, pitchAngleCurrent, pitchAngleRateCurrent, elevatorCurrent):
        errorPitchAngle = pitchAngleReference - pitchAngleCurrent
        elevatorCommand = errorPitchAngle * p_pitch - pitchAngleRateCurrent * d_pitch
        elevatorCommand = elevatorCommand + elevatorCurrent
        elevatorCommand = np.clip(elevatorCommand, -1, 1) - 0.1
        return elevatorCommand

    sim = Simulation()
    result = sim.run()
    sim.set_controls('fcs/throttle-cmd-norm', 0)
    i = 0
    state = ""
    before = datetime.now()
    while result and sim.jsbsim.get_sim_time() <= 50:
        #print(i)
        state = sim.get_state()
        if i%5==0:
            sim.set_controls('fcs/aileron-cmd-norm', _innerLoopAileron(np.deg2rad(10), state['phi'], state['p'],
                                                                       sim.jsbsim.get_property_value(
                                                                           'fcs/aileron-cmd-norm')))
            sim.set_controls('fcs/elevator-cmd-norm', _innerLoopElevator(np.deg2rad(-7), state['theta'], state['q'],
                                                                         sim.jsbsim.get_property_value(
                                                                             'fcs/elevator-cmd-norm')))
        sim.run()
        #print(np.rad2deg(state['phi']))
        df = df.append({'u': state['u'], 'phi': np.rad2deg(state['phi']), 'theta': np.rad2deg(state['theta'])}, ignore_index=True)

        i += 1
    after = datetime.now()
    dt = (after - before)
    print(dt)
    sim.close()
    plot(df)






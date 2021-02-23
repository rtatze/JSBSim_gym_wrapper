from core.simulation import Simulation
import numpy as np
import pandas as pd
from bokeh.plotting import figure, output_file, save
from _datetime import datetime

from services import pid_regler

if __name__ == "__main__":
    pid = pid_regler.PID_regler()
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
        p.line(df['rpm'].index.values, df['rpm'], line_width=2,
               legend_label='rpm', name='rpm', color="black")
        output_file("plot.html")
        save(p)


    sim = Simulation()
    result = sim.run()
    sim.set_properties('propulsion/starter_cmd', 1)
    sim.set_properties('propulsion/engine/set-running', 1)
    sim.set_properties('propulsion/magneto_cmd', 2.0)
    sim.set_properties('fcs/mixture-cmd-norm', 0.87)
    sim.set_properties('fcs/throttle-cmd-norm', 1.0)
    i = 0
    state = ""
    before = datetime.now()
    while result and sim.jsbsim.get_sim_time() <= 50:
        #print(i)
        state = sim.get_state()
        sim.set_properties('fcs/throttle-cmd-norm', 0.99)
        sim.set_properties('fcs/mixture-cmd-norm', 0.87)
        if i%5==0:
            sim.set_properties('fcs/aileron-cmd-norm', pid.innerLoopAileron(np.deg2rad(5), state['phi'], state['p'],
                                                                            sim.jsbsim.get_property_value(
                                                                           'fcs/aileron-cmd-norm')))
            sim.set_properties('fcs/elevator-cmd-norm', pid.innerLoopElevator(np.deg2rad(0), state['theta'], state['q'],
                                                                              sim.jsbsim.get_property_value(
                                                                             'fcs/elevator-cmd-norm')))
        sim.run()
        #print(np.rad2deg(state['phi']))
        df = df.append({'u': state['u']*0.51444, 'phi': np.rad2deg(state['phi']), 'theta': np.rad2deg(state['theta']), 'rpm': sim.get_properties('propulsion/engine/propeller-rpm')}, ignore_index=True)

        i += 1
    after = datetime.now()
    dt = (after - before)
    print(dt)
    sim.close()
    plot(df)






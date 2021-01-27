import time
import jsbsim
import toml
import sys
sys.path.append('..')
sys.path.append('.')
from core.aircraft import Aircraft, cessna172P
init_configuration = toml.load('./config/init_configuration.toml')
lokal_configuration = toml.load('./lokal_config/lokal_configuration.toml') # included: '/Users/######/Programme/jsbsim-code' #an System anpassen.

class Simulation(object):
    """
    A class which wraps an instance of JSBSim and manages communication with it.
    """
    encoding = 'utf-8'  # encoding of bytes returned by JSBSim Cython funcs
    OUTPUT_FILE = 'flightgear.xml'
    LONGITUDINAL = 'longitudinal'
    FULL = 'full'

    def __init__(self,
                 sim_frequency_hz: float = init_configuration['simulation']['jsbsim_dt_hz'],
                 aircraft: Aircraft = cessna172P):
        self.jsbsim = jsbsim.FGFDMExec(lokal_configuration['simulation']['path_jsbsim'])
        self.jsbsim.set_debug_level(0)
        self.sim_dt = 1.0 / sim_frequency_hz
        self.wall_clock_dt = 0
        self.initialise(aircraft)

    def initialise(self, aircraft: Aircraft):
        self.load_model(aircraft.jsbsim_id)
        self.jsbsim.set_dt(self.sim_dt)
        self.set_custom_initial_conditions(init_configuration)

    def load_model(self, model_name: str) -> None:
        load_success = self.jsbsim.load_model(model_name)
        if not load_success:
            raise RuntimeError('JSBSim could not find specified model_name: ' + model_name)

    def set_custom_initial_conditions(self, init_conditions) -> None:
        if init_conditions is not None:
            for prop, value in init_conditions['simulation']['initial_state'].items():
                self.jsbsim.set_property_value(prop, value)
        no_output_reset_mode = 0
        self.jsbsim.reset_to_initial_conditions(no_output_reset_mode)

    def reset_with_initial_condition(self) -> None:
        for prop, value in init_configuration['simulation']['initial_state'].items():
            self.jsbsim.set_property_value(prop, value)
        no_output_reset_mode = 0
        self.jsbsim.reset_to_initial_conditions(no_output_reset_mode)

    def get_state(self):
        state_keys = ["u", "v", "w", "lat", "long", "h", "p", "q", "r", "phi", "theta", "psi"]
        state_values = [
            self.jsbsim.get_property_value('velocities/u-fps'), self.jsbsim.get_property_value('velocities/v-fps'), \
            self.jsbsim.get_property_value('velocities/w-fps'), self.jsbsim.get_property_value('position/lat-gc-deg'), \
            self.jsbsim.get_property_value('position/long-gc-deg'), self.jsbsim.get_property_value('position/h-sl-meters'), \
            self.jsbsim.get_property_value('velocities/p-rad_sec'), self.jsbsim.get_property_value('velocities/q-rad_sec'), \
            self.jsbsim.get_property_value('velocities/r-rad_sec'), self.jsbsim.get_property_value('attitude/phi-rad'), \
            self.jsbsim.get_property_value('attitude/theta-rad'), self.jsbsim.get_property_value('attitude/psi-rad')
        ]
        state_dict = dict(zip(state_keys, state_values))
        return state_dict

    def set_properties(self, control_name, control_value):
        self.jsbsim[control_name] = control_value

    def get_properties(self, prop):
        return self.jsbsim.get_property_value(prop)

    def run(self) -> bool:
        result = self.jsbsim.run()
        if self.wall_clock_dt is not None:
            time.sleep(self.wall_clock_dt)
        return result

    def close(self):
        if self.jsbsim:
            self.jsbsim = None


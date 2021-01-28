import os

import toml
import jsbsim

configuration = toml.load('../config/default_configuration.toml') # included: '/Users/######/Programme/jsbsim-code' #an System anpassen.
sim = jsbsim.FGFDMExec(os.path.expanduser(configuration["simulation"]["path_jsbsim"]))
sim.load_model('c172p')

print(sim.print_property_catalog())
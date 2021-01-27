import toml
import jsbsim


init_configuration = toml.load('init_configuration.toml')
local_configuration = toml.load('./local_config/local_configuration.toml') # included: '/Users/######/Programme/jsbsim-code' #an System anpassen.
sim = jsbsim.FGFDMExec(local_configuration['simulation']['path_jsbsim'])
sim.load_model('c172p')

print(sim.print_property_catalog())
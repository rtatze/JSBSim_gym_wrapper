import toml
import jsbsim


init_configuration = toml.load('init_configuration.toml')
lokal_configuration = toml.load('./lokal_config/lokal_configuration.toml') # included: '/Users/######/Programme/jsbsim-code' #an System anpassen.
sim = jsbsim.FGFDMExec(lokal_configuration['simulation']['path_jsbsim'])
sim.load_model('c172p')

print(sim.print_property_catalog())
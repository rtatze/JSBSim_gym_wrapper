import toml
import jsbsim


init_configuration = toml.load('init_configuration.toml')
sim = jsbsim.FGFDMExec(init_configuration['simulation']['path_jsbsim'])
sim.load_model('c172p')

print(sim.print_property_catalog())
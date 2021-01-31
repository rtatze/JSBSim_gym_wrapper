# Flugdynamisches Modell (FDM) als gym-Environment mit JSBSim

Das Projektziel ist, einen einfachen Wrapper für ein gym-Environment (openAI) zu implementieren.

Bestehende Projekte zur Umsetzung dieses Projektziel sind zwar vorhanden, aber zum Teil zu komplex für einfache Prototypen.

genutzt wird das Flugdynamische Modell (FDM) JSBSim: https://github.com/JSBSim-Team/jsbsim

# Beispiel
Ein Beispiel liegt im `example` Ordner
```
import gym
import numpy as np
from gym_wrapper.jsbsimgymenvironmentwrapper import JsbsimGymEnvironmentWrapper

configuration_path="../config/default_configuration.toml"

env = JsbsimGymEnvironmentWrapper(configuration_path=configuration_path)

throttle = 0
time_step_sec = 0
while time_step_sec <= 30:
    print("time_step_sec: ", time_step_sec)
    #env.render() # comment render() for faster training
    action = env.action_space.sample()
    state, rewards, dones, _ = env.step([np.array([action])],)
    time_step_sec = env.sim.get_properties('simulation/sim-time-sec')
    print("state", state)
```
# Ablauf der Installation
###1. Installation JSBSim:
Beschreibungen für verschiedene Rechnersystem (Windows, Mac, Linux) sind unter:<br>
   https://jsbsim-team.github.io/jsbsim-reference-manual/mypages/quickstart-building-the-program/
   
###2. Installation der Python Bibliothek jsbsim:

```
pip install jsbsim
```

###3. Klonen von jsbsim: 
```
git clone https://github.com/JSBSim-Team/jsbsim
```

###4. Testen der JSBSim-Umgebung
```
import jsbsim

path_jsbsim = '/PFAD_ZU_JSBSIM_ORDNER/jsbsim' #an System anpassen.

sim = jsbsim.FGFDMExec(path_jsbsim)
sim.load_model('c172p')

print(sim.print_property_catalog())

result = sim.run()

while result and sim.get_sim_time() <= 3:
    print(sim.get_property_value('velocities/u-fps'))
```
### 5. Installation von JSBSim-gym-wrapper
Klonen des https://github.com/rtatze/JSBSim_gym_wrapper repos:

```
git clone https://github.com/rtatze/JSBSim_gym_wrapper
```
Installation des Paketes: (-e steht für editor mode)
```
cd JSBSIM_gym_wrapper
python3 -m pip install -e .
```

### 6. Struktur des gym-Wrappers

a) die Schnittstelle zur Anbindung an JSBSim wird durch die Datei **simulation** bzw. die Klasse **Simulation** realisiert. Die folgenden Methoden sind implementiert:

* run():
das FDM (JSBSim) macht einen Zeitschritt.
  
* get_state()
die 12 Zustandswerte des FDM werden zurück gegeben
  
* set_properties()
der jeweilige Parameter des FDM wird gesetzt
  
* get_properties()
der jeweilige Parameter des FDM wird gelesen
  
b) die Klasse/Datei **Jsbsim_gym_environment_wrapper** ummantelt (Wrapper) die Simulation des FDM

im Sinne der Struktur von openAI sind u. a. die Methoden: 

* reset
* step

implementiert






# Erstellen eines Docker-Images


# Cite as:
@misc{Titze2021,
  author = {Titze, Rene},
  title = {JSBSim_wrapper},
  year = {2021},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/rtatze/JSBSim_gym_wrapper}}
}

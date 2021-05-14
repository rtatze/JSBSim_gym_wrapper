# Flugdynamisches Modell (FDM) als gym-Environment mit JSBSim

Das Projektziel ist es, einen einfachen Wrapper für ein gym-Environment (openAI) zu implementieren.

Bestehende Projekte zur Umsetzung dieses Projektziels sind zwar vorhanden, aber zum Teil zu komplex für einfache Prototypen.

Grundlage der Implementierung ist das flugdynamische Modell aus folgendem Repository: [gym-jsbsim](https://github.com/Gor-Ren/gym-jsbsim)

Description: [Working-Paper](https://www.researchgate.net/publication/349039926_Working_Paper_Configuration_and_use_of_the_flight_dynamic_model_-_JSBSim_-_as_a_reinforcement_learning_environment)

<!-- TOC -->

- [Beispiel](#beispiel)
- [Ablauf der Installation](#ablauf-der-installation)
    - [Installation JSBSim:](#installation-jsbsim)
    - [Installation der Python Bibliothek jsbsim:](#installation-der-python-bibliothek-jsbsim)
    - [Klonen von jsbsim:](#klonen-von-jsbsim)
    - [Testen der JSBSim-Umgebung](#testen-der-jsbsim-umgebung)
    - [Installation von JSBSim-gym-wrapper](#installation-von-jsbsim-gym-wrapper)
    - [Struktur des gym-Wrappers](#struktur-des-gym-wrappers)
- [Erstellen eines Docker-Images](#erstellen-eines-docker-images)

<!-- /TOC -->
# Beispiel

Folgendes Beispiel zeigt eine einfache Implementierung eines Random-Agent

```Python
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
### 1. Installation JSBSim:

Beschreibungen für verschiedene Rechnersystem (Windows, Mac, Linux) sind unter:
<br>
   [jsbsim: quickstart-building-the-program](https://jsbsim-team.github.io/jsbsim-reference-manual/mypages/quickstart-building-the-program/)
   
### 2. Installation der Python Bibliothek jsbsim:

```
pip install jsbsim
```

### 3. Klonen von jsbsim: 
```
git clone https://github.com/JSBSim-Team/jsbsim
```

### 4. Testen der JSBSim-Umgebung
```Python
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
Klonen des [JSBSim_gym_wrapper](https://github.com/rtatze/JSBSim_gym_wrapper) repos:

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

Gute Referenzen:

https://github.com/JSBSim-Team/jsbsim-reference-manual/blob/master/docs/_mypages/Jupyter_Notebooks/python/property_map.py




# Erstellen eines Docker-Images

es werden 2 Dockerfiles vorgestellt. Mit dem ersten Dockerfile wird die Basis für ein Image des JSBSim_gym_wrapper 
erstellt. Das zweite Dockerfile zeigt eine Beipsielausführung eines Tests.

1. Dockerfile für die Basis
```dockerfile
# aufbauend auf einem Linux-Image mit Python
FROM python:latest

# JSBSim wird in ein zusätzliches Verzeichnis kopiert
RUN mkdir -p ${CODE_DIR}/JSBSim_gym_wrapper
RUN git clone https://github.com/JSBSim-Team/jsbsim.git

# das gesamte Verzeichnis und Abhängigkeiten werden in das Image kopiert
ADD . ${CODE_DIR}/JSBSim_gym_wrapper
RUN pip install -e ./JSBSim_gym_wrapper

# das Arbeitsverzeichnis ist root
WORKDIR ${CODE_DIR}/JSBSim_gym_wrapper
RUN echo "$PWD"
```
erstellt wird das Image: JSBSim_Basis


2. Dockerfile für eine Beispielanwendung auf Basis des oben (unter 1) erstellten Images:
```dockerfile
# aufbauend auf dem Basis-Image
FROM jsbsim_basis:latest

# wechsel in das Verzeichnis mit dem Beipsiel:
WORKDIR ${CODE_DIR}/JSBSim_gym_wrapper/example

# Ausführung der Beipsielanwendung
CMD [ "python", "random_actions.py" ]
```

ACHTUNG: da nun der JSBSim-Code im Image innerhalb des Verzeichnisses jsbsim liegt, muss die Configuration geändert werden:

```Python
#path_jsbsim = '~/Programme/jsbsim-code' ### path to jsbsim folder
path_jsbsim = '../jsbsim' # Für Dockercontainer
```

Cite as:
@misc{Titze2021,
  author = {Titze, Rene},
  title = {JSBSim_wrapper},
  year = {2021},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/rtatze/JSBSim_gym_wrapper}}
}

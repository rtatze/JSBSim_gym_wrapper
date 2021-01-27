# Flugdynamisches Modell (FDM) als gym-Environment mit JSBSim

Das Projektziel ist, einen einfachen Wrapper für ein gym-Environment (openAI) zu implementieren.

Bestehende Projekte zur Umsetzung dieses Projektziel sind zwar vorhanden, aber zum Teil zu komplex für einfache Prototypen.

Grundlage der Implementierung ist das folgenden Repository: https://github.com/Gor-Ren/gym-jsbsim

genutzt wird das Flugdynamische Modell (FDM) JSBSim: https://github.com/JSBSim-Team/jsbsim


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
```
python3 -m pip install git+https://github.com/rtatze/JSBSim_gym_wrapper
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

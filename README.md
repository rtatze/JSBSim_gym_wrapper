# Flugdynamisches Modell (FDM) als gym-Environment mit JSBSim

Das Projektziel ist, einen einfachen Wrapper für ein gym-Environment (openAI) zu implementieren.

Bestehende Projekte zur Umsetzung dieses Projektziel sind zwar vorhanden, aber zum Teil zu komplex für einfache Prototypen.

Grundlage der Implementierung ist das folgenden Repository: https://github.com/Gor-Ren/gym-jsbsim

genutzt wird das Flugdynamische Modell (FDM) JSBSim: https://github.com/JSBSim-Team/jsbsim


# Ablauf der Installation
1. Installation JSBSim:
Beschreibungen für verschiedene Rechnersystem (Windows, Mac, Linux) sind unter:<br>
   https://jsbsim-team.github.io/jsbsim-reference-manual/mypages/quickstart-building-the-program/
  
 
2. Installation der Python Bibliothek jsbsim: <br>
```
pip install jsbsim
```


3. Testen der JSBSim-Umgebung
```
import jsbsim

path_jsbsim = '/Users/########/Programme/jsbsim-code' #an System anpassen.

sim = jsbsim.FGFDMExec(path_jsbsim)
sim.load_model('c172p')

print(sim.print_property_catalog())

result = sim.run()

while result and sim.jsbsim.get_sim_time() <= 3:
    print(sim.get_property_value('velocities/u-fps'))
```

4. Struktur des gym-Wrappers

a) die Schnittstelle zur Anbindung an JSBSim wird durch die Datei **simulation** bzw. die KLasse **Simulation** realisiert. Die folgenden Methoden sind implementiert:

* run():
das FDM (JSBSim) macht einen Zeitschritt.
  
* get_state()
die 12 Zustandswerte des FDM werden zurück gegeben
  
* set_controls()
der jeweilige Parameter des FDM wird gesetzt
  
b) die Klasse/Datei **Jsbsim_gym_environment_wrapper** ummantelt (Wrapper) die Simulation des FDM

im Sinne der Struktur von openAI sind u. a. die Methoden: 

* reset
* step

implementiert

c) damit das FDM wie ein openAI-Environment genutzt werden kann, ist die Klasse Environment implementiert.

Die Klasse wird innerhalb eines RL-Agenten instanziiert mit  






# Erstellen eines Docker-Images

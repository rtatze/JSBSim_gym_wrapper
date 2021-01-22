# Flugdynamisches Modell (FDM) als gym-Environment mit JSBSim

Das Projektziel ist, einen einfachen Wrapper für ein gym-Environment (openAI) zu implementieren.

Bestehende Projekte zur Umsetzung dieses Projektziel sind zwar vorhanden, aber zum Teil zu komplex für einfache Prototypen.

Grundlage der Implementierung ist das folgenden Repository: https://github.com/Gor-Ren/gym-jsbsim

genutzt wird das FDM JSBSim: https://github.com/JSBSim-Team/jsbsim


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




# Erstellen eines Docker-Images

# MasterThesisEMFI
This repository contains simulation code and the PCB layout necessary to reproduce the thesis. 
## Simulation
MagneticFieldSolverTilted simulates magnetic field around a coil using cyllindrical coordinates. Radius of calculated field, height/z of calculated field and resolution can be changed to suit your needs.
PlotFromCsv plots the magnetic field in 3D using matplotlib
TotalFieldThroughCircuit calculates magnetic flux through a PCB trace with two parallel wires with configured spacing. This script is used to get electromotive force induces on trace. An offsetarr can be used to see how moving the coil in x-direction affects the induced electromotive force.
PlotTotalFields plots calculated result from previous script.
Scripts ending with CPW are for Coplanar waveguides and are otherwise similar to the simple trace scripts.
## PCB
### Altium
Contains the Altium project for the custom PCB made for this thesis.
### 3dPrintedHolder
Contains Fusion files for the 3D printed holder to secure the PCB to a 3D printer.

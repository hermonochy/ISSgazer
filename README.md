# ISS gazer

## Purpose

Tool to predict next times when the ISS is flying over your home. Tells you how well it is visible.

Visualizes predicted ISS trajectory on world map. User interaction to predict position for selected times.


## How it works

Latest ISS trajectory data are loaded from [ARISS](https://live.ariss.org/iss.txt).

Takes coordinates (latitude/longitude) of your home.

Predicts orbit of ISS and compiles a list of passover timings.

For each passover, computes how far away from home coordinates and in which direction to look.

## Software dependencies

- [Wrapper for orbit predictor](https://github.com/satellogic/orbit-predictor). Included as git submodule.
- PySimpleGUI and TurtleGraphics for user interaction visualisation.
- [SGP4](https://github.com/brandon-rhodes/python-sgp4) for orbit prediction.


## Install and run



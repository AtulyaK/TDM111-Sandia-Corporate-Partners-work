# Flight Prediction (DMCP) Package

Make sure to load the `tdm` and `python/sandia` modules on Anvil! 😄✈️

This package contains work from The Data Mine Corporate Partners Sandia team. We are interested in predicting the destination of a flight trajectory given an incomplete locational history. We take into consideration historical flight patterns by storing the information in a raster-like grid. Comparing the flight of interest to this historical grid produces a destination likelihood list.

To run the code, execute `python3 conductor.py` from the `src/` directory.
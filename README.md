# Flight Prediction (DMCP) Package

## Overview
This package contains work from The Data Mine Corporate Partners Sandia team. Our primary objective is to predict the destination of a flight trajectory given an incomplete locational history. We achieve this by considering historical flight patterns, which are stored in a raster-like grid (minimum dimensions of 2, lattitude and longitude). The prediction process involves comparing the flight of interest to this historical grid to produce a destination likelihood list.

## Features
- Prediction of flight destinations based on partial trajectory data
- Utilization of historical flight patterns
- Storage of flight data in a raster-like grid structure
- Comparison algorithm to generate destination likelihood

## Usage
To run the code, navigate to the `src/` directory and execute:
`python3 conductor.py`
## Project Structure
(Brief description of the project's folder structure and main files)
The project's main program is in the src folder. The other folders were used for data exploration and data analysis.

## Contributors
Mentors: Dr. Andy Ward and Dr. Kat Ward of Sandia National Labs
TA's : Bryce Castle, and Sean Lee
Students: Ishaan Agrawal, Connor Federoff, Ishaan Handa, Shash Karthikeyan, Atulya Kadur, Kush Khanna, Hersh Thakkar, Arnav Wadhwa​

## License
This project is licensed under the MIT License. See the LICENSE file for details.


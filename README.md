# raspy
Python interface for HEC-RAS.  RAS + Python = raspy.

This is developed primarily for use with [raspy-cal](https://github.com/quantum-dan/raspy-cal), an automatic calibrator for HEC-RAS.  However, it could be used for any other HEC-RAS automation project.  See [PyRAS](https://pypi.org/project/PyRAS/) and the paper "[Application of Python Scripting Techniques for Control and Automation of HEC-RAS Simulations](https://www.mdpi.com/2073-4441/10/10/1382)" for similar ideas.

# Usage

This section will be filled in once functionality has been implemented.

# Functionality
Raspy does or will implement the following functionality.  Functionality is not yet implemented unless it is marked as such in the list below.  Functionality is implemented through the HEC-RAS API where possible, or failing that through the direct manipulation of HEC-RAS files (as in [PyRASFile](https://github.com/LARFlows/PyRASFile)).

## HEC-RAS Interface

That is, what HEC-RAS interactions will be supported.

* Flow boundary conditions specification
    * Unsteady flow timeseries
    * Steady flow rates [partial support through PyRASFile]
    * Other boundary conditions, e.g. normal depth [partial support through PyRASFile]
* Modification of numerical geometric parameters, e.g. Manning's n
* Simulation results retrieval [partial, very inefficient, support through PyRASFile]
* Project geometry information retrieval, e.g. cross section spacing [minimal, awkward, support through PyRASFile]
* Running HEC-RAS simulations

Combined, this set of capabilities permits fully automated use of HEC-RAS once geometry has been specified, which can be used to support calibration as well as other applications (e.g. testing a wide range of flow inputs).

## Raspy External Interface

That is, what means for other programs to interface with Raspy will be supported.  Aside from the Python module, these are longer-term goals, since the immediate objective is for use by an automatic calibrator which will also be written in Python.

* Abstraction layer for use as a module by other Python programs
* R interface to the abstraction layer (using Reticulate)
* Text input files for generic control by any program

This set of capabilities permits the above-described HEC-RAS interface to be easily used by any program even if that program does not fit one of the direct interfaces (Python or R), facilitating easy extensibility for unforeseen applications or methods.
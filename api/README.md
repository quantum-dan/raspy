This directory contains the high-level interface for other programs to
make easy use of raspy, including direct use from Python, the R interface
with Reticulate, and use via text files and command line arguments.

In some cases it may just wrap lower-level functions without actually
doing anything extra in order to provide a unified abstraction layer
in case later modification is necessary.

The general idea is to define all relevant functions in the modules,
then wrap these in a single API class that has all necessary functionality
and can be passed to raspy-cal or other users.  This will allow programs
that use this library to be written in a somewhat library-agnostic manner,
requiring only that the relevant methods be available with the correct
arguments and return types.

Initially, only the priority functionality will be implemented, with
other functionality as a longer-term goal.

## General Functionality

* Running HEC-RAS
	* Open project
	* Set plan, geometry, etc
	* Run
	* Close project
* Data retrieval
	* Flow data from any or all nodes (as in HEC-RAS Report output)
	* Rating curves
	* Numerical geometry data
* Setting parameters
	* Flow data
	* Numerical geometric parameters
	* Launch HEC-RAS editors for things that need to be graphically edited

### Priorities for use in raspy-cal

The top priorities that will be implemented first are:

* Running HEC-RAS (all)
* Data retrieval
	* Flow data: flow rate, velocity, and stage
	* Numerical geometry data: Manning's n
* Setting parameters
	* Flow data
	* Numerical geometric parameters: Manning's n
	
These features will be sufficient to support automatic calibration in raspy-cal,
while leaving the project easy to extend for other functionality.
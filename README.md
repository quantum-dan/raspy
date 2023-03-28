# raspy
Python interface for HEC-RAS.  RAS + Python = raspy.

This can be installed on pip/PyPI as [raspy-auto](https://pypi.org/project/raspy-auto/).

This is developed primarily for use with [raspy-cal](https://github.com/quantum-dan/raspy-cal), an automatic calibrator for HEC-RAS.  However, it could be used for any other HEC-RAS automation project.  See [PyRAS](https://pypi.org/project/PyRAS/) and the paper "[Application of Python Scripting Techniques for Control and Automation of HEC-RAS Simulations](https://www.mdpi.com/2073-4441/10/10/1382)" for similar ideas.

# HEC-RAS Versions

It is now straightforwardly possible to specify different HEC-RAS versions when
creating a `Ras` object.  There is now a second, optional argument `which` specifying
a HEC-RAS version string, which is the version number with no periods.  The
default is `"507"`, specifying HEC-RAS 5.0.7.  To use the current default download
as of this writing, 6.3.1, use `Ras(projectPath, "631")`.  I have not extensively
tested this with HEC-RAS 6, but a few methods I did test still work; open an
Issue if one does not.

# Updates and Maintenance

If extended functionality would be useful, open an Issue and I will look into making updates.

# Usage

The default setup assumes HEC-RAS 5.0.7.  If you need support for a different version, let me know and I will see about implementing it.

Raspy is intended to be used through an `API` object, which provides a uniform way to access functionality.  The argument to the `API` class is a `Ras` object, which by default is from the `Ras` module but could come from another library as long as compatible functionality is provided (requirements are documented in a comment at the top of `api.py`).  By default, a `Ras` object is created with a project path to a prepared HEC-RAS project, which must have geometry set up, a flow file to write to, etc.  The assumption is that the desired plan (pointing to the correct flow file and geometry) is already open in that project, but `API.ops.setPlan` can set a plan file.

Core functionality is built and tested for steady-state models.  I may be able to implement some simplistic unsteady-state functionality on request.

The `API` object contains three other objects: `ops`, which contains operations functionality (e.g. opening, closing, running); `params`, which contains functionality to set parameters (e.g. roughness, flow profiles); and `data`, which contains data retrieval functionality.  The methods and arguments of those are hopefully fairly self-explanatory, but a few important ones are highlighted here.

* `API.ops.compute()` runs the model (optional: specify steady/unsteady flow, plan ID, and whether to wait for the compute run to complete before returning).
* `API.params.modifyN(manning, river, reach)` specifies Manning's roughness coefficient.  This can be done in a number of ways, as described by a comment in that function.  In theory, it is possible to specify multiple roughnesses per cross section (e.g. left overbank, main channel, right overbank) and roughnesses for each cross section in a reach; however, only setting a single roughness for the whole channel has been tested, so use more advanced functionality at your own risk.
* `API.params.setSteadyFlows()` sets steady flow rates.  The HEC-RAS Windows API does support setting flow profiles directly, but this seems to be highly buggy, at least for 5.0.7, so instead it directly writes the flow file using `pyrasfile`.  In order to load the new flow data, it then has to save, close, and reopen the HEC-RAS project.
* `api.data.velocity()` and `api.data.stage()` retrieve main channel velocity or stage for the specified river, reach, and cross-section.  If any of these are unspecified, it will return nested dictionaries covering all possibilities.  In order to retrieve multiple flow profiles' data, specify the number of flow profiles.  For example, if you set up 100 steady flows with `setSteadyFlows()`, specify `nprofs=100` to retrieve data for all of them.

These four key points are what support roughness autocalibration; they would also support automatically running and extracting data for a wide range of flows and the like.  The source code for Raspy-Cal provides usage examples.

General users should be aware that, in the short term, only functionality needed for raspy-cal will be implemented.  Other functionality
may be added over the longer term, but the current primary purpose of this project is to support automatic calibration with raspy-cal.  However, other contributors are welcome to focus on broadening the functionality.  In addition, I may be able to implement straightforward additional functionality on request.

## Dependencies

* pywin32
* pyrasfile

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

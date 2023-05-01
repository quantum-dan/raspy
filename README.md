# raspy
Python interface for HEC-RAS.  RAS + Python = raspy.

This can be installed on pip/PyPI as [raspy-auto](https://pypi.org/project/raspy-auto/).

See [PyRAS](https://pypi.org/project/PyRAS/) and the paper "[Application of Python Scripting Techniques for Control and Automation of HEC-RAS Simulations](https://www.mdpi.com/2073-4441/10/10/1382)" for similar ideas.

Related packages:

* [RaspyGeo](https://github.com/quantum-dan/raspygeo) builds on Raspy to automate geometry modification scenarios.
* [Raspy-Cal](https://github.com/quantum-dan/raspy-cal) uses Raspy for automatic calibration of Manning's roughness.

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

Raspy is intended to be used through an `API` object, which provides a uniform way to access functionality.  The argument to the `API` class is a `Ras` object, which by default is from the `Ras` module but could come from another library as long as compatible functionality is provided (requirements are documented in a comment at the top of `api.py`).  By default, a `Ras` object is created with a project path to a prepared HEC-RAS project, which must have geometry set up, a flow file to write to, etc.  The assumption is that the desired plan (pointing to the correct flow file and geometry) is already open in that project, but `API.ops.setPlan` can set a plan file.

Core functionality is built and tested for steady-state models.  I may be able to implement some simplistic unsteady-state functionality on request.

The `API` object contains three other objects: `ops`, which contains operations functionality (e.g. opening, closing, running); `params`, which contains functionality to set parameters (e.g. roughness, flow profiles); and `data`, which contains data retrieval functionality.  The methods and arguments of those are hopefully fairly self-explanatory, but a few important ones are highlighted here.

* `API.ops.compute()` runs the model (optional: specify steady/unsteady flow, plan ID, and whether to wait for the compute run to complete before returning).
* `API.params.modifyN(manning, river, reach)` specifies Manning's roughness coefficient.  This can be done in a number of ways, as described by a comment in that function.  In theory, it is possible to specify multiple roughnesses per cross section (e.g. left overbank, main channel, right overbank) and roughnesses for each cross section in a reach; however, only setting a single roughness for the whole channel has been tested, so use more advanced functionality at your own risk.
* `API.params.setSteadyFlows()` sets steady flow rates.  The HEC-RAS Windows API does support setting flow profiles directly, but this seems to be highly buggy, at least for 5.0.7, so instead it directly writes the flow file using `pyrasfile`.  In order to load the new flow data, it then has to save, close, and reopen the HEC-RAS project.
* `api.data.velocity()`, `api.data.stage()`, and `api.data.shear()` retrieve main channel velocity, stage, or shear for the specified river, reach, and cross-section.  If any of these are unspecified, it will return nested dictionaries covering all possibilities.  In order to retrieve multiple flow profiles' data, specify the number of flow profiles.  For example, if you set up 100 steady flows with `setSteadyFlows()`, specify `nprofs=100` to retrieve data for all of them.
* The above three have corresponding methods `velocityDist`, `depthDist`, and `shearDist` retrieving the left overbank/main channel/right overbank distributions (as lists in that order).  `depthDist` uses hydraulic depths for the overbanks and maximum channel depth for the main channel.

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

## Raspy External Interfaces

If there is need for it (open an Issue), I should be able to fairly quickly implement an R interface (through Reticulate) or a plain text config file-based mechanism for using Raspy.  Currently, Raspy can only be used as a Python module.

# Current Applications

Raspy is currently used by two other HEC-RAS automation tools.

- [RaspyGeo](https://github.com/quantum-dan/raspygeo) automatically implements and tests HEC-RAS cross-section geometry scenarios (channel geometry modifications).  It handles HEC-RAS geometry editing, then uses Raspy to run scenarios and retrieve results.
- [Raspy-Cal](https://github.com/quantum-dan/raspy-cal) is an automatic calibration application for Manning's roughness in HEC-RAS.  It uses Raspy to set roughness, run the model, and retrieve results.

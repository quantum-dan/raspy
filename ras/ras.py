"""
Outer wrapper for lower-level functionality.
"""

"""
The following classes and methods are required (note: class names don't need to be as listed here,
but methods and properties do)

rasObj - containing a project with a specified geometry file and plan etc
rasObj.reach(river, reach, geom = None) - returning the relevant reach.  If geom (optional) is specified,
    use that geometry file (specified as an ID, if string, or file number, if integer); otherwise, use the currently
    active geometry, if any, or throw an error if no geometry is active
rasObj.openProject(projectPath) - open the relevant project
rasObj.setPlan(plan) - set the plan to that one (by ID or file number)
rasObj.setGeom(geom) - set the plan geometry file/active geometry file (by ID or file number)
rasObj.computeSteady, computeUnsteady(plan = None) - run the plan (optional) or, if plan is None, the currently active plan
rasObj.exit() - exit HEC-RAS
rasObj.newPlan(planId) - create a new plan with the given ID and make it the active plan
rasObj.set<Steady/Unsteady>Flow(flow) - set the steady/unsteady flow file (by ID or file number)
rasObj.getSimData(river = None, reach = None, rs = None): get the simulation flow data for a given river, reach, and river station.
    If rs is none, return a dictionary of all the river stations' data.  Likewise river and reach (nested dictionaries).
    Simulation flow data should be as a simdata class.

reach - containing a reach in the geometry file
reach.xses - return a list of cross sections

simdata - simulation data for a given cross section
properties: velocity, maxDepth, flow, and other data

xs - a cross section
xs.setAllManning(ns): set all Manning's ns to a list of ns given
xs.setMainChannelManning(n): set the main channel n to the given n
"""

"""
The following HEC-RAS COM methods must therefore have wrappers available:
Compute_CurrentPlan
Compute_<Show/Hide>ComputationWindow
Compute_WATPlan
Create_WATPlanName
Current<GeomFile, ProjectFile, SteadyFile, UnSteadyFile>
Get<Nodes, Reaches, Rivers>
SetMann
SetMann_LChR
Plan_<GetFilename, SetCurrent>
Output_VelDist
"""
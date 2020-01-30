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

class XS(object):
    """
    A cross section.
    """
    def __init__(self, ras, river, reach, rs):
        """
        :param ras: RasObject (from wrapper)
        :param river: river (string)
        :param reach: string
        :param rs: river station (string)
        """
        self.ras = ras
        self.river = river
        self.reach = reach
        self.rs = rs

    def setAllManning(self, ns):
        """
        Set left, main, right ns.
        :param ns: [left, main, right] Manning's n
        """
        self.ras.SetMannLCR(self.river, self.reach,  self.rs, ns[0], ns[1], ns[2])

    def setMainChannelManning(self, n):
        """
        Set the main channel n.  For now, set left/right ns to be the same; in future, keep them as-is.
        :param n: main channel n.
        """
        self.ras.SetMannLCR(self.river, self.reach, self.rs, n, n, n)

class Reach(object):
    """
    A reach.
    """
    def __init__(self, ras, river, reach):
        self.ras = ras
        self.river = river
        self.reach = reach
        self.xses = self.getCrossSections()

    def getCrossSections(self):
        """
        Get a list of the cross sections.  First, get integer IDs for river and reach, then call
        ras.GetNodes(riv, rch).  It'll be the third item, and all of the non-blank ones within.
        """


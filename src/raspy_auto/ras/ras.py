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

from raspy_auto.ras.wrapper import RasObject

class Ras(object):
    """
    The whole RAS controller.
    """
    def __init__(self, projectPath, rasObject = RasObject()):
        self.ras = rasObject
        if not (projectPath is None):
            self.openProject(projectPath)
        self.rivers = [River(self.ras, river.strip()) for river in self.ras.GetRivers()[1]]

    def openProject(self, path):
        self.ras.OpenProject(path)

    def quit(self):
        self.ras.QuitRas()

    def currentProject(self):
        return self.ras.CurrentProject()

    def save(self):
        self.ras.Save()

    def river(self, river, geom = None):
        return [riv for riv in self.rivers if riv.river == river][0]

    def reach(self, river, reach, geom = None):
        # Geom not implemented yet.
        return self.river(river, geom).reach(reach)

    def computeSteady(self, plan = None):
        self.ras.Compute()

    def computeUnsteady(self, plan = None):
        self.ras.Compute()

    def computeIsComplete(self):
        return self.ras.Complete()

    def getSimData(self, river = None, reach = None, rs = None, prof = 1):
        if river is None:
            return {riv.river: self.getSimData(riv.river, reach, rs) for riv in self.rivers}
        elif reach is None:
            riv = self.river(river)
            return {rch.reach: self.getSimData(riv.river, rch.reach, rs) for rch in riv.reaches}
        elif rs is None:
            riv = self.river(river)
            rch = self.reach(river, reach)
            return {xs.rs: self.getSimData(riv.river, rch.reach, xs.rs) for xs in rch.xses}
        else:
            riv = self.river(river)
            rch = riv.reach(reach)
            xs = rch.xs(rs)
            sd = self.ras.GetVelDist(xs.riverID, xs.reachID, xs.xsID, 0, prof)
            # sd: (6x args, (left station), (right station), (conv perc), (area), (wetted perimeter), (flow),
            # (depth), (velocity))
            velocity = sd[-1][0]
            depth = sd[-2][0]
            flow = sd[-3][0]
            etc = {
                "area": sd[-4][0],
                "wp": sd[-5][0]
            }
            return SimData(velocity, depth, flow, etc)

class SimData(object):
    """
    Simulation data for a cross section.  "etc" is a dictionary of less relevant data.
    """
    def __init__(self, velocity, maxDepth, flow, etc):
        self.velocity = velocity
        self.maxDepth = maxDepth
        self.flow = flow
        self.etc = etc

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
        self.riverID = getRiverID(self.ras, self.river)
        self.reachID = getReachID(self.ras, self.river, self.reach)
        self.xsID = getXSID(self.ras, self.river, self.reach, self.rs)

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

    def editSteadyFlow(self):
        self.ras.EditSteadyFlow()

    def setSteadyFlow(self, flows, wait = False):
        self.ras.setSteadyFlow(self.river, self.reach, self.rs, flows, wait)


def getRiverID(ras, river):
    """
    Find river ID from river name
    :param ras: RasObject
    :param river: river name
    :return: river id
    """
    rivers = ras.GetRivers()[1]
    for ix, riv in enumerate(rivers):
        if riv.startswith(river): # starts with because the names often have a bunch of extra spaces
            return ix + 1
    return False

def getReachID(ras, river, reach):
    reaches = ras.GetReaches(getRiverID(ras, river))[2]
    for ix, rch in enumerate(reaches):
        if rch.startswith(reach):
            return ix + 1
    return False

def getXSID(ras, river, reach, xs):
    """
    Count from the top, not the bottom. <not currently>
    """
    xses = [xs.strip() for xs in ras.GetNodes(getRiverID(ras, river), getReachID(ras, river, reach))[3]]
    for (ix, rs) in enumerate(xses):
        if rs.startswith(xs):
            return ix + 1
    return False

class Reach(object):
    """
    A reach.
    """
    def __init__(self, ras, river, reach):
        self.ras = ras
        self.river = river
        self.reach = reach
        self.riverID = getRiverID(self.ras, self.river)
        self.reachID = getReachID(self.ras, self.river, self.reach)
        self.xses = [XS(self.ras, self.river, self.reach, rs) for rs in self.getCrossSections()]

    def getCrossSections(self):
        return [xs.strip() for xs in self.ras.GetNodes(self.riverID, self.reachID)[3]]

    def xs(self, rs):
        return [xs for xs in self.xses if xs.rs == rs][0]

    def xsAt(self, rs):
        return self.xs(rs)

class River(object):
    """
    A river.
    """
    def __init__(self, ras, river):
        self.ras = ras
        self.river = river
        self.riverID = getRiverID(self.ras, self.river)
        self.reaches = [Reach(self.ras, self.river, reach) for reach in self.getReaches()]

    def getReaches(self):
        return [r.strip() for r in self.ras.GetReaches(self.riverID)[2]]

    def reach(self, reach):
        return [rch for rch in self.reaches if rch.reach == reach][0]


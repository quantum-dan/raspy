"""
The API class.  No new functionality, but a place to gather together all relevant functions.
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

from raspy.PyRASFile import profileWriter as pw

class OpsAPI(object):
    # Running and general operation
    def __init__(self, rasObj):
        self.ras = rasObj
    def openProject(self, projectPath):
        self.ras.openProject(projectPath)
    def setPlan(self, plan):
        self.ras.setPlan(plan)
    def setGeometry(self, geom):
        self.ras.setGeom(geom)
    def compute(self, steady = True, plan = None, wait = True):
        if steady:
            self.ras.computeSteady(plan)
        else:
            self.ras.computeUnsteady(plan)
        if wait:
            while not self.ras.computeIsComplete():
                pass
    def exit(self):
        self.ras.exit()
    def newPlan(self, planId):
        self.ras.newPlan(planId)
    def setFlow(self, flow, steady = True):
        if steady:
            self.ras.setSteadyFlow(flow)
        else:
            self.ras.setUnsteadyFlow(flow)

def nestedDictMap(map, func):
    # Apply func to all the values at the bottom level in map
    if map.__class__ == {}.__class__:
        for key in map:
            map[key] = nestedDictMap(map[key], func)
        return map
    else:
        return func(map)

class DataAPI(object):
    # Data retrieval
    def __init__(self, rasObj):
        self.ras = rasObj
    def allFlow(self, river = None, reach = None, rs = None, nprofs = 1):
        if nprofs == 1:
            return self.ras.getSimData(river, reach, rs)
        else:
            return {i: self.ras.getSimData(river, reach, rs, prof = i) for i in range(1, nprofs + 1)}
    def getSingleDatum(self, func, river, reach, rs, nprofs = 1):
        # Get a single datum (e.g. velocity, stage), regardless of level of nesting
        # func: function to extract relevant value from data class (e.g. lambda x: x.velocity)
        result = self.allFlow(river, reach, rs, nprofs)
        return nestedDictMap(result, func)
        # if not (rs is None): # just the one station
        #     return func(result)
        # elif not (reach is None): # just the one reach
        #     for rs, dat in result.items():
        #         dat = func(dat)
        #         result[rs] = dat
        #     return result
        # elif not (river is None): # just the one river
        #     for rch, rdat in result.items():
        #         for rs, dat in rdat.items():
        #             rdat[rs] = func(dat)
        #     return result
        # else: # all rivers
        #     for riv, ridat in result.items():
        #         for rch, rdat in ridat.items():
        #             for rs, dat in rdat.items():
        #                 rdat[rs] = func(dat)
        #     return result
    def velocity(self, river = None, reach = None, rs = None, nprofs = 1):
        return self.getSingleDatum(lambda x: x.velocity, river, reach, rs, nprofs)
    def stage(self, river = None, reach = None, rs = None, nprofs = 1):
        return self.getSingleDatum(lambda x: x.maxDepth, river, reach, rs, nprofs)
    # Below not strictly needed for raspy-cal
    # def ratingCurve
    # def n

class ParamsAPI(object):
    # Setting parameters
    def __init__(self, rasObj):
        self.ras = rasObj
    # def newSteadyFlow
    # def newUnsteadyFlow
    # def modifySteadyFlow
    # def modifyUnsteadyFlow
    # While the above methods will be useful, they are not critical to initial raspy-cal functionality
    def modifyN(self, manning, river, reach, geom = None):
        """
        Specify the Manning's n for the relevant geometry.
        :param manning: specifies Manning's n.  If it is a list of doubles, then this will set the main channel ns for
        the entire reach.  A list of lists of doubles will set that many ns at each point for the entire reach.
        Alternatively, a dictionary of <river station>:<n> can be used; if there is one n it will set the main channel,
        and if there is a list it will set all of them.  Note that Manning's equation seems to not be very sensitive to
        non-main channel n, in general. If the argument is just a number, it will set all main channel n to that number.
        Note that Manning's equation seems to not be very sensitive to non-main channel n, in general.

        Note that for now the list functionality will instead take a list of 3 to set left, main channel, right ns.
        :param river: name of the river.
        :param reach: name of the reach
        :param geom: name (if string) or number (if integer) of the geometry file.  If None, it will use the currently active geometry, if any.
        """
        if manning.__class__ == [].__class__ and len(manning) > 0:
            # List
            i = 0
            for xs in self.ras.reach(river = river, reach = reach, geom = geom).xses:
                if manning[i].__class__ == [].__class__:
                    # List of lists
                    xs.setAllManning(manning[i])
                else:
                    # List of individual ns
                    xs.setMainChannelManning(manning[i])
                i += 1
        elif manning.__class__ == {}.__class__:
            # Dictionary
            rch = self.ras.reach(river = river, reach = reach, geom = geom)
            for rs in manning:
                xs = rch.xsAt(rs)
                val = manning[rs]
                if val.__class__ == [].__class__:
                    xs.setAllManning(val)
                else:
                    xs.setMainChannelManning(val)
        elif manning.__class__ == 0.1.__class__:
            # Single value
            for xs in self.ras.reach(river, reach, geom).xses:
                xs.setMainChannelManning(manning)
        else:
            raise (TypeError("Manning must be a list, dictionary or float"))

    def editSteadyFlows(self):
        self.ras.editSteadyFlow()

    def setSteadyFlows(self, river, reach, rs, flows, slope = 0.001, fileN = "01", hecVer = "5.0.7"):
        # Slope is used for boundary conditions - normal depth
        rs = self.ras.reach(river, reach).xses[0].rs if rs is None else rs
        header = pw.mkFlowHeader(river, reach, rs)
        otherHeaders = []
        boundKeys = []
        for riv in self.ras.rivers:
            for rch in riv.reaches:
                topXs = rch.xses[0]
                otherHeaders.append(pw.mkFlowHeader(riv.river, rch.reach, topXs.rs))
                boundKeys.append("%s,%s" % (riv.river, rch.reach))
        count = len(flows)
        pdata = {h: [1] * count for h in otherHeaders}  # Meaningless data so HEC-RAS doesn't complain
        pdata[header] = flows
        bound = lambda pn, q: pw.mkBoundaryData("Normal Depth", "Normal Depth", slope, slope)
        bounds = {h: bound for h in boundKeys}
        flowFile = pw.buildFile(count, pdata, bounds, title="Flow" + fileN, ver=hecVer)
        projPath = self.ras.currentProject()
        basePath = "\\".join(projPath.split("\\")[:-1])
        projName = projPath.split("\\")[-1][:-4]  # without the .prj
        flowPath = "%s\\%s.f%s" % (basePath, projName, fileN)
        with open(flowPath, "w") as f:
            f.write(flowFile)
        self.ras.save()



class API(object):
    def __init__(self, rasObj):
        self.ras = rasObj
        self.ops = OpsAPI(rasObj)
        self.data = DataAPI(rasObj)
        self.params = ParamsAPI(rasObj)
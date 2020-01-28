"""
The API class.  No new functionality, but a place to gather together all relevant functions.
"""

"""
The rasObj used by the classes below requires the following methods:


"""

class OpsAPI(object):
    # Running and general operation
    def __init__(self, rasObj):
        self.ras = rasObj
    def openProject
    def setPlan
    def setGeometry
    def compute
    def closeProject
    def newPlan
    def setFlow

class DataAPI(object):
    # Data retrieval
    def __init__(self, rasObj):
        self.ras = rasObj
    def allFlow
    def velocity
    def stage
    def ratingCurve
    def n

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
        :param manning: specifies Manning's n.  If it is a list of doubles, then this will set the main channel ns for the entire reach.  A list of lists of doubles will set that many ns at each point for the entire reach.  Alternatively, a dictionary of <river station>:<n> can be used; if there is one n it will set the main channel, and if there is a list it will set all of them.  Note that Manning's equation seems to not be very sensitive to non-main channel n, in general.
        :param river: name of the river.
        :param reach: name of the reach
        :param geom: name (if string) or number (if integer) of the geometry file.  If None, it will use the currently active geometry, if any.
        """

class API(object):
    def __init__(self, rasObj):
        self.ras = rasObj
        self.ops = OpsAPI(rasObj)
        self.data = DataAPI(rasObj)
        self.params = ParamsAPI(rasObj)
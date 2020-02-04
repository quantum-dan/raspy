"""
This script doesn't provide any extra functionality; it just creates a wrapper class for the HEC-RAS controller
that documents important methods, making everything else easier.  Arguments to methods etc are more or less
the same, at most shuffled around a bit.  No actual processing work is done here.  Many methods are renamed
as the original names were somewhat awkward

See https://engineerpaige.com/2018/11/hecras-controller/ for how to open the object browser in Excel.  This
may be helpful for finding useful methods and their arguments.

This module should generally not be directly used from outside the "ras" module.  Other parts of the "ras"
module should wrap all necessary functionality in a more user-friendly manner.
"""

"""
The following HEC-RAS COM methods must therefore have wrappers available:
Current<GeomFile, ProjectFile, SteadyFile, UnSteadyFile>
SetMann
SetMann_LChR
Plan_<GetFilename, SetCurrent>

Mainly just SetMann and SetMann_LChR are needed, as the other stuff can be done through the GUI

Geometry_SetMann(string River, string Reach, string RS, int nMann, Single[] Mann_n, Single[] station, string errmsg)
Geometry_SetMann_LChR(string River, string Reach, string RS, Single MannLOB, Single MannChan, Single MannROB, string errmsg)
"""

from win32com import client


class RasObject(object):
    def __init__(self, rasName = "RAS507.HECRASController", ras=None):
        # By default, initialize a new RAS controller object; otherwise, use the provided one.
        if ras is None:
            self.ras = client.Dispatch(rasName)
        else:
            self.ras = ras

    def ShowRas(self):
        # Show HEC-RAS window
        self.ras.ShowRas()

    def OpenProject(self, path):
        # Open a project at the given path
        self.ras.Project_Open(path)

    def GetNodes(self, riv, rch):
        """
        Get information on geometry nodes.
        :param riv: integer river
        :param rch: integer reach
        :return: (riv, rch, (node river stations))
        """
        return self.ras.Geometry_GetNodes(riv, rch)

    def GetRivers(self):
        """
        Get list of rivers.
        :return: (n. rivers, ("river a", "river b", ...))
        """
        return self.ras.Geometry_GetRivers()

    def GetReaches(self, riv):
        """
        Get list of reaches.
        :param riv: integer river number (1 indexed).
        :return: (riv, n. reaches, (reach names, ...))
        """
        return self.ras.Geometry_GetReaches(riv)

    def GetNodeOutput(self, riv, rch, n, updn = None, prof = None):
        """
        Get node output.
        :param riv: int river
        :param rch: int reach
        :param n: int node number (from top)
        :return: (some float (output?), riv, rch, n, updn, prof, nVar)
        """
        return self.ras.Output_NodeOutput(riv, rch, n, updn, prof)

    def GetVelDist(self, riv, rch, n, updn = None, prof = 1):
        """
        Get vel dist.  What is that?
        :param riv: int river
        :param rch: int reach
        :param n: int node number (from top)
        :return: (riv, rch, n, updn, prof[ile?], nv, (left stations), (right stations), (conv percs), (areas),
            (wetted perimeters), (flows), (depths), (velocities)
        """
        return self.ras.Output_VelDist(riv, rch, n, updn, prof)

    def GetVariables(self):
        """
        Get a list of output variables.
        :return: (n. variables, (variable names), (variable descriptions))
        """
        return self.ras.Output_Variables()

    def Compute(self):
        """
        Run the current plan.
        :return: (some bool, nmsg, (messages), blockingmode)
        """
        return self.ras.Compute_CurrentPlan()

    def Complete(self):
        return self.ras.Compute_Complete()

    def SetMannLCR(self, river, reach, rs, left, channel, right):
        # Geometry_SetMann_LChR(string River, string Reach, string RS, Single MannLOB, Single MannChan, Single MannROB, string errmsg)
        """
        Set the Manning's n for left, main channel, right.
        :param river: river name (string)
        :param reach: reach name (string)
        :param rs: river station (string)
        :param left: left bank Manning's n
        :param right: right bank Manning's n
        :param channel: main channel Manning's n
        :return: (arguments, errmsg)
        """
        return self.ras.Geometry_SetMann_LChR(river, reach, rs, left, channel, right)

    def SetMann(self, river, reach, rs, manns):
        # Geometry_SetMann(string River, string Reach, string RS, int nMann, Single[] Mann_n, Single[] station, string errmsg)
        """
        Set all Manning's n at various stations.
        :param river: river name (string)
        :param reach: reach name (string)
        :param rs: river station (string)
        :param manns: Manning's ns
        :param stations: stations (from the left)
        :return: (arguments, errmsg)
        """
        nMann = len(manns)
        return self.ras.Geometry_SetMann(river, reach, rs, nMann, manns)


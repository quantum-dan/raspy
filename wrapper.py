"""
This script doesn't provide any extra functionality; it just creates a wrapper class for the HEC-RAS controller
that documents important methods, making everything else easier.  Arguments to methods etc are more or less
the same, at most shuffled around a bit.  No actual processing work is done here.  Many methods are renamed
as the original names were somewhat awkward

See https://engineerpaige.com/2018/11/hecras-controller/ for how to open the object browser in Excel.  This
may be helpful for finding useful methods and their arguments.
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
        self.ras.ProjectOpen(path)

    def GetNodes(self):
        # Get information on geometry nodes.  Arguments etc unknown.
        return self.ras.Geometry_GetNodes()

    def GetNodeOutput(self):
        # Get node output.  Arguments etc unknown.
        return self.hec.Output_NodeOutput()


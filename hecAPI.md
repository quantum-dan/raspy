# HEC-RAS COM Information

Much of this information was found in the code associated with the Water paper "Application of Python Scripting Techniques..." linked in the README.

HEC-RAS provides a Windows COM interface, accessible via pywin32.  For example:

```
from win32com import client
hec = client.Dispatch("RAS507.HECRASController")
```

Methods include (functionality specified if known):

* `hec.ShowRas()`: launches HEC-RAS.
* `hec.ProjectOpen(<path>)`: opens the project file specified.  Does not require the HEC-RAS window to be open in order to work, as HEC-RAS is running in the COM object itself.
* `hec.Geometry_GetNodes()`
* `hec.Output_NodeOutput()`
* `hec.QuitRas()`
* `hec.Plan_SetCurrent()`
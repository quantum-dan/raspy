# HEC-RAS COM Information

Much of this information was found in the code associated with the Water paper "Application of Python Scripting Techniques..." linked in the README.

HEC-RAS provides a Windows COM interface, accessible via pywin32.  For example:

```
from win32com import client
hec = client.Dispatch("RAS507.HECRASController")
```

How to look through methods (one known approach):

1. Open the Excel VBA editor (Alt + F11 in Excel)
1. Tools -> References -> Select HEC River Analysis System
1. View -> Object Browser -> under "Library" dropdown select RAS\<version\>

Methods include (functionality specified if known):

Note: I think the Single class referenced is what most of us would call a "float", but I'm not positive.

* `hec.ShowRas()`: launches HEC-RAS.
* `hec.ProjectOpen(<path>)`: opens the project file specified.  Does not require the HEC-RAS window to be open in order to work, as HEC-RAS is running in the COM object itself.
* `hec.Geometry_GetNodes()`
* `hec.Output_NodeOutput()`
* `hec.QuitRas()`
* `hec.Plan_SetCurrent()`
* `hec.Compute_Cancel()`: Bool
* `hec.Compute_Complete()`: Bool
* `hec.Compute_CurrentPlan(int nmsg, string[] Msg, [Bool BlockingMode])`: Bool
* `hec.Compute_HideComputationWindow()`
* `hec.Compute_ShowComputationWindow()`
* `hec.Compute_WATPlan(string RasBasePlanTitle, string SimluationName, string newFPart, string DestinationDirectory, string InputDSSFile, string OutputDSSFile, string StartDate, string StartTime, string EndDate, string EndTime, Bool ShowMessageList)`: Bool (sic)
* `hec.Create_WATPlanName(string HECBasePlanName, string SimulationName)`: String
* `hec.CurrentGeomFile()`: String
* `hec.CurrentGeomHDFFile()`: String
* `hec.CurrentPlanFile()`: String
* `hec.CurrentProjectFile()`: String
* Similarly `...ProjectFile()`, `...SteadyFile()`, `...UnSteadyFile()`
* `hec.Edit_AddBC(string River, string Reach, string RS, string errmsg)`
* `hec.Edit_AddIW(string River, string Reach, string RS, string errmsg)`
* `hec.Edit_`...:
    * `AddLW(string River, string Reach, string RS, string errmsg)`
    * `AddXS(string River, string Reach, string RS, string errmsg)`
    * `BC(string River, string Reach, string RS)`
    * `GeometricData()`
    * `IW(string River, string Reach, string RS)`, likewise `LW(...)`
    * `MultipleRun()`
    * `PlanData()`
    * `QuasiUnsteadyFlowData()`, likewise `SedimentData`, `SteadyFlowData`, `UnsteadyFlowData`, and `WaterQualityData`
    * `XS(string River, string Reach, string RS)`
* `hec.ExportGis()`
* `hec.Geometry_GISImport(string title, string filename)`
* `hec.Geometry()`
* `hec.Geometry_BreachParamGetXML()`: String
* `hec.Geometry_`...:
    * `BreachParamSetXML(string xmlText)`
    * `Get2DFlowAreas(int count, string[] D2Names)`
    * `GetGateNames(string River, string Reach, string RS, int nGate, string[] gateName, string errmsg)`
    * `GetGML(string geomfilename)`
    * `GetMann((string River, string Reach, string RS, int nMann, Single[] Mann_n, Single[] station, string errmsg)`: Bool (Single is Excel VBA class, meaning unknown)
    * `GetNode(int riv, int rch, string RS)`: int
    * `GetNodes(int riv, int rch, int nRS, string[] RS, string[] NodeType)`
    * `GetReaches(int riv, int nReach, string[] Reach)`
    * `GetRivers(int nRiver, string[] River)`
    * `GetStorageAreas(int count, string[] SAnames)`
    * `RatioMann(int riv, int rchUp, int nup, int rchDn, int ndn, Single ratio, string errmsg)`
    * `SetMann(string River, string Reach, string RS, int nMann, Single[] Mann_n, Single[] station, string errmsg)`: Bool
    * `SetMann_LChR(string River, string Reach, string RS, Single MannLOB, Single MannChan, Single MannROB, string errmsg)`: Bool
    * `SetSAArea(string saName, Single Area, string errmsg)`: Bool
* `hec.GetDataLocations_Output(string planTitle, string[] DSSFiles, string[] DSSPathnames,string errmsg)`
* `hec.HECRASVersion()`: String
* `hec.nNode(int riv, int rch)`: int
* `hec.NodeCType(int riv, int rch, int n)`: String
* `hec.NodeCutLine_nPoints(int riv, int rch, int n)`: int
* `hec.NodeCutLine_Points(int riv, int rch, int n, double[] PointX, double[] PointY)`
* `hec.NodeIndex(int riv, int rch, string RS)`: int
* `hec.NodeRS(int riv, int rch, int n)`: String
* `hec.NodeType(int riv, int rch, int n)`: int
* `hec.nReach(int riv)`: int
* `hec.nRiver()`: int
* `hec.Output_`...:
    * `ComputationLevel_Export(string filename, string errmsg, [Bool WriteFlow, Bool WriteStage, Bool WriteArea, Bool WriteTopWidth])`
    * `GetNode(int riv, int rch, string RS)`: int
    * `GetNodes(int riv, int rch, int nRS, string[] RS, string[] NodeType)`
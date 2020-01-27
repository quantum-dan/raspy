# HEC-RAS COM Information

Some of this information was found in the code associated with the Water paper "Application of Python Scripting Techniques..." linked in the README.

HEC-RAS provides a Windows COM interface, accessible via pywin32.  For example:

```
from win32com import client
hec = client.Dispatch("RAS507.HECRASController")
```

How to look through methods (one known approach):

1. Open the Excel VBA editor (Alt + F11 in Excel)
1. Tools -> References -> Select HEC River Analysis System
1. View -> Object Browser -> under "Library" dropdown select RAS\<version\>

At present these are described as shown in the VBA Object Browser, so it is unclear if there are differences in how e.g. Python would handle them (for example, all of the methods that seem like they should return something but don't--is that how VBA handles it, or written into it?).  Information will be updated as and if they are tested in Python, but this will only be for a subset of them as I am putting this document together mainly in support of raspy and will only be testing those relevant to raspy.  I suspect that many of the arguments passed in may actually be set by reference within the method to avoid limitations in VBA.  Alternatively, this may be the case but done rather to avoid limitations in whatever HEC-RAS is written in (FORTRAN? Or C++?).

Methods include (functionality specified if known):

Note: I think the Single class referenced is what most of us would call a "float", but I'm not positive.

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
    * `GetMann((string River, string Reach, string RS, int nMann, Single[] Mann_n, Single[] station, string errmsg)`: Bool (Single is Excel VBA class, meaning unknown - float?)
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
    * `GetProfiles(int nProfile, string[] ProfileName)`
    * `GetReach(int riv, string Reach)`: int
    * `GetReaches(int riv, int nReach, string[] Reach)`
    * `GetRiver(string River)`: int
    * `GetRivers(int nRiver, string[] River)`
    * `Initialize()`
    * `NodeOutput(int riv, int rch, int n, int updn, int prof, int nVar)`: Single
    * `ReachOutput(int riv, int rch, int prof, int nVar, int nRS, string[] RS, Single[] ChannelDist, Single[] value)`
    * `Variables(int nVar, string[] VarName, string[] VarDesc)`
    * `VelDist(int riv, int rch, int n, int updn, int prof, int nv, Single[] LeftSta, Single[] RightSta, Single[] ConvPerc, Single[] Area, Single[] WP, Single[] Flow, Single[] HydrDepth, Single[] Velocity)`
* `hec.OutputDSS_`...:
    * `GetStageFlow(string River, string Reach, string RS, int nvalue, double[] ValueDateTime, Single[] Stage, Single[] Flow, string errmsg)`: Bool
    * `GetStageFlowSA(string StorageArea, int nvalue, double[] ValueDateTime, Single[] Stage, Single[] Flow, string errmsg)`: Bool
* `hec.Plan_`...:
    * `GetFilename(string planName)`: String
    * `GetParameterUncertaintyXML()`: String
    * `InformationXML(string requestXML)`: String
    * `Names(int PlanCount, string[] PlanNames, Bool IncludeOnlyPlansInBaseDirectory)`
    * `Reports(int ReportCount, string[] ReportNames)`
    * `SetCurrent(string PlanTitleToSet)`: Bool
    * `SetParameterUncertaintyXML(string xmlText)`
* `hec.PlanOutput_`...:
    * `IsCurrent(string PlanTitleToCheck, Bool ShowMessageList, string errmsg)`: Bool
    * `SetCurrent(string PlanTitleToSet)`: Bool
    * `SetMultiple(int nPlanTitleToSet, string[] PlanTitleToSet_0, Bool ShowMessageList)`: int
* `hec.Plot`...: (note: no underscore)
    * `HydraulicTables(string River, string Reach, string RS)`
    * `PF(string River, string Reach)`
    * `PFGeneral(string River, string Reach)`
    * `RatingCurve(string River, string Reach, string RS)`
    * `StageFlow(string River, string Reach, string RS)`
    * `StageFlow_SA(string saName)`
    * `XS(string River, string Reach, string RS)`
    * `XYZ(string River, string Reach)`
* `hec.Project_`...:
    * `Close()`
    * `Current()`: String
    * `New(string title, string filename)`
    * `Open(string projectFilename)`
    * `Save()`
    * `SaveAs(string newProjectName)`
* `hec.ProjectionSRSFilename()`: String
* `hec.QuitRas()`: hide the HEC-RAS window (does not exit the project etc)
* `hec.ReachIndex(int riv, string ReachName)`: int
* `hec.ReachInvert_nPoints(int riv, int rch)`: int
* `hec.ReachInvert_Points(int riv, int rch, double[] PointX, double[] PointY)`
* `hec.ReachName(int riv, int rch)`: String
* `hec.RiverIndex(string RiverName)`: int
* `hec.RiverName(int riv)`: String
* `hec.Save()`
* `hec.Schematic_`...:
    * `D2FlowAreaPolygon(string Name, int count, double[] x, double[] Y)`
    * `ReachCount()`: int
    * `ReachPointCount()`: int
    * `ReachPoints(string[] RiverName_0, string[] ReachName_0, int[] ReachStartIndex_0, int[] ReachPointCount_0, double[] ReachPointX_0, double[] ReachPointY_0)`
    * `StorageAreaPolygon(string Name, int count, double[] x, double[] Y)`
    * `XSCount()`: int
    * `XSPointCount()`: int
    * `XSPoints(string[] RSName_0, int[] ReachIndex_0, int[] XSStartIndex_0, int[] XSPointCount_0, double[] XSPointX_0, double[] XSPointY_0)`
* `hec.ShowRas()`: show the HEC-RAS window
* `hec.ShowRasMapper()`
* `hec.SteadyFlow_`...:
    * `ClearFlowData()`
    * `FixedWSBoundary(string River, string Reach, Bool Downstream, Single[] WSElev)`: Bool
    * `nProfile`: int (property, not method)
    * `SetFlow(string River, string Reach, string RS, Single[] Flow)`
* `hec.TablePF(string River, string Reach)`
* `hec.TableXS(string River, string Reach, string RS)`
* `hec.UnsteadyBoundaryIndex(string River, string Reach, string RS, string StorageArea, string Connection)`: int
* `hec.UnsteadyFlow_SetGateOpening_Constant(string River, string Reach, string RS, string gateName, Single OpenHeight, string errmsg)`
* `hec.wcf_`...:
    * `ComputePlan(string xmlText)`: string
    * `CreateNewPlan(string xmlText)`: string
    * `InputDataLocations_Get(string projectfile, string planTitle)`: string
    * `InputDataLocations_Set(string projectfile, string planTitle, string xmlText)`: string
    * `OutputDataLocations(string projectfile, string PlanFilename, string planTitle, string planShortID)`: string
    * `SetOutputPlans(string xmlText, string errMessage)`: Bool
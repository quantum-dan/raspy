"""
General HEC-RAS operation: opening, closing, running, etc.
"""

PATH_SEP = "\\"

# ras, in all cases, is a Model object from the ras module

from ras import Model

def openProject(model, projectName, projectDir, basePath):
    projectPath = basePath + PATH_SEP + projectDir + PATH_SEP + projectName + ".prj"
    model.openProject(projectPath)
    return model    

def setPlan
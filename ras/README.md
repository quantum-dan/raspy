This directory contains the lower-level wrappers around HEC-RAS to provide
easier functionality for the rest of the project.

The general idea is that a collection of modules should define functions
which, given a RasObject (from "ras.wrapper"), provide the relevant
functionality in a more usable manner.  For neatness without excessively
large classes, all of these functions will be wrapped into a Model
class (i.e. Model.OpenProject = running.OpenProject(self)) that can be used
by the "api" module to define higher-level functionality.

Initially, functionality will be implemented only as needed to support the
top priorities defined in api/README.md.  Other functionality will be added
in the longer term.
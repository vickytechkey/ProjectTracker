from projectManagement.projects.resolve_project import ResolveProject
from projectManagement.install import InstallationModule
from projectManagement.projects.createproject import CreateProject

from projectManagement.subtask.createSubtask import CreateSubTask

i = InstallationModule()
c = CreateProject("testproject2",{"start_date":"01-01-2025","end_date":"01-01-2026"},10)
c.CreateProject()

c1 = CreateSubTask("testsubtask","01-01-2025","01-01-2026",10,1,1)
c1.CreateSubTask()








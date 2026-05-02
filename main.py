from projectManagement.projects.resolve_project import ResolveProject
from projectManagement.install import InstallationModule
from projectManagement.projects.createproject import CreateProject

i = InstallationModule()
c = CreateProject("testproject2",{"start_date":"01-01-2025","end_date":"01-01-2026"},10)
c.CreateProject()
# r = ResolveProject(1)
# r.CloseProject()







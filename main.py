from db.mongo import MongoDB
from projectManagement.projects.createproject import CreateProject
from projectManagement.subtask.createSubtask import CreateSubTask
from projectManagement.subtask.adding_correspondence import AddingMessage

# c = CreateProject(projectName="Testproject",project_start_end_date={"start_date":"17-05-2026","end_date":"20-05-2026"},plannedEfforts=10)
# c.CreateProject()

# s = CreateSubTask(taskname="planning",start_date="05-05-2026",end_date="05-06-2026",planned_efforts=10,project_name="Testproject")
# s.CreateSubTask()

c1 = AddingMessage(projectname="Testproject",subtaskname="planning",message="Test Message")
c1.createcorrespondence()









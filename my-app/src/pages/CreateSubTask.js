import { useState } from "react";
import "./CreateSubTask.css";

function CreateSubTask() {

    // Temporary data
    const activeProjects = [
        "Project Alpha",
        "Project Tracker",
        "ML Dashboard"
    ];

    const [subTask, setSubTask] = useState({
        project: "",
        subTaskName: "",
        startDate: "",
        endDate: "",
        estimatedEfforts: ""
    });

    const handleChange = (e) => {
        setSubTask({
            ...subTask,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        console.log(subTask);

        alert("Subtask created successfully");
    };

    return (
        <div className="subtask-container">

            <div className="subtask-box">

                <h2>Create Sub Task</h2>

                <form onSubmit={handleSubmit}>

                    <label>Select Project</label>

                    <select
                        name="project"
                        value={subTask.project}
                        onChange={handleChange}
                        required
                    >
                        <option value="">
                            Select Project
                        </option>

                        {activeProjects.map((project,index)=>(
                            <option key={index} value={project}>
                                {project}
                            </option>
                        ))}

                    </select>

                    <input
                        type="text"
                        name="subTaskName"
                        placeholder="Sub Task Name"
                        value={subTask.subTaskName}
                        onChange={handleChange}
                        required
                    />

                    <label>Sub Task Start Date</label>

                    <input
                        type="date"
                        name="startDate"
                        value={subTask.startDate}
                        onChange={handleChange}
                        required
                    />

                    <label>Sub Task End Date</label>

                    <input
                        type="date"
                        name="endDate"
                        value={subTask.endDate}
                        onChange={handleChange}
                        required
                    />

                    <input
                        type="number"
                        name="estimatedEfforts"
                        placeholder="Estimated Efforts (Hours)"
                        value={subTask.estimatedEfforts}
                        onChange={handleChange}
                        required
                    />

                    <button type="submit">
                        Create Sub Task
                    </button>

                </form>

            </div>

        </div>
    );
}

export default CreateSubTask;
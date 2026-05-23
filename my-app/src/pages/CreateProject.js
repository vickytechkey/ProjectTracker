import { useState } from "react";
import "./CreateProject.css";

function CreateProject() {

    const [project, setProject] = useState({
        projectName: "",
        startDate: "",
        endDate: ""
    });

    const handleChange = (e) => {
        setProject({
            ...project,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        console.log(project);

        alert("Project created successfully");
    };

    return (
        <div className="project-container">

            <div className="project-box">

                <h2>Create Project</h2>

                <form onSubmit={handleSubmit}>

                    <input
                        type="text"
                        name="projectName"
                        placeholder="Project Name"
                        value={project.projectName}
                        onChange={handleChange}
                        required
                    />

                    <label>Project Start Date</label>
                    <input
                        type="date"
                        name="startDate"
                        value={project.startDate}
                        onChange={handleChange}
                        required
                    />

                    <label>Project End Date</label>
                    <input
                        type="date"
                        name="endDate"
                        value={project.endDate}
                        onChange={handleChange}
                        required
                    />

                    <button type="submit">
                        Create Project
                    </button>

                </form>

            </div>

        </div>
    );
}

export default CreateProject;
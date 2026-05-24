import { useState } from "react";
import "./Dashboard.css";

import {
    PieChart,
    Pie,
    Cell,
    Tooltip,
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Legend,
    ResponsiveContainer
} from "recharts";

function Dashboard() {

    const projects = [
        "Project Tracker",
        "ML Dashboard",
        "AWS Migration"
    ];

    const [selectedProject, setSelectedProject] =
        useState(projects[0]);

    const projectData = {

        "Project Tracker": {
            completedSubTasks:10,
            outstandingSubTasks:4,
            plannedEfforts:80,
            actualEfforts:65,
            totalEffortsUsed:65
        },

        "ML Dashboard": {
            completedSubTasks:7,
            outstandingSubTasks:3,
            plannedEfforts:60,
            actualEfforts:50,
            totalEffortsUsed:50
        },

        "AWS Migration": {
            completedSubTasks:15,
            outstandingSubTasks:5,
            plannedEfforts:150,
            actualEfforts:120,
            totalEffortsUsed:120
        }
    };


    const subTaskData = {

        "Project Tracker":[
            {
                subTask:"Login Page",
                plannedEffort:8,
                spentEffort:6,
                status:"Completed"
            },

            {
                subTask:"Dashboard",
                plannedEffort:16,
                spentEffort:12,
                status:"In Progress"
            },

            {
                subTask:"API Integration",
                plannedEffort:10,
                spentEffort:0,
                status:"Pending"
            }
        ],

        "ML Dashboard":[
            {
                subTask:"Data Load",
                plannedEffort:12,
                spentEffort:10,
                status:"Completed"
            }
        ],

        "AWS Migration":[
            {
                subTask:"EC2 Setup",
                plannedEffort:20,
                spentEffort:15,
                status:"In Progress"
            }
        ]

    };

    const currentProject =
        projectData[selectedProject];

    const selectedSubTasks =
        subTaskData[selectedProject];


    const taskData = [

        {
            name:"Completed",
            value:currentProject.completedSubTasks
        },

        {
            name:"Outstanding",
            value:currentProject.outstandingSubTasks
        }

    ];


    const effortData = [

        {
            name:"Efforts",
            Planned:currentProject.plannedEfforts,
            Actual:currentProject.actualEfforts
        }

    ];


    const colors=[
        "#00C49F",
        "#FF8042"
    ];



    return (

        <div className="dashboard-container">

            <h1>
                Project Dashboard
            </h1>


            <div className="project-selector">

                <label>
                    Select Project:
                </label>

                <select
                    value={selectedProject}
                    onChange={(e)=>
                        setSelectedProject(
                            e.target.value
                        )
                    }
                >

                    {
                        projects.map(
                            (project,index)=>(

                            <option
                                key={index}
                                value={project}
                            >

                                {project}

                            </option>

                            )
                        )
                    }

                </select>

            </div>



            <div className="cards">

                <div className="card">

                    <h3>
                        Completed Tasks
                    </h3>

                    <p>
                        {currentProject.completedSubTasks}
                    </p>

                </div>



                <div className="card">

                    <h3>
                        Outstanding Tasks
                    </h3>

                    <p>
                        {currentProject.outstandingSubTasks}
                    </p>

                </div>



                <div className="card">

                    <h3>
                        Planned Efforts
                    </h3>

                    <p>
                        {currentProject.plannedEfforts}
                        hrs
                    </p>

                </div>



                <div className="card">

                    <h3>
                        Actual Efforts
                    </h3>

                    <p>
                        {currentProject.actualEfforts}
                        hrs
                    </p>

                </div>



                <div className="card">

                    <h3>
                        Total Efforts Used
                    </h3>

                    <p>
                        {currentProject.totalEffortsUsed}
                        hrs
                    </p>

                </div>

            </div>



            <div className="chart-container">


                <div className="chart-box">

                    <h3>
                        Completed vs Outstanding
                    </h3>

                    <ResponsiveContainer
                        width="100%"
                        height={300}
                    >

                        <PieChart>

                            <Pie
                                data={taskData}
                                dataKey="value"
                                outerRadius={100}
                                label
                            >

                            {
                                taskData.map(
                                (entry,index)=>(

                                <Cell
                                    key={index}
                                    fill={
                                        colors[index]
                                    }
                                />

                                ))
                            }

                            </Pie>

                            <Tooltip/>

                        </PieChart>

                    </ResponsiveContainer>

                </div>




                <div className="chart-box">

                    <h3>
                        Planned vs Actual
                    </h3>

                    <ResponsiveContainer
                        width="100%"
                        height={300}
                    >

                        <BarChart
                            data={effortData}
                        >

                        <CartesianGrid
                            strokeDasharray="3 3"
                        />

                        <XAxis
                            dataKey="name"
                        />

                        <YAxis/>

                        <Tooltip/>

                        <Legend/>

                        <Bar
                            dataKey="Planned"
                            fill="#3b82f6"
                        />

                        <Bar
                            dataKey="Actual"
                            fill="#8b5cf6"
                        />

                        </BarChart>

                    </ResponsiveContainer>

                </div>


            </div>



            <div className="table-container">

                <h2>
                    Sub Task Details
                </h2>

                <table>

                    <thead>

                        <tr>

                            <th>#</th>

                            <th>
                                Sub Task Name
                            </th>

                            <th>
                                Planned Effort
                            </th>

                            <th>
                                Spent Effort
                            </th>

                            <th>
                                Status
                            </th>

                        </tr>

                    </thead>

                    <tbody>

                    {
                        selectedSubTasks.map(
                            (task,index)=>(

                            <tr
                                key={index}
                            >

                            <td>
                                {index+1}
                            </td>

                            <td>
                                {task.subTask}
                            </td>

                            <td>
                                {task.plannedEffort} hrs
                            </td>

                            <td>
                                {task.spentEffort} hrs
                            </td>

                            <td>

                            <span
                                className={

                                task.status==="Completed"
                                ? "completed"

                                : task.status==="In Progress"
                                ? "progress"

                                : "pending"

                                }
                            >

                                {task.status}

                            </span>

                            </td>

                            </tr>

                            )
                        )
                    }

                    </tbody>

                </table>

            </div>

        </div>

    );

}

export default Dashboard;
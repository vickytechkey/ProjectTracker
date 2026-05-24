import { useState } from "react";
import "./SubTaskDetails.css";

function SubTaskDetails() {

    const [message, setMessage] = useState("");

    const [messages, setMessages] = useState([
        {
            user: "John",
            text: "Please make sure validation is added",
            time: "10:30 AM"
        },
        {
            user: "Alice",
            text: "Working on frontend changes",
            time: "11:15 AM"
        }
    ]);


    const addMessage = () => {

        if(message.trim()===""){
            return;
        }

        setMessages([
            ...messages,
            {
                user:"You",
                text:message,
                time:new Date().toLocaleTimeString()
            }
        ]);

        setMessage("");

    };


    return (

        <div className="subtask-page">

            <div className="header">

                <h1>Sub Task Details</h1>

                <button className="edit-btn">
                    Edit Task
                </button>

            </div>



            <div className="main-section">

                <div className="task-info">

                    <h2>
                        Task Information
                    </h2>

                    <div className="input-group">

                        <label>
                            Task Title
                        </label>

                        <input
                            type="text"
                            defaultValue="Design Login Page"
                        />

                    </div>


                    <div className="input-group">

                        <label>
                            Description
                        </label>

                        <textarea
                            rows="5"
                            defaultValue="Create responsive login page UI with validation"
                        />

                    </div>


                    <div className="row">

                        <div className="input-group">

                            <label>
                                Assignee
                            </label>

                            <select>

                                <option>
                                    John
                                </option>

                                <option>
                                    Alice
                                </option>

                                <option>
                                    David
                                </option>

                            </select>

                        </div>



                        <div className="input-group">

                            <label>
                                Labels
                            </label>

                            <input
                                type="text"
                                placeholder="Frontend,UI"
                            />

                        </div>

                    </div>


                    <div className="row">

                        <div className="input-group">

                            <label>
                                Status
                            </label>

                            <select>

                                <option>
                                    Pending
                                </option>

                                <option>
                                    In Progress
                                </option>

                                <option>
                                    Completed
                                </option>

                            </select>

                        </div>


                        <div className="input-group">

                            <label>
                                Priority
                            </label>

                            <select>

                                <option>
                                    Low
                                </option>

                                <option>
                                    Medium
                                </option>

                                <option>
                                    High
                                </option>

                            </select>

                        </div>

                    </div>


                    <button className="save-btn">

                        Save Changes

                    </button>

                </div>



                <div className="message-panel">

                    <h2>
                        Messages & Activity
                    </h2>


                    <div className="messages">

                    {
                        messages.map(
                            (msg,index)=>(

                            <div
                                key={index}
                                className="message-card"
                            >

                                <div>

                                <strong>
                                    {msg.user}
                                </strong>

                                <p>
                                    {msg.text}
                                </p>

                                </div>

                                <small>
                                    {msg.time}
                                </small>

                            </div>

                            )
                        )
                    }

                    </div>


                    <div className="message-input">

                        <textarea
                            rows="3"
                            value={message}
                            placeholder="Write a message..."
                            onChange={
                                (e)=>
                                setMessage(
                                    e.target.value
                                )
                            }
                        />

                        <button
                            onClick={addMessage}
                        >

                            Send

                        </button>

                    </div>

                </div>

            </div>



            <div className="history-section">

                <h2>
                    Task History
                </h2>

                <div className="timeline">

                    <div className="timeline-item">
                        Task Created
                    </div>

                    <div className="timeline-item">
                        Assigned to John
                    </div>

                    <div className="timeline-item">
                        Status changed → In Progress
                    </div>

                    <div className="timeline-item">
                        Label added → Frontend
                    </div>

                </div>

            </div>

        </div>

    );

}

export default SubTaskDetails;
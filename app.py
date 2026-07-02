# pyrefly: ignore [missing-import]
import streamlit as st
import datetime
import hashlib
from db.mongo import MongoDB
from projectManagement.main import (
    CreateProject,
    CreateSubTask,
    AddingMessage,
    BlockProject,
    ProgressProject,
    ResolveProject,
    BlockSubtask,
    ProgressSubtask,
    ResolvedSubtask
)

# Set page configuration
st.set_page_config(
    page_title="Project Tracker",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- Security Hashing -----------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ----------------- Database Helpers -----------------
def get_users():
    db = MongoDB(collectionname="users", findkey={})
    cursor = db.find()
    return list(cursor)

def get_user(username):
    db = MongoDB(collectionname="users", findkey={"username": username})
    res = db.findOne()
    return res

def add_user(username, password, role="User", status="PENDING", permissions=None):
    if permissions is None:
        permissions = ["read_only"]
    user_doc = {
        "username": username,
        "password_hash": hash_password(password),
        "role": role,
        "status": status,
        "permissions": permissions
    }
    db = MongoDB(collectionname="users", insertdata=user_doc)
    db.insertData()

def update_user_status(username, status):
    db = MongoDB(
        collectionname="users",
        filterkey={"username": username},
        updatekey={"status": status}
    )
    db.updateOne()

def update_user_permissions(username, role, permissions):
    db = MongoDB(
        collectionname="users",
        filterkey={"username": username},
        updatekey={"role": role, "permissions": permissions}
    )
    db.updateOne()

def get_projects():
    db = MongoDB(collectionname="Projects", findkey={})
    cursor = db.find()
    return list(cursor)

def get_subtasks(project_name):
    db = MongoDB(collectionname="subtasks", findkey={"project_name": project_name})
    cursor = db.find()
    return list(cursor)

def get_correspondence(project_name, subtask_name):
    db = MongoDB(collectionname="correspondence", findkey={"project_name": project_name, "subtask_name": subtask_name})
    cursor = db.find()
    return list(cursor)

def update_subtask_spent_efforts(project_name, subtask_name, spent_efforts):
    db = MongoDB(
        collectionname="subtasks",
        filterkey={"project_name": project_name, "subTask_name": subtask_name},
        updatekey={"spend_efforts": spent_efforts}
    )
    db.updateOne()

def get_sprints():
    db = MongoDB(collectionname="sprints", findkey={})
    cursor = db.find()
    return list(cursor)

def create_sprint(sprint_name, start_date, end_date, project_names):
    sprint_doc = {
        "sprint_name": sprint_name,
        "start_date": start_date,
        "end_date": end_date,
        "status": "ACTIVE",
        "project_names": project_names
    }
    db = MongoDB(collectionname="sprints", insertdata=sprint_doc)
    db.insertData()
    # Assign projects
    assign_projects_to_sprint(sprint_name, project_names)

def update_sprint_status(sprint_name, status):
    db = MongoDB(
        collectionname="sprints",
        filterkey={"sprint_name": sprint_name},
        updatekey={"status": status}
    )
    db.updateOne()

def update_project_sprint(project_name, sprint_name):
    db = MongoDB(
        collectionname="Projects",
        filterkey={"project_name": project_name},
        updatekey={"sprint_name": sprint_name}
    )
    db.updateOne()

def assign_projects_to_sprint(sprint_name, assigned_project_names):
    all_projects = get_projects()
    for proj in all_projects:
        p_name = proj["project_name"]
        if p_name in assigned_project_names:
            update_project_sprint(p_name, sprint_name)
        elif proj.get("sprint_name") == sprint_name:
            update_project_sprint(p_name, "")

def check_sla_breach(end_date_str):
    try:
        end_date = datetime.datetime.strptime(end_date_str, "%d-%m-%Y").date()
        return end_date < datetime.date.today()
    except Exception:
        return False

# ----------------- Session State Init -----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "user_permissions" not in st.session_state:
    st.session_state.user_permissions = []
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"
if "selected_project" not in st.session_state:
    st.session_state.selected_project = None
if "selected_subtask" not in st.session_state:
    st.session_state.selected_subtask = None

# Helper to redirect page
def navigate_to(page, project=None, subtask=None):
    st.session_state.current_page = page
    if project is not None:
        st.session_state.selected_project = project
    if subtask is not None:
        st.session_state.selected_subtask = subtask
    st.rerun()

# ----------------- Custom Premium CSS -----------------
st.markdown("""
<style>
/* App container adjustments */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Glassmorphic Project Card */
.project-card {
    background: rgba(30, 41, 59, 0.7);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.project-card:hover {
    transform: translateY(-4px);
    border-color: rgba(99, 102, 241, 0.6);
    box-shadow: 0 10px 30px rgba(99, 102, 241, 0.15);
}

/* Beautiful badges for status */
.status-badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.status-yet-to-start {
    background-color: rgba(148, 163, 184, 0.15);
    color: #94a3b8;
    border: 1px solid rgba(148, 163, 184, 0.3);
}
.status-progress {
    background-color: rgba(59, 130, 246, 0.15);
    color: #60a5fa;
    border: 1px solid rgba(59, 130, 246, 0.3);
}
.status-blocked {
    background-color: rgba(239, 68, 68, 0.15);
    color: #fca5a5;
    border: 1px solid rgba(239, 68, 68, 0.3);
}
.status-resolved {
    background-color: rgba(16, 185, 129, 0.15);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.3);
}

/* Metric styling */
.metric-container {
    background: rgba(30, 41, 59, 0.4);
    border-radius: 12px;
    padding: 16px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    text-align: center;
}

/* Correspondence chat style */
.chat-bubble {
    background: rgba(15, 23, 42, 0.6);
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 12px;
    border-left: 4px solid #6366f1;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    border-right: 1px solid rgba(255, 255, 255, 0.05);
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}
.chat-meta {
    font-size: 0.8rem;
    color: #94a3b8;
    margin-bottom: 6px;
    display: flex;
    justify-content: space-between;
}
.chat-user {
    font-weight: 700;
    color: #e2e8f0;
}
.chat-text {
    font-size: 0.95rem;
    color: #cbd5e1;
    line-height: 1.5;
}
</style>
""", unsafe_allow_html=True)

# Helper function to render HTML status badge
def get_status_badge_html(status):
    status_class = "status-yet-to-start"
    status_label = status
    
    if status in ["PROGRESS", "IN_PROGRESS", "STARTED", "ACTIVE"]:
        status_class = "status-progress"
        status_label = "In Progress" if status != "ACTIVE" else "Active"
    elif status == "BLOCKED":
        status_class = "status-blocked"
        status_label = "Blocked"
    elif status in ["RESOLVED", "DONE", "COMPLETED"]:
        status_class = "status-resolved"
        status_label = "Resolved" if status != "COMPLETED" else "Completed"
    elif status in ["YET_TO_START", "NOT_STARTED"]:
        status_class = "status-yet-to-start"
        status_label = "Yet To Start"
        
    return f'<span class="status-badge {status_class}">{status_label}</span>'

# ==========================================
# ============ AUTHENTICATION ===============
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #f8fafc; padding-bottom: 2rem;'>🎯 Project Tracker Portal</h1>", unsafe_allow_html=True)
    col_l, col_r = st.columns([1, 1])
    
    with col_l:
        st.markdown("<div class='project-card'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color:#6366f1; margin-top:0;'>🔑 Sign In</h2>", unsafe_allow_html=True)
        with st.form("login_form", clear_on_submit=False):
            li_username = st.text_input("Username").strip()
            li_password = st.text_input("Password", type="password")
            li_submit = st.form_submit_button("Log In", use_container_width=True)
            
            if li_submit:
                if not li_username or not li_password:
                    st.error("Please fill in both fields.")
                else:
                    user_doc = get_user(li_username)
                    if not user_doc:
                        st.error("User does not exist.")
                    else:
                        pwd_hash = hash_password(li_password)
                        if user_doc["password_hash"] != pwd_hash:
                            st.error("Incorrect password.")
                        elif user_doc["status"] == "PENDING":
                            st.warning("Your registration request is pending approval by an administrator.")
                        elif user_doc["status"] == "REJECTED":
                            st.error("Your access request has been rejected.")
                        else:
                            st.session_state.logged_in = True
                            st.session_state.username = user_doc["username"]
                            st.session_state.user_role = user_doc.get("role", "User")
                            st.session_state.user_permissions = user_doc.get("permissions", ["read_only"])
                            st.session_state.current_page = "Dashboard"
                            st.success("Successfully logged in!")
                            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
                            
    with col_r:
        st.markdown("<div class='project-card'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color:#34d399; margin-top:0;'>📝 Register Account</h2>", unsafe_allow_html=True)
        with st.form("signup_form", clear_on_submit=True):
            su_username = st.text_input("Preferred Username").strip()
            su_password = st.text_input("Choose Password", type="password")
            su_confirm = st.text_input("Confirm Password", type="password")
            su_submit = st.form_submit_button("Sign Up", use_container_width=True)
            
            if su_submit:
                if not su_username or not su_password or not su_confirm:
                    st.error("All fields are required.")
                elif su_password != su_confirm:
                    st.error("Passwords do not match.")
                elif len(su_password) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    existing = get_user(su_username)
                    if existing:
                        st.error("Username is already taken.")
                    else:
                        # Auto-approve first user as Admin
                        all_users = get_users()
                        if len(all_users) == 0:
                            add_user(su_username, su_password, role="Admin", status="APPROVED", permissions=["all"])
                            st.success("First user registered and auto-approved as Admin! You can log in now.")
                        else:
                            add_user(su_username, su_password, role="User", status="PENDING", permissions=["read_only"])
                            st.success("Registration submitted! Please request an administrator to approve your request.")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ==========================================
# ============ MAIN APPLICATION ============
# ==========================================

# ----------------- Sidebar -----------------
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #6366f1; margin-bottom: 0;'>🎯 ProjectTracker</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #94a3b8; font-size: 0.9rem;'>Logged in: <b>{st.session_state.username}</b> ({st.session_state.user_role})</p>", unsafe_allow_html=True)
    
    if st.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.user_role = None
        st.session_state.user_permissions = []
        st.session_state.current_page = "Dashboard"
        st.session_state.selected_project = None
        st.session_state.selected_subtask = None
        st.rerun()
        
    st.markdown("---")
    
    # Navigation Radio
    nav_options = {
        "Dashboard": "📊 Dashboard Overview",
        "Sprint": "🏃 Sprint Dashboard",
        "Explorer": "📁 Project Explorer",
        "Create": "➕ Create New Project"
    }
    
    # Check Admin Access
    if st.session_state.user_role == "Admin":
        nav_options["Admin"] = "🛡 Admin Panel"
        
    current_idx = list(nav_options.keys()).index(st.session_state.current_page)
    selected_nav = st.radio(
        "Navigation",
        options=list(nav_options.values()),
        index=current_idx
    )
    
    mapped_page = [k for k, v in nav_options.items() if v == selected_nav][0]
    if mapped_page != st.session_state.current_page:
        st.session_state.current_page = mapped_page
        st.rerun()
        
    st.markdown("---")
    # Quick info helper
    if st.session_state.selected_project:
        st.markdown(f"**Active Project:**\n`{st.session_state.selected_project}`")
        if st.session_state.selected_subtask:
            st.markdown(f"**Active Subtask:**\n`{st.session_state.selected_subtask}`")
        
        if st.button("Clear Selection", use_container_width=True):
            st.session_state.selected_project = None
            st.session_state.selected_subtask = None
            st.session_state.current_page = "Dashboard"
            st.rerun()

# ----------------- Pages -----------------

# Page 1: Dashboard
if st.session_state.current_page == "Dashboard":
    st.markdown("<h1 style='color: #f8fafc;'>Dashboard Overview</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8;'>Overview of all active tracked projects and subtasks</p>", unsafe_allow_html=True)
    
    projects = get_projects()
    
    # KPIs calculation
    total_proj = len(projects)
    progress_proj = len([p for p in projects if p.get("status") in ["PROGRESS", "IN_PROGRESS", "STARTED"]])
    blocked_proj = len([p for p in projects if p.get("status") == "BLOCKED"])
    resolved_proj = len([p for p in projects if p.get("status") in ["RESOLVED", "DONE"]])
    
    # Render KPI metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <h4 style="margin: 0; color: #94a3b8;">Total Projects</h4>
            <h2 style="margin: 5px 0 0 0; color: #f8fafc;">{total_proj}</h2>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-container">
            <h4 style="margin: 0; color: #60a5fa;">In Progress</h4>
            <h2 style="margin: 5px 0 0 0; color: #60a5fa;">{progress_proj}</h2>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-container">
            <h4 style="margin: 0; color: #fca5a5;">Blocked</h4>
            <h2 style="margin: 5px 0 0 0; color: #fca5a5;">{blocked_proj}</h2>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-container">
            <h4 style="margin: 0; color: #34d399;">Resolved</h4>
            <h2 style="margin: 5px 0 0 0; color: #34d399;">{resolved_proj}</h2>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br><h3 style='color: #e2e8f0;'>Projects List</h3>", unsafe_allow_html=True)
    
    if not projects:
        st.info("No projects created yet. Click 'Create New Project' in the sidebar or menu to start.")
    else:
        # Render project grid (2 columns)
        for i in range(0, len(projects), 2):
            cols = st.columns(2)
            for j in range(2):
                if i + j < len(projects):
                    proj = projects[i + j]
                    p_name = proj["project_name"]
                    p_status = proj.get("status", "YET_TO_START")
                    p_start = proj.get("start_date", "N/A")
                    p_end = proj.get("end_date", "N/A")
                    p_sprint = proj.get("sprint_name", "")
                    
                    # Fetch subtask stats for efforts
                    subtasks = get_subtasks(p_name)
                    total_subtasks = len(subtasks)
                    planned_efforts = sum(s.get("planned_efforts", 0) for s in subtasks)
                    spent_efforts = sum(s.get("spend_efforts", 0) for s in subtasks)
                    
                    badge_html = get_status_badge_html(p_status)
                    sprint_str = f"🏃 <b>Sprint:</b> {p_sprint}" if p_sprint else "🏃 <b>Sprint:</b> Unassigned"
                    
                    with cols[j]:
                        st.markdown(f"""
                        <div class="project-card">
                            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;">
                                <h3 style="margin: 0; color: #f8fafc; font-size: 1.4rem;">{p_name}</h3>
                                {badge_html}
                            </div>
                            <p style="margin: 4px 0; color: #94a3b8; font-size: 0.9rem;">
                                📅 <b>Duration:</b> {p_start} to {p_end}
                            </p>
                            <p style="margin: 4px 0; color: #cbd5e1; font-size: 0.9rem;">
                                {sprint_str}
                            </p>
                            <p style="margin: 4px 0; color: #94a3b8; font-size: 0.9rem;">
                                📝 <b>Subtasks:</b> {total_subtasks} task(s)
                            </p>
                            <p style="margin: 4px 0; color: #94a3b8; font-size: 0.9rem;">
                                📊 <b>Efforts:</b> {spent_efforts}h spent / {planned_efforts}h planned
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Use streamlit button aligned with card
                        if st.button(f"View Details: {p_name}", key=f"btn_{str(proj['_id'])}", use_container_width=True):
                            navigate_to("Explorer", project=p_name)

# Page 2: Sprint Dashboard
elif st.session_state.current_page == "Sprint":
    st.markdown("<h1 style='color: #f8fafc;'>Sprint Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8;'>Manage sprint cycles, track progress metrics, and detect SLA breaches.</p>", unsafe_allow_html=True)
    
    sprints = get_sprints()
    sprint_names = [s["sprint_name"] for s in sprints]
    
    tab_track, tab_create = st.tabs(["📊 Track Active Sprint", "➕ Create Sprint"])
    
    with tab_track:
        if not sprint_names:
            st.info("No sprints exist. Create a new sprint in the next tab to get started.")
        else:
            selected_sprint_name = st.selectbox("Select Sprint to View", options=sprint_names)
            sprint_doc = [s for s in sprints if s["sprint_name"] == selected_sprint_name][0]
            
            s_start = sprint_doc.get("start_date", "N/A")
            s_end = sprint_doc.get("end_date", "N/A")
            s_status = sprint_doc.get("status", "ACTIVE")
            
            # Fetch all projects currently assigned to this sprint in DB
            db_projects = [p for p in get_projects() if p.get("sprint_name") == selected_sprint_name]
            db_project_names = [p["project_name"] for p in db_projects]
            
            # Header card
            st.markdown(f"""
            <div class="project-card">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 15px;">
                    <h2 style="margin:0; color: #f8fafc;">🏃 {selected_sprint_name}</h2>
                    {get_status_badge_html(s_status)}
                </div>
                <hr style="border-color: rgba(255,255,255,0.05)">
                <p style="color: #cbd5e1; font-size:1.05rem;">📅 <b>Duration:</b> {s_start} to {s_end}</p>
                <p style="color: #cbd5e1; font-size:1.05rem;">📁 <b>Assigned Projects ({len(db_project_names)}):</b> {", ".join(db_project_names) if db_project_names else "None"}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Status update buttons for Sprint (Only if user has permissions to manage sprints)
            if "manage_sprints" in st.session_state.user_permissions or "all" in st.session_state.user_permissions or st.session_state.user_role == "Admin":
                col_sp1, col_sp2, col_sp3 = st.columns([1, 1, 2])
                with col_sp1:
                    if s_status != "ACTIVE" and st.button("Set Active", key="sp_act_btn", use_container_width=True):
                        update_sprint_status(selected_sprint_name, "ACTIVE")
                        st.success("Sprint marked as Active!")
                        st.rerun()
                with col_sp2:
                    if s_status != "COMPLETED" and st.button("Set Completed", key="sp_comp_btn", use_container_width=True):
                        update_sprint_status(selected_sprint_name, "COMPLETED")
                        st.success("Sprint marked as Completed!")
                        st.rerun()
                        
            # Compute sprint metrics
            num_projects = len(db_projects)
            sprint_subtasks = []
            for p_name in db_project_names:
                sprint_subtasks.extend(get_subtasks(p_name))
                
            num_tasks = len(sprint_subtasks)
            pending_tasks = len([s for s in sprint_subtasks if s.get("status") != "RESOLVED"])
            blocker_tasks = len([s for s in sprint_subtasks if s.get("status") == "BLOCKED"])
            
            sla_breaches = 0
            for s in sprint_subtasks:
                if s.get("status") != "RESOLVED":
                    s_end_str = s.get("end_date", "")
                    if check_sla_breach(s_end_str):
                        sla_breaches += 1
                        
            # Visual Cards
            col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
            with col_m1:
                st.markdown(f"""
                <div class="metric-container">
                    <h5 style="margin: 0; color: #94a3b8;">Projects</h5>
                    <h2 style="margin: 5px 0 0 0; color: #6366f1;">{num_projects}</h2>
                </div>
                """, unsafe_allow_html=True)
            with col_m2:
                st.markdown(f"""
                <div class="metric-container">
                    <h5 style="margin: 0; color: #94a3b8;">Tasks</h5>
                    <h2 style="margin: 5px 0 0 0; color: #f8fafc;">{num_tasks}</h2>
                </div>
                """, unsafe_allow_html=True)
            with col_m3:
                st.markdown(f"""
                <div class="metric-container">
                    <h5 style="margin: 0; color: #60a5fa;">Pending</h5>
                    <h2 style="margin: 5px 0 0 0; color: #60a5fa;">{pending_tasks}</h2>
                </div>
                """, unsafe_allow_html=True)
            with col_m4:
                st.markdown(f"""
                <div class="metric-container">
                    <h5 style="margin: 0; color: #fca5a5;">Blockers</h5>
                    <h2 style="margin: 5px 0 0 0; color: #fca5a5;">{blocker_tasks}</h2>
                </div>
                """, unsafe_allow_html=True)
            with col_m5:
                st.markdown(f"""
                <div class="metric-container" style="border-color: rgba(239, 68, 68, 0.4)">
                    <h5 style="margin: 0; color: #ef4444;">SLA Breaches</h5>
                    <h2 style="margin: 5px 0 0 0; color: #ef4444;">{sla_breaches}</h2>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("<br><h3 style='color: #e2e8f0;'>Sprint Subtask Tracker</h3>", unsafe_allow_html=True)
            
            if not sprint_subtasks:
                st.info("No tasks are currently active in this sprint.")
            else:
                # Display in table/listing
                for s in sprint_subtasks:
                    s_name = s["subTask_name"]
                    s_proj = s["project_name"]
                    s_status = s.get("status", "YET_TO_START")
                    s_start = s.get("start_date", "N/A")
                    s_end = s.get("end_date", "N/A")
                    
                    is_breached = (s_status != "RESOLVED" and check_sla_breach(s_end))
                    sla_badge = '<span class="status-badge status-blocked" style="background-color: rgba(239, 68, 68, 0.15); border-color: rgba(239, 68, 68, 0.3)">SLA BREACHED</span>' if is_breached else '<span class="status-badge status-resolved" style="background-color: rgba(16, 185, 129, 0.15); border-color: rgba(16, 185, 129, 0.3)">ON TRACK</span>'
                    
                    st.markdown(f"""
                    <div style="background-color: rgba(30, 41, 59, 0.4); border-radius: 12px; padding: 16px; margin-bottom: 12px; border: 1px solid rgba(255, 255, 255, 0.05);">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <b style="font-size: 1.15rem; color: #f8fafc;">{s_name}</b>
                                <span style="font-size: 0.85rem; color: #94a3b8; margin-left: 10px;">({s_proj})</span>
                            </div>
                            <div style="display: flex; gap: 8px;">
                                {sla_badge}
                                {get_status_badge_html(s_status)}
                            </div>
                        </div>
                        <div style="margin-top: 8px; font-size: 0.9rem; color: #94a3b8;">
                            📅 Duration: {s_start} to {s_end} | ⏱ {s.get("spend_efforts", 0)}h spent / {s.get("planned_efforts", 0)}h planned
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col_mng1, col_mng2 = st.columns([1, 4])
                    with col_mng1:
                        if st.button(f"Manage Task: {s_name}", key=f"mng_sp_sub_{s_proj}_{s_name}", use_container_width=True):
                            navigate_to("Explorer", project=s_proj, subtask=s_name)

    with tab_create:
        if "create_sprints" in st.session_state.user_permissions or "all" in st.session_state.user_permissions or st.session_state.user_role == "Admin":
            st.markdown("### Create New Sprint")
            with st.form("create_sprint_form", clear_on_submit=True):
                sp_name = st.text_input("Sprint Name", placeholder="e.g. Sprint 24Q3 - Core Architecture")
                sp_start = st.date_input("Start Date", value=datetime.date.today())
                sp_end = st.date_input("End Date", value=datetime.date.today() + datetime.timedelta(days=14))
                
                # Select projects to assign
                all_projects_list = get_projects()
                all_proj_names = [p["project_name"] for p in all_projects_list]
                sp_assigned_projects = st.multiselect("Assign Projects to Sprint", options=all_proj_names)
                
                submit_sp = st.form_submit_button("Create Sprint", use_container_width=True)
                if submit_sp:
                    if not sp_name.strip():
                        st.error("Sprint name is required.")
                    elif sp_start > sp_end:
                        st.error("Start date must be before or equal to end date.")
                    elif sp_name.strip() in sprint_names:
                        st.error("A sprint with this name already exists.")
                    else:
                        start_str = sp_start.strftime("%d-%m-%Y")
                        end_str = sp_end.strftime("%d-%m-%Y")
                        create_sprint(sp_name.strip(), start_str, end_str, sp_assigned_projects)
                        st.success(f"Sprint '{sp_name}' created successfully!")
                        st.rerun()
        else:
            st.warning("You do not have permissions to create sprints.")

# Page 3: Project Explorer
elif st.session_state.current_page == "Explorer":
    projects = get_projects()
    project_names = [p["project_name"] for p in projects]
    
    if not project_names:
        st.markdown("<h1 style='color: #f8fafc;'>Project Explorer</h1>", unsafe_allow_html=True)
        st.warning("No projects exist. Please create a project first.")
    else:
        # Choose active project
        default_proj_idx = 0
        if st.session_state.selected_project in project_names:
            default_proj_idx = project_names.index(st.session_state.selected_project)
            
        st.markdown("<h1 style='color: #f8fafc;'>Project Explorer</h1>", unsafe_allow_html=True)
        
        col_sel, col_empty = st.columns([1, 2])
        with col_sel:
            selected_proj_name = st.selectbox(
                "Select Project to Track",
                options=project_names,
                index=default_proj_idx
            )
            
        if selected_proj_name != st.session_state.selected_project:
            st.session_state.selected_project = selected_proj_name
            st.session_state.selected_subtask = None
            st.rerun()
            
        # Get active project doc
        proj_doc = [p for p in projects if p["project_name"] == selected_proj_name][0]
        p_status = proj_doc.get("status", "YET_TO_START")
        p_start = proj_doc.get("start_date", "N/A")
        p_end = proj_doc.get("end_date", "N/A")
        p_sprint = proj_doc.get("sprint_name", "")
        
        # Subtask navigation context
        if st.session_state.selected_subtask:
            # Subtask view
            subtasks = get_subtasks(selected_proj_name)
            subtask_names = [s["subTask_name"] for s in subtasks]
            
            if st.session_state.selected_subtask not in subtask_names:
                st.session_state.selected_subtask = None
                st.rerun()
                
            sub_doc = [s for s in subtasks if s["subTask_name"] == st.session_state.selected_subtask][0]
            s_name = sub_doc["subTask_name"]
            s_status = sub_doc.get("status", "YET_TO_START")
            s_start = sub_doc.get("start_date", "N/A")
            s_end = sub_doc.get("end_date", "N/A")
            s_planned = sub_doc.get("planned_efforts", 0)
            s_spent = sub_doc.get("spend_efforts", 0)
            s_creation = sub_doc.get("creationDate", "N/A")
            
            # Header
            st.markdown(f"### [Project: {selected_proj_name}](#) > Subtask: {s_name}")
            
            if st.button("⬅ Back to Project Details"):
                st.session_state.selected_subtask = None
                st.rerun()
                
            col_s1, col_s2 = st.columns([2, 1])
            with col_s1:
                st.markdown(f"""
                <div class="project-card">
                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 15px;">
                        <h2 style="margin:0; color: #f8fafc;">{s_name}</h2>
                        {get_status_badge_html(s_status)}
                    </div>
                    <hr style="border-color: rgba(255,255,255,0.05)">
                    <p style="color: #cbd5e1; font-size:1.05rem;">📅 <b>Duration:</b> {s_start} to {s_end} (Created on {s_creation})</p>
                    <p style="color: #cbd5e1; font-size:1.05rem;">📊 <b>Efforts:</b> {s_spent}h spent / {s_planned}h planned</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Check write permissions
                has_edit_permission = "edit_projects" in st.session_state.user_permissions or "all" in st.session_state.user_permissions or st.session_state.user_role == "Admin"
                
                # Subtask action buttons
                if has_edit_permission:
                    st.markdown("##### Update Subtask Status")
                    col_btn1, col_btn2, col_btn3 = st.columns(3)
                    with col_btn1:
                        if st.button("Mark In Progress", key="sub_prog_btn", use_container_width=True):
                            ProgressSubtask(selected_proj_name, s_name).progress_task()
                            st.success("Subtask marked as In Progress!")
                            st.rerun()
                    with col_btn2:
                        if st.button("Mark Blocked", key="sub_block_btn", use_container_width=True):
                            BlockSubtask(selected_proj_name, s_name).block_task()
                            st.warning("Subtask marked as Blocked!")
                            st.rerun()
                    with col_btn3:
                        if st.button("Mark Resolved", key="sub_res_btn", use_container_width=True):
                            ResolvedSubtask(selected_proj_name, s_name).resolve_task()
                            st.success("Subtask marked as Resolved!")
                            st.rerun()
                            
                    # Update Spent efforts form
                    with st.expander("⏱ Update Spent Efforts"):
                        with st.form("efforts_form", clear_on_submit=True):
                            new_spent = st.number_input("Spent Efforts (Hours)", min_value=0, value=int(s_spent))
                            submit_eff = st.form_submit_button("Save Spent Efforts")
                            if submit_eff:
                                update_subtask_spent_efforts(selected_proj_name, s_name, new_spent)
                                st.success(f"Spent efforts updated to {new_spent} hours!")
                                st.rerun()
                else:
                    st.info("You have read-only access. Status and efforts update options are disabled.")
                            
            with col_s2:
                # Correspondence/Messages
                st.markdown("### 💬 Correspondence Log")
                messages = get_correspondence(selected_proj_name, s_name)
                
                # Render messages
                msg_container = st.container(height=350)
                with msg_container:
                    if not messages:
                        st.info("No messages logged for this subtask yet.")
                    else:
                        for msg in messages:
                            m_date = msg.get("correspondence_date", "N/A")
                            m_user = msg.get("user", "User")
                            m_text = msg.get("message", "")
                            
                            st.markdown(f"""
                            <div class="chat-bubble">
                                <div class="chat-meta">
                                    <span class="chat-user">{m_user}</span>
                                    <span>{m_date}</span>
                                </div>
                                <div class="chat-text">{m_text}</div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                # Post message form
                has_post_permission = "post_correspondence" in st.session_state.user_permissions or "all" in st.session_state.user_permissions or st.session_state.user_role == "Admin"
                if has_post_permission:
                    with st.form("message_form", clear_on_submit=True):
                        st.markdown("##### Post Update / Message")
                        user_name = st.text_input("Your Name", value=st.session_state.username)
                        msg_body = st.text_area("Message Detail", placeholder="Type your subtask update or message here...")
                        submit_msg = st.form_submit_button("Send Message", use_container_width=True)
                        if submit_msg:
                            if not msg_body.strip():
                                st.error("Message content cannot be empty.")
                            else:
                                AddingMessage(selected_proj_name, s_name, msg_body, user=user_name).createcorrespondence()
                                st.success("Message posted!")
                                st.rerun()
                else:
                    st.info("You do not have permissions to post correspondence updates.")
                            
        else:
            # Project View
            sprint_tag = f" — Sprint: <b>{p_sprint}</b>" if p_sprint else ""
            st.markdown(f"""
            <div class="project-card">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 15px;">
                    <h2 style="margin:0; color: #f8fafc;">{selected_proj_name} {sprint_tag}</h2>
                    {get_status_badge_html(p_status)}
                </div>
                <hr style="border-color: rgba(255,255,255,0.05)">
                <p style="color: #cbd5e1; font-size:1.05rem;">📅 <b>Duration:</b> {p_start} to {p_end}</p>
            </div>
            """, unsafe_allow_html=True)
            
            has_edit_permission = "edit_projects" in st.session_state.user_permissions or "all" in st.session_state.user_permissions or st.session_state.user_role == "Admin"
            
            # Action buttons
            if has_edit_permission:
                st.markdown("##### Update Project Status")
                col_btn1, col_btn2, col_btn3 = st.columns(3)
                with col_btn1:
                    if st.button("Mark In Progress", key="proj_prog_btn", use_container_width=True):
                        ProgressProject(selected_proj_name).progressproject()
                        st.success("Project marked as In Progress!")
                        st.rerun()
                with col_btn2:
                    if st.button("Mark Blocked", key="proj_block_btn", use_container_width=True):
                        BlockProject(selected_proj_name).blockproject()
                        st.warning("Project marked as Blocked!")
                        st.rerun()
                with col_btn3:
                    if st.button("Resolve/Close Project", key="proj_res_btn", use_container_width=True):
                        ResolveProject(selected_proj_name).closeproject()
                        st.success("Project marked as Resolved!")
                        st.rerun()
            else:
                st.info("You have read-only access. Status and details change options are disabled.")
                    
            st.markdown("---")
            
            # Subtasks List
            col_sub1, col_sub2 = st.columns([2, 1])
            
            with col_sub1:
                st.markdown("### 📝 Subtasks")
                subtasks = get_subtasks(selected_proj_name)
                if not subtasks:
                    st.info("No subtasks created for this project yet.")
                else:
                    for s in subtasks:
                        s_name = s["subTask_name"]
                        s_status = s.get("status", "YET_TO_START")
                        s_start = s.get("start_date", "N/A")
                        s_end = s.get("end_date", "N/A")
                        s_planned = s.get("planned_efforts", 0)
                        s_spent = s.get("spend_efforts", 0)
                        
                        # Custom render
                        st.markdown(f"""
                        <div style="background-color: rgba(30, 41, 59, 0.4); border-radius: 12px; padding: 16px; margin-bottom: 12px; border: 1px solid rgba(255, 255, 255, 0.05);">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <b style="font-size: 1.15rem; color: #f8fafc;">{s_name}</b>
                                {get_status_badge_html(s_status)}
                            </div>
                            <div style="margin-top: 8px; font-size: 0.9rem; color: #94a3b8;">
                                📅 {s_start} to {s_end} | ⏱ {s_spent}h spent / {s_planned}h planned
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button(f"Manage Subtask: {s_name}", key=f"mng_sub_{str(s['_id'])}", use_container_width=True):
                            st.session_state.selected_subtask = s_name
                            st.rerun()
                            
            with col_sub2:
                # Add subtask form
                if has_edit_permission:
                    st.markdown("### ➕ Add Subtask")
                    with st.form("add_subtask_form", clear_on_submit=True):
                        sub_name = st.text_input("Subtask Name", placeholder="e.g. Layout Planning")
                        sub_start = st.date_input("Start Date", value=datetime.date.today())
                        sub_end = st.date_input("End Date", value=datetime.date.today() + datetime.timedelta(days=7))
                        sub_planned = st.number_input("Planned Efforts (Hours)", min_value=0, value=10)
                        
                        submit_sub = st.form_submit_button("Add Subtask", use_container_width=True)
                        if submit_sub:
                            if not sub_name.strip():
                                st.error("Subtask name is required.")
                            elif sub_start > sub_end:
                                st.error("Start date must be before or equal to end date.")
                            else:
                                # Convert dates
                                start_str = sub_start.strftime("%d-%m-%Y")
                                end_str = sub_end.strftime("%d-%m-%Y")
                                
                                CreateSubTask(
                                    taskname=sub_name,
                                    start_date=start_str,
                                    end_date=end_str,
                                    planned_efforts=int(sub_planned),
                                    project_name=selected_proj_name
                                ).CreateSubTask()
                                
                                st.success(f"Subtask '{sub_name}' added successfully!")
                                st.rerun()
                else:
                    st.info("You do not have permissions to add subtasks.")

# Page 4: Create New Project
elif st.session_state.current_page == "Create":
    has_create_permission = "create_projects" in st.session_state.user_permissions or "all" in st.session_state.user_permissions or st.session_state.user_role == "Admin"
    
    if has_create_permission:
        st.markdown("<h1 style='color: #f8fafc;'>Create New Project</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #94a3b8;'>Initialize a new project record and add details</p>", unsafe_allow_html=True)
        
        # Sprints dropdown
        sprints = get_sprints()
        sprint_options = ["None"] + [s["sprint_name"] for s in sprints]
        
        with st.form("create_project_form", clear_on_submit=True):
            proj_name = st.text_input("Project Name", placeholder="e.g. Marketing Campaign Q3")
            proj_start = st.date_input("Start Date", value=datetime.date.today())
            proj_end = st.date_input("End Date", value=datetime.date.today() + datetime.timedelta(days=30))
            planned_efforts = st.number_input("Initial Planned Efforts (Hours)", min_value=0, value=40)
            
            selected_sprint = st.selectbox("Assign to Sprint", options=sprint_options)
            
            submit_proj = st.form_submit_button("Create Project", use_container_width=True)
            if submit_proj:
                if not proj_name.strip():
                    st.error("Project name is required.")
                elif proj_start > proj_end:
                    st.error("Start date must be before or equal to end date.")
                else:
                    # Convert dates to string DD-MM-YYYY
                    start_str = proj_start.strftime("%d-%m-%Y")
                    end_str = proj_end.strftime("%d-%m-%Y")
                    
                    # Check if project already exists
                    existing_projects = get_projects()
                    if any(p["project_name"].lower() == proj_name.strip().lower() for p in existing_projects):
                        st.error("A project with this name already exists.")
                    else:
                        CreateProject(
                            projectName=proj_name.strip(),
                            project_start_end_date={"start_date": start_str, "end_date": end_str},
                            plannedEfforts=int(planned_efforts)
                        ).CreateProject()
                        
                        # Set sprint association
                        if selected_sprint != "None":
                            update_project_sprint(proj_name.strip(), selected_sprint)
                        
                        st.success(f"Project '{proj_name}' created successfully!")
                        # Auto select and redirect
                        navigate_to("Explorer", project=proj_name.strip())
    else:
        st.warning("You do not have permissions to create projects.")

# Page 5: Admin Control Panel
elif st.session_state.current_page == "Admin" and st.session_state.user_role == "Admin":
    st.markdown("<h1 style='color: #f8fafc;'>🛡 Admin Control Panel</h1>", unsafe_allow_html=True)
    
    tab_approve, tab_permissions = st.tabs(["🔒 Pending Approvals", "🔑 User Permissions"])
    
    # Tab 1: Pending Approvals
    with tab_approve:
        users = get_users()
        pending_users = [u for u in users if u.get("status") == "PENDING"]
        
        if not pending_users:
            st.info("No pending login/signup requests.")
        else:
            st.markdown(f"### Pending Requests ({len(pending_users)})")
            for u in pending_users:
                username = u["username"]
                col_u1, col_u2, col_u3 = st.columns([2, 1, 1])
                with col_u1:
                    st.markdown(f"👤 **{username}** (Requested User Access)")
                with col_u2:
                    if st.button("Approve", key=f"app_{username}", use_container_width=True):
                        update_user_status(username, "APPROVED")
                        st.success(f"Approved {username}!")
                        st.rerun()
                with col_u3:
                    if st.button("Reject", key=f"rej_{username}", use_container_width=True):
                        update_user_status(username, "REJECTED")
                        st.error(f"Rejected {username}!")
                        st.rerun()
                        
    # Tab 2: User Permissions
    with tab_permissions:
        users = get_users()
        approved_users = [u for u in users if u.get("status") == "APPROVED"]
        
        st.markdown("### Approved Users & Permissions")
        
        for u in approved_users:
            username = u["username"]
            role = u.get("role", "User")
            perms = u.get("permissions", ["read_only"])
            
            # Form or inputs to edit
            with st.expander(f"👤 {username} [{role}]"):
                with st.form(f"perm_form_{username}"):
                    new_role = st.selectbox("Role", ["User", "Admin"], index=0 if role == "User" else 1)
                    
                    available_perms = ["read_only", "create_projects", "edit_projects", "create_sprints", "manage_sprints", "post_correspondence", "all"]
                    default_selected = [p for p in perms if p in available_perms]
                    
                    new_perms = st.multiselect("Permissions Flags", options=available_perms, default=default_selected)
                    
                    save_btn = st.form_submit_button("Update User Permissions")
                    if save_btn:
                        update_user_permissions(username, new_role, new_perms)
                        st.success(f"Permissions updated for {username}!")
                        st.rerun()

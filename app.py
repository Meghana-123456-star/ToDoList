import streamlit as st

st.set_page_config(
    page_title="Todo List",
    page_icon="✅",
    layout="centered"
)

# -----------------------------
# Temporary task storage
# -----------------------------
if "tasks" not in st.session_state:
    st.session_state.tasks = []


# -----------------------------
# Title
# -----------------------------
st.title("✅ Todo List Application")
st.write("Manage your daily tasks easily.")


# -----------------------------
# Add Task
# -----------------------------
st.subheader("Add a Task")

task = st.text_input(
    "Task",
    placeholder="Enter your task..."
)

if st.button("Add Task", use_container_width=True):

    if task.strip() == "":
        st.warning("Please enter a task.")

    else:
        st.session_state.tasks.append({
            "title": task.strip(),
            "completed": False
        })

        st.success("Task added successfully!")
        st.rerun()


# -----------------------------
# Statistics
# -----------------------------
total = len(st.session_state.tasks)

completed = sum(
    task["completed"]
    for task in st.session_state.tasks
)

active = total - completed


st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total", total)

with col2:
    st.metric("Active", active)

with col3:
    st.metric("Completed", completed)


# -----------------------------
# Filter
# -----------------------------
st.divider()

st.subheader("My Tasks")

filter_option = st.radio(
    "Show:",
    ["All", "Active", "Completed"],
    horizontal=True
)


# -----------------------------
# Display Tasks
# -----------------------------
if total == 0:

    st.info("No tasks available. Add your first task!")

else:

    for index, task in enumerate(st.session_state.tasks):

        # Filtering
        if filter_option == "Active" and task["completed"]:
            continue

        if filter_option == "Completed" and not task["completed"]:
            continue


        col1, col2, col3 = st.columns([5, 1, 1])


        # Complete / Uncomplete
        with col1:

            checked = st.checkbox(
                task["title"],
                value=task["completed"],
                key=f"complete_{index}"
            )

            if checked != task["completed"]:

                task["completed"] = checked

                st.rerun()


        # Edit
        with col2:

            if st.button(
                "✏️",
                key=f"edit_{index}"
            ):

                st.session_state.editing = index
                st.rerun()


        # Delete
        with col3:

            if st.button(
                "🗑️",
                key=f"delete_{index}"
            ):

                st.session_state.tasks.pop(index)
                st.rerun()


        # Edit form
        if st.session_state.get("editing") == index:

            new_title = st.text_input(
                "Edit task",
                value=task["title"],
                key=f"edit_input_{index}"
            )

            col_save, col_cancel = st.columns(2)

            with col_save:

                if st.button(
                    "Save",
                    key=f"save_{index}"
                ):

                    if new_title.strip() == "":
                        st.warning("Task cannot be empty.")

                    else:
                        task["title"] = new_title.strip()

                        st.session_state.editing = None

                        st.success("Task updated!")

                        st.rerun()


            with col_cancel:

                if st.button(
                    "Cancel",
                    key=f"cancel_{index}"
                ):

                    st.session_state.editing = None
                    st.rerun()
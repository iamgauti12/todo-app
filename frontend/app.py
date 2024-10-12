import streamlit as st
import requests

# Set API URL
API_URL = "http://35.243.137.215"

# Main title and description
st.title("📝 To-Do App")
st.markdown("Manage your tasks efficiently with this simple To-Do app.")

# Function to fetch to-dos
def get_todos():
    response = requests.get(f"{API_URL}/todos")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to load to-dos")
        return []

# Function to add a new to-do
def add_todo(task):
    response = requests.post(f"{API_URL}/todos", json={"task": task})
    if response.status_code == 201:
        st.success("To-do added!")
    else:
        st.error("Failed to add to-do")

# Function to update a to-do
def update_todo(todo_id, task, done):
    response = requests.put(f"{API_URL}/todos/{todo_id}", json={"task": task, "done": done})
    if response.status_code == 200:
        st.success("To-do updated!")
    else:
        st.error("Failed to update to-do")

# Function to delete a to-do
def delete_todo(todo_id):
    response = requests.delete(f"{API_URL}/todos/{todo_id}")
    if response.status_code == 204:
        st.success("To-do deleted!")
    else:
        st.error("Failed to delete to-do")

# Function to export to-dos
def export_todos():
    response = requests.get(f"{API_URL}/export-todos")
    if response.status_code == 200:
        data = response.json()
        st.success(f"To-do list exported! [Download CSV]({data['gcs_uri']})")
    else:
        st.error("Failed to export to-dos")

# Fetch and display the to-dos
todos = get_todos()

# Section for exporting
st.markdown("### Export To-Do List")
st.button("📥 Export as CSV", on_click=export_todos)

# Display existing to-dos with edit/delete options
st.markdown("### Your To-Dos")
if todos:
    for todo in todos:
        with st.container():
            col1, col2, col3 = st.columns([5, 1, 1])
            with col1:
                task_input = st.text_input(f"Task {todo['id']}", value=todo['task'], key=todo['id'])
            with col2:
                done_checkbox = st.checkbox("Done", value=todo['done'], key=f"done_{todo['id']}")
            with col3:
                st.button("❌", on_click=delete_todo, args=(todo['id'],), key=f"delete_{todo['id']}")
            
            st.button("✅ Update", on_click=update_todo, args=(todo['id'], task_input, done_checkbox), key=f"update_{todo['id']}")

# Add a new to-do section with better spacing
st.markdown("---")
st.markdown("### Add a New Task")
new_task = st.text_input("Enter a new task", key="new_task")

if st.button("➕ Add Task"):
    if new_task:
        add_todo(new_task)
        st.session_state["new_task"] = ""  # Clear input field after adding
    else:
        st.error("Please enter a task")

# Footer message
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit")

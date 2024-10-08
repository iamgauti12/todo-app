import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000"
st.title("To-Do App")

# Fetch the to-do list
def get_todos():
    response = requests.get(f"{API_URL}/todos")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to load to-dos")
        return []

# Add a new to-do
def add_todo(task):
    response = requests.post(f"{API_URL}/todos", json={"task": task})
    if response.status_code == 201:
        st.success("To-do added!")
    else:
        st.error("Failed to add to-do")

# Update a to-do
def update_todo(todo_id, task, done):
    response = requests.put(f"{API_URL}/todos/{todo_id}", json={"task": task, "done": done})
    if response.status_code == 200:
        st.success("To-do updated!")
    else:
        st.error("Failed to update to-do")

# Delete a to-do
def delete_todo(todo_id):
    response = requests.delete(f"{API_URL}/todos/{todo_id}")
    if response.status_code == 204:
        st.success("To-do deleted!")
    else:
        st.error("Failed to delete to-do")

# Export to-do list as CSV
def export_todos():
    response = requests.get(f"{API_URL}/export-todos")
    if response.status_code == 200:
        data = response.json()
        st.success(f"To-do list exported! [Download CSV]({data['gcs_uri']})")
    else:
        st.error("Failed to export to-dos")

# Fetch the signed URL for the CSV file
def get_download_url():
    response = requests.get(f"{API_URL}/download-url")
    if response.status_code == 200:
        return response.json().get('url', '')
    else:
        st.error("Failed to fetch download URL.")
        return None

# Show todos
todos = get_todos()

# Export button
if st.button("Export To-Do List as CSV"):
    export_todos()

# Display existing to-dos with edit/delete features
for todo in todos:
    col1, col2, col3 = st.columns([5, 1, 1])
    with col1:
        task_input = st.text_input(f"Task {todo['id']}", value=todo['task'], key=todo['id'])
    with col2:
        done_checkbox = st.checkbox("Done", value=todo['done'], key=f"done_{todo['id']}")
    with col3:
        st.button("Delete", on_click=delete_todo, args=(todo['id'],), key=f"delete_{todo['id']}")
    
    if st.button("Update", key=f"update_{todo['id']}"):
        update_todo(todo['id'], task_input, done_checkbox)

# Add a new to-do section
st.text_input("New Task", key="new_task")
if st.button("Add"):
    new_task = st.session_state.get("new_task")
    if new_task:
        add_todo(new_task)
    else:
        st.error("Please enter a task")

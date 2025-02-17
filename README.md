# 📝 To-Do App

A simple and user-friendly To-Do application built with [Streamlit](https://streamlit.io/). This app allows users to create, update, delete, and manage their to-do tasks efficiently. It connects to a backend API hosted on Google Cloud, making it ideal for learning about full-stack development with Python.

## 🚀 Features

- **Add New To-Do**: Quickly add new tasks to your to-do list.
- **View To-Dos**: Display all existing tasks with their status.
- **Update Tasks**: Edit tasks and mark them as done or incomplete.
- **Delete Tasks**: Remove tasks from the list when they are no longer needed.
- **Export to CSV**: Download your to-do list as a CSV file for offline use.

## 🛠️ Technologies Used

- **Frontend**: Streamlit
- **Backend**: Python API hosted on Google Cloud
- **Deployment**: Google Kubernetes Engine (GKE), Docker
- **Database**: Google Cloud SQL (PostgreSQL)

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- [Python 3.8+](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/get-started)
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
- [Streamlit](https://docs.streamlit.io/)

## 📄 Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-username/todo-app.git
    cd todo-app
    ```

2. **Install Required Packages**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up Environment Variables**:
    Create a `.env` file and add your API details:
    ```
    API_URL=http://35.243.**.**
    ```

4. **Run the Streamlit App**:
    ```bash
    python -m streamlit run app.py
    ```

    The app should open in your web browser at `http://localhost:8501`.

## 📤 Deploying the Backend API to GCP

Follow these steps to deploy your API to Google Kubernetes Engine:

1. **Authenticate with Google Cloud**:
    ```bash
    gcloud auth login
    gcloud config set project [YOUR_PROJECT_ID]
    ```

2. **Create a Kubernetes Cluster**:
    ```bash
    gcloud container clusters create todo-cluster --zone us-central1-a --num-nodes 3 --machine-type e2-medium
    ```

3. **Push Docker Image to Google Container Registry (GCR)**:
    ```bash
    docker build -t gcr.io/[YOUR_PROJECT_ID]/todo-api:v1 .
    docker push gcr.io/[YOUR_PROJECT_ID]/todo-api:v1
    ```

4. **Deploy API to GKE**:
    Use the provided Kubernetes manifest files to deploy the API:
    ```bash
    kubectl apply -f deploy-backend.yaml
    kubectl apply -f deploy-frontend.yaml
    ```
## 📖 Usage

1. **Add a Task**: Use the text input to add new tasks.
2. **View Tasks**: See all tasks with their current status (done or not).
3. **Update Tasks**: Edit the task's name or mark it as done.
4. **Delete Tasks**: Click on the delete button to remove a task.
5. **Export Tasks**: Download your to-do list as a CSV file.

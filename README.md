# CSE 587 - Rainfall Prediction Project

This repository contains a Dockerized application for predicting whether it will rain in Australia. The application consists of a frontend and a backend, both running in separate Docker containers.

## Installation and Setup

### Prerequisites

- Docker installed on your machine

### Steps

1. Clone this repository:

   ```bash
   git clone https://github.com/imounish/cse587-rainfall-prediction.git
   ```

2. Navigate to the cloned repository:

   ```bash
   cd cse587-rainfall-prediction
   ```

3. Create a `.streamlit/secrets.toml` file in the current working directory `cse587-rainfall-prediction` and add the following secrets:

   ```toml
   predict_path = "predict"

   [backend.local]
   url = "http://backend:8000"
   ```

4. Build and run the Docker containers using Docker Compose:

   ```bash
   docker-compose up --build
   ```

5. Once the containers are up and running, you can access the application in your web browser at `http://localhost:8501`.

## Directory Structure

- `frontend`: Contains the frontend code written in Streamlit.
- `backend/`: Contains the backend code written in Python FastAPI.
- `docker-compose.yml`: Docker Compose file to orchestrate the containers.

## Usage

- Visit `http://localhost:8501` in your web browser to access the Weather Prediction App.
- Enter the required input features in the frontend UI and submit the form.
- The frontend will make a POST request to the backend API endpoint, which will predict whether it will rain based on the input features.

## API Endpoint

- The backend server exposes an API endpoint at `/predict` which accepts POST requests containing input features and returns the prediction.

## Notes

- Make sure to create the `.streamlit/secrets.toml` file as mentioned in the installation steps to securely store the API endpoint URL.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

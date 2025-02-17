# Flask Application

A simple Flask REST API application that provides health check and message endpoints.

## Description

This is a basic Flask application that exposes two endpoints:
- `/health` - Returns the health status of the application
- `/message` - Returns a greeting message

## Project Structure

```
flask-application/
├── app/
│   ├── main.py              # Main application file with Flask routes
│   ├── requirements.txt     # Python dependencies
│   └── venv/               # Python virtual environment
├── k8s/                    # Kubernetes manifests directory
├── Dockerfile              # Docker configuration for containerization
├── Jenkinsfile            # Jenkins CI/CD pipeline configuration
└── README.md              # Project documentation
```

## Prerequisites

- Python 3.x
- Docker (optional, for containerized deployment)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd flask-application
```

2. Install the required dependencies:
```bash
pip install -r app/requirements.txt
```

## Running the Application

### Local Development
To run the application locally:
```bash
python app/main.py
```
The application will start on `http://localhost:5000`

### Using Docker
1. Build the Docker image:
```bash
docker build -t flask-app .
```

2. Run the container:
```bash
docker run -p 5000:5000 flask-app
```

## API Endpoints

### Health Check
- **URL**: `/health`
- **Method**: `GET`
- **Response**: `{"status": "ok"}`

### Message
- **URL**: `/message`
- **Method**: `GET`
- **Response**: `{"message": "Hello from DevOps case study"}`

## CI/CD

This application includes a Jenkins pipeline configuration for automated building, testing, and deployment.

## License

[MIT](https://opensource.org/licenses/MIT)

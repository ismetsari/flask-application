# Flask Application

A simple Flask REST API application that provides health check and message endpoints also creates a random payload and stores it in MongoDB.

## Why This Project?

- Simple and functional
- Multiple endpoints
- Includes health check endpoint
- Good for showing DevOps practices
- Demonstrates basic web service concepts

## Description

This is a basic Flask application that exposes two endpoints:
- `/health` - Returns the health status of the application
- `/message` - Returns a greeting message

## Services
- Flask API: Creates 2 endpoints and genereates random payloads.
- MongoDB: Stores the payloads.

## Project Structure

```
flask-application/
├── app/
│   ├── main.py              # Main application file with Flask routes
│   ├── requirements.txt     # Python dependencies
│   └── venv/               # Python virtual environment
├── k8s/                    # Kubernetes manifests directory
│   ├── flask-application-deployment.yaml
│   ├── flask-application-service.yaml
│   ├── mongo-deployment.yaml
│   └── mongo-service.yaml
├── Dockerfile              # Docker configuration for containerization
├── Jenkinsfile            # Jenkins CI/CD pipeline configuration
└── README.md              # Project documentation
```

## Prerequisites

- Python 3.x
- Docker 
- Minikube
- Jenkins
- Kubectl
- Git
- Java 17 or higher(Dependency for Jenkins)

## Installation

1. Install Prequisities:
```bash
- Install dependencies you can find in prequisities section
```

2. Clone the repository:
```bash
git clone https://github.com/ismetsari/flask-application
```

3. Go to Jenkins UI and configure the pipeline
```bash
- If you didn't specify any port, you can reach it from http://localhost:8080/
- Click on "New Item" 
- Name pipeline as flask-api-pipeline(this is important since the name is used in commands)
- Select "Pipeline" as item type and click "OK"
- In the opened "Configuration" page, copy Jenkinsfile and paste it to script part and click "Save"
```

4. Move repository to Jenkins workspace. Jenkins creates dedicated workspace for every project we created from UI, we will move project to that workspace to avoid possible user permission issues.
```bash
sudo mv ~/flask-application /var/lib/jenkins/workspace/flask-api-pipeline
```

5. Be sure that jenkins user is member of docker group. You can check it by using groups jenkins command. If jenkins is not a member, you need to add it by using usermod command.
```bash
sudo usermod -aG docker jenkins(check the name)
```

6. Start minikube
```bash
minikube start --driver=docker
```

7. Jenkins uses user jenkins when it runs pipelines. Since then we need to have proper kubeconfig configuration and certificates for user. If you already have them for jenkins user you can skip this step. There are two ways to achive this.

7.1 Storing kubeconfig file as Jenkins credentials (This is the more robust way)
```bash
- Log into Jenkins UI
- Go to "Manage Jenkins" → "Credentials"
- Click on the domain where you want to store credentials (typically "global")
- Click "Add Credentials" in right top corner   
- From the "Kind" dropdown, select "Secret file"
- Click "Browse" and upload your kubeconfig file
- In the "ID" field, enter a meaningful ID like kubeconfig-minikube
- Click "OK" to save
```
7.2 If you have them for some other user **login** to that user and copy kubeconfig and certificates to jenkins user.
```bash
# Create .kube directory for jenkins user
sudo mkdir -p /var/lib/jenkins/.kube
# Copy your config file
sudo cp ~/.kube/config /var/lib/jenkins/.kube/
# Change ownership to jenkins user
sudo chown -R jenkins:jenkins /var/lib/jenkins/.kube/
# Create directories jor jenkins
sudo mkdir -p /var/lib/jenkins/.minikube
# Copy your minikube certificates
sudo cp -r ~/.minikube/* /var/lib/jenkins/.minikube/
# Fix the paths in the copied config file
sudo sed -i "s|$HOME/.minikube|/var/lib/jenkins/.minikube|g" /var/lib/jenkins/.kube/config
# Set ownership of directories(this is the critical part)
sudo chown -R jenkins:jenkins /var/lib/jenkins/.minikube
# Set permissions on all files first
sudo find /var/lib/jenkins/.minikube -type f -exec chmod 644 {} \;
sudo find /var/lib/jenkins/.kube -type f -exec chmod 644 {} \;
# Now set proper permissions on key files
sudo find /var/lib/jenkins/.minikube -name "*.key" -exec chmod 600 {} \;
```

8. After making these changes restart jenkins and docker services
```bash
systemctl restart jenkins
systemctl restart docker
```

9. Restarting services can damage minikube. Check its status with minikube status command. If it is not running, you need to start it.
```bash
minikube start --driver=docker
```

10. Run pipeline from UI
```bash
- Go to Jenkins UI
- Click on "Build Now" button for flask-api-pipeline
```

11. Check the pipeline logs
```bash
- Go to Jenkins UI
- Click on "flask-api-pipeline" project
- Click on "Console Output"
```

12. Now if you check pods. You should see 2 pods running.
```bash
kubectl get po
```

## How to Test Application

1. Verify Pod Health

    Ensure that all pods are running and in a healthy state.

2. Check Endpoints Availability 

    The application should be accessible via HTTP at **your-minikube-ip:30500**.

3. Health Check

    Navigate to **your-minikube-ip:30500/health**. You should see the response: {"status": "ok"}.

4. Message Endpoint Check

    Navigate to **your-minikube-ip:30500/message**. You should see the response: {"message": "Hello from DevOps case study"}.

5. Modify the Deployment

    Open **main.py** and update the message, for example: Change "Hello from DevOps case study" to "Hello from DevOps case study v2".

6. Run the Deployment Pipeline

    Execute the pipeline to redeploy the application.

7. Verify Deployment Update

    Once the pipeline completes and the pods are running, navigate to **your-minikube-ip:30500/message**. You should see the updated response: {"message": "Hello from DevOps case study v2"}.

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

This application includes a Jenkins pipeline configuration for automated building and deployment.

## Future Works and Improvements

- SonarQube can be added to the pipeline for code quality inspections.
- Security checks can be added to the pipeline.(e.g. Trivy, SonarQube)
- ReplicasCount in K8 deployments are set to 1 due to resource constraints. This can be increased for scalability purposes.
- Docker compose file can be add for local development. This make developers life easier.

## License

[MIT](https://opensource.org/licenses/MIT)

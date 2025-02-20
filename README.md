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

## Installation

1. Install Prequisities:
```bash
Install dependencies you can find in prequisities section
```

2. Clone the repository:
```bash
git clone https://github.com/ismetsari/flask-application
```

3. Go to Jenkins UI and configure the pipeline
```bash
If you didn't specify any port, you can reach it from http://localhost:8080/
- Click on "New Item" 
- Name pipeline as flask-api-pipeline(this is important since the name is used in commands)
- Select "Pipeline" as item type and click "OK"
- In the opened "Configuration" page, copy Jenkinsfile and paste it to script part and click "Save"
```

4. Move repository to Jenkins workspace
```bash
Jenkins creates dedicated workspace for every project we created from UI, we will move project to that workspace to avoid possible user permission issues.
mv ~/flask-application /var/lib/jenkins/workspace/flask-api-pipeline
```

5. Be sure that jenkins user is member of docker group
```bash
You can check it by using groups jenkins command. If jenkins is not a member, you need to add it by using usermod command.
sudo usermod -aG docker jenkins(check the name)
```

6. Jenkins uses user jenkins when it runs pipelines. Since then we need to have proper kubeconfig configuration and certificates for user. If you already have them for jenkins user you can skip this step. If you have them for some other user login to that user and run below commands.
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
# Set proper permissions (this is the critical part)
# Set ownership of directories
sudo chown -R jenkins:jenkins /var/lib/jenkins/.minikube
# Set permissions on all files first
sudo find /var/lib/jenkins/.minikube -type f -exec chmod 644 {} \;
sudo find /var/lib/jenkins/.kube -type f -exec chmod 644 {} \;
# Now set proper permissions on key files
sudo find /var/lib/jenkins/.minikube -name "*.key" -exec chmod 600 {} \;

!!! kubectl command in pipeline is already modified like: sh 'kubectl --kubeconfig=/var/lib/jenkins/.kube/config apply -f k8s/'
```

7. After making these changes restart jenkins and docker services
```bash
systemctl restart jenkins
systemctl restart docker
```

8. Run pipeline from UI
```bash
- Go to Jenkins UI
- Click on "Build Now" button for flask-api-pipeline
```

9. Check the pipeline logs
```bash
- Go to Jenkins UI
- Click on "flask-api-pipeline" project
- Click on "Console Output"
```

10. Check kubectl get po commands output
```bash
- Go to Jenkins UI
- Click on "flask-api-pipeline" project
- Click on "Console Output"
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

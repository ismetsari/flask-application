# Flask Application

A simple Flask REST API application that provides health check and message endpoints also creates a random payload and stores them in MongoDB.

## Why Did I Choose This Project?

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
- **Flask API**: Creates 2 endpoints and generates random payloads.
- **MongoDB**: Stores the payloads.

## API Endpoints

### Health Check
- **URL**: `/health`
- **Method**: `GET`
- **Response**: `{"status": "ok"}`

### Message
- **URL**: `/message`
- **Method**: `GET`
- **Response**: `{"message": "Hello from DevOps case study"}`

## Project Structure

```
flask-application/
├── app/
│   ├── main.py              # Main application file with Flask routes
│   ├── requirements.txt     # Python dependencies
│   └── venv/                # Python virtual environment
├── k8s/                     # Kubernetes manifests directory
│   ├── flask-application-deployment.yaml
│   ├── flask-application-service.yaml
│   ├── mongo-deployment.yaml
│   └── mongo-service.yaml
├── Dockerfile               # Docker configuration for containerization
├── Jenkinsfile              # Jenkins CI/CD pipeline configuration
└── README.md                # Project documentation
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

**NOTE:** It is recommended to have more than 4GB of memory to prevent issues during pipeline execution; otherwise, new pods may get stuck in a pending state.

1. Install Prequisities:
- Install dependencies you can find them in prequisities section above

2. Clone the repository:
```bash
git clone https://github.com/ismetsari/flask-application
```

3. Go to Jenkins UI and configure the pipeline
- If you did not specify any port, you can reach it from http://localhost:8080/
- Click on "New Item" 
- Name pipeline as flask-api-pipeline(this is important since the name is used in commands)
- Select "Pipeline" as item type and click "OK"
- In the opened "Configuration" page, copy Jenkinsfile and paste it to script part and click "Save"
- Click the "Build Now" button for the flask-api-pipeline. The build will fail, but this step is necessary for Jenkins to create the workspace mentioned in the next step.

4. Move the repository to the Jenkins workspace. Jenkins crated a dedicated workspace for our project(mentioned in the previous step). To prevent potential permission issues, we will move the project to that workspace.
```bash
sudo mv ~/flask-application /var/lib/jenkins/workspace/flask-api-pipeline
```

5. Ensure that the jenkins user is a member of the docker group. You can verify this by running the command **groups jenkins**. If the jenkins user is not a member, add it using the usermod command.
```bash
sudo usermod -aG docker jenkins
```

6. Start minikube
```bash
minikube start --driver=docker
```

7. Jenkins runs pipelines using the jenkins user. To ensure proper Kubernetes access, the jenkins user must have a correctly configured kubeconfig and certificates. **If these are already set up, you can skip step 7 completely.** If not there are two ways to achieve this:

**IMPORTANT NOTE:** 7.1 is a more robust approach, but it requires some UI configurations. To simplify the project setup for you, I used 7.2, as it only requires a simple copy-paste.

7.1 Storing kubeconfig file as Jenkins credentials (This is the more robust way)
- Log into Jenkins UI
- Go to "Manage Jenkins" → "Credentials"
- Click on the domain where you want to store credentials (typically "global")
- Click "Add Credentials" in right top corner   
- From the "Kind" dropdown, select "Secret file"
- Click "Browse" and upload your kubeconfig file
- In the "ID" field, enter a meaningful ID like kubeconfig-minikube
- Click "OK" to save
- Then change **Deploy to Minikube** stage in Jenkinsfile to below code.
- You also need to apply same stages for certificates.
```bash
    stage('Deploy to Minikube') {
      steps {
        withCredentials([file(credentialsId: 'kubeconfig-minikube', variable: 'KUBECONFIG')]) {
          sh '''
          echo "Deployment starting."
          cd flask-application
          kubectl --kubeconfig=$KUBECONFIG apply -f k8s/
          kubectl --kubeconfig=$KUBECONFIG rollout restart deployment flask-application
          echo "Deployment completed successfully."
          '''
        }
      }
    }
```
7.2 If they exist for another user, **log in to that user** and copy the kubeconfig and certificates to the Jenkins user's target directory.
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

8. After making these changes restart jenkins and docker services.
```bash
systemctl restart jenkins
systemctl restart docker
```

9. Restarting services can affect Minikube. Check its status using the **minikube status** command. If it is not running, start it manually.
```bash
minikube start --driver=docker
```

10. Run pipeline from UI
- Go to Jenkins UI
- Click on "Build Now" button for flask-api-pipeline

11. Check the pipeline logs
- Go to Jenkins UI
- Click on "flask-api-pipeline" project
- Click on "Console Output"
- Ensure that the pipeline is completed successfully

12. Now, if you check the pods, you should see two running: flask-application and mongo.
```bash
kubectl get po
```

## How to Test Application

1. Verify Pod Health

    Ensure that all pods are running and in a healthy state.

2. Check Endpoints Availability 

    The application should be accessible via HTTP at **your-minikube-ip:30500**.

3. Health Check

    Navigate to **your-minikube-ip:30500/health**. You should see the response: status: "ok".

4. Message Endpoint Check

    Navigate to **your-minikube-ip:30500/message**. You should see the response: message: "Hello from DevOps case study".

5. Modify the Deployment

    Open **main.py** and update the message, for example: Change "Hello from DevOps case study" to "Hello from Arf's DevOps case study".

6. Run the Deployment Pipeline

    Execute the pipeline to redeploy the application.

7. Verify Deployment Update

    Once the pipeline completes and the pods are running, navigate to **your-minikube-ip:30500/message**. You should see the updated response: message: "Hello from Arf's DevOps case study".

8. Check entries in MongoDB

    Exec it mongo pod 
    ```bash
    kubectl exec -it **mongo-pod-name** -- sh
    ```
    Swith to mongoshell
    ```bash
    mongosh
    ```
    Pick the database
    ```bash
    use events_db
    ```
    Print all entries
    ```bash
    db.events.find()
    ```

## CI/CD

This application includes a Jenkins pipeline configuration for automated building and deployment.

## Future Works and Improvements

- SonarQube can be added to the pipeline for code quality inspections.
- Security checks can be added to the pipeline.(e.g. Trivy, SonarQube)
- ReplicasCount in K8 deployments are set to 1 due to resource constraints. This can be increased for scalability purposes.
- Docker compose file can be add for local development. This make developers life easier.
- Pushing an image to the Minikube daemon is not a scalable approach. Using an image registry like Docker Hub offers a more robust and reusable solution. However, I did not use it because I don't have access to the company's Docker account. 🙂

## License

[MIT](https://opensource.org/licenses/MIT)

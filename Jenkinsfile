pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'flask-application:latest'
    }

    stages {

        stage('Build Docker Image') {
            steps {
                sh '''
                echo "Starting Docker Build"
                cd flask-application
                eval $(minikube docker-env)
                docker build --no-cache -t $DOCKER_IMAGE .
                echo "Docker build completed successfully."
                '''
            }
        }

        stage('Deploy to Minikube') {
            steps {
                sh '''
                echo "Deployment starting."
                cd flask-application
                kubectl --kubeconfig=/var/lib/jenkins/.kube/config apply -f k8s/
                # Force the pods to recreate by deleting them
                #kubectl --kubeconfig=/var/lib/jenkins/.kube/config delete pods -l app=flask-application
                kubectl --kubeconfig=/var/lib/jenkins/.kube/config rollout restart deployment flask-application
                echo "Deployment completed successfully."
                '''
            }
        }
    }
}

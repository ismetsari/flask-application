pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'ismetsari/flask-application:latest'
    }

    stages {

        stage('Build Docker Image') {
            steps {
                sh '''
                echo "Starting Docker Build"
                cd /home/ismet/repository/flask-application
                docker build --no-cache -t $DOCKER_IMAGE .
                echo "Docker build completed successfully."
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withDockerRegistry([credentialsId: 'dockerhub-credentials', url: 'https://index.docker.io/v1/']) {
                    sh '''
                    echo "image name is: ${DOCKER_IMAGE}"
                    docker push $DOCKER_IMAGE
                    '''
                }
            }
        }

        stage('Deploy to Minikube') {
            steps {
                sh '''
                echo "Deployment starting."
                cd /home/ismet/repository/flask-application
                kubectl --kubeconfig=/var/lib/jenkins/.kube/config apply -f k8s/
                kubectl --kubeconfig=/var/lib/jenkins/.kube/config rollout restart deployment flask-application
                echo "Deployment completed successfully."
                '''
            }
        }
    }
}

pipeline {
    agent {
        node {
            label 'linux'
        }
    }

    environment {

        DOCKERHUB_REPO = "peenesss/chatbot-llm-peraturan-tinggi"
        CONTAINER_NAME = "chatbot-llm-peraturan-tinggi"

        APP_PORT = "9092"
        VPS_IP = "103.149.177.39"

        PATH = "/usr/local/bin:/usr/bin:/bin:${env.PATH}"

        GEMINI_API_KEY = "AIzaSyALUpcIQcRl3h6chr1uAh5Z42bLbW1tz0w"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                source venv/bin/activate

                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Quality Checks') {
            parallel {

                stage('Lint') {
                    steps {
                        sh '''
                        source venv/bin/activate
                        pip install flake8
                        flake8 app || true
                        '''
                    }
                }

                stage('Test') {
                    steps {
                        sh '''
                        source venv/bin/activate
                        pip install pytest
                        pytest || true
                        '''
                    }
                }

            }
        }

        stage('Docker Build (CI)') {
            steps {
                sh '''
                docker build -t ${DOCKERHUB_REPO}:latest .
                '''
            }
        }

        stage('Push Image (CI)') {

            when {
                branch 'main'
            }

            steps {

                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {

                    sh '''
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    docker push ${DOCKERHUB_REPO}:latest
                    '''
                }
            }
        }

        stage('Deploy (CD)') {

            steps {

                sshagent(['vps-ssh']) {

                    sh """
                    ssh -o StrictHostKeyChecking=no root@${VPS_IP} '

                        echo "Stopping old container..."
                        docker stop ${CONTAINER_NAME} || true
                        docker rm ${CONTAINER_NAME} || true

                        echo "Pulling latest image..."
                        docker pull ${DOCKERHUB_REPO}:latest

                        echo "Running new container..."

                        docker run -d \
                        --name ${CONTAINER_NAME} \
                        -p ${APP_PORT}:8000 \
                        --restart unless-stopped \
                        -v /root/chatbot-datasets:/app/datasets:ro \
                        -e GEMINI_API_KEY=${GEMINI_API_KEY} \
                        --health-cmd="curl -f http://localhost:8000 || exit 1" \
                        --health-interval=30s \
                        --health-timeout=10s \
                        --health-retries=3 \
                        ${DOCKERHUB_REPO}:latest

                    '
                    """
                }
            }
        }

        stage('API Health Check') {
            steps {
                sh '''
                echo "Waiting API..."
                sleep 10

                curl -f http://${VPS_IP}:${APP_PORT} || exit 1
                '''
            }
        }

        stage('Debug') {
            steps {
                sh 'docker --version'
                sh 'docker ps -a'
                sh 'python3 --version'
                sh 'echo $PATH'
            }
        }

    }

    post {

        always {
            echo "Pipeline finished"
        }

        success {
            echo "Build SUCCESS"
        }

        failure {
            echo "Build FAILED"
        }

    }
}
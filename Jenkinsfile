pipeline {
    agent any

    environment {
        DOCKERHUB_USERNAME = 'anastasees' 
        APP_NAME = 'meter-service'
        DOCKER_CREDS_ID = 'dockerhub-creds' 
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test') {
           
            steps {
                sh 'pip install -r requirements.txt'
                sh 'python app_tests.py'
            }
            post {
                always {
                    junit 'test-reports/*.xml'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker Image...'
                    // Тут ми на Windows, тому використовуємо bat
                    bat "docker build -t %DOCKERHUB_USERNAME%/%APP_NAME%:latest -t %DOCKERHUB_USERNAME%/%APP_NAME%:%BUILD_NUMBER% ."
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    echo 'Pushing to Docker Hub...'
                    withCredentials([usernamePassword(credentialsId: DOCKER_CREDS_ID, usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                        // Використовуємо bat для логіну та пушу
                        // У bat змінні оточення викликаються через %VAR%
                        bat 'echo %PASS% | docker login -u %USER% --password-stdin'
                        bat "docker push %DOCKERHUB_USERNAME%/%APP_NAME%:latest"
                        bat "docker push %DOCKERHUB_USERNAME%/%APP_NAME%:%BUILD_NUMBER%"
                    }
                }
            }
        }
    }
}
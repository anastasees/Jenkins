pipeline {
    agent any

    environment {
        // ВАЖЛИВО: Ваш логін Docker Hub
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
            agent {
                docker {
                    image 'python:3.9-slim' 
                }
            }
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
                    sh "docker build -t $DOCKERHUB_USERNAME/$APP_NAME:latest -t $DOCKERHUB_USERNAME/$APP_NAME:${env.BUILD_NUMBER} ."
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    echo 'Pushing to Docker Hub...'
                    withCredentials([usernamePassword(credentialsId: DOCKER_CREDS_ID, usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                        sh "echo $PASS | docker login -u $USER --password-stdin"
                        sh "docker push $DOCKERHUB_USERNAME/$APP_NAME:latest"
                        sh "docker push $DOCKERHUB_USERNAME/$APP_NAME:${env.BUILD_NUMBER}"
                    }
                }
            }
        }
    }
}
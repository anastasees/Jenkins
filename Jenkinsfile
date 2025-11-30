pipeline {
    agent any

    environment {
        // УВАГА: Заміни на свій логін Docker Hub
        DOCKERHUB_USERNAME = 'ТУТ_ПИШИ_СВІЙ_ЛОГІН'
        
        // Назва образу
        APP_NAME = 'meter-service'
        
        // ID ключа, який ти створила в налаштуваннях Jenkins (Manage Credentials)
        // Якщо ти назвала його інакше, зміни цю назву тут
        DOCKER_CREDS_ID = 'dockerhub-creds' 
    }

    stages {
        // Етап 1: Завантаження коду з GitHub
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // Етап 2: Тестування (без xmlrunner)
        stage('Test') {
            agent {
                docker {
                    // Використовуємо ізольований контейнер Python для тестів
                    image 'python:3.9-slim' 
                }
            }
            steps {
                // Встановлюємо залежності та запускаємо тести
                sh 'pip install -r requirements.txt'
                sh 'python app_tests.py'
            }
        }

        // Етап 3: Створення Docker-образу
        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker Image...'
                    // Збираємо образ з двома тегами: latest і номером збірки
                    sh "docker build -t $DOCKERHUB_USERNAME/$APP_NAME:latest -t $DOCKERHUB_USERNAME/$APP_NAME:${env.BUILD_NUMBER} ."
                }
            }
        }

        // Етап 4: Завантаження на Docker Hub
        stage('Push to Docker Hub') {
            steps {
                script {
                    echo 'Pushing to Docker Hub...'
                    // Використовуємо логін і пароль з Credentials Jenkins
                    withCredentials([usernamePassword(credentialsId: DOCKER_CREDS_ID, usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                        // Логінимось
                        sh "echo $PASS | docker login -u $USER --password-stdin"
                        // Відправляємо образи
                        sh "docker push $DOCKERHUB_USERNAME/$APP_NAME:latest"
                        sh "docker push $DOCKERHUB_USERNAME/$APP_NAME:${env.BUILD_NUMBER}"
                    }
                }
            }
        }
    }
}
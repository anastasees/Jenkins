pipeline {
    // 'any' означає, що код виконується прямо на вашому комп'ютері (host machine)
    agent any

    environment {
        // ВАЖЛИВО: Ваш логін Docker Hub
        DOCKERHUB_USERNAME = 'anastasees' 
        APP_NAME = 'meter-service'
        // ID, який ви створили в Jenkins (Manage Jenkins -> Credentials)
        DOCKER_CREDS_ID = 'dockerhub-creds' 
    }

    stages {
        stage('Checkout') {
            steps {
                // Завантажуємо код з GitHub
                checkout scm
            }
        }

        stage('Test') {
            steps {
                script {
                    echo 'Installing requirements...'
                    // Використовуємо 'bat' для Windows команд
                    // pip має бути у вас в PATH
                    bat 'python -m pip install -r requirements.txt'
                    
                    echo 'Running tests...'
                    // Запускаємо тестування
                    bat 'python app_tests.py'
                }
            }
            post {
                always {
                    // Збираємо XML звіти (переконайтесь, що xmlrunner створює їх)
                    junit 'test-reports/*.xml'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker Image...'
                    // ${env.BUILD_NUMBER} - це змінна Jenkins, Groovy підставить її сам
                    bat "docker build -t ${DOCKERHUB_USERNAME}/${APP_NAME}:latest -t ${DOCKERHUB_USERNAME}/${APP_NAME}:${env.BUILD_NUMBER} ."
                }
            }
        }

       stage('Push to Docker Hub') {
            steps {
                script {
                    echo 'Pushing to Docker Hub...'
                    withCredentials([usernamePassword(credentialsId: DOCKER_CREDS_ID, usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                        // ЗМІНА ТУТ: Використовуємо одинарні лапки і %ЗМІННА%
                        // Це дозволяє Windows взяти пароль напряму з середовища, не "ламаючи" команду
                        bat 'docker login -u %USER% -p %PASS%'
                        
                        bat "docker push ${DOCKERHUB_USERNAME}/${APP_NAME}:latest"
                        bat "docker push ${DOCKERHUB_USERNAME}/${APP_NAME}:${env.BUILD_NUMBER}"
                    }
                }
            }
        }
    }
}
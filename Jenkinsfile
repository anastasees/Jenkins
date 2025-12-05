// Етап 2: Тестування
        stage('Test') {
           agent any,
            steps {
                // Встановлюємо залежності (тепер там є xmlrunner)
                sh 'pip install -r requirements.txt'
                // Запускаємо тести, які створять папку test-reports
                sh 'python app_tests.py'
            }
            post {
                always {
                    // Ця команда збирає XML звіти для Jenkins
                    junit 'test-reports/*.xml'
                }
            }
        }
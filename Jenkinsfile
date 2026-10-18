pipeline {
    agent any

    environment {
        // GANTI "ganti-username" dengan username Docker Hub kamu (huruf kecil semua)
        IMAGE_NAME           = 'alysharefa/simple-app'
        REGISTRY_CREDENTIALS = 'dockerhub-credentials'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                bat 'echo Mulai build aplikasi'
                bat 'docker --version'
                bat 'docker compose version'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat "docker build -t %IMAGE_NAME%:%BUILD_NUMBER% -t %IMAGE_NAME%:latest ."
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: REGISTRY_CREDENTIALS,
                                                  usernameVariable: 'DH_USER',
                                                  passwordVariable: 'DH_PASS')]) {
                    bat 'echo %DH_PASS%| docker login -u %DH_USER% --password-stdin'
                    bat "docker push %IMAGE_NAME%:%BUILD_NUMBER%"
                    bat "docker push %IMAGE_NAME%:latest"
                    bat 'docker logout'
                }
            }
        }

        stage('Deploy (App + Database)') {
            steps {
                bat 'docker compose -p simple-app up -d --build'
            }
        }

        stage('Verifikasi') {
            steps {
                // tunggu aplikasi dan database siap (ping dipakai sebagai "sleep" di Windows)
                bat 'ping -n 25 127.0.0.1 > nul'
                bat 'curl -f http://localhost:5000/health'
            }
        }
    }

    post {
        success {
            echo 'Pipeline selesai. Aplikasi jalan di http://localhost:5000'
        }
        failure {
            echo 'Pipeline gagal. Cek Console Output untuk detail error.'
        }
        always {
            echo 'Selesai build'
        }
    }
}

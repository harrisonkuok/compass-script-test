final String SOURCE_DIR = "source"

pipeline {
    agent any
    stages {
        
        stage ('Clean Before') {
            steps {
                script {
                    cleanRepo SOURCE_DIR
                }
            }
        }

        stage ('Checkout') {
            steps {
                dir (SOURCE_DIR) {
                    checkout scm
                }
            }
        }

        stage ('Python Script') {
            steps {
                script {
                    bat 'ls'
                    bat 'python --version'
                }
            }
        }
    }
}
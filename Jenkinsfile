final String SOURCE_DIR = "source"

pipeline {
    agent any
    stages {
        
        stage ('Clean Before') {
            steps {
                try {
                    dir (SOURCE_DIR) {
                    bat 'git clean -fdx'
                    bat 'git reset --hard'
                    }
                }
                catch (err) {
                    echo "clean failed, there probably is nothing to clean. ${err}"
                }
            }
        }

        stage ('Checkout') {
            steps {
                dir (SOURCE_DIR) {
                    checkout scm
                    bat 'dir'
                }
            }
        }

        stage ('Python Script') {
            steps {
                dir (SOURCE_DIR) {
                    bat 'python hello.py'
                }
            }
        }
    }
}
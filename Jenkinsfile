final String SOURCE_DIR = "source"

def cleanRepo(directory) {
    try {
        dir (directory) {
        bat 'git clean -fdx'
        bat 'git reset --hard'
        }
    }
    catch (err) {
        echo "clean failed, there probably is nothing to clean. ${err}"
    }
}

pipeline {
    agent any
    stages {
        
        stage ('Clean Before') {
            steps {
                cleanRepo SOURCE_DIR
                dir (SOURCE_DIR) {
                    bat 'dir'
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

        stage ('Clean After') {
            steps {
                cleanRepo SOURCE_DIR
                dir (SOURCE_DIR) {
                    bat 'dir'
                }
            }
        }
    }
}
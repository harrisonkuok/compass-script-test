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
                dir (SOURCE_DIR) {
                    bat '.\\venv\\Scripts\\activate'
                    bat 'python run-scripts.py'
                    bat 'python -m pytest --junitxml results.xml run-tests.py'
                }
            }
        }

        stage ('Publish') {
            steps {
                script {
                    junit SOURCE_DIR + '/*.xml'
                }
            }
        }
    }
}

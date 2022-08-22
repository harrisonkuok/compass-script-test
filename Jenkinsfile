final String SOURCE_DIR = "source"

pipeline {
    agent any
    stages {
        
        stage ('Clean Before') {
            steps {
                script {
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
        }

        stage ('Checkout') {
            steps {
                dir (SOURCE_DIR) {
                    bat 'dir'
                    checkout scm
                }
            }
        }

        stage ('Python Script') {
            steps {
                script {
                    bat 'python --version'
                }
            }
        }
    }
}
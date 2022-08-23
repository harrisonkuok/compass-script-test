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
                dir ('../Compass(trunk)/source/com.proteinsimple.compass.e4.product/target/products/compass/win32') {
                    bat 'dir'
                }
            }
        }
    }
}
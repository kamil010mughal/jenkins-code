pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                // This checks out the code from your repository defined in the job
                checkout scm
            }
        }
        stage('Build') {
            steps {
                // Replace this command with your project's build command
                // For example, for a Maven project you might use: sh 'mvn clean package'
                echo 'Building the project...'
                sh './build.sh'
            }
        }
        stage('Test') {
            steps {
                // Replace this command with your project's test command
                // For example, for a Maven project you might use: sh 'mvn test'
                echo 'Running tests...'
                sh './run-tests.sh'
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline execution completed.'
        }
        success {
            echo 'Build and tests succeeded!'
        }
        failure {
            echo 'Build or tests failed. Please check the logs.'
        }
    }
}

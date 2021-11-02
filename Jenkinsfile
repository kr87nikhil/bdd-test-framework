pipeline {
    agent {
        dockerfile {
            additionalBuildArgs '--target test'
            args '-v .:/pytest_project'
        }
    }
    options {
        timeout(time: 30, unit: 'MINUTES')
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '5', daysToKeepStr: '30'))
    }
    parameters {
        choice(
            name: 'TEST_SUITE',
            choices: ['calculator'],
            description: 'Select performance environment'
        )
    }
    environment {
        TEST_MODULE = test_${TEST_SUITE}
    }
    stages {
        stage('Git Checkout') {
            steps {
                git(
                    url: 'https://github.com/kr87nikhil/python-bdd.git',
                    branch: 'main',
                    credentialsId: 'GitHub'
                )
            }
        }
        stage('Test Execution') {
            steps {
                bat '''
                py.test ${TEST_MODULE} -n auto^
                --log-file=reports/${TEST_SUITE}/log.txt^
                --junitxml=reports/${TEST_SUITE}/execution_results.xml^
                --html=reports/${TEST_SUITE}/index.html --self-contained-html^
                --cucumberjson=reports/${TEST_SUITE}/cucumber.json --cucumberjson-expanded
                '''
            }
        }
    }
    post {
        failure {
            emailext body: '$DEFAULT_CONTENT', subject: '$DEFAULT_SUBJECT',
            recipientProviders: [developers(), requestor()]
        }
    }
}
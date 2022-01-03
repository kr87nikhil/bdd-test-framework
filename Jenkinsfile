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
                --log-file=target/${TEST_SUITE}/log.txt^
                --junitxml=target/${TEST_SUITE}/reports/execution_results.xml^
                --html=target/${TEST_SUITE}/reports/index.html --self-contained-html^
                --cucumberjson=target/${TEST_SUITE}/reports/cucumber.json
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
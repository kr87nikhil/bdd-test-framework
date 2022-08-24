pipeline {
    agent {
//     Root user needed to install virtualenv
        dockerfile {
            label 'docker-agent'
            additionalBuildArgs '--network=host'
            reuseNode true
        }
    }
    options {
        timeout(time: 30, unit: 'MINUTES')
        timestamps()
        skipStagesAfterUnstable()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '5', daysToKeepStr: '30'))
    }
    parameters {
        choice(
            name: 'TEST_SUITE',
            choices: ['calculator', 'dynamo_db'],
            description: 'Select test suite'
        )
        booleanParam(
            name: 'IS_TESTRAIL_ENABLED',
            defaultValue: false,
            description: 'Publish Test execution report to Testrail'
        )
    }
    stages {
        stage('Docker Build') {
            steps {
//                 sh '''
//                     pip install virtualenv
//                     if [ ! -d "$VIRTUAL_ENVIRONMENT" ]; then
//                         python3 -m virtualenv $VIRTUAL_ENVIRONMENT
//                     fi
//                 '''
                sh '''
                    pip install .
                '''
            }
        }
        stage('SonarQube analysis') {
            agent any
            steps {
                script {
                    scannerHome = tool 'SonarScanner 4.7'
                }
                withSonarQubeEnv(credentialsId: 'sonar-creds', installationName: 'SonarCloud') {
                    sh '${scannerHome}/bin/sonar-scanner -D"project.projectBaseDir=python-bdd'
                }
            }
        }
        stage("Quality Gate") {
            agent any
            steps {
                timeout(time: 30, unit: 'MINUTES') {
                    // Parameter indicates whether to set pipeline to UNSTABLE if Quality Gate fails
                    // true = set pipeline to UNSTABLE, false = don't
                    waitForQualityGate abortPipeline: true
                }
            }
        }
        stage('AWS Connectivity') {
            agent any
            environment {
                AWS_DEFAULT_REGION = 'us-east-1'
            }
            steps {
                sh 'aws --version'
                withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'aws-creds', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    sh 'aws ec2 describe-instances'
                }
            }
        }
        stage('Test Execution') {
            environment {
                RP_UUID = credentials('RP_ACCESS_KEY')  // ReportPortal Access token under "Profile" section
            }
            steps {
                sh '''
                    py.test -k ${params.TEST_SUITE} -n auto --reportportal --cache-clear\
                    --log-file=reports/${params.TEST_SUITE}/log.txt\
                    --junitxml=reports/${params.TEST_SUITE}/execution_result.xml\
                    --html=reports/${params.TEST_SUITE}/index.html --self-contained-html\
                    --cucumberjson=reports/${params.TEST_SUITE}/cucumber.json\
                    --alluredir=reports/${params.TEST_SUITE}/tmp/allure_results
                '''
            }
        }
        stage('Generate Reports') {
            agent any
            parallel {
                stage('TestRail Report') {
                    when {
                        expression {
                            return params.IS_TESTRAIL_ENABLED
                        }
                    }
                    steps {
                        // TestRail API KEY under "My Settings" section
                        withCredentials([usernamePassword(credentialsId: 'TESTRAIL',
                        passwordVariable: 'TESTRAIL_KEY', usernameVariable: 'TESTRAIL_ID')]) {
                            bat 'python tests/publish_testrail_report.py --test_modules QA'
                        }
                    }
                }
                stage('Cucumber BDD Report') {
                    steps {
                        cucumber buildStatus: 'UNSTABLE', reportTitle: "${params.TEST_SUITE} report", trendsLimit: 10,
                            fileIncludePattern: "reports/${params.TEST_SUITE}/cucumber.json", sortingMethod: 'ALPHABETICAL'
                    }
                }
                stage('HTML Report') {
                    steps {
                        publishHTML (target: [
                            allowMissing: false, alwaysLinkToLastBuild: false, keepAll: true,
                            reportName: "${params.TEST_SUITE} HTML Report", reportDir: "reports/${params.TEST_SUITE}", reportFiles: 'index.html'
                        ])
                    }
                }
                stage('Allure Report') {
                    steps {
                        script {
                            allure([
                                includeProperties: false, jdk: '', properties: [], reportBuildPolicy: 'ALWAYS',
                                results: [[path: "reports/${params.TEST_SUITE}/tmp/allure_results"]]
                            ])
                        }
                    }
                }
            }
        }
    }
    post {
        always {
            junit "reports/${params.TEST_SUITE}/execution_result.xml"
        }
        unstable {
            archiveArtifacts "reports/${params.TEST_SUITE}/log.txt"
        }
    }
}
pipeline {
    agent {
        dockerfile true
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
        password(
            name: 'REPORT_PORTAL_ACCESS_KEY',
            defaultValue: '',
            description: 'ReportPortal Access token under "Profile" section'
        )
        string(
            name: 'TESTRAIL_USERNAME',
            defaultValue: '',
            description: 'TestRail email id'
        )
        password(
            name: 'TESTRAIL_API_KEY',
            defaultValue: '',
            description: 'TestRail API KEY under "My Settings" section'
        )
    }
    environment {
        RP_UUID = "${params.REPORT_PORTAL_ACCESS_KEY}"
        TESTRAIL_ID = "${params.TESTRAIL_USERNAME}"
        TESTRAIL_KEY = "${params.TESTRAIL_API_KEY}"
    }
    stages {
        stage('SonarQube analysis') {
            environment {
                scannerHome = tool 'SonarScanner 4.7'
            }
            steps {
                withSonarQubeEnv(credentialsId: 'sonar-creds', installationName: 'SonarCloud') {
                    sh '${scannerHome}/bin/sonar-scanner -D"project.projectBaseDir=python-bdd'
                }
            }
        }
        stage("Quality Gate") {
            steps {
                timeout(time: 30, unit: 'MINUTES') {
                    // Parameter indicates whether to set pipeline to UNSTABLE if Quality Gate fails
                    // true = set pipeline to UNSTABLE, false = don't
                    waitForQualityGate abortPipeline: true
                }
            }
        }
        stage('AWS Connectivity') {
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
            steps {
                script {
                    REPORT_PORTAL_FLAG = "${params.REPORT_PORTAL_ACCESS_KEY}" == "" ? "" : "--reportportal"
                }
                sh '''
                    py.test -k ${params.TEST_SUITE} -n auto $REPORT_PORTAL_FLAG --cache-clear\
                    --log-file=reports/${params.TEST_SUITE}/log.txt\
                    --junitxml=reports/${params.TEST_SUITE}/execution_result.xml\
                    --html=reports/${params.TEST_SUITE}/index.html --self-contained-html\
                    --cucumberjson=reports/${params.TEST_SUITE}/cucumber.json\
                    --alluredir=reports/${params.TEST_SUITE}/tmp/allure_results
                '''
            }
        }
        stage('Generate Reports') {
            parallel {
                stage('TestRail Report') {
                    when {
                        expression {
                           return params.TESTRAIL_USERNAME == '' && params.TESTRAIL_KEY == ''
                        }
                    }
                    steps {
                        bat 'python tests/publish_testrail_report.py --test_modules QA'
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
        failure {
            archiveArtifacts "reports/${params.TEST_SUITE}/log.txt"
//             emailext body: '$DEFAULT_CONTENT', subject: '$DEFAULT_SUBJECT', recipientProviders: [developers()]
        }
    }
}
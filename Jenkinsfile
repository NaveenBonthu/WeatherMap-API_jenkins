pipeline {
    agent any
    
    parameters {
        string(name: 'CITY', defaultValue: 'London', description: 'City name for weather data')
        string(name: 'COUNTRY', defaultValue: 'UK', description: 'Country code')
        choice(name: 'RUN_TYPE', choices: ['Test', 'Production'], description: 'Select run type')
        booleanParam(name: 'SAVE_ARTIFACT', defaultValue: true, description: 'Save CSV as artifact')
    }
    
    environment {
        // Sensitive data should be stored in Jenkins credentials
        WEATHER_API_KEY = credentials('weather-api-key')
        
        // Project paths
        PROJECT_DIR = "${WORKSPACE}/weather-project"
        PYTHON_SCRIPT = "${PROJECT_DIR}/weather_collector.py"
        CSV_FILE = "${PROJECT_DIR}/weather_data.csv"
        REQUIREMENTS = "${PROJECT_DIR}/requirements.txt"
        
        // Notification settings
        EMAIL_TO = 'bonthu.naveen1@gmail.com'
    }
    
    stages {
        stage('Checkout Code') {
            steps {
                echo 'Checking out code from GitHub...'
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],  // or '*/master'
                    userRemoteConfigs: [[
                        url: 'https://github.com/NaveenBonthu/WeatherMap-API_jenkins',
                        credentialsId: ''  // Add if private repo
                    ]],
                    extensions: [[
                        $class: 'CleanBeforeCheckout'
                    ]]
                ])
                
                script {
                    // Display repository info
                    sh 'git log --oneline -5'
                }
            }
        }
        
        stage('Setup Environment') {
            steps {
                echo 'Setting up Python environment...'
                
                dir(PROJECT_DIR) {
                    // Check Python installation
                    sh 'python3 --version'
                    sh 'pip3 --version'
                    
                    // Install dependencies
                    sh 'pip3 install -r requirements.txt || echo "No requirements.txt found"'
                    
                    // List installed packages
                    sh 'pip3 list'
                }
            }
        }
        
        stage('Run Weather Script') {
            steps {
                echo 'Running weather data collection...'
                echo "City: ${params.CITY}, Country: ${params.COUNTRY}"
                
                dir(PROJECT_DIR) {
                    script {
                        try {
                            // Run Python script with parameters
                            sh """
                            python3 weather_collector.py \
                                --city "${params.CITY}" \
                                --country "${params.COUNTRY}" \
                                --api-key ${WEATHER_API_KEY}
                            """
                            
                            // Check if CSV was created
                            if (fileExists('weather_data.csv')) {
                                def lines = sh(script: 'wc -l weather_data.csv | awk \'{print $1}\'', returnStdout: true).trim()
                                echo "CSV file created/updated with ${lines} lines"
                                
                                // Display last entry
                                sh 'tail -1 weather_data.csv'
                            }
                        } catch (Exception e) {
                            echo "Error running script: ${e.getMessage()}"
                            currentBuild.result = 'FAILURE'
                            error('Script execution failed')
                        }
                    }
                }
            }
        }
        
        stage('Data Validation') {
            steps {
                echo 'Validating collected data...'
                
                dir(PROJECT_DIR) {
                    script {
                        if (fileExists('weather_data.csv')) {
                            // Basic validation
                            def fileSize = sh(script: "du -h weather_data.csv | cut -f1", returnStdout: true).trim()
                            def isValid = sh(
                                script: "head -1 weather_data.csv | grep -q 'temperature' && echo 'valid' || echo 'invalid'",
                                returnStdout: true
                            ).trim()
                            
                            echo "File size: ${fileSize}"
                            echo "CSV format: ${isValid}"
                            
                            if (isValid != 'valid') {
                                error('Invalid CSV format detected')
                            }
                        } else {
                            echo 'Warning: CSV file not found'
                        }
                    }
                }
            }
        }
        
        stage('Generate Report') {
            steps {
                echo 'Generating execution report...'
                
                dir(PROJECT_DIR) {
                    script {
                        // Create a simple report
                        def reportContent = """
                        WEATHER DATA COLLECTION REPORT
                        ================================
                        Timestamp: ${new Date()}
                        Build: ${env.BUILD_NUMBER}
                        Status: ${currentBuild.currentResult}
                        City: ${params.CITY}
                        Country: ${params.COUNTRY}
                        
                        Files Created:
                        """
                        
                        // List files
                        def files = sh(script: 'ls -la', returnStdout: true)
                        reportContent += files
                        
                        // Write report
                        writeFile file: 'jenkins_report.txt', text: reportContent
                        
                        // Display report
                        echo reportContent
                    }
                }
            }
        }
    }
    
    post {
        always {
            echo "Build ${env.BUILD_NUMBER} completed with status: ${currentBuild.currentResult}"
            
            // Clean workspace (optional)
            cleanWs()
        }
        
        success {
            echo 'Weather data collection successful!'
            
            script {
                if (params.SAVE_ARTIFACT) {
                    archiveArtifacts artifacts: "${PROJECT_DIR}/*.csv, ${PROJECT_DIR}/jenkins_report.txt", fingerprint: true
                    echo "Artifacts saved"
                }
            }
        }
        
        failure {
            echo 'Weather data collection failed!'
            
            // Optional: Send email notification
            // emailext (
            //     subject: "FAILED: Weather Data Collection Build #${env.BUILD_NUMBER}",
            //     body: "The weather data collection pipeline failed. Check Jenkins for details.",
            //     to: "${EMAIL_TO}"
            // )
        }
        
        unstable {
            echo 'Weather data collection unstable!'
        }
    }
}
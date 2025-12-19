pipeline {
    agent any
    
    parameters {
        string(name: 'CITY', defaultValue: 'London', description: 'City name')
        string(name: 'COUNTRY', defaultValue: 'UK', description: 'Country code')
    }
    
    environment {
        PYTHON = "C:\\Python\\python.exe"
        WEATHER_API_KEY = credentials('weather-api-key')
        OUTPUT_PATH = "C:\\weather-jenkins\\weather_data.csv"
        WORKSPACE_PATH = "weather_data_final.csv"  // File in workspace for archiving
    }
    
    stages {
        stage('Setup') {
            steps {
                echo 'Checking out code...'
                checkout scm
                
                bat 'python --version'
                bat 'pip install requests pandas --quiet'
                
                // Create output directory if it doesn't exist
                bat 'if not exist "C:\\weather-jenkins" mkdir "C:\\weather-jenkins"'
            }
        }
        
        stage('Collect Weather') {
            steps {
                echo "Getting weather for ${params.CITY}, ${params.COUNTRY}..."
                
                // Run Python script
                bat "\"%PYTHON%\" weather_collector.py --city \"${params.CITY}\" --country \"${params.COUNTRY}\" --api-key %WEATHER_API_KEY% --output \"%OUTPUT_PATH%\""
                
                // Also copy to workspace for archiving
                bat "copy /Y \"%OUTPUT_PATH%\" \"%WORKSPACE_PATH%\""
            }
        }
        
        stage('Verify & Archive') {
            steps {
                script {
                    // Check if file exists in output directory
                    def outputExists = bat(script: 'if exist "%OUTPUT_PATH%" echo EXISTS', returnStdout: true).contains('EXISTS')
                    
                    if (outputExists) {
                        echo 'SUCCESS: Weather data saved to C:\\weather-jenkins\\'
                        
                        // Show file info
                        bat 'dir "%OUTPUT_PATH%"'
                        
                        // Also check workspace copy
                        if (fileExists(env.WORKSPACE_PATH)) {
                            echo 'Archiving from workspace...'
                            archiveArtifacts artifacts: 'weather_data_final.csv', fingerprint: true
                            echo 'CSV file archived successfully!'
                        } else {
                            // Copy file to workspace if not there
                            bat 'copy /Y "%OUTPUT_PATH%" weather_data_final.csv'
                            archiveArtifacts artifacts: 'weather_data_final.csv', fingerprint: true
                            echo 'CSV file archived successfully!'
                        }
                    } else {
                        echo 'ERROR: No CSV file created'
                        error('Pipeline failed: No CSV output')
                    }
                }
            }
        }
    }
    
    post {
        always {
            echo "Build #${env.BUILD_NUMBER} - ${currentBuild.currentResult}"
        }
        success {
            echo 'PIPELINE SUCCESS! Weather data collected and saved.'
            bat 'echo CSV saved to: C:\\weather-jenkins\\weather_data.csv'
            bat 'echo Archived as: weather_data_final.csv'
        }
        failure {
            echo 'Pipeline completed with errors.'
        }
    }
}
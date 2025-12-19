pipeline {
    agent any
    
    parameters {
        string(name: 'CITY', defaultValue: 'London', description: 'City name')
        string(name: 'COUNTRY', defaultValue: 'UK', description: 'Country code')
    }
    
    environment {
        PYTHON = "C:\\Python\\python.exe"
        WEATHER_API_KEY = credentials('weather-api-key')
        OUTPUT_DIR = "C:\\weather-jenkins"
        OUTPUT_FILE = "C:\\weather-jenkins\\weather_data.csv"
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code...'
                checkout scm
                bat 'echo Files: && dir /B'
            }
        }
        
        stage('Verify Setup') {
            steps {
                echo 'Verifying setup...'
                bat """
                \"%PYTHON%\" --version
                \"%PYTHON%\" -c "import requests; print('requests OK')"
                \"%PYTHON%\" -c "import pandas; print('pandas OK')"
                """
                
                // Create output directory if it doesn't exist
                bat "if not exist \"%OUTPUT_DIR%\" mkdir \"%OUTPUT_DIR%\""
            }
        }
        
        stage('Run Weather Script') {
            steps {
                echo "Getting weather for ${params.CITY}, ${params.COUNTRY}..."
                script {
                    // Update Python script to save to specific path
                    // Option 1: Pass output path as argument if your script supports it
                    bat "\"%PYTHON%\" weather_collector.py --city \"${params.CITY}\" --country \"${params.COUNTRY}\" --api-key %WEATHER_API_KEY% --output \"%OUTPUT_FILE%\""
                    
                    // Option 2: Move the file after creation
                    bat """
                    if exist weather_data.csv (
                        echo Moving CSV to output directory...
                        move /Y weather_data.csv \"%OUTPUT_FILE%\"
                    )
                    """
                }
            }
        }
        
        stage('Verify & Archive') {
            steps {
                echo 'Processing results...'
                
                script {
                    // Check if CSV was created in the output directory
                    if (fileExists(env.OUTPUT_FILE)) {
                        echo 'Weather data collected successfully!'
                        
                        // Show file info
                        bat "dir \"%OUTPUT_FILE%\""
                        
                        // Archive the CSV from output directory
                        archiveArtifacts artifacts: "C:\\weather-jenkins\\weather_data.csv", fingerprint: true
                        echo 'CSV file archived as build artifact'
                    } else {
                        // Also check workspace as fallback
                        if (fileExists('weather_data.csv')) {
                            echo 'Found CSV in workspace, moving to output directory...'
                            bat "move /Y weather_data.csv \"%OUTPUT_FILE%\""
                            bat "dir \"%OUTPUT_FILE%\""
                            archiveArtifacts artifacts: "C:\\weather-jenkins\\weather_data.csv", fingerprint: true
                            echo 'CSV file archived as build artifact'
                        } else {
                            echo 'ERROR: No CSV file created'
                            error('Pipeline failed: No CSV output')
                        }
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
            bat "echo CSV saved to: %OUTPUT_FILE%"
        }
        failure {
            echo 'Pipeline completed with errors.'
        }
    }
}
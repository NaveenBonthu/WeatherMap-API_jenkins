pipeline {
    agent any
    
    parameters {
        string(name: 'CITY', defaultValue: 'London', description: 'City name')
        string(name: 'COUNTRY', defaultValue: 'UK', description: 'Country code')
    }
    
    environment {
        PYTHON = "C:\\Python\\python.exe"
        WEATHER_API_KEY = credentials('weather-api-key')
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '📥 Checking out code...'
                checkout scm
                bat 'echo Files: && dir /B'
            }
        }
        
        stage('Verify Setup') {
            steps {
                echo '🔧 Verifying setup...'
                bat """
                \"%PYTHON%\" --version
                \"%PYTHON%\" -c "import requests; print('requests OK')"
                \"%PYTHON%\" -c "import pandas; print('pandas OK')"
                """
            }
        }
        
        stage('Run Weather Script') {
            steps {
                echo "🌤️  Getting weather for ${params.CITY}, ${params.COUNTRY}..."
                bat "\"%PYTHON%\" weather_collector.py --city \"${params.CITY}\" --country \"${params.COUNTRY}\" --api-key %WEATHER_API_KEY%"
            }
        }
        
        stage('Verify & Archive') {
            steps {
                echo '📁 Processing results...'
                
                script {
                    // Check if CSV was created
                    if (fileExists('weather_data.csv')) {
                        echo '✅ Weather data collected successfully!'
                        
                        // Simple file check
                        bat 'dir weather_data.csv'
                        
                        // Archive the CSV
                        archiveArtifacts artifacts: 'weather_data.csv', fingerprint: true
                        echo '📦 CSV file archived as build artifact'
                    } else {
                        echo '❌ ERROR: No CSV file created'
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
            echo '🎉 PIPELINE SUCCESS! Weather data collected and saved.'
        }
        failure {
            echo '⚠️  Pipeline completed with errors.'
        }
    }
}
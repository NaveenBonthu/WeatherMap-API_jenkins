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
        stage('Checkout Code') {
            steps {
                echo '📥 Checking out repository...'
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/NaveenBonthu/WeatherMap-API_jenkins.git'
                    ]]
                ])
                
                bat '''
                echo Workspace Contents:
                dir /B
                echo.
                echo Current Directory: 
                cd
                '''
            }
        }
        
        stage('Verify Environment') {
            steps {
                echo '🔍 Verifying Python environment...'
                
                bat """
                echo Python Version:
                \"%PYTHON%\" --version
                
                echo.
                echo Checking installed packages:
                \"%PYTHON%\" -c "import requests; print('requests:', requests.__version__)"
                \"%PYTHON%\" -c "import pandas; print('pandas:', pandas.__version__)"
                
                echo.
                echo Testing script exists:
                if exist weather_collector.py (
                    echo ✅ weather_collector.py found
                    \"%PYTHON%\" -m py_compile weather_collector.py && echo ✅ Script syntax OK
                ) else (
                    echo ❌ weather_collector.py NOT FOUND
                    exit 1
                )
                """
            }
        }
        
        stage('Run Weather Script') {
            steps {
                echo "🌤️  Collecting weather for ${params.CITY}, ${params.COUNTRY}..."
                
                // SIMPLE ONE-LINE COMMAND - This will work!
                bat "\"%PYTHON%\" weather_collector.py --city \"${params.CITY}\" --country \"${params.COUNTRY}\" --api-key %WEATHER_API_KEY%"
            }
        }
        
        stage('Check Results') {
            steps {
                echo '📊 Checking output...'
                
                bat '''
                echo Checking for output files:
                dir *.csv *.txt *.log 2>nul || echo No output files found
                
                if exist weather_data.csv (
                    echo ✅ SUCCESS: CSV file created!
                    echo.
                    echo File information:
                    dir weather_data.csv
                    echo.
                    echo Preview (first 2 lines):
                    set /p line1=<weather_data.csv
                    echo 1: %line1%
                    for /f "skip=1 tokens=1,2,3 delims=," %%a in (weather_data.csv) do (
                        echo 2: %%a, %%b, %%c...
                        goto :done
                    )
                    :done
                ) else (
                    echo ❌ ERROR: weather_data.csv was NOT created
                    echo.
                    echo Checking for Python error output...
                    dir *.txt 2>nul || echo No error files
                    exit 1
                )
                '''
            }
        }
        
        stage('Archive Artifacts') {
            steps {
                echo '📁 Archiving results...'
                archiveArtifacts artifacts: 'weather_data.csv', fingerprint: true
                echo '✅ Artifact archived'
            }
        }
    }
    
    post {
        always {
            echo "🏁 Build #${env.BUILD_NUMBER} completed: ${currentBuild.currentResult}"
        }
        success {
            bat 'echo ✅ PIPELINE SUCCESSFUL - Weather data collected!'
        }
        failure {
            bat 'echo ❌ PIPELINE FAILED - Check console output above'
        }
    }
}
@Library('jenkins-helpers') _
testBuildReleasePoetryPackage {
    releaseToArtifactory = false
    testWithTox = true
    toxEnvList = ['py36', 'py37', 'py38']
    extraEnvVars = [
		secretEnvVar(key: 'COGNITE_API_KEY', secretName: 'cognite-sdk-python', secretKey: 'integration-test-api-key'),
		envVar(key: 'COGNITE_BASE_URL', value: "https://greenfield.cognitedata.com"),
		envVar(key: 'COGNITE_CLIENT_NAME', value: "cognite-sdk-experimental-integration-tests"),
		envVar(key: 'COGNITE_PROJECT', value: "python-sdk-test"),
	]
    beforeTests = {
        stage('Build Docs'){
            dir('./docs'){
                sh("poetry run sphinx-build -W -b html ./source ./build")
            }
        }
    }
}
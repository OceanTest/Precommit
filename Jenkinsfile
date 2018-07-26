import groovy.xml.*
import static java.util.UUID.randomUUID


def stageCases = [
    // Precommit
    "Build": [passedParser: this.&jsonTypePassedParser]
]

def testcases = ["Build"]

timestamps {
    node("ocean_linux_node") {
        stage('Build'){
            // Get some code from a GitHub repository
            git([url: 'https://github.com/OceanTest/Precommit.git', branch: 'master'])
            writeFile(file: 'Test/1098R20_SDK_sdk_nvme_ramdrive_debug.log', text: "Test")
            writeFile(file: 'Test/ASIC_NVME_Ramdisk_0.log', text: "Test")
            writeFile(file: 'Test/C1_ATCM.log', text: "Test")
            def results = [:]
            testcases.each { test ->
                def settings = stageCases[test]
                sh script: "mkdir -p testlogs/${test}"
                sh script: "python checkfile.py"
                
                //Collect all test results as a map 
                Map currentTestResults = [
                    (test): collectTestResults(                    
                        test,
                        settings.passedParser
                        )
                    ]
                results << currentTestResults    
            
                writeFile(file: 'ocean_test.xml', text: resultsAsJUnit(currentTestResults))
                //Generate the Junit Report 
                //archiveArtifacts(artifacts: 'ocean_test.xml', excludes: null)
                step([
                    $class: 'JUnitResultArchiver',
                    testResults: '**/ocean_test.xml'
                    ])
            }
            //Publish the Table      
            currentBuild.description = "<br /></strong>${resultsAsTable(results)}"
        }        
        stage("Test") {
            echo "Test Stage"
        }
    }
}

// Helper functions
def collectTestResults(String test, Closure passedParser) {
    String copyPath = "$env.ARTIFACTS_COPY_PATH"    
    
    // Initialize empty result map
    def resultMap = [:]

    // Gather all the logfiles produced    
    def logFiles = sh (
            script: "ls testlogs/${test}/*.log",
            returnStdout:true
            ).readLines()

    // Extract the test name and result from each logfile    
    logFiles.each { logFile ->
        passedParser(logFile, resultMap)
    }

    sh script: "tar -zpcv -f ${test}.tar.gz ${copyPath}/testlogs/${test}/*.log"
    // Store the zips as a tar file
    archiveArtifacts artifacts: "${test}.tar.gz", allowEmptyArchive: true

    // Cleanup
    sh "rm -rf testlogs/${test} ${test}.tar.gz"

    // Return the accumulated result
    return resultMap
}


// Parser for regression test results
def jsonTypePassedParser(logFile, resultMap) {   
    String  testName
    boolean testPassed 
    readFile(logFile).split("\n").each { line ->
        testName = line.subSequence(0,line.lastIndexOf(":"))   
        testPassed = line.contains("PASS")
        resultMap << [(testName): testPassed]
        println resultMap
    }    
    return resultMap  
}


@NonCPS
String resultsAsTable(def testResults) {
    StringWriter  stringWriter  = new StringWriter()
    MarkupBuilder markupBuilder = new MarkupBuilder(stringWriter)

    // All those delegate calls here are messing up the elegancy of the MarkupBuilder
    // but are needed due to https://issues.jenkins-ci.org/browse/JENKINS-32766
    markupBuilder.html {
        delegate.body {
            delegate.style(".passed { color: #468847; background-color: #dff0d8; border-color: #d6e9c6; } .failed { color: #b94a48; background-color: #f2dede; border-color: #eed3d7; }", type: 'text/css')
            delegate.table {
                testResults.each { test, testResult ->
                    delegate.delegate.tr {
                        delegate.td {
                            delegate.strong("[Stage] Build ")
                            delegate.a("Build Logs", href: "${env.BUILD_URL}/artifact/" + "${test}.tar.gz")
                        }
                    }
                    testResult.each { testName, testPassed ->
                        delegate.delegate.delegate.tr {
                            delegate.td("$testName", class: testPassed ? 'passed' : 'failed')
                        }
                    }
                }
            }
        }
    }
    return stringWriter.toString()
}

@NonCPS
String resultsAsJUnit(def testResults) {
    StringWriter  stringWriter  = new StringWriter()
    MarkupBuilder markupBuilder = new MarkupBuilder(stringWriter)
    // All those delegate calls here are messing up the elegancy of the MarkupBuilder
    // but are needed due to https://issues.jenkins-ci.org/browse/JENKINS-32766
    markupBuilder.testsuites {
        testResults.each{ test, testresult ->
            delegate.delegate.testsuite(name: testresult.testName, tests: testresult.size(), failures: testresult.values().count(false)) {
                testresult.each{ testName, testPassed ->
                    delegate.delegate.testcase(name: testName) {
                        if(!testPassed){
                            echo "${testResults.testPassed}"
                            delegate.failure()
                        }
                    }
                }
            }
        }
    }  
  return stringWriter.toString()
}
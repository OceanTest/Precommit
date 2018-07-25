import groovy.xml.*
import static java.util.UUID.randomUUID

timestamps {
    node("ocean_linux_node") {
        stage('Checkout'){
        // Get some code from a GitHub repository
            git([url: 'https://github.com/OceanTest/Precommit.git', branch: 'master'])        
        }
        
        Map currentTestResults = [ "Test": collectTestResults()]        
        stage("GenerateXML") {
            currentBuild.description = "Test"
            writeFile(file: 'ocean_test.xml', text: resultsAsJUnit(currentTestResults))
            //Generate the Junit Report 
            archiveArtifacts(artifacts: 'ocean_test.xml', excludes: null)
            step([
                  $class: 'JUnitResultArchiver',
                  testResults: '**/ocean_test.xml'
                ])
            //Publish the Table      
            currentBuild.description = "<br /></strong>${resultsAsTable(currentTestResults)}"
        }
    }
}

// Helper functions
def collectTestResults() {
  // Initialize empty result map
    String  testName
    boolean testPassed 
    def resultMap = [:]
    def logFiles = sh (
            script: "ls /home/jenkins/workspace/Log_Upload_Test/Log_Test*.log",
            returnStdout:true
            ).readLines()

    logFiles.each{ logFile ->            
            testName   = (logFile =~ /(\w*)\.log/)[0][1]
            testPassed = readFile(logFile).contains("=== Test Passed OK ===")
            resultMap << [(testName): testPassed]
        }
  return resultMap
}

def logParser(logFile) {
  // Initialize empty result map
  def logMap = [:]
  String  testName = (logFile =~ /(\w*)\.log/)[0][1]
  logMap << [(testName): logFile]
  return logMap
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

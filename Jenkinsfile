import groovy.json.JsonSlurper

def FRESHBUILDS_VERSION = "1.2.1"
def APP_NAME = 'pullsbury-gitboy'

pipeline {
  agent {
    label "jenkins-python-fbtest"
  }
  environment {
    ARTIFACTORY_CREDENTIALS = credentials('freshbooks-bot-artifactory')
    SLACK_TOKEN = credentials('slack-bot-token')
  }
  options {
    timeout(time: 20, unit: 'MINUTES')
    buildDiscarder(logRotator(daysToKeepStr: '15', artifactDaysToKeepStr: '15'))
  }
  stages {
    stage('Initialization') {
      steps {
        container('python') {
          script {
            sh "sudo pip install -i https://${ARTIFACTORY_CREDENTIALS_USR}:${ARTIFACTORY_CREDENTIALS_PSW}@freshbooks.jfrog.io/freshbooks/api/pypi/pypi/simple freshbuilds==${FRESHBUILDS_VERSION}"

            sshagent(credentials: ["github-freshbooks-bot-ssh-key"]){
              if(env.BRANCH_NAME == 'master'){
                APP_VERSION = parseJsonText(sh(script:"freshbuilds tagger -j print_next_tag", returnStdout: true).trim().split("\n").last())
                APP_VERSION = APP_VERSION.calver_tag
                sh script: "freshbuilds tagger -j tag"
              }
              else{
                APP_VERSION = "${env.BRANCH_NAME}-" + "${env.BUILD_NUMBER}"
              }
            }
          }
        }
      }
    }
    stage('Install python3.8') {
      steps {
        container('python') {
          sh "sudo apt-get update"
          sh "sudo apt-get install -y software-properties-common"
          sh "sudo add-apt-repository -y ppa:deadsnakes/ppa"
          sh "sudo apt-get update"
          sh "sudo apt-get install -y python3.8"
          sh "curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py"
          sh "python3.8 get-pip.py"
          sh "rm get-pip.py"
        }
      }
    }
    stage('Build and Test') {
      parallel {
        stage('Build Application Image') {
          when {
            expression {
              (env.BRANCH_NAME == 'master')
            }
          }
          steps {
            container('python') {
              script {
                sh "APP_VERSION=${APP_VERSION} make build"
              }
            }
          }
        }
        stage('Lint and Test') {
          stages {
            stage('Install') {
              steps {
                container('python') {
                  sh "make dev-install"
                }
              }
            }
            stage('Lint') {
              steps {
                container('python') {
                  sh "pipenv run make lint"
                }
              }
            }
            stage('Unit Tests') {
              steps {
                container('python') {
                  sh "pipenv run make test"
                  cobertura coberturaReportFile: "coverage.xml"
                }
              }
            }
          }
        }
      }
    }
    stage('Tag and Push Image') {
      when {
        expression {
          (env.BRANCH_NAME == 'master')
        }
      }
      steps {
        container('python') {
          sh "docker push gcr.io/freshbooks-builds/${APP_NAME}:${APP_VERSION}"
          sh "docker tag gcr.io/freshbooks-builds/${APP_NAME}:${APP_VERSION} gcr.io/freshbooks-builds/${APP_NAME}:latest"
          sh "docker push gcr.io/freshbooks-builds/${APP_NAME}:latest"
        }
      }
    }
    stage('Deploy pullsbury-gitboy'){
      when {
        expression {
          (env.BRANCH_NAME == 'master')
        }
      }
      steps {
        container('python') {
          sh 'curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.15.12/bin/linux/amd64/kubectl'
          sh 'chmod +x ./kubectl'
          sh "sed \"s/APP_VERSION/${APP_VERSION}/\" deploy.yaml | ./kubectl apply -f -"
        }
      }
    }
  }
  post {
    always {
      container('python') {
        notifyStatus(currentBuild, SLACK_TOKEN)
      }
    }
  }
}

@NonCPS
def parseJsonText(String json) {
  def object = new JsonSlurper().parseText(json)
  if(object instanceof groovy.json.internal.LazyMap) {
      return new HashMap<>(object)
  }
  return object
}

def notifyStatus(build, slackToken) {
  def commits = fetchGitCommits(build)
  def status = build.currentResult
  sh "freshbuilds slack -st ${slackToken} notify_status -s ${status} -r . -c ${commits}"
}

def fetchGitCommits(build) {
  def commits = []
  if (!(env.BRANCH_NAME ==~ /^PR-\d+$/)) {
    commits = getBuildChangeSets(build)
  }

  return commits.size() == 0 ? commitHashForBuild(build) : commits.join(',')
}

@NonCPS
def getBuildChangeSets(build) {
  def commits = []
  if (build == null) {
    return commits
  }
  if (build.rawBuild.changeSets.size() == 0) {
    commits.addAll(getBuildChangeSets(build.getPreviousBuild()))
  } else {
    build.rawBuild.changeSets.each {
      it.each {
        commits.add(it.commitId)
      }
    }
  }

  return commits
}

@NonCPS
def commitHashForBuild(build) {
  def scmAction = build?.rawBuild?.actions.find {
    action -> action instanceof jenkins.scm.api.SCMRevisionAction
  }

  if (scmAction?.revision == null) {
    return "${GIT_COMMIT}"
  }
  else if (scmAction?.revision instanceof org.jenkinsci.plugins.github_branch_source.PullRequestSCMRevision) {
    return scmAction?.revision.getPullHash()
  }

  return scmAction?.revision.getHash()
}

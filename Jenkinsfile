pipeline {
  agent none
  options {
    skipDefaultCheckout true
  }
  environment {
    harbor=credentials('harbor')
    IMAGE_TAG = sh(returnStdout: true, script: "git rev-parse --short=10 HEAD").trim()

  }

  stages {
    stage("Build docker image") {
      parallel {
        stage("Build docker scrapy image") {
          agent {label 'docker'}
          steps {
            dir('scrapy') {
              sh 'docker build -t scrapy:${IMAGE_TAG} .'
            }
          }
        }
        stage("Build docker api image") {
          agent {label 'docker'}
          steps {
            dir('api'){
              sh 'docker build -t api:${IMAGE_TAG} .'
            }
          }
        }
      }
    }
    stage("Remove orpans containers") {
      agent {label 'docker'}
      steps {
        sh 'docker compose down --remove-orphans'
      }
    }
    stage("Login to Harbor Registry") {
      agent {label 'docker'}
      steps {
        sh 'echo $harbor_PSW | docker login 10.33.109.104 -u $harbor_USR --password-stdin'
      }
    }
    stage("Push New data-crawling image") {
      parallel {
        stage("Push Docker Scrapy Image") {
          agent {label 'docker'}
          steps {
            sh 'docker tag scrapy 10.33.109.104/data-crawling/scrapy:'
            sh 'docker push 10.33.109.104/data-crawling/scrapy:${IMAGE_TAG}'
          }
        }
        stage("Push Docker Api Image") {
          agent {label 'docker'}
          steps {
            sh 'docker tag api 10.33.109.104/data-crawling/api:${IMAGE_TAG}'
            sh 'docker push 10.33.109.104/data-crawling/api:${IMAGE_TAG}'
          }
        }
      }
    }
    stage("Run New Containers in Data Crawling Project") {
      agent {label 'docker'}
      steps {
        sh 'docker compose -p data-crawling up -d'
      }
    }
    stage("Deploy in Kubernetes Production"){
      steps {
        dir('k8s-files'){
          sh 'kubectl set image deployment/api api=api:${IMAGE_TAG} --record'
          sh 'kubectl set image deployment/scrapy scrapy=scrapy:${IMAGE_TAG} --record'
        }
      }
    }
  }
  post {
    success {
      sh 'docker ps'
      sh 'kubectl get pods -n data-crawling'
    }
  }
}
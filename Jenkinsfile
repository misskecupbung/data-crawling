pipeline {
  agent {label 'docker'}
  options {
    skipDefaultCheckout false
  }
  environment {
    harbor=credentials('harbor')
    IMAGE_LIST = sh('docker images -aq')
    IMAGE_TAG = sh(returnStdout: true, script: "git rev-parse --short=10 HEAD").trim()

  }
  stages {
    stage("Build docker image") {
      parallel {
        stage("Build docker scrapy image") {
          steps {
            dir('scrapy') {
              sh 'docker build -t scrapy:${IMAGE_TAG} .'
            }
          }
        }
        stage("Build docker api image") {
          steps {
            dir('api'){
              sh 'docker build -t api:${IMAGE_TAG} .'
            }
          }
        }
      }
    }
    stage("Remove Orpans Containers") {
      steps {
        sh 'docker compose down --remove-orphans'
      }
    }
    stage("Login to Harbor Registry") {
      steps {
        sh 'echo $harbor_PSW | docker login 10.33.109.104 -u $harbor_USR --password-stdin'
      }
    }
    stage("Push New data-crawling image") {
      parallel {
        stage("Push Docker Scrapy Image") {
          steps {
            sh 'docker tag scrapy:${IMAGE_TAG} 10.33.109.104/data-crawling/scrapy:${IMAGE_TAG}'
            sh 'docker push 10.33.109.104/data-crawling/scrapy:${IMAGE_TAG}'
          }
        }
        stage("Push Docker Api Image") {
          steps {
            sh 'docker tag api:${IMAGE_TAG} 10.33.109.104/data-crawling/api:${IMAGE_TAG}'
            sh 'docker push 10.33.109.104/data-crawling/api:${IMAGE_TAG}'
          }
        }
      }
    }
    stage("Remove All Local Images") {
      steps {
        sh 'docker rmi -f ${IMAGE_LIST}'
      }
    }
    stage("Run New Containers in Data Crawling Project") {
      steps {
        sh 'docker compose -p data-crawling up -d'
      }
    }
    stage("Deploy in Kubernetes Production"){
      steps {
        dir('k8s-files'){
          sh 'kubectl set image deployment/api api=10.33.109.104/data-crawling/api:${IMAGE_TAG} -n data-crawling'
          sh 'kubectl set image deployment/scrapy scrapy=10.33.109.104/data-crawling/scrapy:${IMAGE_TAG} -n data-crawling'
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
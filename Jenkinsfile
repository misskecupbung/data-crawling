pipeline {
  agent {label 'docker'}
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
    stage("Remove orpans containers") {
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
            sh 'docker tag scrapy 10.33.109.104/data-crawling/scrapy:${IMAGE_TAG}'
            sh 'docker push 10.33.109.104/data-crawling/scrapy:${IMAGE_TAG}'
          }
        }
        stage("Push Docker Api Image") {
          steps {
            sh 'docker tag api 10.33.109.104/data-crawling/api:${IMAGE_TAG}'
            sh 'docker push 10.33.109.104/data-crawling/api:${IMAGE_TAG}'
          }
        }
      }
    }
    stage("Run New Containers in Data Crawling Project") {
      steps {
        sh 'docker rmi -f $(docker images -aq)'
        sh 'docker compose -p data-crawling up -d'
      }
    }
    stage("Deploy in Kubernetes Production"){
      steps {
        dir('k8s-files'){
          sh 'kubectl set image deployment/api 10.33.109.104/data-crawling/api:${IMAGE_TAG} -n data-crawling --record'
          sh 'kubectl set image deployment/scrapy api 10.33.109.104/data-crawling/scrapy:${IMAGE_TAG} -n data-crawling --record'
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
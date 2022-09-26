pipeline {
  agent any
  environment {
    harbor=credentials('harbor')
  }
  stages {
    stage("Build docker image") {
      parallel {
        stage("Build docker scrapy image") {
          steps {
            dir('scrapy') {
              sh 'docker build -t scrapy .'
            }
          }
        }
        stage("Build docker api image") {
          steps {
            dir('api'){
              sh 'docker build -t api .'
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
            sh 'docker tag scrapy 10.33.109.104/data-crawling/scrapy'
            sh 'docker push 10.33.109.104/data-crawling/scrapy'
          }
        }
        stage("Push Docker Api Image") {
          steps {
            sh 'docker tag api 10.33.109.104/data-crawling/api'
            sh 'docker push 10.33.109.104/data-crawling/api'
          }
        }
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
          sh 'kubectl apply -f api_tmp.yaml -f scrapy_tmp.yaml -n data-crawling'
          sh 'kubectl apply -f api.yaml -f scrapy.yaml -n data-crawling'
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
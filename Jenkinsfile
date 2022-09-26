pipeline {
  agent any
  environment {
    harbor=credentials('harbor')
  }
  parameters {
    string(description: 'Image Version Based from Build', name: 'IMAGE_VERSION', defaultValue: '01')
  }
  stages {
    stage("Build docker image") {
      parallel {
        stage("Build docker scrapy image") {
          steps {
            dir('scrapy') {
              sh 'docker build -t scrapy:${params.IMAGE_VERSION} .'
            }
          }
        }
        stage("Build docker api image") {
          steps {
            dir('api'){
              sh 'docker build -t api:${params.IMAGE_VERSION} .'
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
            sh 'docker tag scrapy:${params.IMAGE_VERSION} 10.33.109.104/data-crawling/scrapy:${params.IMAGE_VERSION}'
            sh 'docker push:${params.IMAGE_VERSION} 10.33.109.104/data-crawling/scrapy:${params.IMAGE_VERSION}'
          }
        }
        stage("Push Docker Api Image") {
          steps {
            sh 'docker tag api 10.33.109.104/data-crawling/api:${params.IMAGE_VERSION}'
            sh 'docker push:${params.IMAGE_VERSION} 10.33.109.104/data-crawling/api:${params.IMAGE_VERSION}'
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
          sh 'kubectl delete -f api.yaml -f scrapy.yaml -n data-crawling'
          sh 'kubectl apply -f api.yaml -f scrapy.yaml -n data-crawling'
          sh 'kubectl delete -f api_tmp.yaml -f scrapy_tmp.yaml -n data-crawling'
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
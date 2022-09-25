pipeline {
  agent any
  environment {
    harbor=credentials('harbor')
  }
  stages {
    stage("Checkout SCM"){
      steps {
        checkout scm
      }
    }
    stage("Build docker image") {
      steps {
        dir('scrapy') {
          sh 'docker build -t scrapy .'
        }
        dir('api') {
          sh 'docker build -t api .'
        }
      }
    }
    stage("Remove orpans containers") {
      steps {
        sh 'docker compose down --remove-orphans'
      }
    }
    stage("Push new data-crawling image") {
      steps {
        sh 'echo $harbor_PSW | docker login 10.33.109.104 -u $harbor_USR --password-stdin'
        sh 'docker tag scrapy 10.33.109.104/data-crawling/scrapy'
        sh 'docker push 10.33.109.104/data-crawling/scrapy'
        sh 'docker tag api 10.33.109.104/data-crawling/api'
        sh 'docker push 10.33.109.104/data-crawling/api'
      }
    }
    stage("Run new containers in data crawling project") {
      steps {
        sh 'docker compose -p data-crawling up -d'
        sh 'docker ps'
      }
    }

  }
  post {
    success {
      dir('k8s-files') {
        sh 'kubectl apply -f api_tmp.yaml -f scrapy_tmp.yaml'
        sh 'kubectl delete -f api.yaml -f scrapy.yaml'
        sh 'kubectl apply -f api.yaml -f scrapy.yaml'
        sh 'kubectl delete -f api_tmp.yaml -f scrapy_tmp.yaml'
      }
    }
  }
}

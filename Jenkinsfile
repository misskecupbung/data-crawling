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
        sh 'cd scrapy && docker build -t scrapy . && ls'
        sh 'cd ../api && docker buid -t api .'
        sh 'cd ../'
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
      }
    }

  }
  post {
    always {
      sh 'docker ps'
    }
  }
}

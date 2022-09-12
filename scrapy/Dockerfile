FROM python:3
COPY . .
RUN pip3 install --upgrade pip
RUN pip3 install -r ./requirements.txt
WORKDIR ./shpscp/shpscp
EXPOSE 6800
CMD scrapy crawl shopee -a category="Olahraga & Outdoor" --nolog && \
    scrapy crawl shopee -a category="Perawatan & Kecantikan" --nolog && \
    scrapy crawl shopee -a category="Pakaian Pria" --nolog

FROM python:3
COPY . .
RUN pip3 install --upgrade pip
RUN pip3 install -r ./requirements.txt
RUN flask db migrate 
RUN flask db upgrade
EXPOSE 5000
CMD flask run --host 0.0.0.0

#FROM python:latest
#WORKDIR /code
#ADD requirements.txt requirements.txt
#RUN pip install -r requirements.txt
#COPY app.py app.py
#CMD ["python", "-u", "app.py"]


FROM python:latest

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "app.py"] 
# ["python", "-u", "app.py", "--host=0.0.0.0", "--port=8080"]

FROM python:3.8-slim
WORKDIR /app
ADD requirements.txt /app
RUN pip install -r requirements.txt
ADD /src/app.py /app
CMD python app.py
FROM python:3.9-slim
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD ["python", "./app/mlb-counter-api.py"]
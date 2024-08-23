FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

# Tentukan environment variable
ENV FLASK_APP=app.py

EXPOSE 5000

CMD ["python", "app.py"]

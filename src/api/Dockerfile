FROM python:3.9.1-alpine

WORKDIR /app

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./ ./

EXPOSE 5678

CMD [ "python", "app.py" ]

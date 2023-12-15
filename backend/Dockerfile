FROM python:3.9-alpine
COPY requirements.txt .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . /
RUN python3 manage.py collectstatic --no-input --clear
ENTRYPOINT gunicorn -b 0.0.0.0:8080 star_burger.wsgi:application

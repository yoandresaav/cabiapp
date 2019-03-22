FROM python:3.7

ENV PYTHONUNBUFFERED=1

RUN mkdir /config && mkdir /cabiapp

COPY requirements.txt /config
COPY production.cfg /

RUN pip install --no-cache-dir -r config/requirements.txt

WORKDIR /cabiapp

CMD python manage.py runserver 0.0.0.0:8000
FROM python:3.8
MAINTAINER oleszak.michal@gmail.com
WORKDIR /app
COPY . /app

RUN pip install poetry
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN pip install -r requirements.txt

EXPOSE 8887
CMD ["gunicorn", "--bind", "0.0.0.0:8887", "--workers", "12", "templates.flask_app.wsgi:app"]
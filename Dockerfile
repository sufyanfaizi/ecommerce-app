FROM python:3.18
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]
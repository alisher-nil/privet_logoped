FROM python:3.12
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY ./privet_logoped/ .
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "privet_logoped.wsgi"]
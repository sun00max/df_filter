# Pull base image
FROM python:3.10.2-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . .
#CMD ["flask", "--debug", "run", "--host", "0.0.0.0"]
ENTRYPOINT ["python"]
CMD ["app.py"]
#CMD ["python", "app.py", "runserver", "-h", "0.0.0.0"]
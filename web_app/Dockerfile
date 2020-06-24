FROM python:3.8.3-alpine
LABEL maintainer = "natig.aminov@gmail.com"

# Set work directory
WORKDIR /home/web_app/core

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update && apk upgrade \
  && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY ./core/requirements.txt .
RUN pip install -r requirements.txt

# Copy entrypoint.sh
COPY ./core/entrypoint.sh .

# Copy project
COPY ./core /home/web_app/

# Run entrypoint.sh
ENTRYPOINT ["/home/web_app/core/entrypoint.sh"]


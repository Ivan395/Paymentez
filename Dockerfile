FROM python:latest
ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1
WORKDIR /app
COPY . /app
RUN pip install --user -r requirements.txt

ENTRYPOINT ["sh", "entrypoint.sh"]

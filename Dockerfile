FROM python:3.12-alpine
WORKDIR /app
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
CMD [ "/bin/sh", "start.sh" ]
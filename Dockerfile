FROM python:3.8-alpine

WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN ls -lah
RUN pip install -e .

WORKDIR /apps

COPY ./apps .
RUN chmod +x screenshot.sh

CMD ["ash"]

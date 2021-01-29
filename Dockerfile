FROM python:latest
WORKDIR /


COPY . /
COPY ./config /
COPY ./core /
COPY ./gym_wrapper /
COPY ./lokal_config /
COPY services /
COPY ./tests /

RUN pip install -r requirements.txt

CMD [ "python", "test.py" ]


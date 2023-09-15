
FROM python:3.11.3

RUN mkdir -p /std

COPY ./std

RUN python3 -m pip install -r /std/requirements.txt

EXPOSE 5000

CMD ['python', '/std/app.py']


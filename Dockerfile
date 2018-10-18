FROM python:3.6-alpine

COPY Pipfile /
COPY Pipfile.lock /

RUN pip3 install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

COPY app.py /
COPY swagger/swagger.yaml /swagger/
COPY helpers/* /helpers/

WORKDIR /data
CMD python /app.py
FROM python:3.12-slim

WORKDIR /code

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN cd /tmp && poetry export -f requirements.txt --output requirements.txt

RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt

COPY . /code/

RUN chmod +x /code/start.sh

CMD ["/code/start.sh"]

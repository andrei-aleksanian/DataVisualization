FROM python:3.8-slim

WORKDIR /app

COPY ./common ./common
COPY ./examples_api ./api

RUN pip3 install pipenv

COPY ./Pipfile* ./
COPY ./requirements.txt ./
COPY ./setup.py ./

# This is how you install python dependencies in a virtual environment in docker
RUN pipenv install --deploy --ignore-pipfile
# For some reason these don't go into pipenv
RUN pipenv run pip install -r requirements.txt

# Install common as a module
RUN pipenv run pip install -e .

CMD ["pipenv", "run", "python", "api/main.py"]
# Docker-compose starts up <pipenv run python main.py>

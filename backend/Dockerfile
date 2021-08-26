FROM python:3.8-slim

WORKDIR /backend

RUN pip3 install pipenv

COPY ./Pipfile* ./
COPY ./requirements.txt ./

# This is how you install python dependencies in a virtual environment in docker
RUN pipenv install --deploy --ignore-pipfile
# For some reason these don't go into pipenv
RUN pipenv run pip install -r requirements.txt

COPY . ./

CMD ["pipenv", "run", "python", "main.py"]
# Docker-compose starts up <pipenv run python main.py>

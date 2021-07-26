FROM python:3.8

WORKDIR /backend

RUN pip3 install pipenv

COPY ./Pipfile* ${WORKDIR}

# This is how you install python dependencies in a virtual environment in docker
RUN pipenv install --deploy --ignore-pipfile

COPY . .

CMD ["pipenv", "run", "python", "main.py"]
# Docker-compose starts up <pipenv run python main.py>
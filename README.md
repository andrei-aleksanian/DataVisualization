# Data Visualisation Tool with COVA and ANGEL

A tool to visualise COVA and ANGEL algorithms on the web.

## Getting Started

### Docker

To run the code in Docker, make sure you have [it](https://www.docker.com/) installed on your machine and you are in the root directory and run:

`docker-compose up -d --build`

After you are done, make sure to run:

`docker-compose stop`

### Running Manually

Follow these steps to install all the dependencies on the backend:

1. `cd backend`

2. `pipenv install --dev`

3. `pipenv shell`

4. `pip install -r requirements.txt`

For some mysterious reason, pipenv doesnt install some crucial packages used in COVA and ANGEL.
These packages are listed in `requirements.txt`.

Now, it's time to install dependencies on frontend:

1. `cd ..` (back to root folder)
2. `cd frontend`
3. `npm i`

You are done!

## Production environment

Running the code in a production environment:

1. SSH into your VM. Install docker and copy the `production/docker-compose.yml`
2. Run `docker-compose -f app/docker-compose.yml up -d`
3. You are done! That simple.

The images get built in GitHub Actions and pushed to Docker Hub.
So, there is no need to build them on your VM, just pull them from docker hub!

### Cleaning up jobs

Sometimes your VM won't have much memory. To release unused containers run:

1. `docker system prune`
2. Type "yes" into the console.

If this didn't fix it and your containers keep crushing, try a bigger VM.

## Backend

The backend is done with [fastAPI](https://fastapi.tiangolo.com/). A lightweight, fast and flexible python backend.

## Frontend

The frontend is in React. Some auto generated docs are [here](frontend/README.md).

## Contributing to the project

We follow [Trunk based development](https://trunkbaseddevelopment.com/).
This means all merge requests need to be merged with `trunk` branch first and then into master.

To contribute to the project, you will need to pass git commit hooks:

`git commit` will trigger a sequence of linters checking the quality of your code.

Only after everything passes and there
is no problems can you make a commit.

_Warning: make sure you have lint-staged installed._
_To install, run: `npx mrm@2` and `npx lint-staged`_

_Warning: make sure you have husky installed._
_To install, run: `npx run prepare`_

## Pipenv

More ocumentation will be coming soon...

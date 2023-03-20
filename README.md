# H2gO
This is the H2gO web application. This app promotes the use of water fountains by students at the University of Exeter through a reward-based quiz game system.

## Details
Users of the app can set up profiles to store their information and login details.

When users of the app are in buildings on the Streatham campus, they will be able to register that they have refilled their bottle at a water fountain through the press of a button. This will guide users through a quiz in which they can earn extra XP for correct answers. Leaderboards for each building display the users with the most XP achieved in that building.

Users will be able to spend `droplets` (in-game currency) achieved through challenges in a cosmetics store that provides customisation to their user profiles.

## The Code
The app consists of a backend Django server that communicates with a frontend Reactjs interface.

Users interact with the program through the frontend, which communicates with data stored and manipulated through the backend in order to present the relevant information.

## How to Use
The app has been set up to be run through a Docker container in order to allow for seamless setup of develepment environments including package requirements installations and any other necessary tools.

In order to run the docker container properly, please install the Docker app for the relevant platform, which can be found [here](https://docs.docker.com/get-docker/).

Once installed, first construct the containerised application in the root folder with the command:
    
    docker-compose build

Then launch the server locally by running:

    docker-compose up

In case of node module installation faults, navigate to the `frontend/` directory and manually install the required packages with the command:

    npm install

Please note that [Node.js](https://nodejs.org/en/download/) must be installed on your system in order to do so.

Once running, the frontend view can be found at <http://localhost:3000> and the backend is accessible at <http://localhost:8000>

### Structure
### Backend

The backend is contained within the `API/` directory, and consists of multiple modules that each correspond to a different kind of interaction with the Django server. The backend has been designed in this way to minimise the potential for conflicts between collaborators.

- The core Django module is located in the `backend/` subdirectory which contains all the settings and base URLs. Any additionally created modules with additional views should have the URL patterns included in `backend/urls.py`.
- The `database/` module is responsible for designing models contained in the database, and registering these models to the Django admin view.
- The `tests/` module contains all the tests for functionality of the server.
- The `static/` directory contains any static references that are used by the server (eg. images) and is specified in the `backend/settings.py`.
- The remaining modules are appropriately named referring to the types of interactions they handle with the server.

The `Dockerfile` is responsible for settings up the backend docker image, installing any required packages in the environment.

### Frontend

The frontend is contained within the `frontend/` directory, where it is structured as a Reactjs application. The packages used are specified in the `package.json` and `package-lock.json` files. The source code can be found in the `src/` directory:

- The core application is defined within `src/App.js`, which includes all the pages contained within the app.
- The pages are all located in the `src/pages/` directory, where each page of the website contains its own respective subdirectory.
- Components that are contained within some of the pages are located in the `src/components/` directory.
- Assets (including logos, fonts and other images) that are used by the application are located within `src/assets/`.

The `Dockerfile` sets up the frontend docker image, installing all the necessary packages and initializing the app to run.

### Miscellaneous

- The `Useful_Colours.txt` contains hexadecimal code references to the relevant university colour theme that is used throughout the app.
- The `docker-compose.yaml` is responsible for initialising the frontend and backend docker images when the 'docker-compose' command is executed.

## Testing

The django tests are located in the `API/tests/` directory and can be run from the root directory with the command:

    python3 API/manage.py test API/tests

The tests are also run as part of the GitHub action on pull requests and merges.
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
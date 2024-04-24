#change directory to the location of the docker-compose.yml file
cd /home/etharialle/github/shelter-streamlit

#remove all docker containers
docker rm -v -f $(docker ps -qa)

#start docker-compose in detached mode
docker compose up --build --remove-orphans -d

#run the streamlit apps
#ampersand is used to run the apps in the background
docker exec app sh -c "streamlit run app.py &"
docker exec test sh -c "streamlit run test.py &"
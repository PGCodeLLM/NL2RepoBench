rm -rf docker_logs/*

for id in $(docker ps -a | grep openhands-runtime | awk '{print $1}'); do
    log_file="docker_logs/${id}_allhands_runtime_docker.log"
    echo " -> Dumping logs for $id to $log_file"
    docker logs "$id" &> "$log_file" 2>&1
done

for id in $(docker ps -a | grep openhands-app | awk '{print $1}'); do
    log_file="docker_logs/${id}_allhands_openhands_docker.log"
    echo " -> Dumping logs for $id to $log_file"
    docker logs "$id" &> "$log_file" 2>&1
done
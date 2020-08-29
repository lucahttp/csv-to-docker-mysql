$DOCKER_ACC="lukaneco"
$DOCKER_REPO="csv2mysql"
docker build -t lukaneco/csv2mysql:latest csv2docker.dockerfile
docker push lukaneco/csv2mysql:latest
# Build react front-end locally
rm -R ./build
npm run build

# Create docker container with python
docker build --no-cache -t jvsoest/term-mapper ./

echo  
echo =================================
echo Done building the container
read -p "Run container locally? [y/N] " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    docker run --rm \
        -p 5000:5000 \
        -e ENDPOINT_URL=http://172.18.22.17:7200/repositories/johan_test \
        jvsoest/term-mapper
fi
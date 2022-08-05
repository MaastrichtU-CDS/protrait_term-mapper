# Build react front-end locally
rm -R ./build
npm run build

# Create docker container with python
docker build --no-cache -t jvsoest/term-mapper ./
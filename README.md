# Unofficial MongoDB Docker Image for Raspberry Pi

Deploy recent releases of MongoDB on a Raspberry Pi with these Docker images.

This repo and any code or binaries within it are not explicitly endorsed nor provided by MongoDB Inc.

## Versions

- [_7.0.3_](https://github.com/themattman/mongodb-raspberrypi-docker/releases/tag/r7.0.3-mongodb-raspberrypi-docker-unofficial) [November 11, 2023]

- [_7.0.2_](https://github.com/themattman/mongodb-raspberrypi-docker/releases/tag/r7.0.2-mongodb-raspberrypi-docker-unofficial) [October 28, 2023]

- [_6.0.11_](https://github.com/themattman/mongodb-raspberrypi-docker/releases/tag/r6.0.11-mongodb-raspberrypi-docker-unofficial) [October 25, 2023]

- [_7.0.1_](https://github.com/themattman/mongodb-raspberrypi-docker/releases/tag/r7.0.1-mongodb-raspberrypi-docker-unofficial) [September 25, 2023]

- [_7.0.0_](https://github.com/themattman/mongodb-raspberrypi-docker/releases/tag/r7.0.0-mongodb-raspberrypi-docker-unofficial) [September 25, 2023]

- [_6.0.10_](https://github.com/themattman/mongodb-raspberrypi-docker/releases/tag/r6.0.10-mongodb-raspberrypi-docker-unofficial) [September 25, 2023]

- [_6.0.8_](https://github.com/themattman/mongodb-raspberrypi-docker/releases/tag/r6.0.8-mdb-rpi-docker-unofficial) [September 24, 2023]

- [_6.1.0-rc4_](https://github.com/themattman/mongodb-raspberrypi-docker/releases/tag/r6.1.0-rc4-mdb-rpi-docker-unofficial) [March 9, 2023]

## Super-basic build steps
1. Save the `Dockerfile` & `docker-entrypoint.sh` files from the relevant versions sub-directory, to a local working directory.
2. Adjust permissions on the `docker-entrypoint.sh` file to make it executable - `chmod +x docker-entrypoint.sh`
3. Build the image from your working directory - `docker build -t mongodb-unofficial:7.0.3 .`
The image should now exist in your local docker images, or can be pushed to a registry for wider usage.  

## Source

https://github.com/themattman/mongodb-raspberrypi-binaries/releases

## License

The artifacts in this repo are subject to the [MongoDB Server-Side Public License](https://github.com/mongodb/mongo/blob/r6.0.10/LICENSE-Community.txt).

## Fork

This repo is loosely based on: https://github.com/docker-library/mongo

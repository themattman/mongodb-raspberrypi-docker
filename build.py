#!/usr/bin/env python3

import os

if not os.path.exists("./mongodb-raspberrypi-docker"):
    os.system("git clone https://github.com/themattman/mongodb-raspberrypi-docker.git")
    os.chdir("./mongodb-raspberrypi-docker/")    
else:
    os.chdir("./mongodb-raspberrypi-docker/")
    os.system("git pull")

# remove template folder
if os.path.exists("./template"):
    os.system("rm -R ./template")

# Ask if the user wants to push to Docker Hub
def ask_push():
    os.system("clear")
    push = input("Do you want to push the images to the Docker Hub? (Y/n): ")
    if push.lower() == "n":
        push = False
    else:
        push = True
    return push
push = ask_push()

if push:
    def docker_login():
        os.system("clear")
        print("Please enter your Docker credentials to push the images to the Docker Hub.")
        docker_user = input("Docker Username: ").lower()
        docker_token = input("Docker Token: ")
        if not docker_token.startswith("dckr_pat_"):
            print("Invalid Docker Token. Please enter a valid Docker Token.")
            docker_login()
        elif docker_user and docker_token:
            os.system(f"docker login -u {docker_user} -p {docker_token}")
        else:
            print("Please enter your Docker credentials.")
            docker_login()
        os.system(f"docker login -u {docker_user} -p {docker_token}")
    docker_login()
    
subfolders = [f.path for f in os.scandir() if f.is_dir() and not f.name.startswith('.')]
subfolders.sort()

# Ask if specific images should be built (list subfolders and ask for input)
def ask_build():
    os.system("clear")
    print("The following images will be built:")
    for folder in subfolders:
        print(f" - {os.path.basename(folder)}")
    print("Do you want to build all images or specific images?")
    print("Enter 'all' to build all images or enter the name of the image to build.")
    print("You can enter multiple image names separated by a comma (',').")
    build = input("Images to build: ")
    if build.lower() == "all":
        return subfolders
    else:
        # Check if the entered image names are valid
        build = build.split(",")
        for b in build:
            if not os.path.exists(b):
                input(f"The image '{b}' does not exist. Please enter a valid image name...")
                ask_build()
        return build
build = ask_build()
os.system("clear")

counter = 0

# Build the images
for folder in build:
    os.chdir(folder)
    os.system("chmod +x *.sh")
    os.system(f"docker build -t serpensin/mongodb-unofficial-armv8:{os.path.basename(folder)} {'--push .' if push else '.'}")

    counter += 1

    if counter == len(subfolders) and counter == len(build):
        os.system(f"docker tag serpensin/mongodb-unofficial-armv8:{os.path.basename(folder)} serpensin/mongodb-unofficial-armv8:latest")
        if push:
            os.system("docker push serpensin/mongodb-unofficial-armv8:latest")

    os.chdir("..")

os.system("clear")
print("All images have been built.")
# docker image prune -af
if push:
    remove_images = input("Do you want to remove all unused images? (Y/n)")
    if remove_images.lower() == "n":
        print("Images are not removed.")
    else:
        os.system("docker image prune -af")
        print("All unused images have been removed.")

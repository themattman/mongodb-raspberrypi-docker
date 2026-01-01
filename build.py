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
    
def patch_dockerfile(dockerfile_path: str):
    with open(dockerfile_path, "r") as f:
        lines = f.readlines()

    already_patched = any("ARG EXTRA_RUN" in line for line in lines)
    if already_patched:
        return  # no change needed

    new_lines = []
    inserted = False
    for line in lines:
        if line.strip().startswith("CMD") and not inserted:
            new_lines.append("ARG EXTRA_RUN\n")
            new_lines.append("RUN if [ -n \"$EXTRA_RUN\" ]; then eval \"$EXTRA_RUN\"; fi\n")
            inserted = True
        new_lines.append(line)

    # fallback: if no CMD found, append at end
    if not inserted:
        new_lines.append("\nARG EXTRA_RUN\n")
        new_lines.append("RUN if [ -n \"$EXTRA_RUN\" ]; then eval \"$EXTRA_RUN\"; fi\n")

    with open(dockerfile_path, "w") as f:
        f.writelines(new_lines)

    print(f"✅ Patched {dockerfile_path}")

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

    dockerfile_path = os.path.join(os.getcwd(), "Dockerfile")
    if os.path.exists(dockerfile_path):
        patch_dockerfile(dockerfile_path)

    os.system("chmod +x *.sh")

    extra_run = (
        "mkdir -p /usr/local/lib && "
        "wget -q -O /usr/local/lib/libstdc++.so.6.0.29 "
        "'https://github.com/themattman/raspberrypi-binaries/raw/main/libstdc%2B%2B/libstdc%2B%2B.so.6.0.29' && "
        "ln -sf /usr/local/lib/libstdc++.so.6.0.29 /lib/aarch64-linux-gnu/libstdc++.so.6 && "
        "ldconfig"
    )

    os.system(
        f"docker build "
        f"--build-arg EXTRA_RUN=\"{extra_run}\" "
        f"-t serpensin/mongodb-unofficial-armv8:{os.path.basename(folder)} "
        f"{'--push .' if push else '.'}"
    )

    counter += 1

    if counter == len(subfolders) and counter == len(build):
        os.system(f"docker tag serpensin/mongodb-unofficial-armv8:{os.path.basename(folder)} serpensin/mongodb-unofficial-armv8:latest")
        if push:
            os.system("docker push serpensin/mongodb-unofficial-armv8:latest")

    os.chdir("..")

#os.system("clear")
print("All images have been built.")
# docker image prune -af
if push:
    remove_images = input("Do you want to remove all unused images? (Y/n)")
    if remove_images.lower() == "n":
        print("Images are not removed.")
    else:
        os.system("docker image prune -af")
        print("All unused images have been removed.")

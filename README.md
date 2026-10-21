# Dynalene Graphical User Interface (GUI) in Python

## Platform

- Rocky Linux 9.8
- python: 3.12.15

## Needed Package

- pyside6 (install by `conda`)

## Code Format

This code is automatically formatted by `black` using a git pre-commit hook (see `.pre-commit-config.yaml`), which comes from the `.ts_pre_commit_config.yaml`.

To enable this, see [pre-commit](https://pre-commit.com).

### AlmaLinux / RockyLinux

If the user of docker container has no writing permission to the X11 socket, you need to run the following command first (use the `root` user in container):

```bash
xhost local:root
```

Then, do the image forwarding by the following command (note you need to use the `root` as the user or not):

```bash
docker run -it --rm -e DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v ${path_to_this_package}:${path_of_package_in_container} ${docker_image}:${image_tag}
```

### MacOS

1. Setup the x11 by following: [x11_docker_mac](https://gist.github.com/cschiewek/246a244ba23da8b9f0e7b11a68bf3285).

2. Forward GUI by (note the MacOS will handle the writing permission for you):

```bash
xhost +
IP=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}')
docker run -it --rm -e DISPLAY=${IP}:0 -v /tmp/.X11-unix:/tmp/.X11-unix -v ${path_to_this_package}:${path_of_package_in_container} ${docker_image}:${image_tag}
```

## Executable

The executable (`run_dynalenegui`) is under the `bin/` directory.
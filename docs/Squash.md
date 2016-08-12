# Description
Docker images usually was built in layerer, so it may tooks lots disk space. 

### Why squash ?

Let's say a Dockerfile as 

    ```
    FROM alpine:latest
    # add one package, or a file
    RUN apk add wget
    # remove the package or file
    RUN apk del wget
    ```

The images will be 3 layers, first is alpine, second is wget installation, third is wget uninstallation. 
Even though 'wget' is invisible when we launch the container, but in fact, the 'wget' file binary still exists and occupies disk at 2nd layer. 

It's very often to have hidden files eating hundred of metabytes to gigabytes disk, which slow down not only network but also runtime efficiency.

### How squash ?

'Docker squash' is a request to implement but not yet there. So there are lots 3rd tools to do that, one is [docker-squash](https://github.com/goldmann/docker-squash/)

* Install docker-squash
    ```
    $ sudo pip install docker-squash
    ```

* Build a fat image 
    ```
    $ docker build -t my-fat-image . 
    ```

* Squash it
    ```
    $ docker-squash -t my-fat-image my-fit-image
    ```

* See how much it lose weight, 500 MB!
    ```
    $ docker images -a
    REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
    my-fit-image        latest              72f89fac15dc        38 minutes ago      331.8 MB
    my-fat-image        latest              2122a45833ff        About an hour ago   859.2 MB
    alpine              latest              4e38e38c8ce0        6 weeks ago         4.799 MB
    ```

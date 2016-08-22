# Description
Interact with DroneKit and OpenCV

(*) DroneKit does NOT support Python 3 (http://python.dronekit.io/develop/installation.html)

### Setup & Manual
* [Setup Pyenv & Virtualenv](docs/pyenv.md)

* Setup runtime environment for local and debug
    ```
    // replace [drone-2.7.2] with prefered name
    $ pyenv virtualenv 2.7.12 drone-2.7.12
    $ pyenv local drone-2.7.12
    $ pip install numpy
    $ pip install dronekit
    $ pip install dronekit-sitl
    $ echo "/usr/local/opt/opencv3/lib/python2.7/site-packages" >> /usr/local/pyenv/versions/drone-2.7.12/lib/python2.7/site-packages/opencv3.pth
    ```


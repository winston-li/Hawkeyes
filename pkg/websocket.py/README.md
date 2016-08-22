# Description
An web application detect and track human face 

### Setup & Manual
* [Setup Pyenv & Virtualenv](docs/pyenv.md)

* Setup runtime environment for local and debug
    ```
    // replace [opencv-3.5.2] with prefered name
    $ pyenv virtualenv 3.5.2 opencv-3.5.2
    $ pyenv local opencv-3.5.2
    $ pip install numpy
    $ pip install tornado
    $ echo "/usr/local/opt/opencv3/lib/python3.5/site-packages" >> /usr/local/pyenv/versions/opencv-3.5.2/lib/python3.5/site-packages/opencv3.pth
    ```

* Run locally
    ```
    $ python app.py
    $ open http://localhost:8888/
    ```

* [Alternative] Run in container
    ```
    $ docker pull quay.io/rainbean/scipy-notebook
    $ docker run -v $PWD:/mnt -it --rm -p 8888:8888 quay.io/rainbean/scipy-notebook bash -c "cd /mnt; python app.py"
    $ open http://localhost:8888/
    ```

### Underhook
[Frontend Javascript](public/javascripts/webcam.js)
* Initialize webcam video 
* Connect websocket to backend site
* Render webcam frames on HTML5 canvas
* Capture each frame and send to websocket
* Render rentangle upon video canvas if backend site feedback rectangle location

[Backend Websocket](app.py)
* Create web site and handle websocket data

[Backend OpenCV](hawk.py)
* Convert ARBG png image to grayscale frame
* Detect face by Haar cascading slide windows model (not real time, due to high computation)
* Once first face rectangle identified, it keep tracking the rectangle by Adaptive Correlation Filters, which supports non-stational camera and moving object real-time 

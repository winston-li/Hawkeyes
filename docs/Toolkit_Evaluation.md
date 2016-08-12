# Description
Evaluate solutions and toolkits of machine learning and computing vision, in order to get a picture when to apply them appropriately.

## Table of Contents
- [Solutions](#)
- [Feature Matrix](#)
- [Lanscape](#)
- [Use Cases](#)
- [FAQ](#)
- [Reference](#)
- [Future Plan](#)


# Brief of each components

--------
### OpenCV

OpenCV is a general-purpose computer vision and image processing library. 
It offers a wide variety of modules aimed at computer vision work, specialized for real-time computer vision. 
OpenCV is also not based on computational graphs (aka neural network), but it uses the imperative programming paradigm in which you give instructions what to do next step by step.
OpenCV shines for tasks like 3D reconstruction, motion tracking, augmented reality and whenever there is very little training data available

Key use cases:
* Image processing
* Facial recognition, Gesture recognition
* Segmentation
* Augmented reality, Motion tracking

--------
### OpenVX

OpenVX is an open, royalty-free standard for cross platform acceleration of computer vision applications. OpenVX enables performance and power-optimized computer vision processing, especially important in embedded and real-time use cases such as face, body and gesture tracking, smart video surveillance, advanced driver assistance systems (ADAS), object and scene reconstruction, augmented reality, visual inspection, robotics and more.

OpenCV is open source library implemented by community, while OpenVX is standard spec to be implemented by (hardware) vendors.

--------
### TensorFlow

TensorFlow basically provides very useful abstractions when you have to deal with a relatively fixed chain of operations 
on very large matrices, or, more generally tensors¹, such as the weights, inputs and outputs of a neural network. 
TensorFlow hides a lot of the complexity of resource management of large tensors and also provides very useful abstractions 
to scale up computational graphs to be distributed on large compute facilities, e.g. on GPU clusters, but it also works on handhelds.

--------
### Octave

GNU Octave is a high-level interpreted language, primarily intended for numerical computations.

--------
### Scipy & its friends

Scipy is a Python-based ecosystem of open-source software for mathematics, science, and engineering. In particular, these are some of the core packages:
- Scipy
    ```
    a library for computing integrals numerically, solving differential equations, optimization, and sparse matrices.
    ```
- NumPy
    ```
    N-dim array objects, linear algebra, Fourier transform, and random number capabilities
    ```
- matplotlib
    ```
    2D plotting library
    ```
- IPython
    ```
    a enhanced Python interactive computing shell, with tab-completion, object introspection, system shell access, command history retrieval across sessions. 
    ```
- SymPy
    ```
    a Python library for symbolic mathematics, majorly for presentation. 
    ```
- Panda
    ```
    a library providing high-performance, easy-to-use data structures
    ```
- SciKits
    ```
    Short for SciPy Toolkits, are add-on packages for SciPy.
    ```
- Scikit-learn
    ```
    A collection of machine learning algorithms and sample databases.
    ```

# Brief of commercial Solutions

--------
### Itseez

Itseez, Inc., a leading developer of computer vision technology, has introduced Accelerated CV (ACV) library, a set of most popular computer vision functions from well known OpenCV library. Optimized specifically for ARM platform, ACV provides rapid acceleration of OpenCV based products with minimal impacts on existing code base. Acquired by Intel on 2016 May.

![Accelerated CV on Qualcomm SoC](http://opencv.org/wp-content/uploads/2016/04/image01.png)

# Feature comparison

| Component | License | Languages   | Deep Learning | Neural Network | Linear regression | Logstics regression | Multiclass classification | SVM | Anomaly detection  | Clustering | Density estimation | Dimension reduction |
| ---        | ---    | ---         | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| OpenCV     | BSD    | Python, C++ |   | O | O | O | O | O |   | O |   |   | 
| TensorFlow | Apache | Python, C   | O | O |
| Octave     | GPL    | Matlab, C++ | 
| Scikit     | BSD    | Python      |   |   | O | O | O | O | O | O | O | O | 

--------
## Feature mapping between OpenCV and rest

| Feature of OpenCV                       | Alternative |
| ---                                     | ---         |
| Image load/show/save                    | Matplot     |
| Camera load/show/save                   |  |
| Rectangle/text draw                     | Matplot |
| Layer, cut-copy-paste                   |  |
| Color space, alpha blending             |  |
| Transform, rotation, histogram          | Numpy |
| Segmentation                            |  |
| (Video) Background Subtraction          |  |
| (Video) Color, optical tracking         |  |
| Stereo 3D depth map                     |  |
| Noise, denoise, HDR, inpaint            |  |
| Machine learning                        | Scipy | 
| Object, face and gesture detection      |  |

[Mix up OpenCV and Jupyter notebook](http://giusedroid.blogspot.tw/2015/04/blog-post.html)

[Markdown table syntax](https://help.github.com/articles/organizing-information-with-tables/)

# Landscape

# Use cases

# FAQ

--------
### Q: Difference between Deep learning and Neural networks?

**_Short answer_**: Deep neural networks were a set of techniques that were discovered to overcome the vanishing gradient problem which was severely limiting the depth of neural networks.

Neural networks are trained using backpropagation gradient descent. That is, you update the weights of each layer as a function of the derivative of the previous layer. The problem is that the update signal was lost as you increased the depth of the neural network.

Therefore, in the old days, people pretty much only used neural networks with a single hidden-layer.

Deep learning, includes new techniques with non-vanishing derivative, enabling us to build very big neural networks, it has opened the door to such things as auto-encoders for unsupervised problems, convolutional neural networks to classify images, recurrent neural networks for time series, etc, etc. It was a revolution. But essentially, it’s the same old neural networks, just with bigger and cooler network topologies that can learn more advanced and exciting stuff. Some of these start to resemble the human brain.

https://www.quora.com/How-does-deep-learning-work-and-how-is-it-different-from-normal-neural-networks-applied-with-SVM

### Q: Disk footprint requirement of OpenCV?

**_Short answer_**: less than 100 MB. 

Docker images 'quay.io/rainbean/opencv' disk usage distribution:

| Package       | MByes | 
| ---           | --- |
| Python 2.7    | 150 |
| GCC/C++       | 450 | 
| OpenCV 3.1    | 150 |
| Others        | 100 | 

It would be much smaller to get rid of C/C++ development toolkits, ie. only Python+OpenCV .

### Q: Disk footprint requirement of Scipy-Notebook?

Docker images 'jupyter/scipy-notebook' disk usage distribution:

| Package       | MByes |
| ---           | ---  |
| Python 2.7    | 1400 |
| Python 3      | 1300 |
| TexLive       | 800  |
| Font & locale | 300  |
| Doc           | 100  |
| Emacs         | 100  |
| Others        | 900  |

[TexLive for download as menu](https://github.com/jupyter/docker-stacks/issues/62)

Break down python packages (duplicated in python 2 and 3):

| Package       | MByes | 
| ---           | --- |
| Intel MKL     | 200 |
| Scikit Learn  | 100 |
| Scipy         | 130 |
| Panda         | 80  |
| Sympy         | 50  |
| Numpy         | 30  |
| Notebook      | 30  |
| Matplot       | 30  |
| LLVM          | 30  |
| Cython        | 30  |


# Reference

* [Scientific Python for Raspberry Pi](http://geoffboeing.com/2016/03/scientific-python-raspberry-pi/)
* [Math symbol](http://matplotlib.org/1.4.0/users/mathtext.html)

# Future Plan


# Home Server

Home Server is a project that allows users to set up a local network server that acts like a micro social media, where users can follow, message and share files with each other.

## Getting Started

If you've ever accessed the command line, you'll find this pretty trivial. We'll go through installing and setting-up all of the necessary components to get the server up and running.

### Prerequisites

In order to host *Home Server*, you'll need to install [Python 3](https://www.python.org/about/gettingstarted/). All of the other tools will be installed through *Python* and its package installer, *pip*.

### Installing

Getting Home Server to start is pretty simple. Clone the repository into a desired location. Then, fire up the command line on the *home_server* directory.

Follow the steps below on your command line to set up the environment.

#### For Windows

\#1: Setting up the environment:

```
$: py -m venv env
```

\#2: Activating the environment:

```
$: .\env\Scripts\activate
```

\#3: Installing the required packages:

```
$: pip install -r requirements.txt
```

\#4: Generating the *home_server* database:

```
$: flask db init
$: flask db migrate
$: flask db upgrade
```

\#5: Running the server:

```
$: flask run
```

#### For macOS and Linux

\#1: Setting up the environment:

```
$: python3 -m venv env
```

\#2: Activating the environment:

```
$: source env/bin/activate
```

\#3: Installing the required packages:

```
$: pip install -r requirements.txt
```

\#4: Generating the *home_server* database:

```
$: flask db init
$: flask db migrate
$: flask db upgrade
```

\#5: Running the server:

```
$: flask run
```

With the server set up, navigate to *localhost:5000* on your web browser. From there, you should be able to register, login and use the **Home Server** app. If you want other people to join in as well, instead of entering

```
$: flask run
```

You should enter

```
$: flask run --host=0.0.0.0
```

## Deployment

Not currently deployable.

## Built With

* [Flask](http://flask.pocoo.org/) - Back-end Python based microframework
* [Bootstrap](https://getbootstrap.com/) - Front-end HTML toolkit
* [VSCode](https://code.visualstudio.com/) - Open source code editor

## Contributing

More information will be provided soon.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/lukeathedev/home_server/tags). 

## Authors

* **Luke A (lukeathedev)** - *Initial work*.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

* **Miguel Grinberg** for providing a fantastic [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
* The [Stack Overflow Community](https://stackoverflow.com/) for providing great information on recurring development issues

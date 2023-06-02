# LogFilter
[![.github/workflows/docker.yaml](https://github.com/joaoss35/logFilter/actions/workflows/docker.yaml/badge.svg?branch=master)](https://github.com/joaoss35/logFilter/actions/workflows/docker.yaml)

A log filter for a legacy application.

To make the file easier to follow, I will divide it into five sections. Each section will cover how the solution itself was
implemented, but also things that could be improved.
These four sections are:
- Python Application
- `Dockerfile`
- Helm Chart
- Bootstrap script
- Github Pipeline

## Prerequisites

In order to launch this project, you will need the following:

- Helm 3+
- Minikube 1.28+
- Kubernetes 1.18+

If you want to extend the capabilities of what you can do, and introduce a development experience to it, you will
also need:

- Docker 20+
- Python 3.10+

## Python Application

The app itself can be defined as a simple log filter engine that can be used to filter the log lines of a certain set
of files based on a set of markers previously defined. I tried to abstract as much as possible the engine implementation,
which means that it can be used for any log file pattern, as well as any marker.
The logFilter `class` itself it's independent of the rest of the logic, and I tried to treat it almost as the business
logic of a company, which should be as independent as possible.

The way the `logFilter` works is by **first finding all the log files that match a given pattern**. After, it **reads
the lines from each file and filters them based on the provided markers**. The **filtered lines are then written to
standard output**.

### Structure

Both the patterns, markers and log messages can be centrally changed in the `contants` class located under
`constants/constants.py`. The app itself has only one file named `app.py` and, for the sake of simplicity, both the
logFile engine and the main entry point of the application were defined there.

### Improvements

There are a few things that could be improved in the code out of the box. First, the code could be made more efficient
by using a more efficient module to find the log files, such as the [`glob`](https://docs.python.org/3/library/glob.html)
one.

Secondly, the constants could be passed  as parameters on the logFilterEngine constructor (`init()`), which would
decouple the engine from the constants file and make the logFilterEngine completely independent and used in any context.

Third, the code could have some error handling improvement, which would make it much more predictable and robust.

### Tests

I added some unit tests that I considered to be critical to validate the logic of the logFilterEngine class. However,
they could be expanded to cover less critical logic as well.

To run the tests, just execute on the root of the repo:
```shell 
python3 -m unittest tests/app_test.py -v
```

### Execution

To run the code locally, just run:

```shell
python3 app.py
```
> **Note**: Be sure to have Python 1.10 or higher

### Extras

The app also performs some other checks, such as:

- **Not log files found**: If no file pattern is find on the provided path, a log message is provided and the app exits
- **Wrong file permissions**: If the log file pattern is met on the provided path, but the file can't be reached (e.g.
  no read permissions), a log message is provided and the app exits
- **Invalid log level**: If the log level is different from 0, 1 or 2 the app will provide a log message and the app
  will exit.

## Dockerfile

### Structure

The `Dockerfile` starts by creating a single-layer image that contains the source code for the log filter engine. I used
this layer to avoid having to copy the source code to the final image every time the image had to be built (something
I believe I mentioned during our technical interview).

The Dockerfile then creates a second image based on the `python:3.10-alpine` image that runs the log filter engine,
through a non-root user called logfilter. I used the alpine image to try to reduce the image size as much as possible.

Finally, I set `PYTHONUNBUFFERED` to 1 to ensure that output from the log filter engine is not buffered. This will force
python to use unbuffered output, allowing the logs to be printed immediately. Not doing this would probably result on
not having any logs being printed by the logFilter container at all.

I didn't include any architectural logic inside the image since the only possible place where a multi-architectural
logic could be needed is on the python image, which supports both arch's as per
[here](https://hub.docker.com/layers/library/python/3.10-alpine/images/sha256-653fe1ead6d3d2de547ae0f1715c5a463ece62222b7d9e50c630f7ba28d7ce67?context=explore).

### Improvements

At the moment, I am only allowing the user to specify which markers will be used through the `log_level` environment
variable. However, this could be expanded (by also implementing the parameterized solution mentioned above) by giving
the user the ability to pass arguments and specify other options.

### Execution
First we should pull the image:
```shell
docker pull joaoss35/logfilter:v1.3
```

Then execute it by running:
```shell
docker run --rm --name logfilter --env LOG_LEVEL=-0 -v /var/log/app/app.log:/var/log/app/app.log joaoss35/logfilter:v1.3 
```

> **Note**: Be sure to have **a valid /var/log/app/app.log file locally** if you wish to mount to the volume as above.

## Helm Chart

The helm chart is very simply templated and easily configurable. All the relevant information can be changed directly
from the `values` file without any actual k8s manifest manipulation itself.

I opted to use the sidecar approach, making both containers share the same volume inside the pod. This was
accomplished by simply define an empty volume and mount a `/var/log/app` path on both containers.

### Improvements

Something that could be improved right out of the box is adding resource definition, to limit the amount the resources
that the pod could consume.
Another improvement could be pushing the helm chart to a registry and make it live there. This would enable users to
install the chart from anywhere, without having to necessarily fetch and reference the chart source code for the
installation.
Other possible improvement could be the introduction of an
HPA([horizontal pod autoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)),
which would scale the pod based on resource metrics.
Finally, in the case that the logs would be meaningfully for the company, the volume attached could be persisted
somewhere (e.g. EBS on AWS). This would prevent the content to be lost everytime the pod dies.

### Installation

On the root of the repo, run:
```shell
helm upgrade -i our-app charts/logfilter -f charts/logfilter/values.yaml -n logfilter-demo
```

> **Note**: Be sure to have a valid Kubernetes 1.18+ environment setup and a namespace named logfilter-demo

## Bootstrap script

In order to bootstrap this solution, I built a simple `bash` script that will start all of this. The script will check
if the dependencies are met (needed binaries are installed), start a local kubernetes environment with minikube through
the docker driver, create the necessary namespace and install the helm chart.

### Improvements

This is the only component that I feel that could have some serious refactoring and improved error handling.
Also, instead of just validating if the dependencies are met, it could install them based on the OS and arch of the host
machine.

### Execution

On the root of the repo, run the following to give execution permissions to the script:
```shell
chmod +x bootstrap.sh
```

Finally, from the root of the repo, run it:
```shell
./bootstrap.sh
```

## Github Pipelines

I felt the necessity to build this pipeline, not just to have a centralised way of building my image with
multi-architectural support (because that would be unattainable from just my machine), but also to give more visibility
to the tests.
Even though the images are always being built, the push is only performed when a release is published.

### Improvements

The pipeline could be seperated into different pipelines, each one with its own responsibility, i.e., we should
separate the tests from the image build.
We could also introduce more flexibility when it comes to when the pipeline is triggered since, at the moment, triggers
are only happening for the master branch, as well as for created releases. If I was a developer and wanted to run this
for a specific environment (e.g. development), I wouldn't have any trigger. Or even if the branch where I am merging to
is not `master` (e.g. merging from `branch-a` to `branch-b`), the pipeline won't be triggered which could be improved.

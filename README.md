# PDS_MOD1_DIPLOMADO_AI_PUCP

Mod 1: Specialization Diploma in Application Development with Artificial Intelligence - PUCP - 2024

Materia: Python for Data Science

## Overview

This project is about Earthquakes in Peru.
This seismic database includes all the parameters that characterize an earthquake, calculated under the same conditions to ensure a homogeneous dataset:

- date
- time
- latitude
- longitude
- depth
- magnitude

The dataset contains the Instrumental Earthquake Catalog for the period from 1960 to 2023 - Peru.

## Requirements

Verify the Python version for the current project

```
    $ python --version
    Python 3.10.11
```

## Development

Ensure you have all the requirements libreries installed:

Follow the instructions:

- Clone the repository on your local machine

```
    git clone https://github.com/Amos-Luna/PDS_mod1_diplom_ai_pucp_2024.git
    cd PDS_mod1_diplom_ai_pucp_2024
```

- Create your custom virtual environment -> example: `venv`

```
    python3 -m venv venv
    source venv/bin/activate
```

- Install dependencies and open VSCode

```
    pip install -r requirements.txt
    code .
```

## Docker

You can esaly run into Docker Container by following the next step:

- Build the Docker image

```
    docker build -t streamlit-sismos:v1 .
```

- Run the Docker image to create a Docker Container

```
    docker run -p 8501:8501 -v $(pwd)/src:/app/src -v $(pwd)/data:/app/data streamlit-sismos:v1
```

- Copy the url showed into the terminal. Example:

```
    http://0.0.0.0:8501/
```

# License

This project is licensed under the MIT License - see the LICENSE file for details.

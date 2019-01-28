# File from: https://fmgdata.kinja.com/using-docker-with-conda-environments-1790901398

FROM continuumio/miniconda3:latest

ARG DEBIAN_FRONTEND=noninteractive

# Set the ENTRYPOINT to use bash
# (this is also where you’d set SHELL,
# if your version of docker supports this)
SHELL [ "/bin/bash", "-c" ]

# Update conda
RUN conda update -n base conda

EXPOSE 5000

# Install nano
RUN apt-get update
RUN apt-get install nano
RUN apt-get install -y coinor-cbc
RUN apt-get install -y python3-gdal
RUN apt-get install -y build-essential

# Create code and config folder
RUN mkdir /code
RUN mkdir /config

# Install WAM conda environment
COPY environment.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml
RUN echo "source activate django" > ~/.bashrc
RUN source activate django
RUN pip install --upgrade pip

# Copy WAM folder and apps
COPY . /code/
WORKDIR /code/

# Install dependencies from WAM_APPS:
ARG WAM_APPS
ENV WAM_APPS=$WAM_APPS
RUN echo "Installing reqiurements for following apps: $WAM_APPS"
RUN python /code/install_requirements.py

# run entrypoint.sh
ENTRYPOINT ["/code/entrypoint.sh"]

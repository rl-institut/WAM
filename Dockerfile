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

# Install additional libs
RUN apt-get clean && apt-get update && apt-get install -y nano coinor-cbc python3-gdal build-essential locales

# Set locale
RUN sed -i -e 's/# de_DE.UTF-8 UTF-8/de_DE.UTF-8 UTF-8/' /etc/locale.gen && locale-gen
ENV LANG de_DE.UTF-8
ENV LANGUAGE de_DE:en
ENV LC_ALL de_DE.UTF-8

# Create code and config folder
RUN mkdir /code
RUN mkdir /config

# Install WAM conda environment
COPY environment.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml
RUN echo "source activate django" > ~/.bashrc
ENV PATH="/opt/conda/envs/django/bin:$PATH"
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

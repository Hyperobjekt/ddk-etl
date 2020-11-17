# Start from ubuntu
FROM ubuntu:16.04

# Update repos and install dependencies
RUN apt-get update \
  && apt-get -y upgrade \
  && apt-get -y install git build-essential \
    libsqlite3-dev zlib1g-dev libssl-dev \
    python3-dev python3-pip gzip curl wget \
    libspatialindex-dev unzip locales

# Set locale for UTF 8 encoding in shell
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
ENV NODE_VERSION=12.6.0

# Create a directory and copy in all files
RUN mkdir -p /tmp/tippecanoe-src
RUN git clone -b 1.32.9 https://github.com/mapbox/tippecanoe.git /tmp/tippecanoe-src
WORKDIR /tmp/tippecanoe-src

# Build tippecanoe
RUN git checkout -b master && \
  make && \
  make install

# Remove the temp directory
WORKDIR /
RUN rm -rf /tmp/tippecanoe-src

# Build NodeJS and install NPM packages
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.0/install.sh | bash
ENV NVM_DIR="/root/.nvm"
RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm use v${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm alias default v${NODE_VERSION}
ENV PATH="/root/.nvm/versions/node/v${NODE_VERSION}/bin/:${PATH}"
RUN node --version
RUN npm --version

RUN npm install -g mapshaper csv2geojson

COPY . /app
WORKDIR /app/

# Install Python packages
# RUN pip3 install pipenv && pipenv install --system
# RUN npm install

# make entrypoint executable
RUN chmod +x build.sh

ENTRYPOINT ["./build.sh"]

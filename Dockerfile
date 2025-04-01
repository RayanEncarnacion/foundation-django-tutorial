# Set the python version as a build-time argument
# with Python 3.12 as the default
ARG PYTHON_VERSION=3.12-slim-bullseye
FROM python:${PYTHON_VERSION}

# Create a virtual environment
RUN python -m venv /opt/venv

# Set the virtual environment as the current location
ENV PATH=/opt/venv/bin:$PATH

# Upgrade pip
RUN pip install --upgrade pip

# Set Python-related environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install os dependencies for our mini vm
RUN apt-get update && apt-get install -y \
    # for postgres
    libpq-dev \
    # for tailwind setup
    curl \
    # for Pillow
    libjpeg-dev \
    # for CairoSVG
    libcairo2 \
    # other
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create the mini vm's code directory
RUN mkdir -p /code

# Set the working directory to that same code directory
WORKDIR /code

# Copy the requirements file into the container
COPY requirements.txt /tmp/requirements.txt

# copy the project code into the container's working directory
COPY ./src /code

# Install the Python project requirements
RUN pip install -r /tmp/requirements.txt

ARG DJANGO_SECRET_KEY
ENV DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}

ARG DJANGO_DEBUG=0
ENV DJANGO_DEBUG=${DJANGO_DEBUG}

# Setup TailwindCSS
RUN echo "Downloading Tailwind CSS binary..." && \
    curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/download/v4.0.14/tailwindcss-linux-x64 && \
    echo "Making Tailwind CSS binary executable..." && \
    chmod +x tailwindcss-linux-x64 && \
    echo "Renaming Tailwind CSS binary to 'tailwindcss'..." && \
    mv tailwindcss-linux-x64 tailwindcss && \
    echo "Create input.css with the TailwindCSS import..." && \
    mkdir -p ./staticfiles/vendors && echo '@import "tailwindcss";' > ./staticfiles/vendors/input.css && \
    echo "Processing and minifying CSS files..." && \
    ./tailwindcss -i ./staticfiles/vendors/input.css -o ./staticfiles/vendors/output.css --minify && \
    echo "Deleting Tailwind CSS executable..." && \
    rm tailwindcss && \
    echo "Tailwind CSS setup completed successfully."

# database isn't available during build
# run any other commands that do not need the database
# such as:

# Download files and move to local-cdn
RUN python manage.py vendor_pull
RUN python manage.py collectstatic --noinput

# set the Django default project name
ARG PROJ_NAME="foundation"

# create a bash script to run the Django project
# this script will execute at runtime when
# the container starts and the database is available
RUN printf "#!/bin/bash\n" > ./paracord_runner.sh && \
    printf "RUN_PORT=\"\${PORT:-8000}\"\n\n" >> ./paracord_runner.sh && \
    printf "python manage.py migrate --no-input\n" >> ./paracord_runner.sh && \
    printf "gunicorn ${PROJ_NAME}.wsgi:application --bind \"[::]:\$RUN_PORT\"\n" >> ./paracord_runner.sh
    # Command to process schedules tasks
    printf "python manage.py process_tasks" >> ./paracord_runner.sh

# make the bash script executable
RUN chmod +x paracord_runner.sh

# Clean up apt cache to reduce image size
RUN apt-get remove --purge -y \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Run the Django project via the runtime script
# when the container starts
CMD ./paracord_runner.sh
FROM python:3.7

RUN mkdir /app

WORKDIR /app

# Add source files

ADD . /app

# Install dependencies

RUN python -m pip install -r requirements.txt

# Install package

RUN python -m pip install . --upgrade

# Prepare API port

EXPOSE 5000

# Start application

CMD ["mlgdansk132"]
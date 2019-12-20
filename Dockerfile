FROM python:3.7-slim-buster

# Copy & Install project dependencies
COPY requirements.txt /opt/app/requirements.txt
WORKDIR /opt/app
RUN pip install -r requirements.txt

# Copy projects code
COPY . /opt/app
RUN pip install . --no-deps

# Start app
CMD ["sh", "/opt/app/start.sh"]

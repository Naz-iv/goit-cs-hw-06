# Use the official Python image as base image
FROM python:3.10-alpine

# set env parameters
ENV APP_HOME /app

# Set the working directory in the container
WORKDIR $APP_HOME

# Copy application files to the container
COPY . .

#  install the dependencies
RUN pip install -r requirements.txt

# Expose ports
EXPOSE 3000
EXPOSE 5000
EXPOSE 27017


# Specify the command to run on container start
CMD ["python", "main.py"]
#Using a minimal base image
FROM python:3.9.10-slim
# Set the working directory to /app
WORKDIR /app
# Copy the current directory contents into the container at /app
ADD . /app

# Make port 1010 available outside this container
EXPOSE 1010/udp
EXPOSE 1010/tcp

CMD ["python3","-u", "tlsproxy.py"]

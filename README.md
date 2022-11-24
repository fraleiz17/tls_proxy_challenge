# Challenge
DNS to DNS-over-TLS proxy in python


## DNS to DNS-over-TLS proxy - Questions
- Imagine this proxy being deployed in an infrastructure. What would be the security concerns you would raise?

    This take to the problem does not involve certificates, I would Advice to use them to connect to the Cloudflare server and as well to authorize the incoming requests to process. 

- How would you integrate that solution in a distributed, microservices-oriented and containerized architecture?

    This solution can be implemented as the local DNS resolver for the application given that it is running in a cluster,  this means that this service will not be exposed to the internet. If we were to expose this I will need to investigate how to harden it before the go-live

- What other improvements do you think would be interesting to add to the project?
    * Cover Testing, I was not able to implement it due to time constraints.
    * Do a static code analysis and the docker image to see if there are known vulnerabilities
    * Create a path on the container matching the conventions of the solution to write logs, maybe to be sent to another place for further processing
    * Improve error handling and adopt a convention for docstrings
    * Improve the way that queries are send to Cloudflare, maybe another thread to avoid multiple connections
    * Implement a config file with YML
    * Python is not the best handling threads and parallelism, definitely try to implement this in GoLang for better performance


### To run the code
You can do this in 2 ways: 
- __Manually__

    From the root dir of this project run: `docker build -t tlsproxy .` This will build the image.

    Run the image with `docker run  -p 1010:1010 -p 1010:1010/udp -d --rm --name tlsproxy tlsproxy`

    You should be able to see it running from your local Docker GUI, then you can test it with:
    `dig  @127.0.0.1 -p 1010  www.google.com`
    `dig  @127.0.0.1 -p 1010  www.google.com`

- __Execute Script__

    Run the build script:
    `./build.sh`

To test how the threading works, I used multiple terminals running the `./test.sh` script not fully sure if concurrent, I found this hard to test.

### Notes
- This implementation currently supports:
    * Multiple incoming requests 
    * TCP and UDP requests


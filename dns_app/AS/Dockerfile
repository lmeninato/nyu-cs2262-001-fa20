FROM python:3.9

RUN apt-get update \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


RUN groupadd -g 799 nyu && \
    useradd -r -u 999 -g nyu nyu

# docker build -t lmeninato/as:latest .
# docker run --network dns_app --name as -p 53533:53533/udp -it lmeninato/as:latest

# Set up a working folder and install the pre-reqs
WORKDIR /app

USER nyu

COPY --chown=nyu:nyu . .

CMD [ "python", "./run.py" ]
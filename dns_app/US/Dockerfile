FROM python:3.9

RUN apt-get update \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


RUN groupadd -g 799 nyu && \
    useradd -r -u 999 -g nyu nyu

# Set up a working folder and install the pre-reqs
WORKDIR /app

RUN pip install Flask
RUN pip install requests

# docker build -t lmeninato/us:latest .
# docker run --network dns_app --name us -p 8080:8080 -it lmeninato/us:latest

USER nyu

COPY --chown=nyu:nyu . .

CMD [ "python", "./run.py" ]
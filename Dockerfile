FROM ubuntu:latest
WORKDIR /app
COPY /webapp /app
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y tzdata
RUN apt-get install -y python3.9 python3-pip
RUN apt-get install -y fluidsynth
RUN pip install music21
RUN pip install midi2audio
RUN pip install flask
ENTRYPOINT ["python3"]
CMD ["run.py"]
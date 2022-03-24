FROM tensorflow/tensorflow

RUN pip install pillow

COPY ./runnerlib /opt/lib/runnerlib
WORKDIR /opt/lib/runnerlib
RUN pip install .

WORKDIR /opt/project

COPY ./meme-classifier/model ./model

COPY ./meme-classifier/* ./

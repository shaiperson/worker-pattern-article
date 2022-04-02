FROM tensorflow/tensorflow

# Install Tesseract engine
RUN apt-get update
RUN apt-get -y install tesseract-ocr

RUN pip install pillow
COPY ./meme-classifier/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./runnerlib /opt/lib/runnerlib
WORKDIR /opt/lib/runnerlib
RUN pip install .

WORKDIR /opt/project

COPY ./meme-classifier/ ./

FROM tensorflow/tensorflow

COPY ./nlp/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./runnerlib /opt/lib/runnerlib
WORKDIR /opt/lib/runnerlib
RUN pip install .

WORKDIR /opt/project

COPY ./nlp/* ./

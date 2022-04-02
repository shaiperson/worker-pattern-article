FROM tensorflow/tensorflow

WORKDIR /opt/project

COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install pillow

COPY ./ ./

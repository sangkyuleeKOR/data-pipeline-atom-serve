ARG BASE_IMAGE=nvcr.io/nvidia/l4t-base:r32.4.4
FROM ${BASE_IMAGE}

RUN apt-get update && apt-get install -y python3-distutils python3-virtualenv nginx libgl1-mesa-glx libglib2.0-0 build-essential libssl-dev libffi-dev python3-dev libsndfile1 libpq-dev libsm6 libxext6 libxrender-dev libopenblas-dev libfreetype6-dev openmpi-bin libusb-1.0-0-dev udev gfortran curl \
	&& rm -rf /var/lib/apt/list/* \ 
	&& cd /tmp \
	&& curl -LO https://bootstrap.pypa.io/get-pip.py \
	&& python3 get-pip.py

ADD ./ArenaSDK_Linux_x64 /ArenaSDK_Linux_x64
RUN cd /ArenaSDK_Linux_x64 && sh Arena_SDK.conf

ADD ./arena_api-2.0.1-py3-none-any.whl /arena_api-2.0.1-py3-none-any.whl
ADD ./requirements.txt /requirements.txt

RUN pip install --upgrade pip && pip install --no-cache-dir -r /requirements.txt
RUN pip install arena_api-2.0.1-py3-none-any.whl

ENTRYPOINT ["/app/start.sh"]
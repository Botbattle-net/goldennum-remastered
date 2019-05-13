FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
FROM python:3-slim-bookworm

COPY ./requirements.txt .

COPY ./launch_second_wf.py .

COPY ./infinite_loop.sh .

RUN pip install -r ./requirements.txt

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y gh

CMD ["python", "./launch_second_wf.py"]
# CMD ["bash", "./infinite_loop.sh"]
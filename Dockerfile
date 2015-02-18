FROM python:3.4
RUN apt-get -q update && apt-get -qy install git && apt-get -qy autoremove
RUN pip install git+https://github.com/etalab/addok.git
RUN pip install gunicorn
EXPOSE 7878
ENTRYPOINT ["addok"]

FROM python:3.8-slim-buster

LABEL IMAGE="extractslice2pdf"
LABEL VERSION="0.1.1"
LABEL CI_IGNORE="True"

RUN pip3 install SimpleITK Pillow reportlab

COPY files/extractslice2pdf.py /

CMD ["python3","-u","/extractslice2pdf.py"]

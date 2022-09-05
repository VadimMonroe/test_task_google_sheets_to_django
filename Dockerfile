FROM python:3

COPY . .
WORKDIR /test_task

RUN pip install --upgrade pip 
RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "manage.py" ]
# CMD ["migrate"]
CMD ["runserver", "0.0.0.0:8000"]
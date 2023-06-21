FROM python:3.9-slim

COPY . .
RUN pip install -r requirements.txt

# start bot
EXPOSE 8000
ENTRYPOINT ["python", "-m", "bot"]
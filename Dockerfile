FROM python:3.14-slim
RUN useradd -m myuser
USER myuser
WORKDIR /home/myuser/app
COPY --chown=myuser:myuser requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt
COPY --chown=myuser:myuser api-app.py .
ENV PATH="/home/myuser/.local/bin:${PATH}"
ENV REDIS_HOST="redis-db"
EXPOSE 5000
CMD ["python", "api-app.py"]

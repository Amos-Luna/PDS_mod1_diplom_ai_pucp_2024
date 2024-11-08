FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["streamlit", "run", "src/app.py", "--server.port=8000", "--server.address=0.0.0.0"]
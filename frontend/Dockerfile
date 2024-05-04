FROM python:3.12-slim

WORKDIR /app

COPY . .

# COPY ../.streamlit ./.streamlit

RUN pip install streamlit requests pandas

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]

CMD ["app.py"]
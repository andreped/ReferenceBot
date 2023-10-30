# Use multi-stage builds to reduce the size of the final image
FROM python:3.10-slim as builder

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \ 
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.5.1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Set up a new user named "user" with user ID 1000
RUN useradd -m -u 1000 user

# Switch to the "user" user
USER user

# Set home to the user's home directory
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Set the working directory to the user's home directory
WORKDIR $HOME/app

COPY . $HOME/app

RUN python3 -m pip install -r requirements.txt

# Copy the current directory contents into the container at $HOME/app setting the owner to the user
COPY --chown=user . $HOME/app

# create data/ directory to store PDFs
RUN mkdir $HOME/app/data/ && chmod -R 777 $HOME/app/data/

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8501

CMD ["python", "-m", "streamlit", "run", "knowledge_gpt/main.py", "--server.port=8501", "--server.address=0.0.0.0"]

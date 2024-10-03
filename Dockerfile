# FROM python:3.10.12

# WORKDIR /usr/src/app

# RUN python -m venv /usr/src/app/venv

# ENV PATH="/usr/src/app/venv/bin:$PATH"

# COPY requirements.txt .

# RUN pip install --no-cache-dir -r requirements.txt

# COPY pullenti /usr/src/app/venv/lib/python3.10/site-packages/pullenti

# COPY . .

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM debian:buster

RUN apt-get update && apt-get install -y \
    wget \
    build-essential \
    libffi-dev \
    libgdbm-dev \
    libncurses5-dev \
    libsqlite3-dev \
    libssl-dev \
    zlib1g-dev \
    libexpat1-dev \
    libmpdec-dev \
    libbz2-dev \
    liblzma-dev \
    libsqlite3-dev \
    libssl-dev \
    zlib1g-dev 

WORKDIR /usr/src
RUN wget https://www.python.org/ftp/python/3.10.12/Python-3.10.12.tgz
RUN tar -xzf Python-3.10.12.tgz

WORKDIR /usr/src/Python-3.10.12
RUN ./configure \
    --enable-optimizations \
    --with-computed-gotos \
    --enable-ipv6 \
    --with-system-expat \
    --with-system-libmpdec \
    --with-system-ffi \
    --with-lto \
    LDFLAGS="-Wl,-Bsymbolic-functions -O2" 
RUN make -j8
RUN make altinstall

# ENV PATH="/usr/local/bin:$PATH"
WORKDIR /usr/src/app

RUN python3.10 -m venv /usr/src/app/venv
ENV PATH="/usr/src/app/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY pullenti /usr/src/app/venv/lib/python3.10/site-packages/pullenti

COPY . .

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--limit-concurrency", "100", "--backlog", "2048", "--limit-max-requests", "1000"]

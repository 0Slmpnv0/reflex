FROM python:3.10

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY poetry.lock pyproject.toml .

ENV PATH="/root/.local/bin:$PATH"

RUN ["poetry", "install"]


COPY . .

WORKDIR ./backend

EXPOSE 8000

CMD ["poetry", "run", "fastapi", "run", "main.py", "--port", "8000"]

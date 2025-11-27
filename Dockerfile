FROM astral/uv:python3.12-bookworm-slim
LABEL authors="Jinx@qqAys"

WORKDIR /usr/src/tantian
COPY . .

ENV TZ=UTC
ENV APP_VERSION=0.1.1

ENV UV_DEFAULT_INDEX=https://pypi.tuna.tsinghua.edu.cn/simple

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN uv sync

EXPOSE 8080

CMD ["uv", "run", "-m", "app.main"]
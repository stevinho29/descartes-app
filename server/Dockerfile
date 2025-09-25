# ---- Stage 1: builder ----
    FROM python:3.11-slim AS builder

    WORKDIR /usr/local
    
    # Installer curl
    RUN apt-get update && apt-get install -y curl

    # Installer uv
    RUN curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # Ajouter uv au PATH
    ENV PATH="/root/.local/bin:$PATH"

    # Copier uniquement les fichiers de dépendances
    COPY pyproject.toml uv.lock ./
    
    # Créer l'environnement virtuel et installer les deps
    RUN uv venv /usr/local/venv \
        && . /usr/local/venv/bin/activate \
        && uv sync --active --locked --no-install-project
    
    # ---- Stage 2: final image ----
    FROM python:3.11-slim
    
    WORKDIR /usr/local
    
    # Copier le venv depuis le builder
    COPY --from=builder /usr/local/venv /usr/local/venv
    
    # Ajouter le venv au PATH
    ENV PATH="/usr/local/venv/bin:$PATH"
    
    # Copier ton code
    COPY ./app/ /usr/local/app/

    CMD ["fastapi", "run", "/usr/local/app/main.py", "--reload"]
    
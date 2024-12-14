FROM python:3.11.9

# See https://pytest-qt.readthedocs.io/en/latest/troubleshooting.html#github-actions-azure-pipelines-travis-ci-and-gitlab-ci-cd
RUN apt update && apt install --yes \
        software-properties-common \
        git \
        unzip \
        xvfb \
        libxkbcommon-x11-0 \
        libxcb-icccm4 \
        libxcb-image0 \
        libxcb-keysyms1 \
        libxcb-randr0 \
        libxcb-render-util0 \
        libxcb-xinerama0 \
        libxcb-xfixes0 \
        libxcb-cursor0 \
        libxcb-cursor-dev \
        x11-utils \
        libgl1 \
        libegl1 \
        libdbus-1-3 && \
    apt autoremove --yes && \
    apt autoclean --yes

# See https://github.com/NVlabs/instant-ngp/discussions/300#discussioncomment-5639315
ENV QT_QPA_PLATFORM=offscreen

# Install Poetry 1.7.0 with the official installer
ENV POETRY_HOME=/opt/poetry \
    POETRY_VERSION=1.7.0 \
    POETRY_CACHE_DIR=/var/cache/pypoetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="${POETRY_HOME}/bin:${PATH}"

WORKDIR "/tcp"

COPY poetry.lock pyproject.toml /tcp/
RUN poetry install --no-interaction --no-ansi --no-root

# Allows non-docker users to use virtualenvs in project.
ENV POETRY_VIRTUALENVS_IN_PROJECT=false

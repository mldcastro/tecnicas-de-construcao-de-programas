# Técnicas de construção de programas

Repositório destinado aos trabalhos da cadeira INF01120.

## Requisitos

- [`pandoc`](https://pandoc.org/installing.html);
  - Para gerar PDF a partir de um arquivo markdown.
- `pandoc` [`mermaid-filter`](https://github.com/raghur/mermaid-filter);
  - plug-in para transformar diagramas "mermaid" em imagens no arquivo PDF gerado com `pandoc`.
- `texlive`;
  - Necessário para `pandoc` funcionar;
  - Em Linux: `sudo apt update && sudo apt install -y texlive`
- `libnss`;
  - Necessário para o plug-in `mermaid-filter` funcionar;
  - Em Linux: `sudo apt update && sudo apt install -y libnss3-dev libgdk-pixbuf2.0-dev libgtk-3-dev libxss-dev`
- [`poetry`](https://python-poetry.org/docs/#installation);
  - Ferramente para lidar com ambientes Python;
- [Python 3.11](https://www.python.org/downloads/).

## Instalando dependências

Na raíz deste repositório, rode o seguinte comando no terminal:

```bash
poetry install --no-root
```

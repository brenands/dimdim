#!/bin/bash
# Cria ambiente virtual, instala dependências e executa o script principal

# Cria o ambiente virtual se não existir
test -d .venv || python3 -m venv .venv

# Ativa o ambiente virtual
source .venv/bin/activate

# Instala dependências
pip install -r requirements.txt

# Executa o script principal
python3 main.py

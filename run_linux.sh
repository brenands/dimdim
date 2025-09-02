#!/bin/bash
# Cria ambiente virtual, instala dependências e executa o script principal

# Cria o ambiente virtual se não existir
test -d venv || python -m venv venv

# Ativa o ambiente virtual
source venv/Scripts/activate

# Instala dependências
pip install -r requirements.txt

# Executa o script principal
python main.py

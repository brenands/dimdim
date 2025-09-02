@echo off
REM Cria ambiente virtual, instala dependências e executa o script principal
IF NOT EXIST .venv (
	python -m venv .venv
)
call .venv\Scripts\activate
pip install -r requirements.txt
python main.py
pause

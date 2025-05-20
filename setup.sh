#!/bin/bash

# Atualiza pip (opcional)
pip install --upgrade pip

# Roda o app no Streamlit (Render usa a variável de ambiente $PORT)
streamlit run app.py --server.port=$PORT --server.enableCORS=false

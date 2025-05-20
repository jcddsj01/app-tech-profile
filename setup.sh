#!/bin/bash

# Instala dependências e inicia o app
streamlit run app.py --server.port=$PORT --server.enableCORS=false

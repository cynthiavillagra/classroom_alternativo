"""
Vercel Serverless Function Entry Point

Este archivo es el punto de entrada para Vercel.
Importa y expone la variable 'app' del main.py.

POR QUÉ aquí: Vercel busca funciones en /api/
"""

# Agregar el directorio raíz al path para poder importar main
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar el app de main.py
from main import app

# Vercel busca una variable 'app' o una función 'handler'
# Nuestro app ya es un WSGI callable

#!/bin/sh

echo "Aplicando migraciones..."
flask db upgrade

echo "Iniciando servidor Flask..."
exec flask run --host=0.0.0.0
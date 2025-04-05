#!/bin/bash
set -e

# Esperar a que PostgreSQL esté disponible
echo "Esperando a que la base de datos esté disponible..."
while ! pg_isready -h db -p 5432 -U odoo
do
  sleep 1
done

# Verificar si la base de datos ya existe
echo "Verificando si la base de datos existe..."
if psql -h db -U odoo -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='peliculas'" | grep -q 1; then
  echo "La base de datos 'peliculas' ya existe"
else
  echo "Creando base de datos 'peliculas' e instalando el módulo..."
  odoo -d peliculas -i movie_management --stop-after-init --db_host=db --db_user=odoo --db_password=odoo --without-demo=all
fi

# Iniciar Odoo normalmente
echo "Iniciando Odoo..."
exec odoo "$@"
import pandas as pd
from server.models import Contratante
from decimal import Decimal
import numpy as np

# Carga el archivo Excel
archivo_excel = r"C:\Users\Maloh\Documents\LISTA DE CLIENTES ENERO.xlsx"  # Cambia por la ruta de tu archivo
df = pd.read_excel(archivo_excel)

# Función para manejar conversiones a Decimal
def to_decimal(value):
    """Convierte el valor a Decimal, devuelve None si el valor no es válido."""
    try:
        return Decimal(value) if pd.notna(value) and isinstance(value, (int, float)) else None
    except (ValueError, TypeError):
        return None

# Recorre las filas del Excel y guarda los datos en la base de datos
for _, row in df.iterrows():
    # Si el 'NIT O CC' está vacío o nulo, verificamos por nombre
    if pd.isna(row['NIT O CC']) or row['NIT O CC'] == '':
        print(f"Se verificará por nombre ya que 'NIT O CC' está vacío para el contratante: {row['CONTRATANTE']}")
        existing_contratante = Contratante.objects.filter(contratante=row['CONTRATANTE']).first()
    else:
        # Si el 'NIT O CC' no está vacío, verificamos por este campo
        existing_contratante = Contratante.objects.filter(nit_o_cc=row['NIT O CC']).first()

    # Si ya existe el contratante, actualizamos sus datos
    if existing_contratante:
        print(f"Contratante con {'NIT O CC' if pd.notna(row['NIT O CC']) else 'nombre'} {row['NIT O CC'] or row['CONTRATANTE']} ya existe, actualizando datos.")
        
        existing_contratante.tipo_factura = row['TIPO DE FACTURA']
        existing_contratante.mes_atrasado = row['MES  ATRASADO']
        existing_contratante.mes_actual = row['MES ACTUAL']
        existing_contratante.precio_mes_actual = to_decimal(row['PRECIO MES ACTUAL'])
        existing_contratante.precio_mes_atrasado = to_decimal(row['PRECIO MES ATRASADO'])
        existing_contratante.plan_contratado_mes_atrasado = row['PLAN CONTRATADO MES ATRASADO']
        existing_contratante.plan_contratado_mes_actual = row['PLA CONTRATADO MES ACTUAL']
        existing_contratante.deuda = to_decimal(row['DEUDA'])
        existing_contratante.dane = row['DANE']
        existing_contratante.fecha_instalacion = row['FECHA INSTALACION']
        existing_contratante.total = to_decimal(row['TOTAL'])
        existing_contratante.direccion = row['DIRECCION']
        existing_contratante.municipio = row['MUNICIPIO']
        existing_contratante.telefono = row['TELEFONO']
        existing_contratante.correo = row['CORREO']
        existing_contratante.save()
    else:
        # Si no existe un contratante con el mismo NIT O CC o nombre, lo creamos
        print(f"Contratante {row['CONTRATANTE']} no existe, creando nuevo.")
        
        Contratante.objects.create(
            tipo_factura=row['TIPO DE FACTURA'],
            contratante=row['CONTRATANTE'],
            mes_atrasado=row['MES  ATRASADO'],
            mes_actual=row['MES ACTUAL'],
            precio_mes_actual=to_decimal(row['PRECIO MES ACTUAL']),
            precio_mes_atrasado=to_decimal(row['PRECIO MES ATRASADO']),
            plan_contratado_mes_atrasado=row['PLAN CONTRATADO MES ATRASADO'],
            plan_contratado_mes_actual=row['PLA CONTRATADO MES ACTUAL'],
            deuda=to_decimal(row['DEUDA']),
            dane=row['DANE'],
            fecha_instalacion=row['FECHA INSTALACION'],
            total=to_decimal(row['TOTAL']),
            nit_o_cc=row['NIT O CC'] if pd.notna(row['NIT O CC']) and row['NIT O CC'] != '' else None,  # Si NIT O CC está vacío o nulo, lo dejamos como None
            direccion=row['DIRECCION'],
            municipio=row['MUNICIPIO'],
            telefono=row['TELEFONO'],
            correo=row['CORREO'],
        )

print("Datos cargados exitosamente.")

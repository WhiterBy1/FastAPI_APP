# Sistema de Gestión de Clientes, Transacciones y Planes

Este proyecto es un sistema desarrollado con **FastAPI** para gestionar clientes, transacciones y planes de suscripción.

## **Características**
- **Clientes**: Registro, consulta, actualización y eliminación de clientes.
- **Transacciones**: Registro de compras realizadas por los clientes.
- **Planes**: Administración de planes temporales con beneficios como descuentos.

## **Requisitos**
- Python 3.9 o superior
- FastAPI
- SQLModel
- Uvicorn

## **Instalación**

1. Clona este repositorio:
   ```
   git clone https://github.com/WhiterBy1/FastAPI_APP
   cd FastAPI_APP
   ```

2. Crea y activa un entorno virtual:
   ```
   python -m venv .venv
   source .venv/bin/activate  # En macOS/Linux
   .venv\Scripts\activate     # En Windows
   ```

3. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

## **Ejecución**

1. Inicia el servidor:
   ```
   fastapi dev app/main.py
   ```

2. Accede a la aplicación:
   - **Inicio**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - **Documentación Swagger**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## **Estructura del Proyecto**
```
FASTAPI-SERVER/
├── app/
│   ├── __init__.py
│   ├── main.py           # Punto de entrada de la aplicación
│   ├── routers/          # Routers para clientes, transacciones y planes
│   │   ├── __init__.py
│   │   ├── customers.py  # Funcionalidades relacionadas con clientes
│   │   ├── transactions.py  # Funcionalidades de transacciones
│   │   └── plans.py      # Funcionalidades de planes de suscripción
├── db.py                 # Configuración de la base de datos
├── models.py             # Modelos de datos con SQLModel
├── requirements.txt      # Dependencias del proyecto
├── README.md             # Información del proyecto
```
## **Endpoints**
### **Clientes**
- `GET /customers` - Listar todos los clientes.
- `POST /customers` - Crear un cliente.
- `GET /customers/{customer_id}` - Obtener un cliente por ID.
- `PATCH /customers/{customer_id}` - Actualizar un cliente.
- `DELETE /customers/{customer_id}` - Eliminar un cliente.

### **Transacciones**
- `POST /transactions` - Registrar una transacción.

### **Planes**
- `POST /plans` - Registrar un plan.
- `GET /plans` - Listar planes disponibles.

### **Facturación**
- `POST /invoices` - Crear una factura.

---

Este README incluye las instrucciones necesarias para configurar y ejecutar el proyecto usando`fastapi dev`.  🚀

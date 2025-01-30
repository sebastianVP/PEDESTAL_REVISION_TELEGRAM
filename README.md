**REVISIÓN DE ESTADO DEL RADAR METEOROLOGICO SOPHY**
---

Primero desarrollaremos un programa de verificacion del estado de operacion del radar.
Si esta corriendo el experimento nos indicara el STATUS y el nombre del experimento.
Si no esta corriendo el experimento nos indicara que el radar no esta ejecutando ningun experimento y que por ende esta apagado.

Los comandos utilizados son:

Estado del radar, si esta o no operativo
* curl http://sophy-proc/status
Informacion del experimento configurado
* curl http://sophy-schain/status

---
* System design for software developers and engineers
* Learn about basic engineering design patterns that are used to build large-scale distributed systems.
    *   Large Scale distributed systems
* Design Patterns are a particular practices, principles, or porcesss which are used by engineers to build the systems
* Engineers use system design patterns to make relieble scalable, and maintainable systems.This helps them convert business requirements into technical solutions.
* Revisar a publisher suscriber model
---

En la parte del pedestal deseo añadir.

**Completado 1**
---
1. Mostrar los ultimos 3 archivos, especificar su marca de tiempo y fecha de creación.
2. El momento que se guardo el ultimo archivo
3. Graficar la velocidad del pedestal con esos 3 ultimos archivos.
4. Comparar la marca de tiempo actual con la hora actual y no superar los 2 minutos.
5. La velocidad no debe ser menor a 0.5 en promedio.
6. Si alguna de las condiciones falla indicar que se presento un problema y que requiere revisión.
7. El programa se ejecuta en el minuto 10 y 50 cada hora:
     10,50 * * * * cd /home/soporte/Documents/PEDESTAL_REVISION_TELEGRAM && ./reporte.sh


**Pendiente 1**
---
En la parte del radar deseo revisar los ultimos archivos de rawdata hdf.
8. Revisaremos ahora los archivos hdf5, si existen y se estan creando acorde con el tiempo.
9. Revisar el ultimo grafico generado para identificar si el procesamiento se detuvo.
10. Reiniciar el experimento 
11. Enviar el reporte pdf por telegram

Tomar de ejemplo algo simple como:
```
from telegram import Bot

TOKEN = "TU_TOKEN_AQUÍ"
CHAT_ID = "ID_DEL_CHAT_O_USUARIO"
PDF_PATH = "ruta/al/archivo.pdf"

bot = Bot(token=TOKEN)
bot.send_document(chat_id=CHAT_ID, document=open(PDF_PATH, "rb"))
print("PDF enviado con éxito")
```
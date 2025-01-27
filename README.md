**REVISIÓN DE ESTADO DEL RADAR METEOROLOGICO SOPHY**
---

Primero desarrollaremos un programa de verificacion del estado de operacion del radar.
Si esta corriendo el experimento nos indicara el STATUS y el nombre del experimento.
Si no esta corriendo el experimento nos indicara que el radar no esta ejecutando ningun experimento y que por ende esta apagado.

Los comandos utilizados son:
* curl http://sophy-proc/status
* curl http://sophy-schain/status


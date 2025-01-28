import subprocess
import json
import os
import time
import h5py
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer
from datetime import datetime

def execute_command(command):
    try:
        result = subprocess.run(command,shell=True,capture_output=True,text= True)
        if result.returncode == 0:
            return json.loads(result.stdout) if result.stdout else None
        else:
            return {"error": result.stderr.strip()}
    except Exception as e:
        return  {"error":str(e)}
    
def check_radar_conditions():
    # Check radar status
    radar_status = execute_command("curl http://sophy-proc/status")

    # Check experiment configuration
    experiment_status = execute_command("curl http://sophy-schain/status")


    return {
        "radar_status"      : radar_status,
        "experiment_status" : experiment_status,
    }

def obtener_informacion_archivos(ruta,file):
    filename = os.path.join(ruta,file)
    with h5py.File(filename, "r") as obj:
        for key in obj.keys():
            for key2 in obj[key].keys():
                if key2 == "azi_speed":
                    param = f"{key}/{key2}"
                    key3  = "utc"
                    time_utc= f"{key}/{key3}"
                    try:
                        data = np.array(obj[param])
                        avg_speed = np.mean(data)
                        time_obj = np.array(obj[time_utc])
                        time_0   = time_obj[0]
                        return data, time_obj
                    except Exception as e:
                        print(f"Error al procesar '{key2}' en {filename}: {e}")
                        return None, None


def diccionario(directorio_principal):
    # Obtener la lista de directorios dentro del directorio principal
    directorios = [d for d in os.listdir(directorio_principal) if os.path.isdir(os.path.join(directorio_principal, d))]

    # Ordenar los directorios por fecha de creación (el más reciente primero)
    directorios.sort(key=lambda x: os.path.getctime(os.path.join(directorio_principal, x)), reverse=True)


    # Seleccionar el último directorio creado
    if directorios:
        ultimo_directorio = directorios[0]
        ruta_ultimo_directorio = os.path.join(directorio_principal, ultimo_directorio)

        # Obtener la lista de archivos en el último directorio
        archivos = [archivo for archivo in os.listdir(ruta_ultimo_directorio) if os.path.isfile(os.path.join(ruta_ultimo_directorio, archivo))]    


        # Ordenar los archivos por fecha de modificación (los últimos modificados primero)
        archivos.sort(key=lambda x: os.path.getmtime(os.path.join(ruta_ultimo_directorio, x)), reverse=True)
        print(archivos)
        # Listar los últimos 3 archivos
        ultimos_3_archivos = archivos[:3]

        # Mostrar los resultados
        print("Últimos 3 archivos:")
        informacion_archivos = []
        for archivo in ultimos_3_archivos:
            timestamp      = os.path.getmtime(os.path.join(ruta_ultimo_directorio,archivo))
            fecha_creacion = datetime.fromtimestamp(timestamp)
            informacion_archivos.append({
                "nombre": os.path.basename(archivo),
                "timestamp": timestamp,
                "fecha_creacion": fecha_creacion
            })
        


        return informacion_archivos,ruta_ultimo_directorio
    else:
        return None,None




def generate_pdf_report(data,output_file):
    doc    = SimpleDocTemplate(output_file,pagesize=letter)
    styles =  getSampleStyleSheet()
    story  =  []
    # Title
    story.append(Paragraph("<b>Radar Operativity Report</b>", styles['Title']))
    story.append(Spacer(1, 12))
     
    # Date and time
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    story.append(Spacer(1, 12))

    # Add radar status
    story.append(Paragraph("<b>Radar Status:</b>", styles['Heading2']))
    if "error" in data["radar_status"]:
        story.append(Paragraph(f"Error: {data['radar_status']['error']}", styles['Normal']))
    else:
        story.append(Paragraph(json.dumps(data['radar_status'], indent=4), styles['Code']))
    story.append(Spacer(1, 12))

    # Add experiment configuration status
    story.append(Paragraph("<b>Experiment Configuration:</b>", styles['Heading2']))
    if "error" in data["experiment_status"]:
        story.append(Paragraph(f"Error: {data['experiment_status']['error']}", styles['Normal']))
    else:
        story.append(Paragraph(json.dumps(data['experiment_status'], indent=4), styles['Code']))
    story.append(Spacer(1, 12))
    # Add other checks

    # DOS ESTADOS: STATUS Y REVISION DE EXPERIMENTO
    # STATUS
    print("radar_status",data["radar_status"])

    radar_experiment= data["radar_status"]['status']

    # REVISION EXPERIMENTO

    print("experiment_status",data['experiment_status'])

    conf =data['experiment_status'] 

    experiment = data["radar_status"]["name"]

    PATH = "/DATA_RM/DATA"

    path = conf['usrp_rx']['datadir']

    path_ped = os.path.join(PATH, experiment, 'position')

    print("Directorio adquisicion",path)

    print("Directorio de Pedestal",path_ped)

    checks = [
        ("Radar Experiment", radar_experiment),
    ]

    story.append(Paragraph("<b>Overview Checks:</b>", styles['Heading2']))
    
    for check, result in checks:
        print("check",check)
        if check=="Radar Experiment":
            status = "ON" if result else "OFF"
        else:
            status = "PASS" if result else "FAIL"
        story.append(Paragraph(f"{check}: {status}", styles['Normal']))


    archivos,ruta = diccionario(directorio_principal=path_ped)

    story.append(Paragraph("<b>Pedestal Checks:</b>", styles['Heading2']))

    if not archivos:
        story.append(Paragraph("No se encontraron archivos en el directorio del pedestal.", styles["Normal"]))
    else:
        story.append(Paragraph("<b>Últimos 3 Archivos del Pedestal:</b>", styles["Heading2"]))
        for archivo in archivos:
            story.append(Paragraph(
                f"Nombre: {archivo['nombre']}, Fecha de creación: {archivo['fecha_creacion']}",
                styles["Normal"]
            ))

    story.append(Spacer(1, 12))

    # Build the PDF
    doc.build(story)


if __name__ == "__main__":
    # GET RADAR CONDITION DATA
    data = check_radar_conditions() 
    # Generate PDF report
    output_file = "radar_operativity_report.pdf"
    generate_pdf_report(data,output_file)
    print(f"Report generated: {output_file}")


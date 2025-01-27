import subprocess
import json
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
        "radar_status": radar_status,
        "experiment_status": experiment_status
    }

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

    # Build the PDF
    doc.build(story)


if __name__ == "__main__":
    # GET RADAR CONDITION DATA
    data = check_radar_conditions() 
    # Generate PDF report
    output_file = "radar_operativity_report.pdf"
    generate_pdf_report(data,output_file)

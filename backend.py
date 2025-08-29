from flask import Flask, render_template, request, jsonify, send_file
import os
import cv2
import numpy as np
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from ndvi_utils import calculate_ndvi, classify_vegetation, get_stats, draw_contours_on_ndvi

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"
REPORT_FOLDER = "reports"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

# Global variable to store current analysis data
current_analysis = {}

# ---- PAGE ROUTES ----
@app.route("/")
def home():         
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/visualize")
def visualize():
    return render_template("index.html")

# ---- NDVI PROCESSING ROUTE ----
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        red_band = request.files.get("red_band")
        nir_band = request.files.get("nir_band")

        if not red_band or not nir_band:
            return jsonify({"error": "Both red and NIR band files are required"}), 400

        red_path = os.path.join(UPLOAD_FOLDER, red_band.filename)
        nir_path = os.path.join(UPLOAD_FOLDER, nir_band.filename)
        red_band.save(red_path)
        nir_band.save(nir_path)

        # NDVI calculation
        ndvi, transform = calculate_ndvi(red_path, nir_path)
        healthy, moderate, unhealthy = classify_vegetation(ndvi)
        stats = get_stats(ndvi, healthy, moderate, unhealthy, transform)

        # Draw contours on NDVI image
        ndvi_rgb = draw_contours_on_ndvi(ndvi, healthy, moderate, unhealthy)
        result_path = os.path.join(RESULT_FOLDER, "ndvi_result.png")
        cv2.imwrite(result_path, cv2.cvtColor(ndvi_rgb, cv2.COLOR_RGB2BGR))

        # Store analysis data for PDF generation
        global current_analysis
        current_analysis = {
            'red_filename': red_band.filename,
            'nir_filename': nir_band.filename,
            'stats': stats,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        return jsonify({
            "stats": stats,
            "image_url": "/download_image"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/result_image")
def result_image():
    result_path = os.path.join(RESULT_FOLDER, "ndvi_result.png")
    return send_file(result_path, mimetype="image/png")

@app.route("/download_image")
def download_image():
    result_path = os.path.join(RESULT_FOLDER, "ndvi_result.png")
    return send_file(
        result_path, 
        mimetype="image/png",
        as_attachment=True,
        download_name="ndvi_analysis_result.png"
    )

@app.route("/download_report")
def download_report():
    if not current_analysis:
        return jsonify({"error": "No analysis data available"}), 400
    
    try:
        # Generate PDF report
        report_filename = f"vegetation_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        report_path = os.path.join(REPORT_FOLDER, report_filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(report_path, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        story.append(Paragraph("Vegetation Analysis Report", title_style))
        story.append(Spacer(1, 20))
        
        # Analysis details
        story.append(Paragraph(f"<b>Analysis Date:</b> {current_analysis['timestamp']}", styles['Normal']))
        story.append(Paragraph(f"<b>Red Band File:</b> {current_analysis['red_filename']}", styles['Normal']))
        story.append(Paragraph(f"<b>NIR Band File:</b> {current_analysis['nir_filename']}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Statistics table
        stats = current_analysis['stats']
        data = [
            ['Metric', 'Value'],
            ['NDVI Minimum', f"{stats['ndvi_min']:.3f}"],
            ['NDVI Maximum', f"{stats['ndvi_max']:.3f}"],
            ['Healthy Vegetation', f"{stats['healthy_pct']}% ({stats['healthy_pixels']} pixels)"],
            ['Moderate Vegetation', f"{stats['moderate_pct']}% ({stats['moderate_pixels']} pixels)"],
            ['Unhealthy Vegetation', f"{stats['unhealthy_pct']}% ({stats['unhealthy_pixels']} pixels)"],
            ['Total Area', f"{stats['pixel_area_m2']} m²"]
        ]
        
        table = Table(data, colWidths=[2*inch, 3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(Paragraph("<b>Analysis Results:</b>", styles['Heading2']))
        story.append(Spacer(1, 10))
        story.append(table)
        story.append(Spacer(1, 20))
        
        # Add the NDVI image
        result_path = os.path.join(RESULT_FOLDER, "ndvi_result.png")
        if os.path.exists(result_path):
            img = Image(result_path, width=6*inch, height=4*inch)
            story.append(Paragraph("<b>NDVI Analysis Visualization:</b>", styles['Heading2']))
            story.append(Spacer(1, 10))
            story.append(img)
        
        # Build PDF
        doc.build(story)
        
        return send_file(
            report_path,
            mimetype="application/pdf",
            as_attachment=True,
            download_name=report_filename
        )
        
    except Exception as e:
        return jsonify({"error": f"Failed to generate PDF: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)

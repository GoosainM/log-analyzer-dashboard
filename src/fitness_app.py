import streamlit as st
import pandas as pd
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Configure Page Layout
st.set_page_config(page_title="Hybrid Performance Analytics", layout="wide")
st.title("🏋️‍♂️ Hybrid Performance Analytics & Report Engine")
st.markdown("Log athletic performance metrics, analyze operational volume trends, and compile automated client PDF reports.")

# --- Step 1: User Input Data Interface ---
st.subheader("1. Weekly Metric Logging")
col_input1, col_input2, col_input3, col_input4 = st.columns(4)

with col_input1:
    client_name = st.text_input("Client/Athlete Name", "Matthew Gousain")
    week_num = st.text_input("Training Week", "Week 1")
with col_input2:
    squat_vol = st.number_input("Squat Total Volume (kg)", min_value=0, value=2500)
    deadlift_vol = st.number_input("Deadlift Total Volume (kg)", min_value=0, value=3000)
with col_input3:
    running_dist = st.number_input("Running Distance (km)", min_value=0.0, value=15.5, step=0.1)
    avg_hr = st.number_input("Average Resting HR (BPM)", min_value=0, value=54)
with col_input4:
    sleep_score = st.slider("Average Sleep Quality (1-10)", 1, 10, 8)
    coach_notes = st.text_area("Coach's Performance Feedback", "Excellent adaptation to the hybrid split. Running pacing improved while preserving lower-body structural strength.")

# --- Step 2: PDF Generation Logic ---
def generate_pdf_report(filename, name, week, squat, deadlift, run, hr, sleep, notes):
    """Generates a structured, beautifully aligned performance report using ReportLab."""
    doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom Brand Palette Styles
    title_style = ParagraphStyle(
        'BrandTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#111827'), # Dark Charcoal
        spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        'BrandSubtitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#4B5563'),
        spaceAfter=20
    )
    header_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1F2937'),
        spaceBefore=12,
        spaceAfter=8
    )
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#374151'),
        leading=14
    )

    # Document Header Elements
    story.append(Paragraph("MATTHEWS METHOD PERFORMANCE LAB", title_style))
    story.append(Paragraph(f"Official Weekly Athlete Progress Report • Generated for {name}", subtitle_style))
    story.append(Spacer(1, 10))
    
    # Metrics Table Layout
    story.append(Paragraph("📊 Operational Metrics Summary", header_style))
    data = [
        [Paragraph("<b>Metric Dimension</b>", body_style), Paragraph("<b>Recorded Value</b>", body_style), Paragraph("<b>Target Threshold</b>", body_style)],
        [Paragraph("Training Cycle Block", body_style), Paragraph(str(week), body_style), Paragraph("Build Phase 1", body_style)],
        [Paragraph("Squat Aggregate Volume", body_style), Paragraph(f"{squat} kg", body_style), Paragraph("Progressive Overload", body_style)],
        [Paragraph("Deadlift Aggregate Volume", body_style), Paragraph(f"{deadlift} kg", body_style), Paragraph("Progressive Overload", body_style)],
        [Paragraph("Aerobic Road Mileage", body_style), Paragraph(f"{run} km", body_style), Paragraph("Aerobic Base Build", body_style)],
        [Paragraph("Resting Heart Rate", body_style), Paragraph(f"{hr} BPM", body_style), Paragraph("Recovery Zone (< 60)", body_style)],
        [Paragraph("Sleep Quality Metric", body_style), Paragraph(f"{sleep} / 10", body_style), Paragraph("Optimal Recovery (> 7)", body_style)]
    ]
    
    # Table Formatting
    metrics_table = Table(data, colWidths=[200, 150, 150])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F3F4F6')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB')),
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 15))
    
    # Coach Notes Layout
    story.append(Paragraph("📋 Performance Specialist Feedback & Insights", header_style))
    story.append(Paragraph(notes, body_style))
    
    # Build Document
    doc.build(story)

# --- Step 3: Analytical Data Display & Execution ---
st.markdown("---")
st.subheader("2. Operational Volume Breakdown")

col_view1, col_view2 = st.columns(2)
with col_view1:
    # Dynamic dataframe for bar charts
    metric_chart_data = pd.DataFrame({
        "Exercise Dimension": ["Squat Volume", "Deadlift Volume"],
        "Total Loaded Volume (kg)": [squat_vol, deadlift_vol]
    }).set_index("Exercise Dimension")
    st.bar_chart(metric_chart_data)

with col_view2:
    st.markdown("**Report Action Center**")
    pdf_filename = "data/performance_report.pdf"
    
    if st.button("Build Production PDF Report"):
        os.makedirs("data", exist_ok=True)
        generate_pdf_report(
            pdf_filename, client_name, week_num, squat_vol, 
            deadlift_vol, running_dist, avg_hr, sleep_score, coach_notes
        )
        st.success("✅ PDF Document built successfully inside data/ folder!")
        
        # Immediate download link
        with open(pdf_filename, "rb") as file:
            st.download_button(
                label="📥 Download Performance PDF Report",
                data=file,
                file_name=f"{client_name.lower().replace(' ', '_')}_report.pdf",
                mime="application/pdf"
            )
import streamlit as st
import pandas as pd
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Configure Page Layout
st.set_page_config(page_title="Running Performance Lab", layout="wide")
st.title("🏃‍♂️ Endurance Analytics & Running Performance Engine")
st.markdown("Log aerobic metrics, monitor cardiovascular recovery thresholds, track gear lifespans, and compile automated training reports.")

# --- Step 1: Runner Input Data Interface ---
st.subheader("1. Weekly Run Logging")
col_input1, col_input2, col_input3, col_input4 = st.columns(4)

with col_input1:
    client_name = st.text_input("Athlete Name", "Matthew Gousain")
    week_num = st.text_input("Training Block / Week", "Base Phase - Week 3")
with col_input2:
    weekly_dist = st.number_input("Total Distance (km)", min_value=0.0, value=45.0, step=0.5)
    avg_pace = st.text_input("Average Training Pace (min/km)", "5:15")
with col_input3:
    avg_hr = st.number_input("Average Resting HR (BPM)", min_value=0, value=50)
    avg_hrv = st.number_input("Average HRV (ms)", min_value=0, value=75, help="Heart Rate Variability - higher signals better recovery.")
with col_input4:
    shoe_mileage = st.number_input("Current Shoe Mileage (km)", min_value=0, value=280)
    coach_notes = st.text_area("Performance Specialist Insights", "Aerobic base capacity expanding nicely. Heart rate stabilized during the long slow distance (LSD) efforts. Monitor shoe wear over the next 50km to maintain optimal impact absorption.")

# --- Step 2: PDF Generation Logic ---
def generate_running_report(filename, name, week, dist, pace, hr, hrv, shoe, notes):
    """Generates a beautifully aligned running performance scorecard using ReportLab."""
    doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'BrandTitle', parent=styles['Heading1'], fontSize=22, textColor=colors.HexColor('#0F172A'), spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'BrandSubtitle', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#64748B'), spaceAfter=20
    )
    header_style = ParagraphStyle(
        'SectionHeader', parent=styles['Heading2'], fontSize=13, textColor=colors.HexColor('#1E293B'), spaceBefore=12, spaceAfter=8
    )
    body_style = ParagraphStyle(
        'BodyTextCustom', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#334155'), leading=14
    )

    # Document Headers
    story.append(Paragraph("MATTHEWS METHOD ENDURANCE LAB", title_style))
    story.append(Paragraph(f"Aerobic Metrics Scorecard • Compiled for {name}", subtitle_style))
    story.append(Spacer(1, 10))
    
    # Running Metrics Data Layout
    story.append(Paragraph("📊 Biometric & Telemetry Telemetry", header_style))
    
    # Shoe Status Alert Logic
    shoe_status = "Good Condition" if shoe < 400 else "⚠️ Nearing Retirement (400k+)"
    
    data = [
        [Paragraph("<b>Performance Indicator</b>", body_style), Paragraph("<b>Recorded Value</b>", body_style), Paragraph("<b>Target Focus</b>", body_style)],
        [Paragraph("Current Training Block", body_style), Paragraph(str(week), body_style), Paragraph("Aerobic Capacity Build", body_style)],
        [Paragraph("Total Weekly Distance", body_style), Paragraph(f"{dist} km", body_style), Paragraph("Volume Progression", body_style)],
        [Paragraph("Average Training Pace", body_style), Paragraph(f"{pace} /km", body_style), Paragraph("Aerobic Threshold Zone", body_style)],
        [Paragraph("Resting Heart Rate", body_style), Paragraph(f"{hr} BPM", body_style), Paragraph("Cardiovascular Efficiency (< 55)", body_style)],
        [Paragraph("Heart Rate Variability (HRV)", body_style), Paragraph(f"{hrv} ms", body_style), Paragraph("Parasympathetic Dominance (> 70)", body_style)],
        [Paragraph("Running Shoe Lifespan", body_style), Paragraph(f"{shoe} km", body_style), Paragraph(shoe_status, body_style)]
    ]
    
    metrics_table = Table(data, colWidths=[200, 140, 160])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F8FAFC')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 15))
    
    # Coach Feedback
    story.append(Paragraph("📋 Tactical Performance Feedback", header_style))
    story.append(Paragraph(notes, body_style))
    
    doc.build(story)

# --- Step 3: Analytics Layout ---
st.markdown("---")
st.subheader("2. Physiological & Gear Monitoring")

col_view1, col_view2 = st.columns(2)
with col_view1:
    st.markdown("**Shoe Wear & Replacement Warning Gauge**")
    # A cleaner gauge comparison bar for running gear lifespans (typically 500km retirement mark)
    shoe_df = pd.DataFrame({
        "Status": ["Current Mileage", "Remaining Lifespan"],
        "Kilometers (km)": [shoe_mileage, max(0, 500 - shoe_mileage)]
    }).set_index("Status")
    st.bar_chart(shoe_df)

with col_view2:
    st.markdown("**Report Automation Portal**")
    pdf_filename = "data/running_performance_report.pdf"
    
    if st.button("Generate Running PDF Scorecard"):
        os.makedirs("data", exist_ok=True)
        generate_running_report(
            pdf_filename, client_name, week_num, weekly_dist,
            avg_pace, avg_hr, avg_hrv, shoe_mileage, coach_notes
        )
        st.success("✅ Runner PDF Compiled Successfully!")
        
        with open(pdf_filename, "rb") as file:
            st.download_button(
                label="📥 Download Runner Performance Report",
                data=file,
                file_name=f"{client_name.lower().replace(' ', '_')}_running_report.pdf",
                mime="application/pdf"
            )
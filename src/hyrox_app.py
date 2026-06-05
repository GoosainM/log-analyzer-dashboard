import streamlit as st
import pandas as pd
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Configure Page Layout
st.set_page_config(page_title="Hyrox Performance Lab", layout="wide")
st.title("🏋️‍♂️ HYROX Performance Lab & Work Capacity Engine")
st.markdown("Log functional station times, monitor compromised running metrics, calculate target splits, and automate athlete preparation scorecards.")

# --- Step 1: Athlete Class Selector ---
st.sidebar.header("🏆 Competition Division")
division = st.sidebar.selectbox("Select Hyrox Division", ["Hyrox Open / Pro Men", "Hyrox Open / Pro Women", "Hyrox Doubles"])

# --- Step 2: Current Session Intake Interface ---
st.subheader("1. Weekly Time Trial & Biometric Intake")
col_input1, col_input2, col_input3, col_input4 = st.columns(4)

with col_input1:
    client_name = st.text_input("Athlete Name", "Matthew Gousain")
    week_num = st.text_input("Current Training Week", "Hyrox Prep - Week 4")
with col_input2:
    compromised_run = st.number_input("Avg Compromised 1km Run Pace (min/km)", min_value=2.0, value=4.45, step=0.01, help="Pace during running intervals spaced between heavy functional exercises.")
    sled_push_time = st.number_input("152kg/102kg Sled Push Time (seconds)", min_value=1, value=145, step=1)
with col_input3:
    burpee_bj_time = st.number_input("80m Burpee Broad Jump Time (seconds)", min_value=1, value=190, step=1)
    wall_ball_time = st.number_input("100x/75x Wall Balls Time (seconds)", min_value=1, value=240, step=1)
with col_input4:
    avg_hrv = st.number_input("Weekly Average HRV (ms)", min_value=0, value=78)
    sleep_score = st.slider("Average Sleep Quality (1-10)", 1, 10, 8)

# --- Step 3: Adaptive Progressive Target Logic ---
next_week_run_target = round(compromised_run * 0.98, 2)  # Target 2% speed increase
next_week_sled_target = round(sled_push_time * 0.97)     # Target 3% faster transition
next_week_burpee_target = round(burpee_bj_time * 0.97)   # Target 3% faster movement efficiency
next_week_wall_target = round(wall_ball_time * 0.96)     # Target 4% faster cadence

# --- Step 4: Automated Hyrox Performance Insights Engine ---
insights = []
if avg_hrv < 65:
    insights.append("⚠️ RECOVERY ALERT: Low HRV suggests high central nervous system (CNS) strain from combined heavy lifting and aerobic load. Consider reducing sled volume next week.")
else:
    insights.append("✅ CNS READINESS: Excellent HRV adaptation. System is handling the concurrent strength-endurance adaptations efficiently.")

if sleep_score < 7:
    insights.append("📉 RECOVERY FOOTPRINT: Sub-optimal sleep depths are delaying muscle tissue repair required for explosive wall ball and burpee outputs.")

if sled_push_time > 150:
    insights.append("⚡ STRENGTH BLOCK NEEDED: Sled push time indicates friction threshold limitations. Prioritize concentric leg drive and low-bar positioning.")
else:
    insights.append("🚀 EFFICIENCY CONFIRMED: Sled push times show great absolute force application under fatigue.")

if compromised_run > 5.00:
    insights.append("🏃‍♂️ AEROBIC LIMITATION: Running pace drops severely under compromised conditions. Dedicate 20% more volume to Zone 2 engine building.")

auto_coach_notes = " ".join(insights)
st.info(f"📋 **Automated Performance Specialist Insights:**\n\n{auto_coach_notes}")

# --- Step 5: PDF Generation Engine ---
def generate_hyrox_report(filename, name, week, div, c_run, n_run, c_sled, n_sled, c_bbj, n_bbj, c_wb, n_wb, hrv, notes):
    doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=22, textColor=colors.HexColor('#0F172A'), spaceAfter=4)
    subtitle_style = ParagraphStyle('Sub', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#475569'), spaceAfter=15)
    header_style = ParagraphStyle('Head', parent=styles['Heading2'], fontSize=12, textColor=colors.HexColor('#1E293B'), spaceBefore=12, spaceAfter=6)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#334155'), leading=14)

    story.append(Paragraph("MATTHEWS METHOD HYROX PERFORMANCE LAB", title_style))
    story.append(Paragraph(f"Competition Analytics Profile • Prepared for {name} ({div})", subtitle_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph(f"📈 **Current Cycle:** {week} | **Baseline HRV:** {hrv} ms", body_style))
    story.append(Spacer(1, 10))
    
    data = [
        [Paragraph("<b>Hyrox Testing Metric</b>", body_style), Paragraph("<b>Current Recorded (Time/Pace)</b>", body_style), Paragraph("<b>Next Week Target Goal</b>", body_style)],
        [Paragraph("Compromised 1km Run", body_style), Paragraph(f"{c_run:.2f} min/km", body_style), Paragraph(f"{n_run:.2f} min/km", body_style)],
        [Paragraph("Sled Push (4 x 12.5m)", body_style), Paragraph(f"{c_sled} sec", body_style), Paragraph(f"{n_sled} sec", body_style)],
        [Paragraph("Burpee Broad Jump (80m)", body_style), Paragraph(f"{c_bbj} sec", body_style), Paragraph(f"{n_bbj} sec", body_style)],
        [Paragraph("Wall Balls", body_style), Paragraph(f"{c_wb} sec", body_style), Paragraph(f"{n_wb} sec", body_style)]
    ]
    
    metrics_table = Table(data, colWidths=[200, 150, 150])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F8FAFC')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("📋 Automated Tactical Insights & Strategic Directives", header_style))
    story.append(Paragraph(notes, body_style))
    doc.build(story)

# --- Step 6: UI Visualizations ---
st.markdown("---")
st.subheader("2. Predictive Analytics Runway")

col_view1, col_view2 = st.columns(2)
with col_view1:
    st.markdown("**Station Time Comparison (Lower is Faster/Better)**")
    chart_data = pd.DataFrame({
        "Hyrox Station": ["Sled Push (s)", "Burpee BJ (s)", "Wall Balls (s)"],
        "Current Week": [sled_push_time, burpee_bj_time, wall_ball_time],
        "Next Week Target": [next_week_sled_target, next_week_burpee_target, next_week_wall_target]
    }).set_index("Hyrox Station")
    st.bar_chart(chart_data)

with col_view2:
    st.markdown("**Report Automation Portal**")
    pdf_filename = "data/hyrox_performance_report.pdf"
    
    if st.button("Generate Hyrox PDF Profile"):
        os.makedirs("data", exist_ok=True)
        generate_hyrox_report(
            pdf_filename, client_name, week_num, division, compromised_run, next_week_run_target,
            sled_push_time, next_week_sled_target, burpee_bj_time, next_week_burpee_target,
            wall_ball_time, next_week_wall_target, avg_hrv, auto_coach_notes
        )
        st.success("✅ Hyrox Blueprint Compiled Successfully!")
        
        with open(pdf_filename, "rb") as file:
            st.download_button(
                label="📥 Download Hyrox Performance Blueprint",
                data=file,
                file_name=f"{client_name.lower().replace(' ', '_')}_hyrox_plan.pdf",
                mime="application/pdf"
            )

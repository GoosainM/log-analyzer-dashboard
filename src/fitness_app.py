import streamlit as st
import pandas as pd
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Configure Page Layout
st.set_page_config(page_title="Running Performance Lab", layout="wide")
st.title("🏃‍♂️ Predictive Training Load & Performance Engine")
st.markdown("Log current weekly metrics, calculate adaptive progressive overload targets for next week, and auto-compile analytics sheets.")

# --- Step 1: Target Milestone Setup ---
st.sidebar.header("🎯 Athlete Milestone Goal")
goal_type = st.sidebar.selectbox("Select Target Milestone Type", ["Marathon (Distance Build)", "Pace Optimization (Speed Build)"])

if goal_type == "Marathon (Distance Build)":
    target_value = st.sidebar.number_input("Target Peak Weekly Distance (km)", min_value=1.0, value=70.0, step=1.0)
    unit = "km"
else:
    target_value = st.sidebar.number_input("Target Race Pace (min/km)", min_value=2.0, value=4.5, step=0.1)
    unit = "min/km"

# --- Step 2: Current Week Intake Interface ---
st.subheader("1. Current Week Metric Logging")
col_input1, col_input2, col_input3, col_input4 = st.columns(4)

with col_input1:
    client_name = st.text_input("Athlete Name", "Matthew Gousain")
    week_num = st.text_input("Current Week Label", "Week 3")
with col_input2:
    current_dist = st.number_input("Recorded Weekly Distance (km)", min_value=0.0, value=45.0, step=0.5)
    current_pace = st.number_input("Recorded Average Pace (min/km)", min_value=2.0, value=5.25, step=0.01, help="Enter as a decimal, e.g., 5.25 for 5:15/km")
with col_input3:
    avg_hr = st.number_input("Average Resting HR (BPM)", min_value=0, value=50)
    avg_hrv = st.number_input("Average HRV (ms)", min_value=0, value=75)
with col_input4:
    sleep_score = st.slider("Average Sleep Quality (1-10)", 1, 10, 8)

# --- Step 3: Adaptive Predictive Math Engine ---
# Calculate next week's targets based on safe progressive overload guidelines (e.g., 10% distance rule)
if goal_type == "Marathon (Distance Build)":
    next_week_dist_target = min(target_value, round(current_dist * 1.10, 1))
    next_week_pace_target = current_pace  # Hold pace steady during volume build
    progress_pct = min(100.0, (current_dist / target_value) * 100)
else:
    # Pace Optimization: gradually increase efficiency by targeting a 2% faster pace next week
    next_week_dist_target = current_dist
    next_week_pace_target = max(target_value, round(current_pace * 0.98, 2))
    progress_pct = min(100.0, (target_value / current_pace) * 100)

# --- Step 4: Automated Performance Specialist Insights Engine ---
# This eliminates manual entry by evaluating physiological stress vs performance outputs
insights = []
if avg_hrv < 60 or avg_hr > 55:
    insights.append("⚠️ BIOMETRIC ALERT: Parasympathetic suppression detected via elevated resting HR / compressed HRV. Autonomic recovery is compromised.")
else:
    insights.append("✅ CARDIOVASCULAR ADAPTATION: Stable resting HR and strong HRV show excellent recovery and high physiological readiness.")

if sleep_score < 7:
    insights.append("📉 SLEEP RECOVERY FOOTPRINT: Sub-optimal sleep depth is hindering tissue regeneration. Prioritize a 7+ target window next week.")
else:
    insights.append("🔋 RECOVERY FOOTPRINT: Solid sleep quality is facilitating efficient muscular and central nervous system repair.")

if goal_type == "Marathon (Distance Build)":
    if current_dist >= target_value:
        insights.append(f"🏆 MILESTONE REACHED: Peak target mileage achieved. Shift focus to structural maintenance and tapering protocols.")
    else:
        insights.append(f"📈 VOLUME PROGRESSION: Athlete is currently performing at {progress_pct:.1f}% of ultimate peak volume. Next week adapts safely via a regulated +10% capacity jump.")
else:
    if current_pace <= target_value:
        insights.append(f"🏆 MILESTONE REACHED: Velocity threshold achieved. Athlete is running at or faster than target race pace.")
    else:
        insights.append(f"⚡ VELOCITY ADAPTATION: Running at {progress_pct:.1f}% efficiency relative to target velocity. Next week initiates a progressive 2% pacing restriction to drive threshold adaptations.")

auto_coach_notes = " ".join(insights)

# Display Generated Insights Live on Dashboard
st.info(f"📋 **Automated Performance Specialist Insights:**\n\n{auto_coach_notes}")

# --- Step 5: PDF Generation Engine ---
def generate_adaptive_report(filename, name, week, c_dist, c_pace, n_dist, n_pace, hr, hrv, goal, pct, notes):
    doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=22, textColor=colors.HexColor('#1E293B'), spaceAfter=4)
    subtitle_style = ParagraphStyle('Sub', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#64748B'), spaceAfter=15)
    header_style = ParagraphStyle('Head', parent=styles['Heading2'], fontSize=12, textColor=colors.HexColor('#334155'), spaceBefore=12, spaceAfter=6)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#475569'), leading=14)

    story.append(Paragraph("MATTHEWS METHOD PERFORMANCE LAB", title_style))
    story.append(Paragraph(f"Adaptive Athletic Progress Report • Prepared for {name}", subtitle_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph(f"🏁 Active Milestone Profile: <b>{goal}</b> (Completion Status: {pct:.1f}%)", body_style))
    story.append(Spacer(1, 10))
    
    # Dynamic Data Table Layout
    story.append(Paragraph("📊 Training Matrix: Current Results vs Next Week Targets", header_style))
    data = [
        [Paragraph("<b>Metric Dimension</b>", body_style), Paragraph("<b>Current Week Recorded</b>", body_style), Paragraph("<b>Next Week Target Goal</b>", body_style)],
        [Paragraph("Training Cycle Phase", body_style), Paragraph(str(week), body_style), Paragraph("Next Sequential Block", body_style)],
        [Paragraph("Weekly Running Distance", body_style), Paragraph(f"{c_dist} km", body_style), Paragraph(f"{n_dist} km", body_style)],
        [Paragraph("Average Training Pace", body_style), Paragraph(f"{c_pace:.2f} min/km", body_style), Paragraph(f"{n_pace:.2f} min/km", body_style)],
        [Paragraph("Resting Heart Rate", body_style), Paragraph(f"{hr} BPM", body_style), Paragraph("Maintain / Reduce", body_style)],
        [Paragraph("Heart Rate Variability", body_style), Paragraph(f"{hrv} ms", body_style), Paragraph("Maximize Recovery Trend", body_style)]
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
    
    story.append(Paragraph("📋 Automated Tactical Insights & Directives", header_style))
    story.append(Paragraph(notes, body_style))
    
    doc.build(story)

# --- Step 6: UI Visualizations ---
st.markdown("---")
st.subheader("2. Predictive Analytics Runway")

col_view1, col_view2 = st.columns(2)
with col_view1:
    st.markdown("**Volume Comparison Grid (Current vs Next Week Targets)**")
    chart_data = pd.DataFrame({
        "Metrics": ["Distance (km)", "Target Pace (min/km)"],
        "Current Week": [current_dist, current_pace],
        "Next Week Target": [next_week_dist_target, next_week_pace_target]
    }).set_index("Metrics")
    st.bar_chart(chart_data)

with col_view2:
    st.markdown("**Report Automation Portal**")
    pdf_filename = "data/adaptive_performance_report.pdf"
    
    if st.button("Generate Adaptive Running PDF"):
        os.makedirs("data", exist_ok=True)
        generate_adaptive_report(
            pdf_filename, client_name, week_num, current_dist, current_pace,
            next_week_dist_target, next_week_pace_target, avg_hr, avg_hrv, goal_type, progress_pct, auto_coach_notes
        )
        st.success("✅ Adaptive PDF Compiled Successfully!")
        
        with open(pdf_filename, "rb") as file:
            st.download_button(
                label="📥 Download Tailored Training Report",
                data=file,
                file_name=f"{client_name.lower().replace(' ', '_')}_adaptive_plan.pdf",
                mime="application/pdf"
            )
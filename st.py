import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

st.set_page_config(page_title="KPI Dashboard", layout="wide", page_icon="📊")

st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    h1 { color: #1F4E79; font-size: 1.8rem; }
    h2 { color: #2E75B6; font-size: 1.2rem; margin-top: 2rem; }
    .section-divider { border-top: 2px solid #2E75B6; margin: 2rem 0 1rem 0; }
    .product-header {
        background: linear-gradient(90deg, #1F4E79, #2E75B6);
        color: white;
        padding: 0.5rem 1.2rem;
        border-radius: 8px;
        font-size: 1.1rem;
        font-weight: bold;
        margin: 2rem 0 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
raw = [
    ["Defect Rate","April","Rectangular Duct",2.33,1.77,2,1.95,2.41,2.36,2.55,1.83,2.13,1.78,2.2,0.5],
    ["Defect Rate","April","Circular Duct",1.75,2,1.57,1.73,2.13,2.04,1.75,2.08,2.28,1.56,2.0,0.5],
    ["Defect Rate","April","Diffuser",2.38,2.28,1.96,1.79,2.51,1.95,1.73,1.74,2.41,2.19,2.1,0.5],
    ["Defect Rate","April","Grille",2.18,2.11,1.93,2.33,1.79,1.95,2.2,2.01,2.23,1.97,1.9,0.5],
    ["Defect Rate","May","Rectangular Duct",2.38,1.79,1.96,2.01,1.82,1.96,1.84,2,2.32,2.08,2.2,0.5],
    ["Defect Rate","May","Circular Duct",1.88,1.74,1.79,2.39,2.13,2.1,1.7,2.21,1.7,1.89,2.0,0.5],
    ["Defect Rate","May","Diffuser",2.54,2.23,2.15,2.27,2.41,2.35,1.86,1.68,1.93,1.89,2.1,0.5],
    ["Defect Rate","May","Grille",1.64,2.3,2.24,1.73,2.04,1.81,2.27,1.86,1.69,1.67,1.9,0.5],
    ["Defect Rate","March","Rectangular Duct",2.26,1.99,2.28,2.56,2.11,1.95,2.65,2.21,1.83,1.79,2.2,0.5],
    ["Defect Rate","March","Circular Duct",1.65,2.11,2.26,1.93,1.61,1.89,2.45,2.03,2.42,2.32,2.0,0.5],
    ["Defect Rate","March","Diffuser",1.66,2.3,2.26,2.13,1.89,2.23,1.75,2.04,2.06,2.51,2.1,0.5],
    ["Defect Rate","March","Grille",2.24,1.69,1.9,1.61,2.27,2.23,1.72,2.03,2,1.59,1.9,0.5],
    ["Lead Time","April","Rectangular Duct",165.36,163.35,165.51,163.27,158.51,161.42,158.68,166.86,166.41,165.98,163,5],
    ["Lead Time","April","Circular Duct",169.23,165.63,177.44,178.44,166.03,171.8,165.8,175.75,175.83,166.65,172,8],
    ["Lead Time","April","Diffuser",66.87,67.27,65.73,69.01,66.58,65.44,67.21,68.24,65.39,65.98,67,3],
    ["Lead Time","April","Grille",74.57,72.08,70.55,71.13,68.27,69.02,69.83,71.64,69.06,68.99,71,4],
    ["Lead Time","May","Rectangular Duct",159.14,164.18,160.56,166.65,166.24,159.14,160.64,164.52,160.43,159.69,163,5],
    ["Lead Time","May","Circular Duct",178.27,173.02,171.61,176.1,176.43,167.54,166.2,171.01,170.9,171.53,172,8],
    ["Lead Time","May","Diffuser",68.24,67.94,69.61,64.83,66.47,66.13,68.95,65.64,65.33,66.72,67,3],
    ["Lead Time","May","Grille",70.44,69.41,69.2,74.05,70.59,73.6,71.36,67.76,74.59,73.42,71,4],
    ["Lead Time","March","Rectangular Duct",167.22,166.84,166.14,160,162.87,160.42,162.11,159.03,161.91,167.37,163,5],
    ["Lead Time","March","Circular Duct",168.62,176.09,171.35,170.89,178.59,179.13,172.8,175.15,167.03,169.07,172,8],
    ["Lead Time","March","Diffuser",69.53,67.43,67.23,68.34,64.61,67.45,67.02,68.9,65.15,69.49,67,3],
    ["Lead Time","March","Grille",67.98,68.74,71.68,72.26,69.09,68.26,73.81,69.17,71.68,71.86,71,4],
    ["Downtime","April","Rectangular Duct",7.56,8.45,8.12,10.35,6.4,9.17,6.59,7.44,8.93,6.92,8.0,3.0],
    ["Downtime","April","Circular Duct",4.34,5.91,3.46,4.85,6.79,6.79,3.46,3.97,4.15,6.56,5.0,2.0],
    ["Downtime","April","Diffuser",3.69,3.68,2.77,2.38,3.6,3.37,3.2,3.88,3.28,2.11,3.0,1.0],
    ["Downtime","April","Grille",3.57,2.64,3.29,3.79,2.34,2.31,2.29,3.1,2.59,3.19,3.0,1.0],
    ["Downtime","May","Rectangular Duct",9.18,6.4,8.72,6.73,7.94,10.19,9.87,5.8,7.59,6.79,8.0,3.0],
    ["Downtime","May","Circular Duct",3.21,5.98,5.49,4.14,5.87,5.19,4.74,3.23,3.47,6.38,5.0,2.0],
    ["Downtime","May","Diffuser",3.73,3.08,3.6,3.15,2.37,2.33,2.65,3.72,3.53,3.65,3.0,1.0],
    ["Downtime","May","Grille",3.72,2.48,2.55,2.29,3.5,3.69,2.83,3.22,2.38,3.77,3.0,1.0],
    ["Downtime","March","Rectangular Duct",9.97,10.57,9.68,10.06,5.43,9.28,7.09,10.33,9.63,9.97,8.0,3.0],
    ["Downtime","March","Circular Duct",6.12,4.16,6.03,3.59,6.34,6.29,4,6.14,4.86,4.3,5.0,2.0],
    ["Downtime","March","Diffuser",3.53,2.51,2.14,2.45,2.69,3.66,3.84,2.6,3.25,2.82,3.0,1.0],
    ["Downtime","March","Grille",3.87,3.07,3.79,2.31,3.85,2.42,3.83,2.58,2.3,2.88,3.0,1.0],
    ["OEE","April","Rectangular Duct",75.82,74.33,75.38,75.04,74.59,75.28,74.12,75.75,73.21,76.53,75,2],
    ["OEE","April","Circular Duct",75.14,75.79,75.87,75.61,74.51,73.45,75.59,74.39,74.33,76.25,75,2],
    ["OEE","April","Diffuser",75.79,74.28,74.31,74.67,74.65,74.26,73.66,74.71,76.59,75.64,75,2],
    ["OEE","April","Grille",76.45,75.42,74.28,75.17,73.2,74.23,74.75,75.29,75.56,74.87,75,2],
    ["OEE","May","Rectangular Duct",74.79,73.97,74.9,76.44,76.07,73.81,73.51,75.06,75.48,74.41,75,2],
    ["OEE","May","Circular Duct",76.15,75.9,75.62,74.01,73.92,73.29,74.08,74.91,76.26,73.46,75,2],
    ["OEE","May","Diffuser",74.69,75.47,73.9,75.71,74.98,74.08,75.56,73.22,75.9,75.97,75,2],
    ["OEE","May","Grille",73.58,74.73,73.83,76.65,75.06,73.38,74.1,76.25,74.84,76.09,75,2],
    ["OEE","March","Rectangular Duct",75.6,76.76,75.34,76.62,76.41,75.41,75.79,75.02,76.19,75.17,75,2],
    ["OEE","March","Circular Duct",76.43,75.88,74.91,74.13,74.09,75.5,75.96,75.08,75.46,74.19,75,2],
    ["OEE","March","Diffuser",73.48,74.23,74.18,74.35,75.14,73.7,74.03,75.7,75.74,73.43,75,2],
    ["OEE","March","Grille",74.67,75.15,74.7,73.94,74.71,76.46,75.3,75.7,76.28,75.96,75,2],
]

r_cols = [f"R{i}" for i in range(1,11)]
cols = ["KPI","Month","Product"] + r_cols + ["Center","Tolerance"]
df = pd.DataFrame(raw, columns=cols)
df["UCL"] = df["Center"] + df["Tolerance"]
df["LCL"] = df["Center"] - df["Tolerance"]
df["Avg"] = df[r_cols].mean(axis=1).round(3)
df["Min"] = df[r_cols].min(axis=1)
df["Max"] = df[r_cols].max(axis=1)

kpi_units    = {"Defect Rate": "%", "Lead Time": "sec", "Downtime": "%", "OEE": "%"}
kpi_colors   = {"Defect Rate": "#E53935", "Lead Time": "#1E88E5", "Downtime": "#FB8C00", "OEE": "#43A047"}
month_colors = { "March": "#1E88E5","April": "#43A047", "May": "#FB8C00"}
month_order  = [ "March","April", "May"]
products     = ["Rectangular Duct", "Circular Duct", "Diffuser", "Grille"]
kpis         = ["Defect Rate", "Lead Time", "Downtime", "OEE"]

# ── Header ────────────────────────────────────────────────────────────────────
st.title("Manufacturing KPI Dashboard")

st.markdown("""
<div style="margin-top:-10px; margin-bottom:20px; line-height:1.6;">
    <div style="font-size:22px; font-weight:600; color:#1F4E79;">
        Control KPIs Dashboard
    </div>
    <div style="font-size:18px; color:#444;">
        Khedr Trust Company
    </div>
    <div style="font-size:16px; color:#666;">
        Made by: Muhammed Zidan Abdallah
    </div>
</div>
""", unsafe_allow_html=True)

# ── Month Filter (top, inline) ─────────────────────────────────────────────
st.markdown("**Filter by Month:**")
fc1, fc2, fc3, _ = st.columns([1,1,1,5])

show_march = fc1.checkbox("March", value=True)
show_april = fc2.checkbox("April", value=True)
show_may   = fc3.checkbox("May", value=True)

sel_months = [m for m, v in zip(month_order, [show_march, show_april, show_may]) if v]
if not sel_months:
    sel_months = month_order

dff = df[df["Month"].isin(sel_months)]

st.markdown("---")

# ── Global KPI Cards (overall stable status) ──────────────────────────────────
st.markdown("### 🟢 Overall Process Status")
card_cols = st.columns(4)
for i, kpi in enumerate(kpis):
    sub = dff[dff["KPI"] == kpi]
    avg = sub["Avg"].mean()
    unit = kpi_units[kpi]
    center = sub["Center"].iloc[0]
    tol = sub["Tolerance"].iloc[0]
    within = (center - tol) <= avg <= (center + tol)
    with card_cols[i]:
        st.metric(
            label=f"{kpi}",
            value=f"{avg:.2f} {unit}",
            delta="✅ Stable" if within else "⚠️ Check",
        )

st.markdown("---")

# ── Per Product Section ────────────────────────────────────────────────────────
for product in products:
    st.markdown(f"<div class='product-header'>📦 {product}</div>", unsafe_allow_html=True)

    prod_df = dff[dff["Product"] == product]

    # ── 4 KPI Cards per product ───────────────────────────────────────────────
    pc = st.columns(4)
    for i, kpi in enumerate(kpis):
        sub = prod_df[prod_df["KPI"] == kpi]
        if sub.empty:
            continue
        avg = sub["Avg"].mean()
        ucl = sub["UCL"].iloc[0]
        lcl = sub["LCL"].iloc[0]
        unit = kpi_units[kpi]
        stable = lcl <= avg <= ucl
        with pc[i]:
            color = "#C8E6C9" if stable else "#FFCDD2"
            icon  = "✅" if stable else "⚠️"
            st.markdown(f"""
            <div style="background:{color};border-radius:8px;padding:0.6rem 1rem;text-align:center;margin-bottom:0.5rem;">
                <div style="font-size:0.75rem;color:#333;font-weight:600;">{kpi}</div>
                <div style="font-size:1.3rem;font-weight:bold;color:#1F4E79;">{avg:.2f} {unit}</div>
                <div style="font-size:0.75rem;color:#555;">Limit: {sub['Center'].iloc[0]} ± {sub['Tolerance'].iloc[0]}</div>
                <div style="font-size:0.8rem;">{icon} Stable</div>
            </div>""", unsafe_allow_html=True)

    # ── 4 Control Charts (one per KPI, lines = months) ───────────────────────
    fig = make_subplots(
        rows=1, cols=4,
        subplot_titles=kpis,
        shared_xaxes=False
    )

    for col_i, kpi in enumerate(kpis, 1):
        sub = prod_df[prod_df["KPI"] == kpi]
        ucl = sub["UCL"].iloc[0]
        lcl = sub["LCL"].iloc[0]
        center = sub["Center"].iloc[0]
        unit = kpi_units[kpi]

        # UCL / Center / LCL lines
        fig.add_trace(go.Scatter(
            x=list(range(1,11)), y=[ucl]*10,
            mode="lines", name="UCL" if col_i==1 else None,
            line=dict(color="red", dash="dash", width=1.2),
            showlegend=(col_i == 1), legendgroup="UCL"
        ), row=1, col=col_i)

        fig.add_trace(go.Scatter(
            x=list(range(1,11)), y=[center]*10,
            mode="lines", name="Center" if col_i==1 else None,
            line=dict(color="#388E3C", dash="dot", width=1.2),
            showlegend=(col_i == 1), legendgroup="Center"
        ), row=1, col=col_i)

        fig.add_trace(go.Scatter(
            x=list(range(1,11)), y=[lcl]*10,
            mode="lines", name="LCL" if col_i==1 else None,
            line=dict(color="red", dash="dash", width=1.2),
            showlegend=(col_i == 1), legendgroup="LCL"
        ), row=1, col=col_i)

        # One line per selected month
        for month in sel_months:
            row_data = sub[sub["Month"] == month]
            if row_data.empty:
                continue
            readings = [row_data.iloc[0][f"R{i}"] for i in range(1,11)]
            fig.add_trace(go.Scatter(
                x=list(range(1,11)),
                y=readings,
                mode="lines+markers",
                name=month if col_i==1 else None,
                line=dict(color=month_colors[month], width=2),
                marker=dict(size=6, color=month_colors[month]),
                showlegend=(col_i == 1),
                legendgroup=month
            ), row=1, col=col_i)

        fig.update_xaxes(title_text="Reading #", dtick=2, row=1, col=col_i)
        fig.update_yaxes(title_text=unit if col_i==1 else "", row=1, col=col_i)

    fig.update_layout(
        height=320,
        margin=dict(t=40, b=30, l=40, r=20),
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend=dict(orientation="h", y=-0.25, x=0),
        font=dict(size=11)
    )
    for i in range(1, 5):
        fig.update_xaxes(showgrid=True, gridcolor="#eee", row=1, col=i)
        fig.update_yaxes(showgrid=True, gridcolor="#eee", row=1, col=i)

    st.plotly_chart(fig, use_container_width=True)

    # ── Box Plot per product — 4 subplots each with its own scale ─────────────
    box_fig = make_subplots(
        rows=1, cols=4,
        subplot_titles=kpis,
        shared_yaxes=False
    )

    legend_added = set()
    for col_i, kpi in enumerate(kpis, 1):
        sub = prod_df[prod_df["KPI"] == kpi]
        if sub.empty:
            continue
        ucl    = sub["UCL"].iloc[0]
        lcl    = sub["LCL"].iloc[0]
        center = sub["Center"].iloc[0]
        unit   = kpi_units[kpi]

        for month in sel_months:
            m_row = sub[sub["Month"] == month]
            if m_row.empty:
                continue
            values = [m_row.iloc[0][rc] for rc in r_cols]
            show_leg = month not in legend_added
            box_fig.add_trace(go.Box(
                y=values,
                name=month,
                marker_color=month_colors[month],
                line_color=month_colors[month],
                boxpoints="all",
                jitter=0.3,
                pointpos=0,
                width=0.8,
                showlegend=show_leg,
                legendgroup=month,
            ), row=1, col=col_i)
            legend_added.add(month)

        # UCL / Center / LCL as horizontal lines using shapes per subplot axis
        # Use dummy scatter traces for limit lines (one x trick)
        x_cats = sel_months
        box_fig.add_trace(go.Scatter(
            x=x_cats, y=[ucl]*len(x_cats),
            mode="lines", line=dict(color="red", dash="dash", width=1.2),
            name="UCL", showlegend=(col_i == 1), legendgroup="UCL"
        ), row=1, col=col_i)
        box_fig.add_trace(go.Scatter(
            x=x_cats, y=[center]*len(x_cats),
            mode="lines", line=dict(color="#388E3C", dash="dot", width=1.2),
            name="Center", showlegend=(col_i == 1), legendgroup="Center"
        ), row=1, col=col_i)
        box_fig.add_trace(go.Scatter(
            x=x_cats, y=[lcl]*len(x_cats),
            mode="lines", line=dict(color="red", dash="dash", width=1.2),
            name="LCL", showlegend=(col_i == 1), legendgroup="LCL"
        ), row=1, col=col_i)

        box_fig.update_yaxes(title_text=unit if col_i == 1 else "", row=1, col=col_i,
                              showgrid=True, gridcolor="#eee")
        box_fig.update_xaxes(showgrid=False, row=1, col=col_i)

    box_fig.update_layout(
        height=350,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(t=40, b=30, l=40, r=20),
        legend=dict(orientation="h", y=-0.2, x=0),
        font=dict(size=11),
        boxmode="group"
    )
    st.plotly_chart(box_fig, use_container_width=True)

    st.markdown("<hr style='border:1px solid #ddd;margin:1.5rem 0;'>", unsafe_allow_html=True)

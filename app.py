import math
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="PlastiNoxa | Silverton rLDPE Infrastructure & Commercial Model",
    page_icon="♻️",
    layout="wide",
)

st.markdown(
    """
    <style>
    .status-badge {
        padding: 12px 18px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1.02rem;
        margin-bottom: 14px;
        display: block;
    }
    .story-box {
        background-color: #eff6ff;
        border-left: 5px solid #2563eb;
        padding: 14px 18px;
        border-radius: 6px;
        margin-bottom: 16px;
        color: #1e293b;
        font-size: 0.98rem;
    }
    .innovation-card {
        background-color: #f8fafc;
        border-left: 5px solid #0f766e;
        padding: 15px;
        border-radius: 6px;
        margin-bottom: 12px;
        color: #1e293b;
    }
    .commercial-card {
        background-color: #f0fdf4;
        border-left: 5px solid #15803d;
        padding: 15px;
        border-radius: 6px;
        margin-bottom: 12px;
        color: #1e293b;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# SESSION STATE INITIALIZATION (FOR ONE-CLICK OPTIMAL PRESET BUTTONS)
# -----------------------------------------------------------------------------
if "fiberglass_pct" not in st.session_state:
    st.session_state.fiberglass_pct = 12
if "cover_rib_depth_mm" not in st.session_state:
    st.session_state.cover_rib_depth_mm = 55
if "contracted_units_yr" not in st.session_state:
    st.session_state.contracted_units_yr = 1500
if "loi_units_yr" not in st.session_state:
    st.session_state.loi_units_yr = 900
if "monthly_fixed_opex_zar" not in st.session_state:
    st.session_state.monthly_fixed_opex_zar = 85000
if "plant_capex_zar" not in st.session_state:
    st.session_state.plant_capex_zar = 650000

# -----------------------------------------------------------------------------
# HEADER
# -----------------------------------------------------------------------------
st.title("♻️ PlastiNoxa: Code 4 rLDPE Composite Manhole & Drain Cover Simulator")
st.markdown(
    "**Silverton (East Pretoria) Manufacturing Hub | SANS 1882 Engineering, 3-Tier Pricing (Excl. VAT) & Gauteng 3-Metro Commercial Model**"
)

# 3 Clean, Uncluttered Story Tabs
tab1, tab2, tab3 = st.tabs(
    [
        "🛠️ Tab 1: Product Engineering & 3-Tier Pricing",
        "🎯 Tab 2: Market Opportunity (TAM/SAM/SOM) & Customers",
        "🏭 Tab 3: Silverton Plant Break-Even, Payback Months & ESG Impact",
    ]
)

# =============================================================================
# TAB 1: PRODUCT ENGINEERING & 3-TIER PRICING (EXCL. 15% VAT)
# =============================================================================
with tab1:
    st.subheader("1. Material Formulation, SANS 1882 Load Class & 3-Tier Pricing Ladder (Excl. 15% VAT)")

    # One-Click Guided Preset Buttons so the user knows exact optimal combinations
    st.markdown("**💡 Quick-Select Engineering Presets (Click to auto-set sliders):**")
    p_btn1, p_btn2, p_btn3 = st.columns(3)
    with p_btn1:
        if st.button("🚶 Light Duty Preset (Pedestrian / Parks - 7 kN+)", use_container_width=True):
            st.session_state.fiberglass_pct = 4
            st.session_state.cover_rib_depth_mm = 35
    with p_btn2:
        if st.button("⭐ Optimal Medium Duty (Default: Driveways & Taxis - 40 kN+)", use_container_width=True):
            st.session_state.fiberglass_pct = 12
            st.session_state.cover_rib_depth_mm = 55
    with p_btn3:
        if st.button("🚛 Heavy Curbside / Roadway Preset (Trucks - 125 kN+)", use_container_width=True):
            st.session_state.fiberglass_pct = 18
            st.session_state.cover_rib_depth_mm = 70

    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([1.4, 1.3, 1.3])

    with ctrl_col1:
        product_type = st.selectbox(
            "Select Chosen Product Format",
            options=[
                "600x600mm Manhole Cover & Frame (Standard Utility)",
                "550x550mm Roadside Stormwater Grate & Frame",
            ],
            index=0,
        )

    with ctrl_col2:
        fiberglass_pct = st.slider(
            "Glass Fiber Reinforcement (%) [Optimal: 12%–18%]",
            min_value=0,
            max_value=25,
            key="fiberglass_pct",
            step=1,
            help="Increases tensile & bending strength. 12% is optimal for Medium Duty; 18% for Heavy Roadway.",
        )

    with ctrl_col3:
        cover_rib_depth_mm = st.slider(
            "Waffle-Rib Cover Thickness (mm) [Optimal: 55mm–70mm]",
            min_value=30,
            max_value=85,
            key="cover_rib_depth_mm",
            step=5,
            help="Bending stiffness scales with the cube of thickness. 55mm is optimal for weight vs strength.",
        )

    rldpe_pct = 32
    mape_carbon_pct = 3
    sand_flyash_pct = 100 - rldpe_pct - mape_carbon_pct - fiberglass_pct

    # Product format multiplier (Stormwater grate frame is slightly heavier than standard manhole cover)
    is_stormwater = "Stormwater" in product_type
    base_weight_offset = 17.5 if is_stormwater else 14.0
    hardware_additive_cost = 275.0 if is_stormwater else 240.0

    # Governing Engineering & 3-Tier Pricing Equations (Fixed so default 600x600 = R424, R1,102, R1,488!)
    unit_weight_kg = round(
        base_weight_offset + (cover_rib_depth_mm * 0.28) - (fiberglass_pct * 0.08), 1
    )
    ldpe_waste_used_kg = round(unit_weight_kg * (rldpe_pct / 100.0), 1)
    plastic_bags_diverted = int(round(ldpe_waste_used_kg * 150, 0))

    load_capacity_kn = round(
        (12 + (fiberglass_pct * 4.2)) * ((cover_rib_depth_mm / 40.0) ** 1.8), 1
    )

    # Full Manufacturing Cost (Excl. VAT): Raw rLDPE + Sand/Ash + Fiberglass + R240 (MAPE/Carbon/Lock/Hinge) + R115 (Power/Labor)
    raw_materials_cost = (
        (unit_weight_kg * 0.32 * 3.8)
        + (unit_weight_kg * (0.68 - fiberglass_pct / 100.0) * 0.35)
        + (unit_weight_kg * (fiberglass_pct / 100.0) * 8.5)
    )
    production_cost_zar = round(raw_materials_cost + hardware_additive_cost + 115.0, 0)

    # Tier 2: Direct Hub B2B Wholesale Price (Selling directly from Silverton Hub, Excl. VAT)
    wholesale_price_zar = round(production_cost_zar * 2.6, 0)
    # Tier 3: Hardware Store Retail RRP (+35% Retailer Markup, Excl. VAT)
    retail_rrp_zar = round(wholesale_price_zar * 1.35, 0)

    unit_profit_zar = wholesale_price_zar - production_cost_zar
    gross_margin_pct = round((unit_profit_zar / wholesale_price_zar) * 100, 1)

    # Verified 2026 South African Competitor Prices (Strictly Excl. 15% VAT from Plumblink & Harscan)
    if not is_stormwater:
        benchmarks = {
            "Virgin Polymer Concrete (DMC)": {
                "load_kn": 65.0,
                "weight_kg": 34.0,
                "cost_zar": 780.0,
                "wholesale_zar": 1250.0,
                "retail_zar": 1620.0,  # Plumblink Masco B125 ~R1,863 Incl VAT = R1,620 Excl VAT
            },
            "Cast Iron (SANS 1882 / 558)": {
                "load_kn": 135.0,
                "weight_kg": 82.0,
                "cost_zar": 2550.0,
                "wholesale_zar": 3330.0,
                "retail_zar": 4160.0,  # Harscan 600x600 82kg 9B CI: R4,783.90 Incl VAT = R4,160 Excl VAT
            },
        }
    else:
        benchmarks = {
            "Virgin Polymer Concrete (DMC)": {
                "load_kn": 90.0,
                "weight_kg": 42.0,
                "cost_zar": 1150.0,
                "wholesale_zar": 1820.0,
                "retail_zar": 2350.0,
            },
            "Cast Iron (SANS 1882 / 558)": {
                "load_kn": 180.0,
                "weight_kg": 114.0,
                "cost_zar": 4150.0,
                "wholesale_zar": 5440.0,
                "retail_zar": 6799.0,  # Harscan 550x550 114kg Grate: R7,819.02 Incl VAT = R6,799 Excl VAT
            },
        }

    cast_iron_weight = benchmarks["Cast Iron (SANS 1882 / 558)"]["weight_kg"]
    cast_iron_retail = benchmarks["Cast Iron (SANS 1882 / 558)"]["retail_zar"]
    polymer_retail = benchmarks["Virgin Polymer Concrete (DMC)"]["retail_zar"]
    weight_saved_pct = round(
        ((cast_iron_weight - unit_weight_kg) / cast_iron_weight) * 100, 1
    )
    savings_vs_cast_iron = int(cast_iron_retail - wholesale_price_zar)
    savings_vs_polymer = int(polymer_retail - wholesale_price_zar)

    if load_capacity_kn >= 125:
        sans_class = "✅ PASSES SANS 1882 HEAVY CURBSIDE / ROADWAY (≥ 125 kN) — Suitable for Municipal Main Roads & Truck Yards"
        badge_bg, badge_color = "#dcfce7", "#166534"
    elif load_capacity_kn >= 40:
        sans_class = "✅ PASSES SANS 1882 MEDIUM DUTY (≥ 40 kN) — Suitable for Mamelodi Taxi Corridors, Estates & Commercial Driveways"
        badge_bg, badge_color = "#dbeafe", "#1e40af"
    elif load_capacity_kn >= 7:
        sans_class = "⚠️ PASSES SANS 1882 LIGHT DUTY ONLY (≥ 7 kN) — Suitable Only for Pedestrian Walkways, Parks & Meter Boxes"
        badge_bg, badge_color = "#fef9c3", "#854d0e"
    else:
        sans_class = "❌ BELOW SANS 1882 MINIMUM THRESHOLD (< 7 kN) — Increase Fiberglass % or Rib Thickness"
        badge_bg, badge_color = "#fee2e2", "#991b1b"

    st.markdown(
        f'<div class="status-badge" style="background-color:{badge_bg}; color:{badge_color};">'
        f"{sans_class} <br>Engineered Load: {load_capacity_kn} kN | Active Recipe: {rldpe_pct}% Code 4 rLDPE, "
        f"{sand_flyash_pct}% Silica Sand/Fly Ash, {fiberglass_pct}% Glass Fiber, {mape_carbon_pct}% MAPE/Carbon"
        f"</div>",
        unsafe_allow_html=True,
    )

    # 4 Clean, Wide KPI Columns (No cut-off text!)
    k1, k2, k3, k4 = st.columns(4)
    k1.metric(
        "1. Factory Production Cost (Excl. VAT)",
        f"R{int(production_cost_zar):,} / unit",
        delta=f"Weight: {unit_weight_kg} kg (-{weight_saved_pct}% vs Iron)",
    )
    k2.metric(
        "2. Direct Hub Price (B2B Excl. VAT)",
        f"R{int(wholesale_price_zar):,} / unit",
        delta=f"R{int(unit_profit_zar):,} profit/unit ({gross_margin_pct}% margin)",
    )
    k3.metric(
        "3. Hardware Retail RRP (Excl. VAT)",
        f"R{int(retail_rrp_zar):,} / unit",
        delta=f"Saves R{savings_vs_cast_iron:,} vs Cast Iron RRP",
    )
    k4.metric(
        "Code 4 rLDPE Diverted per Cover",
        f"{ldpe_waste_used_kg} kg / unit",
        delta=f"Equals ~{plastic_bags_diverted:,} plastic bags",
    )

    # Plain-English Live Story Box for Tab 1
    st.markdown(
        f'<div class="story-box">'
        f"<b>📖 How to Read Tab 1:</b> At <b>{fiberglass_pct}% fiberglass</b> and a <b>{cover_rib_depth_mm} mm waffle-rib depth</b>, "
        f"one unit weighs <b>{unit_weight_kg} kg</b> and holds <b>{load_capacity_kn} kN</b>. It costs <b>R{int(production_cost_zar):,}</b> "
        f"to manufacture in Silverton. When sold directly from our Silverton hub (bypassing hardware stores) at <b>R{int(wholesale_price_zar):,} (Excl. VAT)</b>, "
        f"we earn <b>R{int(unit_profit_zar):,} profit per cover</b> while still undercutting Virgin Polymer Concrete retail (R{int(polymer_retail):,}) "
        f"by <b>R{savings_vs_polymer:,}</b> and Cast Iron retail (R{int(cast_iron_retail):,}) by <b>R{savings_vs_cast_iron:,}</b>."
        f"</div>",
        unsafe_allow_html=True,
    )

    df_comp = pd.DataFrame(
        [
            {
                "Material": "PlastiNoxa rLDPE Composite",
                "1. Factory Production Cost (Excl. VAT)": production_cost_zar,
                "2. Direct Hub B2B Price (Excl. VAT)": wholesale_price_zar,
                "3. Hardware Store RRP (Excl. VAT)": retail_rrp_zar,
                "Load Capacity (kN)": load_capacity_kn,
                "Unit Weight (kg)": unit_weight_kg,
            },
            {
                "Material": "Virgin Polymer Concrete (DMC)",
                "1. Factory Production Cost (Excl. VAT)": benchmarks["Virgin Polymer Concrete (DMC)"]["cost_zar"],
                "2. Direct Hub B2B Price (Excl. VAT)": benchmarks["Virgin Polymer Concrete (DMC)"]["wholesale_zar"],
                "3. Hardware Store RRP (Excl. VAT)": benchmarks["Virgin Polymer Concrete (DMC)"]["retail_zar"],
                "Load Capacity (kN)": benchmarks["Virgin Polymer Concrete (DMC)"]["load_kn"],
                "Unit Weight (kg)": benchmarks["Virgin Polymer Concrete (DMC)"]["weight_kg"],
            },
            {
                "Material": "Cast Iron (SANS 1882 / 558)",
                "1. Factory Production Cost (Excl. VAT)": benchmarks["Cast Iron (SANS 1882 / 558)"]["cost_zar"],
                "2. Direct Hub B2B Price (Excl. VAT)": benchmarks["Cast Iron (SANS 1882 / 558)"]["wholesale_zar"],
                "3. Hardware Store RRP (Excl. VAT)": benchmarks["Cast Iron (SANS 1882 / 558)"]["retail_zar"],
                "Load Capacity (kN)": benchmarks["Cast Iron (SANS 1882 / 558)"]["load_kn"],
                "Unit Weight (kg)": benchmarks["Cast Iron (SANS 1882 / 558)"]["weight_kg"],
            },
        ]
    )

    c_left, c_right = st.columns(2)

    with c_left:
        fig_cost = go.Figure()
        fig_cost.add_trace(
            go.Bar(
                name="1. Production Cost (Excl. VAT)",
                x=df_comp["Material"],
                y=df_comp["1. Factory Production Cost (Excl. VAT)"],
                marker_color="#0f766e",
                text=df_comp["1. Factory Production Cost (Excl. VAT)"].apply(lambda x: f"R{int(x):,}"),
                textposition="auto",
            )
        )
        fig_cost.add_trace(
            go.Bar(
                name="2. Direct Hub B2B Price (Excl. VAT)",
                x=df_comp["Material"],
                y=df_comp["2. Direct Hub B2B Price (Excl. VAT)"],
                marker_color="#14b8a6",
                text=df_comp["2. Direct Hub B2B Price (Excl. VAT)"].apply(lambda x: f"R{int(x):,}"),
                textposition="auto",
            )
        )
        fig_cost.add_trace(
            go.Bar(
                name="3. Hardware Store RRP (Excl. VAT)",
                x=df_comp["Material"],
                y=df_comp["3. Hardware Store RRP (Excl. VAT)"],
                marker_color="#f59e0b",
                text=df_comp["3. Hardware Store RRP (Excl. VAT)"].apply(lambda x: f"R{int(x):,}"),
                textposition="auto",
            )
        )
        fig_cost.update_layout(
            title="3-Tier Pricing Ladder (All Values ZAR Excl. 15% VAT)",
            barmode="group",
            yaxis_title="ZAR (Excl. 15% VAT)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            height=400,
        )
        st.plotly_chart(fig_cost, use_container_width=True)

    with c_right:
        fig_load = go.Figure()
        fig_load.add_trace(
            go.Bar(
                name="Load Capacity (kN)",
                x=df_comp["Material"],
                y=df_comp["Load Capacity (kN)"],
                marker_color="#2563eb",
                text=df_comp["Load Capacity (kN)"].apply(lambda x: f"{x} kN"),
                textposition="auto",
            )
        )
        fig_load.add_trace(
            go.Bar(
                name="Total Unit Weight (kg)",
                x=df_comp["Material"],
                y=df_comp["Unit Weight (kg)"],
                marker_color="#64748b",
                text=df_comp["Unit Weight (kg)"].apply(lambda x: f"{x} kg"),
                textposition="auto",
            )
        )
        fig_load.add_hline(
            y=7,
            line_dash="dot",
            line_color="#ca8a04",
            annotation_text="SANS 1882 Light Duty (7 kN)",
        )
        fig_load.add_hline(
            y=40,
            line_dash="dash",
            line_color="#1e40af",
            annotation_text="SANS 1882 Medium Duty (40 kN)",
        )
        fig_load.add_hline(
            y=125,
            line_dash="solid",
            line_color="#dc2626",
            annotation_text="SANS 1882 Heavy Curbside (125 kN)",
        )
        fig_load.update_layout(
            title="Load Capacity (kN) & Weight (kg) vs. SANS 1882 Thresholds",
            barmode="group",
            yaxis_title="kN / kg",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            height=400,
        )
        st.plotly_chart(fig_load, use_container_width=True)

    st.divider()
    st.subheader("🏆 Core Structural & Anti-Theft Engineering Innovations")
    col_i1, col_i2, col_i3 = st.columns(3)
    with col_i1:
        st.markdown(
            """
            <div class="innovation-card">
            <h4>1. Hexagonal Under-Ribbing (Waffle Base)</h4>
            <p>Bending stiffness increases with the <b>cube of thickness</b> (I = bh³/12). A 20 mm solid top plate over 55–75 mm hexagonal ribs cuts weight by 30% while doubling load capacity.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_i2:
        st.markdown(
            """
            <div class="innovation-card">
            <h4>2. Captive Hinge + Non-Metallic Cam Lock</h4>
            <p>Stops both cover theft and underground copper cable theft using an integral polymer hinge and recessed nylon/fiberglass pentagon-key cam lock.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_i3:
        st.markdown(
            f"""
            <div class="innovation-card">
            <h4>3. Color-Coded Utility Inserts & Embossing</h4>
            <p>Permanent pigmented inserts (Blue = Water, Yellow = Fiber, Red = Eskom) plus embossed tread: "MADE FROM {plastic_bags_diverted:,} RECYCLED PLASTIC BAGS".</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# =============================================================================
# TAB 2: COMMERCIAL MARKET OPPORTUNITY (TAM / SAM / SOM) & CUSTOMER PIPELINE
# =============================================================================
with tab2:
    st.subheader("2. Commercial Opportunity (SA / 3 Gauteng Metros / Silverton SOM) & Customer Pipeline")

    s_col1, s_col2 = st.columns(2)
    with s_col1:
        contracted_units_yr = st.slider(
            "1. Contracted Township & Local Civil Projects (Units / Year) [Target: 1,500]",
            min_value=300,
            max_value=3600,
            key="contracted_units_yr",
            step=100,
            help="Target: 2 contracted Mamelodi taxi-rank/corridor drainage & Silverton civil projects (1,500 units/yr).",
        )
    with s_col2:
        loi_units_yr = st.slider(
            "2. Secured LOI Pipeline — Estates & Industrial Parks (Units / Year) [Target: 900]",
            min_value=200,
            max_value=3000,
            key="loi_units_yr",
            step=100,
            help="Target: 3 Letters of Intent from Pretoria East security estates & Silverton industrial parks (900 units/yr).",
        )

    annual_som_units = contracted_units_yr + loi_units_yr
    monthly_units_sold = round(annual_som_units / 12.0, 1)

    contracted_revenue_zar = contracted_units_yr * wholesale_price_zar
    loi_revenue_zar = loi_units_yr * wholesale_price_zar
    annual_som_revenue_zar = annual_som_units * wholesale_price_zar
    gauteng_sam_share_pct = round((annual_som_revenue_zar / 740_000_000) * 100, 2)

    # 4 Clean Market KPI Cards
    m_k1, m_k2, m_k3, m_k4 = st.columns(4)
    m_k1.metric(
        "South Africa TAM (Excl. VAT)",
        "R1.85 Billion / yr",
        delta="All 257 SA Municipalities & Civils",
    )
    m_k2.metric(
        "3 Gauteng Metros SAM (Excl. VAT)",
        "R740 Million / yr",
        delta="Tshwane, Joburg & Ekurhuleni (40% of SA)",
    )
    m_k3.metric(
        "Silverton Year-1 SOM (Excl. VAT)",
        f"R{annual_som_revenue_zar / 1_000_000:.2f} Million / yr",
        delta=f"Only {gauteng_sam_share_pct}% of Gauteng SAM",
    )
    m_k4.metric(
        "Total Year-1 Unit Pipeline",
        f"{annual_som_units:,} units / yr",
        delta=f"{int(monthly_units_sold)} units/month average",
    )

    st.markdown(
        f'<div class="story-box">'
        f"<b>📖 How to Read Tab 2:</b> Based at our <b>Silverton (East Pretoria) hub</b>, we are targeting "
        f"<b>{contracted_units_yr:,} units/yr</b> (R{contracted_revenue_zar / 1_000_000:.2f}M) from 2 local Mamelodi/Silverton civil & taxi-corridor upgrades, plus "
        f"<b>{loi_units_yr:,} units/yr</b> (R{loi_revenue_zar / 1_000_000:.2f}M) from 3 Letters of Intent with Pretoria East security estates and Silverton industrial parks. "
        f"This gives a Year-1 SOM of <b>R{annual_som_revenue_zar / 1_000_000:.2f} Million (Excl. VAT)</b>."
        f"</div>",
        unsafe_allow_html=True,
    )

    left_col, right_col = st.columns([1.35, 1.0])

    with left_col:
        st.markdown("#### 🎯 Target Addressable Market Table (All Values Excl. 15% VAT)")
        df_tam = pd.DataFrame(
            [
                {
                    "Market Tier": "TAM (Total Addressable Market)",
                    "Annual Value (Excl. VAT)": "R1.85 Billion",
                    "Scope & Verified Market Basis": (
                        "Total South African annual Rand value market for municipal & civil manhole covers, "
                        "roadside stormwater grates, and utility vaults (SANS 1882 / SANS 558 replacement demand)."
                    ),
                },
                {
                    "Market Tier": "SAM (Serviceable Available Market)",
                    "Annual Value (Excl. VAT)": "R740 Million",
                    "Scope & Verified Market Basis": (
                        "All 3 Gauteng Metros (City of Tshwane, City of Johannesburg, and City of Ekurhuleni) "
                        "provincial/municipal road & stormwater tenders and 10%–30% green-procurement projects."
                    ),
                },
                {
                    "Market Tier": "SOM (Silverton Year-1 Target)",
                    "Annual Value (Excl. VAT)": f"R{annual_som_revenue_zar / 1_000_000:.2f} Million",
                    "Scope & Verified Market Basis": (
                        f"2 contracted Mamelodi taxi associations / township civil drainage upgrades "
                        f"({contracted_units_yr:,} units = R{contracted_revenue_zar / 1_000_000:.2f}M Excl. VAT) "
                        f"+ 3 Pretoria East security estate & Silverton industrial park Letters of Intent "
                        f"({loi_units_yr:,} units = R{loi_revenue_zar / 1_000_000:.2f}M Excl. VAT)."
                    ),
                },
            ]
        )
        st.table(df_tam)

    with right_col:
        st.markdown("#### 🤝 Customer Profile, Pain Relieved & Validation Status")
        st.markdown(
            f"""
            <div class="commercial-card">
            <b>🎯 Target Customer (Silverton / East Pretoria Hub):</b><br>
            Civil engineering contractors, Mamelodi taxi-rank upgrade contractors, Pretoria East security estates, and municipal depot officers across the 3 Gauteng Metros under 10%–30% green procurement quotas.
            </div>
            <div class="commercial-card">
            <b>💊 Pain Relieved:</b><br>
            • <b>Eliminates Handover Penalties from Cast-Iron Theft:</b> Contractors lose retention money when R{int(cast_iron_retail):,} (Excl. VAT) cast-iron grates are stolen before site sign-off. Our R{int(wholesale_price_zar):,} Direct Hub cover (R{int(retail_rrp_zar):,} Hardware RRP) has zero scrap value and locks shut.<br>
            • <b>Zero Cracking Under Heavy Taxi Wheel Torque:</b> Concrete and virgin polymer lids crack under Mamelodi taxi rank axle turning loads; our rLDPE + {fiberglass_pct}% fiberglass composite absorbs heavy shock.
            </div>
            <div class="commercial-card">
            <b>✅ Validation Status:</b><br>
            Commercial pipeline of <b>{annual_som_units:,} units/year</b> ({contracted_units_yr:,} units via 2 Mamelodi/Silverton civil & taxi-corridor contracts + {loi_units_yr:,} units via 3 Pretoria East estate & Silverton industrial park LOIs).
            </div>
            """,
            unsafe_allow_html=True,
        )

# =============================================================================
# TAB 3: SILVERTON PLANT BREAK-EVEN, PAYBACK MONTHS & ESG IMPACT
# =============================================================================
with tab3:
    st.subheader("3. Silverton Factory Break-Even Volume, Months to Pay Back CAPEX & Environmental Impact")

    st.markdown("**💡 Quick-Select Factory Setup Presets (Click to auto-set OPEX & CAPEX sliders):**")
    f_btn1, f_btn2, f_btn3 = st.columns(3)
    with f_btn1:
        if st.button("🏠 Lean Shared Workshop (R55k/mo OPEX | R450k CAPEX)", use_container_width=True):
            st.session_state.monthly_fixed_opex_zar = 55000
            st.session_state.plant_capex_zar = 450000
    with f_btn2:
        if st.button("⭐ Standard Silverton Hub (Default: R85k/mo OPEX | R650k CAPEX)", use_container_width=True):
            st.session_state.monthly_fixed_opex_zar = 85000
            st.session_state.plant_capex_zar = 650000
    with f_btn3:
        if st.button("🏭 Scaled 2-Mold Factory (R130k/mo OPEX | R1.1M CAPEX)", use_container_width=True):
            st.session_state.monthly_fixed_opex_zar = 130000
            st.session_state.plant_capex_zar = 1100000

    f_col1, f_col2 = st.columns(2)
    with f_col1:
        monthly_fixed_opex_zar = st.slider(
            "Silverton Monthly Fixed OPEX — Rent, 4 Staff & 3-Phase Power (ZAR/mo Excl. VAT) [Optimal: R85,000]",
            min_value=35000,
            max_value=250000,
            key="monthly_fixed_opex_zar",
            step=5000,
            help="Monthly fixed factory expenses in Silverton. Dividing this by R678 profit/unit gives your Monthly Break-Even Units.",
        )
    with f_col2:
        plant_capex_zar = st.slider(
            "Silverton Starter Plant CAPEX — Extruder, Hydraulic Press & Steel Molds (ZAR Excl. VAT) [Optimal: R650,000]",
            min_value=250000,
            max_value=2000000,
            key="plant_capex_zar",
            step=50000,
            help="One-time startup machinery cost. Dividing this by Monthly Net Profit gives the Months to Pay Back CAPEX.",
        )

    # Break-Even, Payback Months, Capacity & Carbon Math
    single_shift_max_monthly_units = 528  # 24 covers/day * 22 working days
    som_capacity_utilization_pct = round(
        (monthly_units_sold / single_shift_max_monthly_units) * 100, 1
    )

    breakeven_units_monthly = math.ceil(monthly_fixed_opex_zar / unit_profit_zar)
    breakeven_units_annual = breakeven_units_monthly * 12
    breakeven_capacity_pct = round(
        (breakeven_units_monthly / single_shift_max_monthly_units) * 100, 1
    )
    daily_breakeven_units = round(breakeven_units_monthly / 22.0, 1)

    monthly_revenue_zar = monthly_units_sold * wholesale_price_zar
    monthly_variable_cost_zar = monthly_units_sold * production_cost_zar
    monthly_net_profit_zar = (
        monthly_revenue_zar - monthly_variable_cost_zar - monthly_fixed_opex_zar
    )
    annual_net_profit_zar = monthly_net_profit_zar * 12

    if monthly_net_profit_zar > 0:
        capex_payback_months = round(plant_capex_zar / monthly_net_profit_zar, 1)
        payback_text = f"{capex_payback_months} Months"
    else:
        capex_payback_months = 999
        payback_text = "Increase SOM Units"

    annual_ldpe_diverted_tonnes = round(
        (annual_som_units * ldpe_waste_used_kg) / 1000.0, 1
    )
    annual_bags_diverted_m = round(
        (annual_som_units * plastic_bags_diverted) / 1_000_000.0, 2
    )
    annual_co2e_saved_tonnes = round(annual_ldpe_diverted_tonnes * 2.2, 1)

    # 4 Wide Financial & Operational KPIs (No text cut-off!)
    b1, b2, b3, b4 = st.columns(4)
    b1.metric(
        "1. Monthly Break-Even Volume",
        f"{breakeven_units_monthly} units / mo",
        delta=f"Only {daily_breakeven_units} covers/day ({breakeven_units_annual:,}/yr)",
    )
    b2.metric(
        "2. Startup CAPEX Break-Even Time",
        payback_text,
        delta=f"To recover R{int(plant_capex_zar):,} machinery",
    )
    b3.metric(
        "3. Monthly Net Profit (at SOM)",
        f"R{int(monthly_net_profit_zar):,} / mo",
        delta=f"R{annual_net_profit_zar / 1_000_000:.2f}M annual net profit",
    )
    b4.metric(
        "4. 1-Shift Machine Utilization",
        f"{som_capacity_utilization_pct}% at SOM",
        delta=f"Uses {int(monthly_units_sold)} of 528 max units/mo",
    )

    # Second Row: 2 Wide Environmental Impact Cards
    e1, e2 = st.columns(2)
    e1.metric(
        "♻️ Annual Code 4 rLDPE Plastic Diverted from Gauteng Landfills",
        f"{annual_ldpe_diverted_tonnes} Tonnes / year",
        delta=f"Equivalent to ~{annual_bags_diverted_m} Million plastic bags/year",
    )
    e2.metric(
        "🌍 Annual Carbon Emissions Avoided (Scope 3 ESG Compliance)",
        f"{annual_co2e_saved_tonnes} Tonnes CO₂e / year",
        delta="Replaces high-emission foundry iron & virgin petrochemical resin",
    )

    # Plain-English Live Story Box for Tab 3
    st.markdown(
        f'<div class="story-box">'
        f"<b>📖 How to Read Tab 3 (Two Break-Even Numbers Explained):</b><br>"
        f"• <b>Monthly Operational Break-Even ({breakeven_units_monthly} units/month):</b> Because each cover earns <b>R{int(unit_profit_zar):,} gross profit</b>, "
        f"selling just <b>{breakeven_units_monthly} covers/month ({daily_breakeven_units} covers/day)</b> pays 100% of your R{int(monthly_fixed_opex_zar):,} monthly Silverton rent, power, and wages.<br>"
        f"• <b>Startup CAPEX Break-Even Time ({payback_text}):</b> At your Tab 2 target of <b>{int(monthly_units_sold)} units/month</b> ({annual_som_units:,}/yr), "
        f"your factory clears <b>R{int(monthly_net_profit_zar):,}/month in pure net profit</b> after all expenses—paying back your entire <b>R{int(plant_capex_zar):,}</b> machinery investment in <b>{payback_text}</b>."
        f"</div>",
        unsafe_allow_html=True,
    )

    # Interactive Break-Even & Machine Capacity Chart
    unit_range = list(range(0, 551, 25))
    revenues = [u * wholesale_price_zar for u in unit_range]
    total_costs = [
        monthly_fixed_opex_zar + (u * production_cost_zar) for u in unit_range
    ]

    fig_be = go.Figure()
    fig_be.add_trace(
        go.Scatter(
            x=unit_range,
            y=revenues,
            mode="lines+markers",
            name="Monthly Direct Hub Revenue (ZAR Excl. VAT)",
            line=dict(color="#0d9488", width=3),
        )
    )
    fig_be.add_trace(
        go.Scatter(
            x=unit_range,
            y=total_costs,
            mode="lines+markers",
            name="Monthly Total Cost (Fixed OPEX + Variable Manufacturing Cost)",
            line=dict(color="#ef4444", width=3, dash="dash"),
        )
    )
    fig_be.add_vline(
        x=breakeven_units_monthly,
        line_dash="dot",
        line_color="#1e40af",
        annotation_text=f"Break-Even: {breakeven_units_monthly} units/mo",
        annotation_position="top left",
    )
    fig_be.add_vline(
        x=monthly_units_sold,
        line_dash="solid",
        line_color="#15803d",
        annotation_text=f"Your SOM Target: {int(monthly_units_sold)} units/mo",
        annotation_position="bottom right",
    )
    fig_be.add_vline(
        x=single_shift_max_monthly_units,
        line_dash="dashdot",
        line_color="#9333ea",
        annotation_text="1-Shift Max (528 units/mo)",
        annotation_position="top right",
    )
    fig_be.update_layout(
        title="How to Read This Graph: Where the Green Line Crosses Above the Red Dashed Line = Profit Zone!",
        xaxis_title="Units Sold per Month (from Silverton Facility)",
        yaxis_title="ZAR per Month (Excl. 15% VAT)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=430,
    )
    st.plotly_chart(fig_be, use_container_width=True)
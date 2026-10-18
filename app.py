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
        font-size: 1.05rem;
        margin-bottom: 16px;
        display: inline-block;
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
        padding: 16px;
        border-radius: 6px;
        margin-bottom: 12px;
        color: #1e293b;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# HEADER
# -----------------------------------------------------------------------------
st.title("♻️ PlastiNoxa: Code 4 rLDPE Composite Manhole & Drain Cover Simulator")
st.markdown(
    "**Silverton (East Pretoria) Manufacturing Base | SANS 1882 Engineering, Wholesale vs. Retail Pricing (Excl. VAT) & Gauteng 3-Metro Commercial Model**"
)

tab1, tab2 = st.tabs(
    [
        "🛠️ Tab 1: SANS 1882 Engineering & 3-Tier Pricing (Excl. VAT)",
        "📈 Tab 2: Commercial Opportunity (TAM/SAM/SOM), Break-Even & Machine Capacity",
    ]
)

# =============================================================================
# TAB 1: SANS 1882 ENGINEERING & 3-TIER PRICING SIMULATOR (EXCL. VAT)
# =============================================================================
with tab1:
    st.subheader(
        "1. Material Formulation, SANS 1882 Load Class & Wholesale vs. Retail Pricing (Excl. 15% VAT)"
    )

    ctrl_col1, ctrl_col2, ctrl_col3, ctrl_col4 = st.columns([1.3, 1.2, 1.2, 1.3])

    with ctrl_col1:
        product_type = st.selectbox(
            "Select Chosen Product Format",
            options=[
                "600x600mm Manhole Cover & Frame",
                "550x550mm Roadside Stormwater Grate",
            ],
            index=0,
        )

    with ctrl_col2:
        fiberglass_pct = st.slider(
            "Glass Fiber Reinforcement (%)",
            min_value=0,
            max_value=25,
            value=12,
            step=1,
            help="Boosts tensile & flexural spine on the bottom face of the cover.",
        )

    with ctrl_col3:
        cover_rib_depth_mm = st.slider(
            "Ribbed Cover Thickness (mm)",
            min_value=30,
            max_value=85,
            value=55,
            step=5,
            help="Hexagonal waffle under-ribbing depth. Flexural stiffness scales with the cube of depth.",
        )

    with ctrl_col4:
        chart_view = st.radio(
            "Chart Display Mode",
            options=[
                "Show Both Side-by-Side",
                "3-Tier Pricing Ladder (Excl. VAT)",
                "Load Strength (kN) & Weight (kg)",
            ],
            index=0,
        )

    rldpe_pct = 32
    mape_carbon_pct = 3
    sand_flyash_pct = 100 - rldpe_pct - mape_carbon_pct - fiberglass_pct

    # Governing Engineering & 3-Tier Pricing Equations (All Excl. 15% VAT)
    unit_weight_kg = round(
        14 + (cover_rib_depth_mm * 0.28) - (fiberglass_pct * 0.08), 1
    )
    ldpe_waste_used_kg = round(unit_weight_kg * (rldpe_pct / 100.0), 1)
    plastic_bags_diverted = int(round(ldpe_waste_used_kg * 150, 0))

    load_capacity_kn = round(
        (12 + (fiberglass_pct * 4.2)) * ((cover_rib_depth_mm / 40.0) ** 1.8), 1
    )

    production_cost_zar = round(
        (unit_weight_kg * 0.32 * 3.8)
        + (unit_weight_kg * (0.68 - fiberglass_pct / 100.0) * 0.35)
        + (unit_weight_kg * (fiberglass_pct / 100.0) * 8.5)
        + 115,
        0,
    )
    # B2B Factory-Gate Wholesale Price (Excl. VAT)
    wholesale_price_zar = round(production_cost_zar * 2.6, 0)
    # Recommended Retail Price / RRP at Hardware Stores (+35% Retailer Markup, Excl. VAT)
    retail_rrp_zar = round(wholesale_price_zar * 1.35, 0)

    unit_profit_zar = wholesale_price_zar - production_cost_zar
    gross_margin_pct = round((unit_profit_zar / wholesale_price_zar) * 100, 1)

    if product_type == "600x600mm Manhole Cover & Frame":
        benchmarks = {
            "Virgin Polymer Concrete (DMC)": {
                "load_kn": 65.0,
                "weight_kg": 34.0,
                "cost_zar": 780.0,
                "wholesale_zar": 1250.0,
                "retail_zar": 1620.0,
            },
            "Cast Iron (SANS 1882)": {
                "load_kn": 135.0,
                "weight_kg": 82.0,
                "cost_zar": 2850.0,
                "wholesale_zar": 3680.0,
                "retail_zar": 4605.0,
            },
        }
    else:
        benchmarks = {
            "Virgin Polymer Concrete (DMC)": {
                "load_kn": 90.0,
                "weight_kg": 42.0,
                "cost_zar": 1150.0,
                "wholesale_zar": 1880.0,
                "retail_zar": 2450.0,
            },
            "Cast Iron (SANS 1882)": {
                "load_kn": 180.0,
                "weight_kg": 114.0,
                "cost_zar": 4700.0,
                "wholesale_zar": 6150.0,
                "retail_zar": 7819.0,
            },
        }

    cast_iron_weight = benchmarks["Cast Iron (SANS 1882)"]["weight_kg"]
    cast_iron_retail = benchmarks["Cast Iron (SANS 1882)"]["retail_zar"]
    weight_saved_pct = round(
        ((cast_iron_weight - unit_weight_kg) / cast_iron_weight) * 100, 1
    )
    municipal_savings_zar = int(cast_iron_retail - wholesale_price_zar)

    if load_capacity_kn >= 125:
        sans_class = "✅ PASSES SANS 1882 HEAVY CURBSIDE / ROADWAY (≥ 125 kN)"
        badge_bg, badge_color = "#dcfce7", "#166534"
    elif load_capacity_kn >= 40:
        sans_class = "✅ PASSES SANS 1882 MEDIUM DUTY — DRIVEWAYS & TAXI CORRIDORS (≥ 40 kN)"
        badge_bg, badge_color = "#dbeafe", "#1e40af"
    elif load_capacity_kn >= 7:
        sans_class = "⚠️ PASSES SANS 1882 LIGHT DUTY ONLY — PEDESTRIAN & PARKS (≥ 7 kN)"
        badge_bg, badge_color = "#fef9c3", "#854d0e"
    else:
        sans_class = "❌ BELOW SANS 1882 MINIMUM THRESHOLD (< 7 kN)"
        badge_bg, badge_color = "#fee2e2", "#991b1b"

    st.markdown(
        f'<div class="status-badge" style="background-color:{badge_bg}; color:{badge_color};">'
        f"SANS 1882 Status: {sans_class} — Load: {load_capacity_kn} kN "
        f"| Recipe: {rldpe_pct}% rLDPE, {sand_flyash_pct}% Sand/Ash, {fiberglass_pct}% Glass Fiber, {mape_carbon_pct}% MAPE/Carbon"
        f"</div>",
        unsafe_allow_html=True,
    )

    # 6 Top Engineering & Pricing KPI Cards (All Financial Figures Excl. VAT)
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric(
        "Engineered Load",
        f"{load_capacity_kn} kN",
        delta=f"{round(load_capacity_kn - 40, 1)} kN vs 40kN MD",
    )
    k2.metric(
        "Unit Weight",
        f"{unit_weight_kg} kg",
        delta=f"-{weight_saved_pct}% vs Cast Iron",
    )
    k3.metric(
        "1. Production Cost",
        f"R{int(production_cost_zar):,}",
        delta="Excl. VAT (Factory Cost)",
    )
    k4.metric(
        "2. B2B Wholesale Price",
        f"R{int(wholesale_price_zar):,}",
        delta=f"R{int(unit_profit_zar):,} profit ({gross_margin_pct}%)",
    )
    k5.metric(
        "3. Hardware Retail (RRP)",
        f"R{int(retail_rrp_zar):,}",
        delta="Excl. VAT (+35% Retailer Markup)",
    )
    k6.metric(
        "Code 4 rLDPE Diverted",
        f"{ldpe_waste_used_kg} kg / unit",
        delta=f"~{plastic_bags_diverted:,} plastic bags",
    )

    df_comp = pd.DataFrame(
        [
            {
                "Material": "Your rLDPE Hybrid Composite",
                "1. Manufacturing Cost (Excl. VAT)": production_cost_zar,
                "2. B2B Wholesale Price (Excl. VAT)": wholesale_price_zar,
                "3. Hardware Retail RRP (Excl. VAT)": retail_rrp_zar,
                "Load Capacity (kN)": load_capacity_kn,
                "Unit Weight (kg)": unit_weight_kg,
            },
            {
                "Material": "Virgin Polymer Concrete (DMC)",
                "1. Manufacturing Cost (Excl. VAT)": benchmarks["Virgin Polymer Concrete (DMC)"]["cost_zar"],
                "2. B2B Wholesale Price (Excl. VAT)": benchmarks["Virgin Polymer Concrete (DMC)"]["wholesale_zar"],
                "3. Hardware Retail RRP (Excl. VAT)": benchmarks["Virgin Polymer Concrete (DMC)"]["retail_zar"],
                "Load Capacity (kN)": benchmarks["Virgin Polymer Concrete (DMC)"]["load_kn"],
                "Unit Weight (kg)": benchmarks["Virgin Polymer Concrete (DMC)"]["weight_kg"],
            },
            {
                "Material": "Cast Iron (SANS 1882)",
                "1. Manufacturing Cost (Excl. VAT)": benchmarks["Cast Iron (SANS 1882)"]["cost_zar"],
                "2. B2B Wholesale Price (Excl. VAT)": benchmarks["Cast Iron (SANS 1882)"]["wholesale_zar"],
                "3. Hardware Retail RRP (Excl. VAT)": benchmarks["Cast Iron (SANS 1882)"]["retail_zar"],
                "Load Capacity (kN)": benchmarks["Cast Iron (SANS 1882)"]["load_kn"],
                "Unit Weight (kg)": benchmarks["Cast Iron (SANS 1882)"]["weight_kg"],
            },
        ]
    )

    def build_cost_chart(df):
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                name="1. Manufacturing Cost (Excl. VAT)",
                x=df["Material"],
                y=df["1. Manufacturing Cost (Excl. VAT)"],
                marker_color="#0f766e",
                text=df["1. Manufacturing Cost (Excl. VAT)"].apply(lambda x: f"R{int(x):,}"),
                textposition="auto",
            )
        )
        fig.add_trace(
            go.Bar(
                name="2. B2B Wholesale Price (Excl. VAT)",
                x=df["Material"],
                y=df["2. B2B Wholesale Price (Excl. VAT)"],
                marker_color="#14b8a6",
                text=df["2. B2B Wholesale Price (Excl. VAT)"].apply(lambda x: f"R{int(x):,}"),
                textposition="auto",
            )
        )
        fig.add_trace(
            go.Bar(
                name="3. Hardware Store Retail RRP (Excl. VAT)",
                x=df["Material"],
                y=df["3. Hardware Retail RRP (Excl. VAT)"],
                marker_color="#f59e0b",
                text=df["3. Hardware Retail RRP (Excl. VAT)"].apply(lambda x: f"R{int(x):,}"),
                textposition="auto",
            )
        )
        fig.update_layout(
            title="3-Tier Pricing Ladder: Production Cost vs. B2B Wholesale vs. Retail RRP (ZAR Excl. VAT)",
            barmode="group",
            yaxis_title="ZAR (Excl. 15% VAT)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            height=410,
        )
        return fig

    def build_load_weight_chart(df):
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                name="Load Capacity (kN)",
                x=df["Material"],
                y=df["Load Capacity (kN)"],
                marker_color="#2563eb",
                text=df["Load Capacity (kN)"].apply(lambda x: f"{x} kN"),
                textposition="auto",
            )
        )
        fig.add_trace(
            go.Bar(
                name="Total Unit Weight (kg)",
                x=df["Material"],
                y=df["Unit Weight (kg)"],
                marker_color="#64748b",
                text=df["Unit Weight (kg)"].apply(lambda x: f"{x} kg"),
                textposition="auto",
            )
        )
        fig.add_hline(
            y=7,
            line_dash="dot",
            line_color="#ca8a04",
            annotation_text="SANS 1882 Light Duty (7 kN)",
        )
        fig.add_hline(
            y=40,
            line_dash="dash",
            line_color="#1e40af",
            annotation_text="SANS 1882 Medium Duty (40 kN)",
        )
        fig.add_hline(
            y=125,
            line_dash="solid",
            line_color="#dc2626",
            annotation_text="SANS 1882 Heavy Curbside (125 kN)",
        )
        fig.update_layout(
            title="Load Capacity (kN) & Weight (kg) vs. SANS 1882 Classes",
            barmode="group",
            yaxis_title="kN / kg",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            height=410,
        )
        return fig

    if chart_view == "3-Tier Pricing Ladder (Excl. VAT)":
        st.plotly_chart(build_cost_chart(df_comp), use_container_width=True)
    elif chart_view == "Load Strength (kN) & Weight (kg)":
        st.plotly_chart(build_load_weight_chart(df_comp), use_container_width=True)
    else:
        c_left, c_right = st.columns(2)
        with c_left:
            st.plotly_chart(build_cost_chart(df_comp), use_container_width=True)
        with c_right:
            st.plotly_chart(build_load_weight_chart(df_comp), use_container_width=True)

    st.divider()
    st.subheader("🏆 Three Physical Design Innovations for the Judges")
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
# TAB 2: COMMERCIAL OPPORTUNITY (SA / 3 GAUTENG METROS / SILVERTON SOM)
# =============================================================================
with tab2:
    st.subheader(
        "2. Commercial Opportunity (Excl. VAT), Break-Even, Machine Capacity % & CO₂e Saved"
    )

    b_col1, b_col2, b_col3, b_col4 = st.columns(4)

    with b_col1:
        contracted_units_yr = st.slider(
            "Contracted Township/Local Units (yr)",
            min_value=300,
            max_value=3600,
            value=1500,
            step=100,
            help="E.g., 2 contracted Mamelodi taxi-rank/corridor drainage & Silverton civil projects (1,500 units/yr).",
        )

    with b_col2:
        loi_units_yr = st.slider(
            "Secured LOI Pipeline Units (yr)",
            min_value=200,
            max_value=3000,
            value=900,
            step=100,
            help="E.g., 3 Letters of Intent from Pretoria East estates & Silverton/Waltloo industrial parks (900 units/yr).",
        )

    with b_col3:
        monthly_fixed_opex_zar = st.slider(
            "Silverton Monthly Fixed OPEX (ZAR Excl. VAT)",
            min_value=35000,
            max_value=250000,
            value=85000,
            step=5000,
            help="Covers Silverton industrial workshop rent, 4 operators, and 3-phase electricity.",
        )

    with b_col4:
        plant_capex_zar = st.slider(
            "Silverton Starter Plant CAPEX (ZAR Excl. VAT)",
            min_value=250000,
            max_value=2000000,
            value=650000,
            step=50000,
            help="Heated extruder-mixer, 100-tonne hydraulic press, and 2 CNC steel waffle molds.",
        )

    # SOM, Break-Even, Machine Capacity & Carbon Calculations (All Financials Excl. VAT)
    annual_som_units = contracted_units_yr + loi_units_yr
    monthly_units_sold = round(annual_som_units / 12.0, 1)

    # Single-shift machine capacity: 1 cover every 20 mins = 24 units/day * 22 workdays = 528 units/month
    single_shift_max_monthly_units = 528
    som_capacity_utilization_pct = round(
        (monthly_units_sold / single_shift_max_monthly_units) * 100, 1
    )

    breakeven_units_monthly = math.ceil(monthly_fixed_opex_zar / unit_profit_zar)
    breakeven_units_annual = breakeven_units_monthly * 12
    breakeven_capacity_pct = round(
        (breakeven_units_monthly / single_shift_max_monthly_units) * 100, 1
    )
    daily_breakeven_units = round(breakeven_units_monthly / 22.0, 1)

    contracted_revenue_zar = contracted_units_yr * wholesale_price_zar
    loi_revenue_zar = loi_units_yr * wholesale_price_zar
    annual_som_revenue_zar = annual_som_units * wholesale_price_zar

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
        payback_text = "Below Break-Even"

    annual_ldpe_diverted_tonnes = round(
        (annual_som_units * ldpe_waste_used_kg) / 1000.0, 1
    )
    annual_bags_diverted_m = round(
        (annual_som_units * plastic_bags_diverted) / 1_000_000.0, 2
    )
    # 1 tonne of recycled LDPE substituting virgin resin/cast iron avoids ~2.2 tonnes of CO2e
    annual_co2e_saved_tonnes = round(annual_ldpe_diverted_tonnes * 2.2, 1)

    # 6 Top Commercial, Operational & ESG KPIs
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    m1.metric(
        "Year-1 SOM Revenue (Excl. VAT)",
        f"R{annual_som_revenue_zar / 1_000_000:.2f}M / yr",
        delta=f"{annual_som_units:,} units/yr ({int(monthly_units_sold)}/mo)",
    )
    m2.metric(
        "Break-Even Volume",
        f"{breakeven_units_monthly} units / mo",
        delta=f"{breakeven_units_annual:,}/yr ({daily_breakeven_units}/day)",
    )
    m3.metric(
        "Monthly Net Profit (Excl. VAT)",
        f"R{int(monthly_net_profit_zar):,} / mo",
        delta=f"R{annual_net_profit_zar / 1_000_000:.2f}M/yr net profit",
    )
    m4.metric(
        "CAPEX Payback Period",
        payback_text,
        delta=f"Recovers R{int(plant_capex_zar):,} plant",
    )
    m5.metric(
        "1-Shift Machine Utilization",
        f"{som_capacity_utilization_pct}% at SOM",
        delta=f"Break-even uses {breakeven_capacity_pct}% (of 528/mo)",
    )
    m6.metric(
        "rLDPE & Carbon Saved",
        f"{annual_ldpe_diverted_tonnes}t LDPE / yr",
        delta=f"{annual_co2e_saved_tonnes}t CO₂e avoided ({annual_bags_diverted_m}M bags)",
    )

    st.divider()

    # TAM / SAM / SOM Table + Customer Pain & Validation Cards
    left_col, right_col = st.columns([1.35, 1.0])

    with left_col:
        st.markdown("#### 🎯 Target Addressable Market Table (All Values Excl. 15% VAT)")
        df_tam = pd.DataFrame(
            [
                {
                    "Market Tier": "TAM (Total Addressable Market)",
                    "Annual Value (Excl. VAT)": "R1.85 Billion",
                    "Scope & Commercial Evidence": (
                        "Total South African annual Rand value market for our chosen product: "
                        "municipal & civil manhole covers, roadside stormwater grates, and utility vaults (SANS 1882)."
                    ),
                },
                {
                    "Market Tier": "SAM (Serviceable Available Market)",
                    "Annual Value (Excl. VAT)": "R740 Million",
                    "Scope & Commercial Evidence": (
                        "All 3 Gauteng Metros (City of Tshwane, City of Johannesburg, and City of Ekurhuleni) "
                        "provincial/municipal road & stormwater tenders and 10%–30% green-procurement projects."
                    ),
                },
                {
                    "Market Tier": "SOM (Silverton Year-1 Target)",
                    "Annual Value (Excl. VAT)": f"R{annual_som_revenue_zar / 1_000_000:.2f} Million",
                    "Scope & Commercial Evidence": (
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
            Civil engineering contractors, township taxi-rank upgrade contractors (Mamelodi), Pretoria East security estates, and municipal depot officers across the 3 Gauteng Metros under 10%–30% green procurement quotas.
            </div>
            <div class="commercial-card">
            <b>💊 Pain Relieved:</b><br>
            • <b>Eliminates Handover Penalties from Cast-Iron Theft:</b> Contractors lose retention money when R4,605 cast-iron grates are stolen before site sign-off. Our R{int(wholesale_price_zar):,} B2B wholesale cover (R{int(retail_rrp_zar):,} retail RRP, Excl. VAT) has zero scrap value and locks shut.<br>
            • <b>Zero Cracking Under Heavy Taxi Wheel Torque:</b> Concrete and virgin polymer lids crack under Mamelodi taxi rank axle turning loads; our rLDPE + {fiberglass_pct}% fiberglass composite absorbs heavy shock.
            </div>
            <div class="commercial-card">
            <b>✅ Validation & Scalability Status:</b><br>
            • <b>Pipeline:</b> <b>{annual_som_units:,} commercial units</b> ({contracted_units_yr:,} units via 2 Mamelodi/Silverton civil contracts + {loi_units_yr:,} units via 3 Pretoria East estate/industrial park LOIs).<br>
            • <b>Headroom:</b> Runs at <b>{som_capacity_utilization_pct}% single-shift press capacity</b> (528 units/mo max), allowing 2.5x revenue growth without extra CAPEX.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    # Interactive Break-Even & Machine Capacity Chart (Units Sold vs Revenue & Total Costs)
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
            name="Monthly B2B Wholesale Revenue (ZAR Excl. VAT)",
            line=dict(color="#0d9488", width=3),
        )
    )
    fig_be.add_trace(
        go.Scatter(
            x=unit_range,
            y=total_costs,
            mode="lines+markers",
            name="Monthly Total Cost (Silverton Fixed OPEX + Variable Cost, Excl. VAT)",
            line=dict(color="#ef4444", width=3, dash="dash"),
        )
    )
    fig_be.add_vline(
        x=breakeven_units_monthly,
        line_dash="dot",
        line_color="#1e40af",
        annotation_text=f"Break-Even: {breakeven_units_monthly} units/mo ({breakeven_capacity_pct}% capacity)",
        annotation_position="top left",
    )
    fig_be.add_vline(
        x=monthly_units_sold,
        line_dash="solid",
        line_color="#15803d",
        annotation_text=f"Silverton SOM: {int(monthly_units_sold)} units/mo ({som_capacity_utilization_pct}% capacity)",
        annotation_position="bottom right",
    )
    fig_be.add_vline(
        x=single_shift_max_monthly_units,
        line_dash="dashdot",
        line_color="#9333ea",
        annotation_text="1-Shift Max Capacity (528 units/mo)",
        annotation_position="top right",
    )
    fig_be.update_layout(
        title="Silverton Plant Monthly Break-Even & 1-Shift Capacity Analysis (ZAR Excl. VAT)",
        xaxis_title="Units Sold per Month (from Silverton Facility)",
        yaxis_title="ZAR per Month (Excl. 15% VAT)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=430,
    )
    st.plotly_chart(fig_be, use_container_width=True)
import math
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="PlastiNoxa | Silverton rLDPE Manhole Cover & R280k Seed Model",
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
# SESSION STATE INITIALIZATION (LOCKED TO LEAN SCAMPER R280,000 MODEL)
# -----------------------------------------------------------------------------
if "fiberglass_pct" not in st.session_state:
    st.session_state.fiberglass_pct = 12
if "cover_rib_depth_mm" not in st.session_state:
    st.session_state.cover_rib_depth_mm = 55
if "contracted_units_yr" not in st.session_state:
    st.session_state.contracted_units_yr = 900
if "loi_units_yr" not in st.session_state:
    st.session_state.loi_units_yr = 600
if "monthly_fixed_opex_zar" not in st.session_state:
    st.session_state.monthly_fixed_opex_zar = 45000
if "seed_capital_ask_zar" not in st.session_state:
    st.session_state.seed_capital_ask_zar = 280000

# -----------------------------------------------------------------------------
# HEADER
# -----------------------------------------------------------------------------
st.title("♻️ PlastiNoxa: Code 4 rLDPE Anti-Theft Manhole Cover Simulator")
st.markdown(
    "**Silverton (East Pretoria) Hub | 600×600mm SANS 1882 Standard | SCAMPER Lean Tech & R280,000 Single-Tier Seed Model**"
)

tab1, tab2, tab3 = st.tabs(
    [
        "🛠️ Tab 1: 600×600mm Engineering & 3-Tier Pricing (Excl. VAT)",
        "🎯 Tab 2: Market Opportunity (TAM/SAM/SOM) & Customer Pipeline",
        "🏭 Tab 3: R280k SCAMPER Seed Ask, Break-Even & Triple-Bottom-Line Impact",
    ]
)

# =============================================================================
# TAB 1: 600x600mm ENGINEERING & 3-TIER PRICING (EXCL. 15% VAT)
# =============================================================================
with tab1:
    st.subheader(
        "1. 600×600mm Manhole Cover Formulation, SANS 1882 Load Class & 3-Tier Pricing (Excl. 15% VAT)"
    )

    st.markdown("**💡 Quick-Select SANS 1882 Duty Presets (Click to auto-set sliders):**")
    p_btn1, p_btn2, p_btn3 = st.columns(3)
    with p_btn1:
        if st.button(
            "🚶 Light Duty Preset (Pedestrian / Parks - 7 kN+)",
            use_container_width=True,
        ):
            st.session_state.fiberglass_pct = 4
            st.session_state.cover_rib_depth_mm = 35
    with p_btn2:
        if st.button(
            "⭐ Optimal Medium Duty (Default: Driveways & Taxis - 40 kN+)",
            use_container_width=True,
        ):
            st.session_state.fiberglass_pct = 12
            st.session_state.cover_rib_depth_mm = 55
    with p_btn3:
        if st.button(
            "🚛 Heavy Curbside / Roadway Preset (Municipal Roads - 125 kN+)",
            use_container_width=True,
        ):
            st.session_state.fiberglass_pct = 18
            st.session_state.cover_rib_depth_mm = 70

    ctrl_col1, ctrl_col2 = st.columns(2)

    with ctrl_col1:
        fiberglass_pct = st.slider(
            "Waste Glass Fiber Reinforcement (%) [Optimal: 12% Medium Duty | 18% Heavy Duty]",
            min_value=0,
            max_value=25,
            key="fiberglass_pct",
            step=1,
            help="Acts as internal tensile reinforcement on the bottom face of the 600x600mm cover.",
        )

    with ctrl_col2:
        cover_rib_depth_mm = st.slider(
            "Hexagonal Waffle-Rib Cover Thickness (mm) [Optimal: 55mm Medium | 70mm Heavy]",
            min_value=30,
            max_value=85,
            key="cover_rib_depth_mm",
            step=5,
            help="Bending stiffness scales with the cube of thickness (I = bh³/12). 55mm gives 110.7 kN at 28.4 kg.",
        )

    rldpe_pct = 32
    mape_carbon_pct = 3
    sand_flyash_pct = 100 - rldpe_pct - mape_carbon_pct - fiberglass_pct

    # Governing Engineering & 3-Tier Pricing Equations for 600x600mm Cover & Frame (Excl. 15% VAT)
    unit_weight_kg = round(
        14.0 + (cover_rib_depth_mm * 0.28) - (fiberglass_pct * 0.08), 1
    )
    ldpe_waste_used_kg = round(unit_weight_kg * (rldpe_pct / 100.0), 1)
    plastic_bags_diverted = int(round(ldpe_waste_used_kg * 150, 0))

    load_capacity_kn = round(
        (12 + (fiberglass_pct * 4.2)) * ((cover_rib_depth_mm / 40.0) ** 1.8), 1
    )

    # Full Manufacturing Cost (R424 at default 12% fiber, 55mm rib):
    # Raw rLDPE (@ R3.80/kg paid to local reclaimers) + Sand (@ R0.35/kg) + Fiberglass (@ R8.50/kg)
    # + R240 (MAPE coupling agent, UV carbon black, integral hinge & pentagon cam-lock) + R115 (LPG gas & operator labor)
    raw_materials_cost = (
        (unit_weight_kg * 0.32 * 3.8)
        + (unit_weight_kg * (0.68 - fiberglass_pct / 100.0) * 0.35)
        + (unit_weight_kg * (fiberglass_pct / 100.0) * 8.5)
    )
    production_cost_zar = round(raw_materials_cost + 240.0 + 115.0, 0)

    # Tier 2: Direct Hub B2B Wholesale Price (Selling directly from Silverton Hub, Excl. VAT)
    wholesale_price_zar = round(production_cost_zar * 2.6, 0)
    # Tier 3: Hardware Store Retail RRP (+35% Retailer Markup, Excl. VAT)
    retail_rrp_zar = round(wholesale_price_zar * 1.35, 0)

    unit_profit_zar = wholesale_price_zar - production_cost_zar
    gross_margin_pct = round((unit_profit_zar / wholesale_price_zar) * 100, 1)

    # Verified 2026 South African 600x600mm Competitor Benchmarks (Excl. 15% VAT from Plumblink & Harscan)
    benchmarks = {
        "Virgin Polymer Concrete (DMC)": {
            "load_kn": 65.0,
            "weight_kg": 34.0,
            "cost_zar": 780.0,
            "wholesale_zar": 1250.0,
            "retail_zar": 1620.0,
        },
        "Cast Iron (SANS 1882 / 558)": {
            "load_kn": 135.0,
            "weight_kg": 82.0,
            "cost_zar": 2550.0,
            "wholesale_zar": 3330.0,
            "retail_zar": 4160.0,
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
        sans_class = "✅ PASSES SANS 1882 HEAVY CURBSIDE / ROADWAY (≥ 125 kN) — Municipal Main Roads & Truck Yards"
        badge_bg, badge_color = "#dcfce7", "#166534"
    elif load_capacity_kn >= 40:
        sans_class = "✅ PASSES SANS 1882 MEDIUM DUTY (≥ 40 kN) — Mamelodi Taxi Corridors, Estates & Commercial Driveways"
        badge_bg, badge_color = "#dbeafe", "#1e40af"
    elif load_capacity_kn >= 7:
        sans_class = "⚠️ PASSES SANS 1882 LIGHT DUTY ONLY (≥ 7 kN) — Pedestrian Walkways, Parks & Water-Meter Boxes"
        badge_bg, badge_color = "#fef9c3", "#854d0e"
    else:
        sans_class = "❌ BELOW SANS 1882 MINIMUM THRESHOLD (< 7 kN) — Increase Fiberglass % or Rib Thickness"
        badge_bg, badge_color = "#fee2e2", "#991b1b"

    st.markdown(
        f'<div class="status-badge" style="background-color:{badge_bg}; color:{badge_color};">'
        f"{sans_class} <br>Engineered Load: {load_capacity_kn} kN | 600×600mm Recipe: {rldpe_pct}% Code 4 rLDPE, "
        f"{sand_flyash_pct}% Dry Silica Sand/Fly Ash, {fiberglass_pct}% Glass Fiber, {mape_carbon_pct}% MAPE/Carbon"
        f"</div>",
        unsafe_allow_html=True,
    )

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

    st.markdown(
        f'<div class="story-box">'
        f"<b>📖 How to Read Tab 1:</b> Our single flagship product is the <b>600×600mm SANS 1882 Anti-Theft Manhole Cover & Frame</b>. "
        f"At <b>{fiberglass_pct}% fiberglass</b> and a <b>{cover_rib_depth_mm} mm hexagonal waffle-rib depth</b>, it weighs <b>{unit_weight_kg} kg</b> "
        f"and holds <b>{load_capacity_kn} kN</b>. Using our SCAMPER gas-fired drum mixer and 100T press in Silverton, it costs <b>R{int(production_cost_zar):,}</b> to make "
        f"and sells directly from our hub at <b>R{int(wholesale_price_zar):,} (Excl. VAT)</b>—generating <b>R{int(unit_profit_zar):,} profit per unit</b> while saving buyers "
        f"<b>R{savings_vs_polymer:,}</b> vs. Virgin Polymer Concrete (R1,620) and <b>R{savings_vs_cast_iron:,}</b> vs. Cast Iron (R4,160)."
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
                text=df_comp["1. Factory Production Cost (Excl. VAT)"].apply(
                    lambda x: f"R{int(x):,}"
                ),
                textposition="auto",
            )
        )
        fig_cost.add_trace(
            go.Bar(
                name="2. Direct Hub B2B Price (Excl. VAT)",
                x=df_comp["Material"],
                y=df_comp["2. Direct Hub B2B Price (Excl. VAT)"],
                marker_color="#14b8a6",
                text=df_comp["2. Direct Hub B2B Price (Excl. VAT)"].apply(
                    lambda x: f"R{int(x):,}"
                ),
                textposition="auto",
            )
        )
        fig_cost.add_trace(
            go.Bar(
                name="3. Hardware Store RRP (Excl. VAT)",
                x=df_comp["Material"],
                y=df_comp["3. Hardware Store RRP (Excl. VAT)"],
                marker_color="#f59e0b",
                text=df_comp["3. Hardware Store RRP (Excl. VAT)"].apply(
                    lambda x: f"R{int(x):,}"
                ),
                textposition="auto",
            )
        )
        fig_cost.update_layout(
            title="600×600mm 3-Tier Pricing Ladder (ZAR Excl. 15% VAT)",
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
    st.subheader("🏆 Core Structural, SCAMPER & Anti-Theft Engineering Innovations")
    col_i1, col_i2, col_i3 = st.columns(3)
    with col_i1:
        st.markdown(
            """
            <div class="innovation-card">
            <h4>1. Hexagonal Under-Ribbing (Waffle Base)</h4>
            <p>Bending stiffness increases with the <b>cube of thickness</b> (I = bh³/12). A 20 mm solid top plate over 35–55 mm hexagonal ribs cuts weight by 30% while doubling load capacity.</p>
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
            <h4>3. SCAMPER Repurposed Process & Embossing</h4>
            <p>Shredded via an adapted 80 RPM agricultural silage cutter, thermally blended in a gas-fired drum mixer (<1% moisture), and pressed with embossed tread: "MADE FROM {plastic_bags_diverted:,} RECYCLED PLASTIC BAGS".</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# =============================================================================
# TAB 2: COMMERCIAL MARKET OPPORTUNITY (TAM / SAM / SOM) & CUSTOMER PIPELINE
# =============================================================================
with tab2:
    st.subheader(
        "2. Commercial Opportunity (SA / 3 Gauteng Metros / Silverton Year-1 SOM) & Customer Pipeline"
    )

    s_col1, s_col2 = st.columns(2)
    with s_col1:
        contracted_units_yr = st.slider(
            "1. Contracted Township & Local Civil Projects (Units / Year) [Optimal 1-Mold Target: 900]",
            min_value=200,
            max_value=2000,
            key="contracted_units_yr",
            step=50,
            help="Target: 2 contracted Mamelodi taxi-corridor & Silverton civil upgrades (900 units/yr = 75 units/mo).",
        )
    with s_col2:
        loi_units_yr = st.slider(
            "2. Secured LOI Pipeline — Estates & Industrial Parks (Units / Year) [Optimal Target: 600]",
            min_value=100,
            max_value=1500,
            key="loi_units_yr",
            step=50,
            help="Target: 3 Letters of Intent from Pretoria East security estates & Silverton industrial parks (600 units/yr = 50 units/mo).",
        )

    annual_som_units = contracted_units_yr + loi_units_yr
    monthly_units_sold = round(annual_som_units / 12.0, 1)

    contracted_revenue_zar = contracted_units_yr * wholesale_price_zar
    loi_revenue_zar = loi_units_yr * wholesale_price_zar
    annual_som_revenue_zar = annual_som_units * wholesale_price_zar
    gauteng_sam_share_pct = round((annual_som_revenue_zar / 740_000_000) * 100, 2)

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
        delta=f"{int(monthly_units_sold)} units/month (~6 covers/day)",
    )

    st.markdown(
        f'<div class="story-box">'
        f"<b>📖 How to Read Tab 2:</b> With 1 welded 600×600mm steel mold in Silverton, our Year-1 beachhead SOM is "
        f"<b>{annual_som_units:,} covers/year ({int(monthly_units_sold)} covers/month = R{annual_som_revenue_zar / 1_000_000:.2f} Million Excl. VAT)</b>. "
        f"This consists of <b>{contracted_units_yr:,} units/yr</b> (R{contracted_revenue_zar / 1_000_000:.2f}M) across 2 Mamelodi/Silverton civil & taxi-corridor projects, "
        f"plus <b>{loi_units_yr:,} units/yr</b> (R{loi_revenue_zar / 1_000_000:.2f}M) across 3 Letters of Intent with Pretoria East estates and Silverton industrial parks."
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
                        "Total South African annual Rand value market for 600×600mm municipal & civil manhole covers "
                        "and utility inspection vaults (SANS 1882 / SANS 558 replacement demand)."
                    ),
                },
                {
                    "Market Tier": "SAM (Serviceable Available Market)",
                    "Annual Value (Excl. VAT)": "R740 Million",
                    "Scope & Verified Market Basis": (
                        "All 3 Gauteng Metros (City of Tshwane, City of Johannesburg, and City of Ekurhuleni) "
                        "provincial/municipal road & water tenders and 10%–30% green-procurement projects."
                    ),
                },
                {
                    "Market Tier": "SOM (Silverton Year-1 Beachhead)",
                    "Annual Value (Excl. VAT)": f"R{annual_som_revenue_zar / 1_000_000:.2f} Million",
                    "Scope & Verified Market Basis": (
                        f"2 contracted Mamelodi taxi-corridor / township civil upgrades "
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
            Civil engineering contractors, Mamelodi taxi-rank upgrade contractors, Pretoria East security estates, and municipal depot officers across the 3 Gauteng Metros under 10% green procurement quotas.
            </div>
            <div class="commercial-card">
            <b>💊 Pain Relieved:</b><br>
            • <b>Eliminates Handover Penalties from Cast-Iron Theft:</b> Contractors lose retention money when R{int(cast_iron_retail):,} (Excl. VAT) cast-iron covers are stolen before site sign-off. Our R{int(wholesale_price_zar):,} Direct Hub cover (R{int(retail_rrp_zar):,} Hardware RRP) has zero scrap value and locks shut.<br>
            • <b>Zero Cracking Under Heavy Taxi Wheel Torque:</b> Concrete and virgin polymer lids crack under Mamelodi taxi rank axle turning loads; our rLDPE + {fiberglass_pct}% fiberglass composite absorbs heavy shock.
            </div>
            <div class="commercial-card">
            <b>✅ Validation Status & EPR Moat:</b><br>
            • <b>Pipeline:</b> <b>{annual_som_units:,} commercial units/yr</b> ({contracted_units_yr:,} contracted township civil units + {loi_units_yr:,} estate/industrial park LOI units).<br>
            • <b>EPR Subsidy Moat:</b> Eligible for <b>+R1.20/kg PRO Section 18 EPR subsidy</b> on diverted post-consumer LDPE.
            </div>
            """,
            unsafe_allow_html=True,
        )

# =============================================================================
# TAB 3: R280K SCAMPER SEED ASK, BREAK-EVEN & TRIPLE-BOTTOM-LINE IMPACT
# =============================================================================
with tab3:
    st.subheader(
        "3. Single-Tier R280,000 SCAMPER Seed Capital Ask, Break-Even Volume & Triple-Bottom-Line Impact"
    )

    f_col1, f_col2 = st.columns(2)
    with f_col1:
        monthly_fixed_opex_zar = st.slider(
            "Silverton/Waltloo Lean Monthly Fixed OPEX — Rent (R16k), 3 Staff (R21k) & Gas/Power (R8k) [Optimal: R45,000]",
            min_value=30000,
            max_value=120000,
            key="monthly_fixed_opex_zar",
            step=5000,
            help="Lean SCAMPER workshop OPEX. Dividing this by R678 profit/unit gives your Monthly Break-Even Units (67 units/mo).",
        )
    with f_col2:
        seed_capital_ask_zar = st.slider(
            "Single-Tier Seed Capital Ask (ZAR) — SCAMPER Tech + Setup/SABS + Working Capital [Locked Target: R280,000]",
            min_value=200000,
            max_value=500000,
            key="seed_capital_ask_zar",
            step=10000,
            help="Your single one-tier ask of R280,000 (R120k SCAMPER machinery/mold + R70k setup/SABS + R60k feedstock + R30k reclaimer scales/PPE).",
        )

    # 1-Shift Single-Mold Capacity: 12 covers/day * 22 workdays = 264 units/month
    single_shift_max_monthly_units = 264
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
        seed_payback_months = round(seed_capital_ask_zar / monthly_net_profit_zar, 1)
        payback_text = f"{seed_payback_months} Months"
    else:
        seed_payback_months = 999
        payback_text = "Increase SOM Units"

    # Triple-Bottom-Line (TBL) Metrics
    annual_ldpe_diverted_tonnes = round(
        (annual_som_units * ldpe_waste_used_kg) / 1000.0, 1
    )
    annual_bags_diverted_m = round(
        (annual_som_units * plastic_bags_diverted) / 1_000_000.0, 2
    )
    annual_co2e_saved_tonnes = round(annual_ldpe_diverted_tonnes * 2.2, 1)
    reclaimers_onboarded = max(15, int(round(annual_ldpe_diverted_tonnes * 1.8, 0)))
    reclaimer_income_injected_zar = int(round(annual_ldpe_diverted_tonnes * 1000 * 3.8, 0))

    # Row 1: 4 Wide Financial & Operational KPIs
    b1, b2, b3, b4 = st.columns(4)
    b1.metric(
        "1. Monthly Break-Even Volume",
        f"{breakeven_units_monthly} units / mo",
        delta=f"Only {daily_breakeven_units} covers/day ({breakeven_units_annual:,}/yr)",
    )
    b2.metric(
        "2. R280k Seed Payback Time",
        payback_text,
        delta=f"Recovers full R{int(seed_capital_ask_zar):,} Seed Ask",
    )
    b3.metric(
        "3. Monthly Net Profit (at SOM)",
        f"R{int(monthly_net_profit_zar):,} / mo",
        delta=f"R{annual_net_profit_zar / 1_000_000:.2f}M annual net profit",
    )
    b4.metric(
        "4. 1-Mold Machine Utilization",
        f"{som_capacity_utilization_pct}% at SOM",
        delta=f"Uses {int(monthly_units_sold)} of {single_shift_max_monthly_units} max units/mo",
    )

    # Row 2: 3 Wide Triple-Bottom-Line (People, Planet, Carbon) Impact Cards
    e1, e2, e3 = st.columns(3)
    e1.metric(
        "👷 PEOPLE: Frontline Reclaimers Empowered",
        f"{reclaimers_onboarded} Waste Reclaimers",
        delta=f"R{reclaimer_income_injected_zar:,}/yr paid directly @ R3.80/kg",
    )
    e2.metric(
        "♻️ PLANET: Annual Code 4 rLDPE Diverted",
        f"{annual_ldpe_diverted_tonnes} Tonnes / year",
        delta=f"Equals ~{annual_bags_diverted_m} Million plastic bags/yr",
    )
    e3.metric(
        "🌍 CARBON: Annual Emissions Avoided",
        f"{annual_co2e_saved_tonnes} Tonnes CO₂e / year",
        delta="Replaces foundry cast iron & virgin resin",
    )

    st.markdown(
        f'<div class="story-box">'
        f"<b>📖 How to Read Tab 3 (Why Our Lean R{int(seed_capital_ask_zar):,} SCAMPER Ask Is De-Risked):</b><br>"
        f"• <b>Monthly Operational Break-Even ({breakeven_units_monthly} units/month = {daily_breakeven_units} covers/day):</b> Because we use a gas-heated drum mixer and 1 welded mold in a R16k/mo Waltloo/Silverton bay, "
        f"our fixed OPEX is only <b>R{int(monthly_fixed_opex_zar):,}/month</b>. Selling just <b>{breakeven_units_monthly} covers/month</b> covers 100% of monthly operating costs—meaning our 2 contracted township projects alone (75 units/mo) already make the plant profitable!<br>"
        f"• <b>Full R{int(seed_capital_ask_zar):,} Seed Capital Payback ({payback_text}):</b> At our SOM run-rate of <b>{int(monthly_units_sold)} units/month</b>, "
        f"we generate <b>R{int(monthly_net_profit_zar):,}/month in pure net profit</b>, paying back the entire <b>R{int(seed_capital_ask_zar):,} seed investment in {payback_text}</b>."
        f"</div>",
        unsafe_allow_html=True,
    )

    ch_col1, ch_col2 = st.columns([1.35, 1.0])

    with ch_col1:
        unit_range = list(range(0, 276, 15))
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
                name="Monthly Total Cost (Lean Fixed OPEX + Variable Cost)",
                line=dict(color="#ef4444", width=3, dash="dash"),
            )
        )
        fig_be.add_vline(
            x=breakeven_units_monthly,
            line_dash="dot",
            line_color="#1e40af",
            annotation_text=f"Break-Even: {breakeven_units_monthly} units/mo (3/day)",
            annotation_position="top left",
        )
        fig_be.add_vline(
            x=monthly_units_sold,
            line_dash="solid",
            line_color="#15803d",
            annotation_text=f"Your SOM: {int(monthly_units_sold)} units/mo",
            annotation_position="bottom right",
        )
        fig_be.add_vline(
            x=single_shift_max_monthly_units,
            line_dash="dashdot",
            line_color="#9333ea",
            annotation_text="1-Mold Max (264/mo)",
            annotation_position="top right",
        )
        fig_be.update_layout(
            title="Monthly Break-Even Analysis (Green Line Above Red Dashed Line = Profit!)",
            xaxis_title="600×600mm Units Sold per Month (Silverton Hub)",
            yaxis_title="ZAR per Month (Excl. 15% VAT)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            height=410,
        )
        st.plotly_chart(fig_be, use_container_width=True)

    with ch_col2:
        st.markdown(f"#### 💰 Single-Tier Seed Capital Ask: R{int(seed_capital_ask_zar):,}")
        df_seed = pd.DataFrame(
            [
                {
                    "Use of Proceeds Bucket": "1. SCAMPER Tech & 1 Welded Mold (43%)",
                    "Allocation (ZAR)": f"R{int(round(seed_capital_ask_zar * 0.4286, -3)):,}",
                    "Verified Items": "80 RPM silage chaff shredder (R15k), gas-heated 350L drum/pot mixer (R22k), 100T press (R43k), 1 welded 600×600mm mold (R28k), fume hood (R12k).",
                },
                {
                    "Use of Proceeds Bucket": "2. Hub Setup & SANS 1882 Test (25%)",
                    "Allocation (ZAR)": f"R{int(round(seed_capital_ask_zar * 0.25, -3)):,}",
                    "Verified Items": "Waltloo/Silverton 245m² bay deposit/rent (R32k), SABS Groenkloof SANS 1882 load test (R25k), LPG gas cage & hookup (R13k).",
                },
                {
                    "Use of Proceeds Bucket": "3. Feedstock & Lock Stock (21%)",
                    "Allocation (ZAR)": f"R{int(round(seed_capital_ask_zar * 0.2143, -3)):,}",
                    "Verified Items": "First 140 units of Code 4 rLDPE film from reclaimers, dry silica sand, chopped fiberglass, MAPE & pentagon cam-locks.",
                },
                {
                    "Use of Proceeds Bucket": "4. Reclaimer Scales & PPE (11%)",
                    "Allocation (ZAR)": f"R{int(round(seed_capital_ask_zar * 0.1071, -3)):,}",
                    "Verified Items": "500kg digital platform scale, heat PPE for 25 reclaimers & operators, and instant USSD/SMS payout system.",
                },
            ]
        )
        st.table(df_seed)
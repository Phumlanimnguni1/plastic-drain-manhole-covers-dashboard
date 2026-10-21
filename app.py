import os
import math
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION (Prevent Text Cut-Off with Clean CSS Sizing)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="PlastiNoxa | Solid 8-Stud Interlocking Eco-Block Simulator",
    page_icon="♻️",
    layout="wide",
)

st.markdown(
    """
    <style>
    div[data-testid="stMetricValue"] {font-size: 1.6rem !important;}
    .status-badge {padding:12px 18px; border-radius:8px; font-weight:700; font-size:0.98rem; margin-bottom:14px; display:block;}
    .story-box {background-color:#eff6ff; border-left:5px solid #2563eb; padding:12px 16px; border-radius:6px; margin-bottom:14px; color:#1e293b; font-size:0.95rem;}
    .innovation-card {background-color:#f8fafc; border-left:5px solid #0f766e; padding:14px; border-radius:6px; margin-bottom:10px; color:#1e293b;}
    .commercial-card {background-color:#f0fdf4; border-left:5px solid #15803d; padding:14px; border-radius:6px; margin-bottom:10px; color:#1e293b;}
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 2. SESSION STATE INITIALIZATION (33% GROSS MARGIN & R270,000 SEED CAPITAL)
# -----------------------------------------------------------------------------
defaults = {
    "fiberglass_pct": 10,
    "wall_thickness_mm": 32,
    "contracted_pallets_mo": 50,
    "loi_pallets_mo": 20,
    "monthly_fixed_opex_zar": 36000,
    "seed_capital_ask_zar": 270000,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# -----------------------------------------------------------------------------
# 3. HEADER & 4 COMPACT TABS (Fits Full Screen Without Scroll Arrows)
# -----------------------------------------------------------------------------
st.title("♻️ PlastiNoxa: 500×245×110mm Solid 8-Stud Interlocking Eco-Block")
st.markdown(
    "**Silverton (East Pretoria) Hub | SANS 1215 & Agrément SA Aligned | Code 5 rPP (3,000 Milk Bottle Caps/Block @ R4.00/kg to Reclaimers)**"
)

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🛠️ Tab 1: Engineering & 33% Margin",
        "🎯 Tab 2: Market & 105-Brick Pallets",
        "🏭 Tab 3: R270k Seed & 6-Mo Roadmap",
        "📊 Tab 4: Self-Service Analytics",
    ]
)

# =============================================================================
# TAB 1: SOLID 8-STUD BLOCK ENGINEERING & 33% GROSS MARGIN PRICING
# =============================================================================
with tab1:
    st.subheader(
        "1. Solid 8-Stud Eco-Block (500×245×110mm) Formulation, Weather/Fire Defense & 33% Gross Margin Pricing (Excl. VAT)"
    )

    possible_imgs = [
        "Solid 8-Stud Interlocking Eco-Block.png",
        "Solid 8-Stud Interlocking Eco-Block.jpg",
        "Twin-Core Interlocking Construction Eco-Brick.jpg",
    ]
    found_img = next((p for p in possible_imgs if os.path.exists(p)), None)

    if found_img:
        img_col, ctrl_area = st.columns([1.0, 2.2])
        with img_col:
            st.image(
                found_img,
                caption="PlastiNoxa 500×245×110mm Solid 8-Stud Interlocking Eco-Block (15.0 kg | 3,000 Milk Caps)",
                use_container_width=True,
            )
    else:
        ctrl_area = st.container()

    with ctrl_area:
        st.markdown("**💡 Quick-Select SANS 1215 Structural Presets:**")
        p1, p2, p3 = st.columns(3)
        if p1.button("🏠 Single-Storey Wall (≥14 MPa | 13.4kg)", use_container_width=True):
            st.session_state.fiberglass_pct = 4
            st.session_state.wall_thickness_mm = 24
        if p2.button("⭐ Optimal Heavy-Duty (28.8 MPa | 15.0kg)", use_container_width=True):
            st.session_state.fiberglass_pct = 10
            st.session_state.wall_thickness_mm = 32
        if p3.button("🏢 Multi-Storey / Retaining (≥38 MPa | 16.5kg)", use_container_width=True):
            st.session_state.fiberglass_pct = 16
            st.session_state.wall_thickness_mm = 38

        c1, c2 = st.columns(2)
        fiberglass_pct = c1.slider(
            "Glass Fiber & Talc Reinforcement (%) [Optimal: 10%–16%]",
            0, 20, key="fiberglass_pct", step=2,
            help="Cuts thermal expansion by 75% and reinforces the 8 LEGO studs against shear.",
        )
        wall_thickness_mm = c2.slider(
            "Solid Top Deck & Underside Tube Wall Thickness (mm) [Optimal: 32mm]",
            22, 42, key="wall_thickness_mm", step=2,
            help="Wall thickness of solid top deck and underside coupling tubes (500×245×110mm block).",
        )

    rpp_pct = 30
    mapp_uv_fire_pct = 3
    sand_flyash_pct = 100 - rpp_pct - mapp_uv_fire_pct - fiberglass_pct
    reclaimer_rate_per_kg = 4.00  # Human-Centric Co-Creation floor price paid to 40 reclaimers

    # Engineering & Milk Bottle Cap Math (1.5g per milk cap -> 4.50kg rPP = 3,000 milk caps)
    unit_weight_kg = round(8.6 + (wall_thickness_mm * 0.21) - (fiberglass_pct * 0.032), 1)
    rpp_waste_used_kg = round(unit_weight_kg * (rpp_pct / 100.0), 2)
    milk_caps_diverted = int(round((rpp_waste_used_kg * 1000.0) / 1.5, 0))
    compressive_strength_mpa = round(
        (14.5 + (fiberglass_pct * 0.90)) * ((wall_thickness_mm / 28.0) ** 1.45), 1
    )

    # Verified Unit Production Cost (COGS) paying R4.00/kg to Reclaimers:
    # Default (15.0kg, 10% fiber): rPP (4.50kg @ R4.00 = R18.00) + Sand (8.55kg @ R0.35 = R2.99)
    # + Fiberglass/Talc (1.50kg @ R1.40 = R2.10) + MAPP/UV/Fire (R1.41) + Direct Gas/Energy (R1.10) = R25.60
    raw_cost = (
        (unit_weight_kg * 0.30 * reclaimer_rate_per_kg)
        + (unit_weight_kg * (0.67 - fiberglass_pct / 100.0) * 0.35)
        + (unit_weight_kg * (fiberglass_pct / 100.0) * 1.40)
    )
    production_cost_zar = round(raw_cost + 1.41 + 1.10, 2)

    # 33.0% Gross Profit Margin Pricing: Price = COGS / (1 - 0.33) -> R38.21 at default!
    wholesale_price_zar = round(production_cost_zar / (1.0 - 0.33), 2)
    retail_rrp_zar = round(wholesale_price_zar * 1.18, 2)
    unit_profit_zar = round(wholesale_price_zar - production_cost_zar, 2)
    gross_margin_pct = round((unit_profit_zar / wholesale_price_zar) * 100, 1)

    # Verified Cashbuild Benchmarks (Excl. 15% VAT)
    cement_weight = 24.0
    cement_retail_excl = 41.27  # R47.46 Incl. VAT at Cashbuild
    cement_installed = 53.00    # Includes wet mortar & slower bricklaying labor
    weight_saved_pct = round(((cement_weight - unit_weight_kg) / cement_weight) * 100, 1)
    savings_per_m2_wall = int(round((cement_installed - wholesale_price_zar) * 18, 0))

    if compressive_strength_mpa >= 21.0:
        sans_txt = "✅ EXCEEDS SANS 1215 HEAVY STRUCTURAL CLASS (≥ 21 MPa) — Houses, Warehouses & Retaining Walls"
        bg, fg = "#dcfce7", "#166534"
    elif compressive_strength_mpa >= 10.5:
        sans_txt = "✅ PASSES SANS 1215 STRUCTURAL LOAD-BEARING (≥ 10.5 MPa) — Single-Storey Houses & Schools"
        bg, fg = "#dbeafe", "#1e40af"
    else:
        sans_txt = "⚠️ PASSES SANS 1215 NON-LOAD PARTITION (≥ 3.5 MPa) — Interior Partitions Only"
        bg, fg = "#fef9c3", "#854d0e"

    st.markdown(
        f'<div class="status-badge" style="background-color:{bg}; color:{fg};">'
        f"{sans_txt}<br>Strength: {compressive_strength_mpa} MPa | Mix: {rpp_pct}% Code 5 rPP (@ R4.00/kg to Reclaimers), "
        f"{sand_flyash_pct}% Silica Sand/Ash, {fiberglass_pct}% Glass Fiber/Talc, {mapp_uv_fire_pct}% MAPP + UV + Fire Retardant"
        f"</div>",
        unsafe_allow_html=True,
    )

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("1. Factory Cost (COGS)", f"R{production_cost_zar:.2f} / block", f"R{rpp_waste_used_kg * 4:.2f} to Reclaimers (@ R4/kg)")
    k2.metric("2. Direct Hub Price (Excl. VAT)", f"R{wholesale_price_zar:.2f} / block", f"R{unit_profit_zar:.2f} profit ({gross_margin_pct}% Margin)")
    k3.metric("3. Hardware RRP (Excl. VAT)", f"R{retail_rrp_zar:.2f} / block", f"Saves R{savings_per_m2_wall}/m² vs Installed Cement")
    k4.metric("Plastic Waste per Block", f"{rpp_waste_used_kg:.2f} kg Code 5 rPP", f"~{milk_caps_diverted:,} milk bottle caps!")

    st.markdown(
        f'<div class="story-box">'
        f"<b>📖 Tab 1 Executive Summary (Unit Economics & SANS 1215 Performance):</b> Each <b>500×245×110mm Solid 8-Stud Eco-Block</b> "
        f"weighs <b>{unit_weight_kg} kg</b> ({weight_saved_pct}% lighter than a 24 kg cement block), achieves <b>{compressive_strength_mpa} MPa</b> compressive strength, "
        f"and upcycles <b>{rpp_waste_used_kg:.2f} kg of Code 5 rPP (~{milk_caps_diverted:,} milk bottle caps at R4.00/kg)</b>. "
        f"With a factory cost of <b>R{production_cost_zar:.2f}</b> and a Direct Hub Price of <b>R{wholesale_price_zar:.2f} (Excl. VAT)</b>, "
        f"the unit generates <b>R{unit_profit_zar:.2f} gross profit ({gross_margin_pct}% gross margin)</b> while undercutting Cashbuild's bare 24 kg block "
        f"(<b>R{cement_retail_excl:.2f} Excl. VAT</b>) and saving builders <b>R{savings_per_m2_wall} per m² of installed wall</b>."
        f"</div>",
        unsafe_allow_html=True,
    )

    df_comp = pd.DataFrame(
        [
            {
                "Block Type": "PlastiNoxa 500×245×110mm Eco-Block",
                "Factory Cost": production_cost_zar,
                "Direct / Retail Block Price": wholesale_price_zar,
                "Installed Cost (incl. Mortar)": retail_rrp_zar,
                "Strength (MPa)": compressive_strength_mpa,
                "Weight (kg)": unit_weight_kg,
            },
            {
                "Block Type": "Cashbuild 500×245×110mm Heavy Block",
                "Factory Cost": 31.50,
                "Direct / Retail Block Price": 41.27,
                "Installed Cost (incl. Mortar)": 53.00,
                "Strength (MPa)": 14.0,
                "Weight (kg)": 24.0,
            },
            {
                "Block Type": "Cashbuild 450×140×220mm Sandstone",
                "Factory Cost": 20.50,
                "Direct / Retail Block Price": 26.43,
                "Installed Cost (incl. Mortar)": 35.00,
                "Strength (MPa)": 10.5,
                "Weight (kg)": 19.5,
            },
        ]
    )

    ch1, ch2 = st.columns(2)
    with ch1:
        fig1 = go.Figure()
        for col_name, color in [
            ("Factory Cost", "#0f766e"),
            ("Direct / Retail Block Price", "#14b8a6"),
            ("Installed Cost (incl. Mortar)", "#f59e0b"),
        ]:
            fig1.add_trace(
                go.Bar(
                    name=col_name,
                    x=df_comp["Block Type"],
                    y=df_comp[col_name],
                    marker_color=color,
                    text=df_comp[col_name].apply(lambda x: f"R{x:.2f}"),
                    textposition="auto",
                )
            )
        fig1.update_layout(
            title="500×245×110mm Pricing Ladder vs. Cashbuild (ZAR Excl. VAT)",
            barmode="group",
            yaxis_title="ZAR per Block (Excl. VAT)",
            legend=dict(orientation="h", y=1.12),
            height=370,
        )
        st.plotly_chart(fig1, use_container_width=True)

    with ch2:
        fig2 = go.Figure()
        fig2.add_trace(
            go.Bar(
                name="Strength (MPa)",
                x=df_comp["Block Type"],
                y=df_comp["Strength (MPa)"],
                marker_color="#2563eb",
                text=df_comp["Strength (MPa)"].apply(lambda x: f"{x} MPa"),
                textposition="auto",
            )
        )
        fig2.add_trace(
            go.Bar(
                name="Weight (kg)",
                x=df_comp["Block Type"],
                y=df_comp["Weight (kg)"],
                marker_color="#64748b",
                text=df_comp["Weight (kg)"].apply(lambda x: f"{x} kg"),
                textposition="auto",
            )
        )
        fig2.add_hline(y=10.5, line_dash="dash", line_color="#1e40af", annotation_text="SANS 1215 House Wall (10.5 MPa)")
        fig2.add_hline(y=21.0, line_dash="solid", line_color="#dc2626", annotation_text="SANS 1215 Heavy Class (21 MPa)")
        fig2.update_layout(
            title="Compressive Strength (MPa) & Weight (kg) vs. SANS 1215",
            barmode="group",
            yaxis_title="MPa / kg",
            legend=dict(orientation="h", y=1.12),
            height=370,
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("🛡️ Structural Reinforcement Against Fire, Sun, Thermal Expansion & Drops")
    d1, d2, d3, d4 = st.columns(4)
    d1.markdown(
        '<div class="innovation-card"><h4>🔥 1. Fire & Heat Shield</h4>'
        "<p><b>57% non-combustible silica sand/ash</b> + <b>APP/ATH flame retardant</b> forms a self-extinguishing ceramic char barrier (SANS 10177-2 / 428 aligned).</p></div>",
        unsafe_allow_html=True,
    )
    d2.markdown(
        '<div class="innovation-card"><h4>🌡️ 2. Anti-Expansion Skeleton</h4>'
        "<p><b>57% sand + 10% fiberglass</b> chemically pinned with MAPP cuts thermal expansion by <b>75%</b>, while 0.5mm LEGO stud tolerances absorb day/night heat swings.</p></div>",
        unsafe_allow_html=True,
    )
    d3.markdown(
        '<div class="innovation-card"><h4>☀️ 3. 50-Yr UV & House Safe</h4>'
        "<p><b>UV Carbon Black + HALS</b> blocks sunlight at the outer 0.2mm skin with <0.5% water absorption—suitable for houses & underpinning under <b>Agrément SA</b> norms.</p></div>",
        unsafe_allow_html=True,
    )
    d4.markdown(
        '<div class="innovation-card"><h4>🔨 4. Zero Broken Corners</h4>'
        "<p>Cement blocks suffer 5–8% breakage when dropped off trucks. Our rPP-fiberglass matrix bounces on impact with <b>0% corner breakage</b> + underside conduit cavities.</p></div>",
        unsafe_allow_html=True,
    )

# =============================================================================
# TAB 2: MARKET OPPORTUNITY & STANDARDIZED 105-BRICK PALLET BUNDLES
# =============================================================================
with tab2:
    st.subheader("2. Commercial Opportunity (SA / 3 Gauteng Metros / Silverton SOM) & Standardized 105-Brick Pallet Bundles")

    BPP = 105  # Industry standard 105 bricks per pallet (Cem Brick SA benchmark)

    sc1, sc2 = st.columns(2)
    contracted_pallets_mo = sc1.slider(
        "1. Contracted Township & Local Builders (Pallets / Month) [Default: 50 Pallets = 5,250 Bricks]",
        10, 100, key="contracted_pallets_mo", step=5,
        help="Each pallet contains 105 bricks (builds 5.8 m² of wall). 50 pallets/mo is just 3 local building projects.",
    )
    loi_pallets_mo = sc2.slider(
        "2. Secured LOI Pipeline — Estates, Schools & Warehouses (Pallets / Month) [Default: 20 Pallets = 2,100 Bricks]",
        5, 80, key="loi_pallets_mo", step=5,
        help="3 Letters of Intent from Pretoria East security estates, school extensions, and Silverton industrial walls.",
    )

    total_pallets_mo = contracted_pallets_mo + loi_pallets_mo
    monthly_units_sold = total_pallets_mo * BPP
    annual_som_units = monthly_units_sold * 12
    wall_area_m2_monthly = int(round(monthly_units_sold / 18.0, 0))

    pallet_price_zar = wholesale_price_zar * BPP
    contracted_rev_yr = contracted_pallets_mo * BPP * 12 * wholesale_price_zar
    loi_rev_yr = loi_pallets_mo * BPP * 12 * wholesale_price_zar
    annual_som_revenue_zar = annual_som_units * wholesale_price_zar
    sam_share_pct = round((annual_som_revenue_zar / 340_000_000) * 100, 2)

    # 4 Clean Metrics (Short Main Value so Nothing Truncates with "...")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("South Africa TAM (Excl. VAT)", "R4.80 Billion / yr", "SA Civil Masonry & Block Market")
    m2.metric("3 Gauteng Metros SAM (Excl. VAT)", "R340 Million / yr", "Tshwane, Joburg & Ekurhuleni")
    m3.metric("Full Run-Rate Annual SOM", f"R{annual_som_revenue_zar / 1_000_000:.2f}M / yr", f"{sam_share_pct}% of Gauteng SAM")
    m4.metric("Monthly Volume (105/Pallet)", f"{total_pallets_mo} Pallets / mo", f"{monthly_units_sold:,} bricks ({wall_area_m2_monthly:,} m² wall/mo)")

    st.markdown("#### 📦 Standardized Bulk Pallet Bundles (105 Bricks per Pallet — Same Transparent Price for All Buyers)")
    st.caption(
        f"Modeled on South Africa's industry standard (**105 bricks per pallet** at **R{wholesale_price_zar:.2f}/brick = R{int(round(pallet_price_zar, 0)):,}/pallet Excl. VAT**), "
        "helping builders plan exact pallet quantities for their project size plus our **5% Damaged-Unit Trade-In Guarantee**:"
    )

    df_bundles = pd.DataFrame(
        [
            {
                "Project Bundle Name": "📦 1-Pallet Starter Bundle",
                "Bricks Included (105/Pallet)": "105 Bricks (1 Pallet)",
                "Wall Coverage (18 bricks/m²)": "5.8 m² Wall (Underpinning / Small Room)",
                "Flat Unit Price (Excl. VAT)": f"R{wholesale_price_zar:.2f} / brick",
                "Total Bundle Price (Excl. VAT)": f"R{int(round(pallet_price_zar, 0)):,}",
                "Plastic Diverted per Bundle": f"{round(105 * rpp_waste_used_kg, 1)} kg ({milk_caps_diverted * 105:,} milk caps)",
            },
            {
                "Project Bundle Name": "🏗️ 5-Pallet Extension / Boundary Bundle",
                "Bricks Included (105/Pallet)": "525 Bricks (5 Pallets)",
                "Wall Coverage (18 bricks/m²)": "29.2 m² Wall (2-Room Extension / 15m Wall)",
                "Flat Unit Price (Excl. VAT)": f"R{wholesale_price_zar:.2f} / brick",
                "Total Bundle Price (Excl. VAT)": f"R{int(round(pallet_price_zar * 5, 0)):,}",
                "Plastic Diverted per Bundle": f"{round(525 * rpp_waste_used_kg, 1):,} kg ({milk_caps_diverted * 525:,} milk caps)",
            },
            {
                "Project Bundle Name": "🏢 10-Pallet Full House / Warehouse Bundle",
                "Bricks Included (105/Pallet)": "1,050 Bricks (10 Pallets)",
                "Wall Coverage (18 bricks/m²)": "58.3 m² Wall (Full House / Warehouse Partition)",
                "Flat Unit Price (Excl. VAT)": f"R{wholesale_price_zar:.2f} / brick",
                "Total Bundle Price (Excl. VAT)": f"R{int(round(pallet_price_zar * 10, 0)):,}",
                "Plastic Diverted per Bundle": f"{round(1050 * rpp_waste_used_kg, 1):,} kg ({milk_caps_diverted * 1050:,} milk caps)",
            },
        ]
    )
    st.table(df_bundles)

    l_col, r_col = st.columns([1.35, 1.0])
    with l_col:
        st.markdown("#### 🎯 Target Addressable Market Table (Excl. 15% VAT)")
        df_tam = pd.DataFrame(
            [
                {
                    "Market Tier": "TAM (South Africa)",
                    "Annual Value": "R4.80 Billion",
                    "Verified Market Scope": "Total SA heavy concrete blocks, retaining walls & structural masonry (SANS 1215).",
                },
                {
                    "Market Tier": "SAM (3 Gauteng Metros)",
                    "Annual Value": "R340 Million",
                    "Verified Market Scope": "Tshwane, Johannesburg & Ekurhuleni commercial builds & 10% green-procurement tenders.",
                },
                {
                    "Market Tier": "SOM (Full Run-Rate Target)",
                    "Annual Value": f"R{annual_som_revenue_zar / 1_000_000:.2f} Million",
                    "Verified Market Scope": (
                        f"3 contracted Mamelodi/Silverton builders ({contracted_pallets_mo} pallets/mo = R{contracted_rev_yr / 1_000_000:.2f}M/yr) "
                        f"+ 3 Pretoria East estate/warehouse LOIs ({loi_pallets_mo} pallets/mo = R{loi_rev_yr / 1_000_000:.2f}M/yr)."
                    ),
                },
            ]
        )
        st.table(df_tam)

    with r_col:
        st.markdown("#### 🤝 Customer Profile & Circular Trade-In Value")
        st.markdown(
            f'<div class="commercial-card"><b>🎯 Target Customer:</b> NHBRC/CIDB contractors, Mamelodi developers, Pretoria East estates & Silverton warehouses ordering in 105-brick pallets (hub walk-in or online website).</div>'
            f'<div class="commercial-card"><b>💊 Pain Relieved:</b> 37.5% lighter than 24kg Cashbuild blocks; 0% broken corners when dropped; dry-stack LEGO lock saves R{savings_per_m2_wall}/m² in mortar & labor.</div>'
            f'<div class="commercial-card"><b>♻️ 5% Damaged-Unit Trade-In:</b> Customers return any damaged block for 5% (R{wholesale_price_zar * 0.05:.2f}) off a new block—recovering R{raw_cost:.2f} of pre-compounded raw material for our shredder!</div>',
            unsafe_allow_html=True,
        )

# =============================================================================
# TAB 3: R270K SEED CAPITAL, 6-MONTH PHASED ROADMAP & REALISTIC PAYBACK
# =============================================================================
with tab3:
    st.subheader("3. R270,000 Seed Capital, 6-Month Phased Execution (Sales Starting Month 3) & Realistic Payback")

    fc1, fc2 = st.columns(2)
    monthly_fixed_opex_zar = fc1.slider(
        "Silverton Monthly Fixed OPEX: Rent (R15.9k) + 2 Factory Workers (R13k) + Gas/Power (R5.6k) + Analytics (R1.5k) [Default: R36,000]",
        25000, 80000, key="monthly_fixed_opex_zar", step=2000,
    )
    seed_capital_ask_zar = fc2.slider(
        "Single-Tier Seed Capital Ask (ZAR) — Includes Worker & Reclaimer PPE + Analytics Setup [Target: R270,000]",
        220000, 350000, key="seed_capital_ask_zar", step=5000,
    )

    single_shift_max = 11025  # 105 pallets/month max (500 bricks/day)
    som_util_pct = round((monthly_units_sold / single_shift_max) * 100, 1)
    breakeven_units_mo = math.ceil(monthly_fixed_opex_zar / unit_profit_zar)
    breakeven_pallets_mo = round(breakeven_units_mo / BPP, 1)
    daily_be_units = math.ceil(breakeven_units_mo / 22.0)

    monthly_rev_zar = monthly_units_sold * wholesale_price_zar
    monthly_var_zar = monthly_units_sold * production_cost_zar
    monthly_net_profit = monthly_rev_zar - monthly_var_zar - monthly_fixed_opex_zar
    annual_net_profit = monthly_net_profit * 12

    # Realistic Payback Period: Includes 2.0 Months of Zero-Sales Setup/SABS Testing + Production Months from Month 3
    if monthly_net_profit > 0:
        prod_months_to_recover = round(seed_capital_ask_zar / monthly_net_profit, 1)
        total_calendar_payback_months = round(2.0 + prod_months_to_recover, 1)
        payback_text = f"{total_calendar_payback_months} Months (Month 7)"
        payback_delta = f"2m Setup/Test + {prod_months_to_recover}m Sales"
    else:
        payback_text = "Increase SOM"
        payback_delta = "Below monthly break-even"

    monthly_rpp_t = round((monthly_units_sold * rpp_waste_used_kg) / 1000.0, 1)
    annual_rpp_t = round((annual_som_units * rpp_waste_used_kg) / 1000.0, 1)
    annual_caps_m = round((annual_som_units * milk_caps_diverted) / 1_000_000.0, 1)
    annual_co2e_t = round(annual_rpp_t * 1.85, 1)
    reclaimer_pay_yr = int(round(annual_rpp_t * 1000 * reclaimer_rate_per_kg, 0))

    # Row 1: 4 Clean Metrics (Zero Text Truncation!)
    b1, b2, b3, b4 = st.columns(4)
    b1.metric("1. Monthly Break-Even", f"{breakeven_pallets_mo} Pallets / mo", f"{breakeven_units_mo:,} bricks ({daily_be_units}/day)")
    b2.metric("2. Total Payback (from Day 1)", payback_text, payback_delta)
    b3.metric("3. Full SOM Net Profit", f"R{int(monthly_net_profit):,} / mo", f"R{annual_net_profit / 1_000_000:.2f}M/yr at {total_pallets_mo} pallets/mo")
    b4.metric("4. 1-Shift Line Utilization", f"{som_util_pct}% at SOM", f"{total_pallets_mo} of 105 max pallets/mo")

    # Row 2: 3 Triple-Bottom-Line Metrics
    e1, e2, e3 = st.columns(3)
    e1.metric(
        "👷 PEOPLE: 40 Reclaimers (@ R4/kg) + 2 Factory Staff",
        f"R{reclaimer_pay_yr:,} / yr",
        "Paid to reclaimers (@ R4/kg) + 2 salaried staff (R6.5k/mo each)",
    )
    e2.metric(
        "♻️ PLANET: Code 5 rPP Diverted (Full Run-Rate)",
        f"{annual_rpp_t} Tonnes / yr",
        f"{monthly_rpp_t}t/mo (~{annual_caps_m} Million milk bottle caps/yr)",
    )
    e3.metric(
        "🌍 CARBON: Annual Emissions Avoided",
        f"{annual_co2e_t} Tonnes CO₂e / yr",
        "Replaces high-emission 24kg Portland cement blocks",
    )

    bc1, bc2 = st.columns([1.2, 1.15])
    with bc1:
        u_rng = list(range(0, 11551, 1050))
        fig_be = go.Figure()
        fig_be.add_trace(go.Scatter(x=u_rng, y=[u * wholesale_price_zar for u in u_rng], mode="lines+markers", name="Monthly Revenue (33% Margin)", line=dict(color="#0d9488", width=3)))
        fig_be.add_trace(go.Scatter(x=u_rng, y=[monthly_fixed_opex_zar + (u * production_cost_zar) for u in u_rng], mode="lines+markers", name="Monthly Total Cost (OPEX + COGS)", line=dict(color="#ef4444", width=3, dash="dash")))
        fig_be.add_vline(x=breakeven_units_mo, line_dash="dot", line_color="#1e40af", annotation_text=f"Break-Even: {breakeven_units_mo:,}/mo ({breakeven_pallets_mo} pallets)")
        fig_be.add_vline(x=monthly_units_sold, line_dash="solid", line_color="#15803d", annotation_text=f"SOM: {monthly_units_sold:,}/mo ({total_pallets_mo} pallets)")
        fig_be.update_layout(title="Monthly Break-Even Analysis (Once Commercial Sales Start in Month 3)", xaxis_title="Bricks Sold / Month", yaxis_title="ZAR / Month (Excl. VAT)", legend=dict(orientation="h", y=1.12), height=390)
        st.plotly_chart(fig_be, use_container_width=True)

    with bc2:
        st.markdown(f"#### 💰 Data-Driven Seed Capital Allocation (Total: R{int(seed_capital_ask_zar):,})")
        sf = seed_capital_ask_zar / 270000.0
        df_seed = pd.DataFrame(
            [
                {
                    "Seed Allocation Bucket": "1. SCAMPER Tech & 8-Stud Mold (45.7%)",
                    "Cost (ZAR)": f"R{int(round(123450 * sf, 0)):,}",
                    "Verified Items Included": "80 RPM silage cutter (R15k), 350L gas drum mixer & bath (R29.5k), Adendorff 100T press (R42,950), 2-cavity 8-stud mold (R36k).",
                },
                {
                    "Seed Allocation Bucket": "2. Waltloo Lease, SANS Test & Backup (25.4%)",
                    "Cost (ZAR)": f"R{int(round(68500 * sf, 0)):,}",
                    "Verified Items Included": "320 Kuit St Waltloo 245m² deposit + rent (R31,850), fume hood (R12,650), SABS SANS 1215 test (R18,500), gas backup (R5,500).",
                },
                {
                    "Seed Allocation Bucket": "3. R4/kg Feedstock + 2 Worker Salaries (19.6%)",
                    "Cost (ZAR)": f"R{int(round(53000 * sf, 0)):,}",
                    "Verified Items Included": "7.0T Code 5 rPP paid to 40 reclaimers @ R4.00/kg (R28k) + sand/fiber/additives (R12k) + Month-1 salaries for 2 workers (R13k).",
                },
                {
                    "Seed Allocation Bucket": "4. Worker & Reclaimer PPE + Analytics (9.3%)",
                    "Cost (ZAR)": f"R{int(round(25050 * sf, 0)):,}",
                    "Verified Items Included": "PPE for 2 factory workers (R4,500) + PPE for 40 reclaimers (R11,550) + 500kg scale (R2,500) + Analytics setup/hosting (R6,500).",
                },
            ]
        )
        st.table(df_seed)

    st.markdown("#### 🗓️ 6-Month Phased Seed Capital Deployment & Cash-Flow Roadmap (Sales Launching in Month 3)")
    m3_4_pallets = int(round(total_pallets_mo * 0.60, 0))  # Avg 42 pallets/mo during M3-M4 ramp-up
    m3_4_rev = int(round(m3_4_pallets * pallet_price_zar, 0))
    df_roadmap = pd.DataFrame(
        [
            {
                "Timeline Phase": "Months 1 – 2: Setup, Tooling & SABS Testing",
                "Seed Capital Spent": f"R{int(round(165000 * sf, 0)):,} (61%)",
                "Key Activities Completed": "Secure 245m² Waltloo bay; install chaff cutter, gas drum mixer, 100T press & 8-stud mold; mold test batch & pass SABS SANS 1215 lab test.",
                "Monthly Sales Volume": "0 Pallets (Testing Phase)",
                "How Money Flows Through System": "100% Seed Investment Outflow: Seed capital covers rent, 2 factory workers, equipment, and SABS testing while revenue is R0.",
            },
            {
                "Timeline Phase": "Months 3 – 4: Commercial Launch & Break-Even",
                "Seed Capital Spent": f"R{int(round(75000 * sf, 0)):,} (28%)",
                "Key Activities Completed": "Onboard 40 reclaimers (@ R4/kg); launch website & hub sales; deliver first pilot pallets to contracted Mamelodi/Silverton builders.",
                "Monthly Sales Volume": f"35 → 50 Pallets/mo (Passes {breakeven_pallets_mo} BE!)",
                "How Money Flows Through System": f"50% Customer Deposits Kick In: Sales cross our {breakeven_pallets_mo}-pallet monthly break-even in Month 3 (~R{m3_4_rev:,}/mo revenue).",
            },
            {
                "Timeline Phase": "Months 5 – 6: Full SOM Run-Rate & Payback",
                "Seed Capital Spent": f"R{int(round(30000 * sf, 0)):,} (11%)",
                "Key Activities Completed": "Scale to full SOM (70 pallets/mo across contractors, estates & website); activate 5% damaged-unit trade-in loop & EPR credits.",
                "Monthly Sales Volume": f"{total_pallets_mo} Pallets/mo ({monthly_units_sold:,} bricks)",
                "How Money Flows Through System": f"Self-Sustaining Profit Engine: Generates R{int(monthly_rev_zar):,}/mo revenue and +R{int(monthly_net_profit):,}/mo net profit—completing full seed payback in Month 7 ({total_calendar_payback_months} mos)!",
            },
        ]
    )
    st.table(df_roadmap)

# =============================================================================
# TAB 4: SELF-SERVICE OPERATIONAL & BUSINESS ANALYTICS (NO SQL REQUIRED)
# =============================================================================
with tab4:
    st.subheader("4. Self-Service Director Analytics: Live Operational Metrics, Online Sales & 1-Click Ad-Hoc Explorer")

    col_op, col_biz = st.columns(2)

    with col_op:
        st.markdown("##### ⚙️ Operational Analytics (Live Factory & Yard Health)")
        returned_bricks_mo = int(round(monthly_units_sold * 0.05, 0))
        net_trade_in_savings_mo = int(round(returned_bricks_mo * (raw_cost - wholesale_price_zar * 0.05), 0))

        op1, op2 = st.columns(2)
        op1.metric("Live Yard Pallet Inventory", "16 Pallets", "1,680 bricks (2.2 days stock buffer)")
        op2.metric("Reclaimer rPP Stockpile", "6.8 Tonnes", "Bought @ R4.00/kg (4.5d stock ready)")
        op3, op4 = st.columns(2)
        op3.metric("2-Worker Daily Output", f"{math.ceil(monthly_units_sold / 22)} bricks / day", "99.4% Quality Pass | 0% Broken Corners")
        op4.metric("5% Trade-Ins Re-Shredded", f"{returned_bricks_mo} bricks / mo", f"Saves R{net_trade_in_savings_mo:,}/mo in raw material")

    with col_biz:
        st.markdown("##### 📈 Business Analytics (Revenue, Website Orders & Margins)")
        online_pallets_mo = int(round(total_pallets_mo * 0.26, 0))
        online_rev_mo = int(round(online_pallets_mo * pallet_price_zar, 0))
        epr_subsidy_mo = int(round(monthly_units_sold * rpp_waste_used_kg * 1.20, 0))

        bz1, bz2 = st.columns(2)
        bz1.metric("Full SOM Monthly Revenue", f"R{int(monthly_rev_zar):,} / mo", f"{total_pallets_mo} Pallets ({monthly_units_sold:,} bricks)")
        bz2.metric("🌐 Online Website Sales", f"R{online_rev_mo:,} / mo", f"{online_pallets_mo} Pallets (26% via plastinoxa.co.za)")
        bz3, bz4 = st.columns(2)
        bz3.metric("Resilient Gross Margin", f"{gross_margin_pct}% Margin", f"R{unit_profit_zar:.2f} gross profit / brick")
        bz4.metric("Section 18 EPR Subsidy", f"+R{epr_subsidy_mo:,} / mo", "+R1.20/kg PRO credit on Code 5 rPP")

    st.divider()

    st.markdown("#### 🔍 1-Click Self-Service Sales Explorer & Ad-Hoc Issue Investigator (No SQL Required)")
    st.caption("Click any button below to aggregate sales by **Day of the Week**, **Week**, or **Month (Showing Months 1–2 Setup & Month 3 Launch)**, and filter by **Sales Channel**:")

    flt1, flt2 = st.columns([1.4, 1.0])
    time_view = flt1.radio(
        "1. Click to Aggregate Time Period:",
        [
            "📅 Daily View (Which Day of the Week Sells Most?)",
            "📊 Weekly View (Spot Weekly Dips & Load-Shedding Impact)",
            "📈 Monthly View (6-Month Rollout: M1–M2 Testing → M3 Launch)",
        ],
        horizontal=True,
    )
    channel_view = flt2.radio(
        "2. Click to Filter Sales Channel:",
        ["All Channels", "Direct Silverton Hub", "Online Website (plastinoxa.co.za)"],
        horizontal=True,
    )

    if "Daily" in time_view:
        x_labels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        hub_vals = [12, 9, 4, 10, 14, 3]
        web_vals = [4, 3, 2, 3, 4, 2]
        chart_title = "Ad-Hoc Investigation: Average Pallets Sold by Day of the Week (Mon–Sat)"
        adhoc_insight = (
            "💡 **Ad-Hoc Discovery (Day-of-Week Pattern):** **Friday (18 pallets) and Monday (16 pallets)** generate **48.6% of weekly sales** "
            "as contractors stock up before weekend and Monday site starts. **Wednesday is our quietest day (6 pallets)**—"
            "**Director Action:** Schedule chaff-cutter blade maintenance and automated Online Website promos for Wednesdays."
        )
    elif "Weekly" in time_view:
        x_labels = ["Week 1", "Week 2", "Week 3 (Stage 4 Load-Shedding)", "Week 4 (Month-End Push)"]
        hub_vals = [14, 15, 9, 14]
        web_vals = [4, 4, 6, 4]
        chart_title = "Ad-Hoc Investigation: Weekly Pallet Sales (Spotting the Week 3 Load-Shedding Dip)"
        adhoc_insight = (
            "💡 **Ad-Hoc Discovery (Why Did Week 3 Walk-In Sales Dip?):** Drilling into **Week 3** shows walk-in Hub sales dipped from 15 to 9 pallets during Stage 4 load-shedding, "
            "but **Online Website Orders jumped +50% (to 6 pallets)** while our 33% gross margin and 16-pallet yard buffer kept the plant profitable!"
        )
    else:
        x_labels = [
            "Month 1 (Setup & SABS)",
            "Month 2 (SABS & Stockpiling)",
            "Month 3 (Sales Launch!)",
            "Month 4 (Ramp-Up)",
            "Month 5 (Expansion)",
            "Month 6 (Full SOM)",
        ]
        hub_vals = [0, 0, 26, 37, 45, 52]
        web_vals = [0, 0, 9, 13, 15, 18]
        chart_title = "Executive Report: 6-Month Phased Rollout (M1–M2 Testing → M3 Commercial Launch → M6 Full SOM)"
        adhoc_insight = (
            f"💡 **Executive Summary (6-Month Rollout):** In **Months 1–2**, commercial sales are **0 pallets** while we complete Waltloo setup and SABS SANS 1215 testing. "
            f"Sales launch in **Month 3 at 35 pallets** (immediately passing our **{breakeven_pallets_mo}-pallet monthly break-even**!) and scale to **70 pallets/month "
            f"(R{int(monthly_rev_zar):,}/mo)** by Month 6, achieving full R{int(seed_capital_ask_zar):,} seed payback in **Month 7 ({total_calendar_payback_months} months)**."
        )

    st.info(adhoc_insight)

    fig_adhoc = go.Figure()
    if channel_view in ["All Channels", "Direct Silverton Hub"]:
        fig_adhoc.add_trace(
            go.Bar(
                name="Direct Silverton Hub Pallets",
                x=x_labels,
                y=hub_vals,
                marker_color="#0f766e",
                text=[f"{v} Pallets" if v > 0 else "Setup/Testing" for v in hub_vals],
                textposition="auto",
            )
        )
    if channel_view in ["All Channels", "Online Website (plastinoxa.co.za)"]:
        fig_adhoc.add_trace(
            go.Bar(
                name="Online Website Pallets (plastinoxa.co.za)",
                x=x_labels,
                y=web_vals,
                marker_color="#2563eb",
                text=[f"{v} Pallets" if v > 0 else "" for v in web_vals],
                textposition="auto",
            )
        )
    fig_adhoc.update_layout(
        title=chart_title,
        barmode="stack" if channel_view == "All Channels" else "group",
        yaxis_title="Pallets Sold (105 Bricks / Pallet)",
        legend=dict(orientation="h", y=1.12),
        height=390,
    )
    st.plotly_chart(fig_adhoc, use_container_width=True)

# === END OF COMPLETE APP.PY ===
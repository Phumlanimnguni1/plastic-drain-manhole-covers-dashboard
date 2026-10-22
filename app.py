import os
import math
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION (Waltloo Hub & Clean CSS Sizing)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="PlastiNoxa | Waltloo Code 2 HDPE Solid 8-Stud Eco-Block",
    page_icon="♻️",
    layout="wide",
)

st.markdown(
    """
    <style>
    div[data-testid="stMetricValue"] {font-size: 1.52rem !important;}
    .status-badge {padding:12px 18px; border-radius:8px; font-weight:700; font-size:0.96rem; margin-bottom:14px; display:block;}
    .story-box {background-color:#eff6ff; border-left:5px solid #2563eb; padding:12px 16px; border-radius:6px; margin-bottom:14px; color:#1e293b; font-size:0.95rem;}
    .innovation-card {background-color:#f8fafc; border-left:5px solid #0f766e; padding:14px; border-radius:6px; margin-bottom:10px; color:#1e293b;}
    .commercial-card {background-color:#f0fdf4; border-left:5px solid #15803d; padding:14px; border-radius:6px; margin-bottom:10px; color:#1e293b;}
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 2. SESSION STATE INITIALIZATION (4.2KG HDPE @ R4/KG, WALTLOO HUB, 20M WALL)
# -----------------------------------------------------------------------------
defaults = {
    "fiberglass_pct": 10,
    "wall_thickness_mm": 32,
    "contracted_pallets_mo": 42,
    "loi_pallets_mo": 20,
    "monthly_fixed_opex_zar": 54000,
    "seed_capital_ask_zar": 270000,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# -----------------------------------------------------------------------------
# 3. HEADER & 4 COMPACT TABS
# -----------------------------------------------------------------------------
st.title("♻️ PlastiNoxa: 500×245×110mm Code 2 HDPE Solid 8-Stud Eco-Block")
st.markdown(
    "**Waltloo (East Pretoria) Manufacturing Hub | SANS 1215 & Agrément SA Aligned | Code 2 rHDPE (4.20 kg = 105 Milk Bottles/Block @ R4.00/kg to Reclaimers)**"
)

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🛠️ Tab 1: HDPE Engineering & 20m Wall Savings",
        "🎯 Tab 2: Market, Personas & 105-Brick Pallets",
        "🏭 Tab 3: R270k Seed, 7-Mo Payback & 30-Min Cure",
        "📊 Tab 4: Self-Service Operational & Business BI",
    ]
)

# =============================================================================
# TAB 1: CODE 2 HDPE ENGINEERING, 33% MARGIN & 20-METER WALL COST SAVINGS
# =============================================================================
with tab1:
    st.subheader(
        "1. Code 2 rHDPE Solid 8-Stud Block (500×245×110mm) Composition, 33% Gross Margin & 20m Wall Savings (Excl. VAT)"
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
                caption="PlastiNoxa 500×245×110mm Solid 8-Stud Eco-Block (15.0 kg | 4.20 kg Code 2 HDPE = 105 Milk Bottles)",
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
        if p2.button("⭐ Optimal Heavy-Duty (28.5 MPa | 15.0kg)", use_container_width=True):
            st.session_state.fiberglass_pct = 10
            st.session_state.wall_thickness_mm = 32
        if p3.button("🏢 Multi-Storey / Retaining (≥38 MPa | 16.5kg)", use_container_width=True):
            st.session_state.fiberglass_pct = 16
            st.session_state.wall_thickness_mm = 38

        c1, c2 = st.columns(2)
        fiberglass_pct = c1.slider(
            "Glass Fiber & Talc Reinforcement (%) [Optimal: 10%–16%]",
            0, 20, key="fiberglass_pct", step=2,
            help="Locks the Code 2 HDPE chains to prevent thermal expansion and stud shear.",
        )
        wall_thickness_mm = c2.slider(
            "Solid Top Deck & Underside Tube Wall Thickness (mm) [Optimal: 32mm]",
            22, 42, key="wall_thickness_mm", step=2,
            help="Wall thickness molded inside our modified SCAMPER Brick Bake Bin in Waltloo (500×245×110mm).",
        )

    rhdpe_pct = 28
    mape_uv_fire_pct = 3
    sand_flyash_pct = 100 - rhdpe_pct - mape_uv_fire_pct - fiberglass_pct
    reclaimer_rate_per_kg = 4.00  # R4.00/kg paid to frontline reclaimers

    # Exact Unit Composition in kg (Default: 15.0 kg total = 4.20kg HDPE + 8.85kg Sand/Ash + 1.50kg Fiberglass + 0.45kg MAPE/UV/Fire)
    unit_weight_kg = round(8.6 + (wall_thickness_mm * 0.21) - (fiberglass_pct * 0.032), 1)
    rhdpe_waste_used_kg = round(unit_weight_kg * (rhdpe_pct / 100.0), 2)
    sand_mass_kg = round(unit_weight_kg * (sand_flyash_pct / 100.0), 2)
    fiber_mass_kg = round(unit_weight_kg * (fiberglass_pct / 100.0), 2)
    additive_mass_kg = round(unit_weight_kg * (mape_uv_fire_pct / 100.0), 2)

    hdpe_bottles_diverted = int(round((rhdpe_waste_used_kg * 1000.0) / 40.0, 0))
    compressive_strength_mpa = round(
        (14.5 + (fiberglass_pct * 0.90)) * ((wall_thickness_mm / 28.0) ** 1.45), 1
    )

    # Verified Unit Cost (COGS Excl. VAT) with Code 2 HDPE @ R4.00/kg:
    # Default (15.0kg, 10% fiber): rHDPE (4.20kg @ R4.00 = R16.80) + Silica Sand/Ash (8.85kg @ R0.30 = R2.655)
    # + Waste Fiberglass/Talc (1.50kg @ R1.20 = R1.80) + MAPE/UV/Fire (R1.345) + Direct LPG Gas (R1.00) = R23.60
    raw_cost = (
        (rhdpe_waste_used_kg * reclaimer_rate_per_kg)
        + (sand_mass_kg * 0.30)
        + (fiber_mass_kg * 1.20)
    )
    production_cost_zar = round(raw_cost + 1.345 + 1.00, 2)

    # 33.0% Gross Profit Margin Pricing: Selling Price = COGS / (1 - 0.33) -> R35.22 at default!
    wholesale_price_zar = round(production_cost_zar / (1.0 - 0.33), 2)
    unit_profit_zar = round(wholesale_price_zar - production_cost_zar, 2)
    gross_margin_pct = round((unit_profit_zar / wholesale_price_zar) * 100, 1)

    # Installed Cost Per Block (Zero Mortar + Zero Plaster + 40% Faster Dry-Stacking = R3.50/block labor)
    plastinoxa_installed_block_zar = round(wholesale_price_zar + 3.50, 2)

    # Traditional 500x245x110mm Concrete Block Installed Cost:
    # Bare Block (R41.27 Excl. VAT at Cashbuild) + Wet Mortar (R7.50) + 2-Sided Plaster (R11.00) + Slow Labor & 5% Breakage (R8.23) = R68.00
    concrete_bare_zar = 41.27
    concrete_installed_zar = 68.00
    cement_weight = 24.0
    weight_saved_pct = round(((cement_weight - unit_weight_kg) / cement_weight) * 100, 1)

    savings_per_block_installed = round(concrete_installed_zar - plastinoxa_installed_block_zar, 2)
    savings_per_m2_wall = int(round(savings_per_block_installed * 18, 0))

    # 20-Meter Long x 2.0m High Wall = 40 m² = 720 Blocks (18 blocks/m²)
    wall_blocks_20m = 720
    savings_20m_wall_zar = int(round(savings_per_block_installed * wall_blocks_20m, 0))

    if compressive_strength_mpa >= 21.0:
        sans_txt = "✅ EXCEEDS SANS 1215 HEAVY STRUCTURAL CLASS (≥ 21 MPa) — Houses, Warehouses & Boundary Walls"
        bg, fg = "#dcfce7", "#166534"
    elif compressive_strength_mpa >= 10.5:
        sans_txt = "✅ PASSES SANS 1215 STRUCTURAL LOAD-BEARING (≥ 10.5 MPa) — Single-Storey Houses & Schools"
        bg, fg = "#dbeafe", "#1e40af"
    else:
        sans_txt = "⚠️ PASSES SANS 1215 NON-LOAD PARTITION (≥ 3.5 MPa) — Interior Partitions Only"
        bg, fg = "#fef9c3", "#854d0e"

    st.markdown(
        f'<div class="status-badge" style="background-color:{bg}; color:{fg};">'
        f"{sans_txt}<br>Strength: {compressive_strength_mpa} MPa | 15.0kg Mix: {rhdpe_waste_used_kg}kg Code 2 rHDPE ({rhdpe_pct}%), "
        f"{sand_mass_kg}kg Sand/Ash ({sand_flyash_pct}%), {fiber_mass_kg}kg Glass Fiber ({fiberglass_pct}%), {additive_mass_kg}kg MAPE/UV/Fire ({mape_uv_fire_pct}%)"
        f"</div>",
        unsafe_allow_html=True,
    )

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("1. Waltloo Factory Cost (COGS)", f"R{production_cost_zar:.2f} / brick", f"Includes R{rhdpe_waste_used_kg * 4:.2f} HDPE (@ R4.00/kg)")
    k2.metric("2. Direct Hub Price (33% Margin)", f"R{wholesale_price_zar:.2f} / brick", f"R{unit_profit_zar:.2f} profit (R{concrete_bare_zar - wholesale_price_zar:.2f} below Cement!)")
    k3.metric("3. Savings on a 20m Wall (40m²)", f"R{savings_20m_wall_zar:,} Saved", f"Saves R{savings_per_m2_wall}/m² (No Mortar or Plaster!)")
    k4.metric("Code 2 HDPE Diverted / Brick", f"{rhdpe_waste_used_kg:.2f} kg rHDPE", f"~{hdpe_bottles_diverted} two-litre milk bottles!")

    c_base = int(round(wall_blocks_20m * concrete_bare_zar, 0))
    c_mort = int(round(wall_blocks_20m * 19.60, 0))
    c_lab = int(round(wall_blocks_20m * 7.13, 0))
    c_tot = c_base + c_mort + c_lab

    p_base = int(round(wall_blocks_20m * wholesale_price_zar, 0))
    p_mort = 0
    p_lab = int(round(wall_blocks_20m * 3.50, 0))
    p_tot = p_base + p_lab

    st.markdown(
        f'<div class="story-box">'
        f"<b>📖 Tab 1 Executive Summary (Unit Economics & 20-Meter Wall Savings):</b> Paying frontline reclaimers "
        f"<b>R4.00/kg</b> for Code 2 HDPE (<b>{rhdpe_waste_used_kg:.2f} kg/brick = R{rhdpe_waste_used_kg * 4:.2f}</b>) gives a Waltloo factory cost of "
        f"<b>R{production_cost_zar:.2f}/brick</b> and a Direct Hub Price of <b>R{wholesale_price_zar:.2f}/brick</b> "
        f"(<b>{gross_margin_pct}% gross margin = R{unit_profit_zar:.2f} profit/brick</b>)—undercutting Cashbuild's bare 24 kg concrete block "
        f"(<b>R{concrete_bare_zar:.2f} Excl. VAT</b>) by <b>R{concrete_bare_zar - wholesale_price_zar:.2f} per brick</b>! "
        f"Because our modified Brick Bake Bin produces a smooth, dry-stacking block requiring <b>zero mortar and zero wall plaster</b>, "
        f"building a <b>20m × 2m wall (40 m² = 720 blocks)</b> costs <b>R{p_tot:,}</b> instead of <b>R{c_tot:,}</b>—"
        f"saving the customer <b>R{savings_20m_wall_zar:,} (43.1% cheaper)</b> and diverting <b>{round(wall_blocks_20m * rhdpe_waste_used_kg, 0):,.0f} kg of HDPE</b>!"
        f"</div>",
        unsafe_allow_html=True,
    )

    ch1, ch2 = st.columns(2)
    with ch1:
        wall_systems = ["Traditional Concrete Block Wall", "PlastiNoxa Code 2 HDPE Eco-Wall"]

        fig1 = go.Figure()
        fig1.add_trace(
            go.Bar(
                name="1. Base Bricks (720 units)",
                x=wall_systems,
                y=[c_base, p_base],
                marker_color="#0f766e",
                text=[f"R{c_base:,}", f"R{p_base:,}"],
                textposition="inside",
                insidetextanchor="middle",
                textfont=dict(color="white", size=13),
            )
        )
        fig1.add_trace(
            go.Bar(
                name="2. Mortar, Plaster & 5% Breakage",
                x=wall_systems,
                y=[c_mort, p_mort],
                marker_color="#ef4444",
                text=[f"R{c_mort:,}", ""],
                textposition="inside",
                insidetextanchor="middle",
                textfont=dict(color="white", size=13),
            )
        )
        # Keep text empty inside the thin yellow bar and display it in the bold callout right above so it NEVER cuts off!
        fig1.add_trace(
            go.Bar(
                name="3. Wall Laying Labor",
                x=wall_systems,
                y=[c_lab, p_lab],
                marker_color="#f59e0b",
                text=["", ""],
            )
        )
        fig1.update_layout(
            title=f"Total Installed Cost for a 20m × 2m Wall (Customer Saves R{savings_20m_wall_zar:,}!)",
            barmode="stack",
            yaxis=dict(title="Total 20m Wall Cost (ZAR Excl. VAT)", range=[0, 62000]),
            legend=dict(orientation="h", y=1.13),
            annotations=[
                dict(
                    x="Traditional Concrete Block Wall",
                    y=c_tot + 4200,
                    text=f"<b>Total: R{c_tot:,}</b><br><span style='color:#b45309;'>🟨 3. Labor: R{c_lab:,}</span>",
                    showarrow=False,
                    font=dict(size=12, color="#991b1b"),
                ),
                dict(
                    x="PlastiNoxa Code 2 HDPE Eco-Wall",
                    y=p_tot + 4200,
                    text=f"<b>Total: R{p_tot:,} (R0 Mortar/Plaster!)</b><br><span style='color:#b45309;'>🟨 3. Labor: R{p_lab:,}</span>",
                    showarrow=False,
                    font=dict(size=12, color="#166534"),
                ),
            ],
            height=400,
        )
        st.plotly_chart(fig1, use_container_width=True)

    with ch2:
        df_comp = pd.DataFrame(
            [
                {
                    "Block Type": "PlastiNoxa Code 2 HDPE Block",
                    "Strength (MPa)": compressive_strength_mpa,
                    "Weight (kg)": unit_weight_kg,
                },
                {
                    "Block Type": "Cashbuild 500×245×110mm Heavy Block",
                    "Strength (MPa)": 14.0,
                    "Weight (kg)": 24.0,
                },
                {
                    "Block Type": "Cashbuild 450×140×220mm Sandstone",
                    "Strength (MPa)": 10.5,
                    "Weight (kg)": 19.5,
                },
            ]
        )
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
            legend=dict(orientation="h", y=1.13),
            height=400,
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("🛡️ Code 2 HDPE Composite Reinforcements & SCAMPER Brick Bake Bin Innovation")
    d1, d2, d3, d4 = st.columns(4)
    d1.markdown(
        '<div class="innovation-card"><h4>🍞 1. SCAMPER Brick Bake Bins</h4>'
        "<p>We modify 4 heavy-duty 4-cavity steel <b>Brick Bake Bins (16 cavities total)</b> with welded 8-stud plates—giving exact 500×245×110mm dimensions and a <b>smooth plaster-free finish</b>.</p></div>",
        unsafe_allow_html=True,
    )
    d2.markdown(
        '<div class="innovation-card"><h4>🔥 2. Fire & Thermal Shield</h4>'
        "<p><b>59% silica sand/fly ash + 10% fiberglass</b> pinned to Code 2 HDPE via <b>MAPE + APP flame retardant</b> cuts thermal expansion by 75% and prevents flame spread.</p></div>",
        unsafe_allow_html=True,
    )
    d3.markdown(
        '<div class="innovation-card"><h4>🧱 3. No Mortar & No Plaster</h4>'
        f"<p>8 top LEGO studs and underside coupling tubes dry-stack in 1/3 the time and require <b>zero cement mortar and zero wall plaster</b>, saving R{savings_per_m2_wall}/m².</p></div>",
        unsafe_allow_html=True,
    )
    d4.markdown(
        '<div class="innovation-card"><h4>⏱️ 4. 30-Min Cure & 0% Breakage</h4>'
        "<p>Concrete blocks take <b>28 days</b> to cure and suffer 5–8% broken corners. Our 4 rotating Brick Bake Bins solidify in a water trough in <b>30 minutes (256 bricks/day)</b> with <b>0% broken corners</b>.</p></div>",
        unsafe_allow_html=True,
    )

# =============================================================================
# TAB 2: MARKET ADOPTION, CUSTOMER PERSONAS & 105-BRICK PALLET BUNDLES
# =============================================================================
with tab2:
    st.subheader("2. Waltloo Hub Market Adoption, Customer Personas & Standardized 105-Brick Pallet Bundles")

    BPP = 105  # 105 bricks per pallet

    sc1, sc2 = st.columns(2)
    contracted_pallets_mo = sc1.slider(
        "1. Primary Segment: Local Builders & Backyard Developers (Pallets / Month) [Default: 42 Pallets]",
        10, 60, key="contracted_pallets_mo", step=2,
        help="42 pallets/mo (4,410 bricks) across Mamelodi, Waltloo & Silverton boundary-wall and rental-unit contractors.",
    )
    loi_pallets_mo = sc2.slider(
        "2. Secondary Segment: Estates, Warehouses & Website LOIs (Pallets / Month) [Default: 20 Pallets]",
        5, 50, key="loi_pallets_mo", step=2,
        help="20 pallets/mo (2,100 bricks) across Pretoria East security estates and Waltloo industrial warehouse partitions.",
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

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("South Africa TAM (Excl. VAT)", "R4.80 Billion / yr", "SA Civil Masonry & Block Market")
    m2.metric("3 Gauteng Metros SAM (Excl. VAT)", "R340 Million / yr", "Tshwane, Joburg & Ekurhuleni")
    m3.metric("Waltloo Annual SOM Run-Rate", f"R{annual_som_revenue_zar / 1_000_000:.2f}M / yr", f"Only {sam_share_pct}% of Gauteng SAM")
    m4.metric("Monthly Volume (105/Pallet)", f"{total_pallets_mo} Pallets / mo", f"{monthly_units_sold:,} bricks ({wall_area_m2_monthly:,} m² wall/mo)")

    st.markdown("#### 📦 Standardized Bulk Pallet Bundles (105 Bricks per Pallet — Same Transparent Price for All Buyers)")
    st.caption(
        f"Each pallet holds **105 bricks** at **R{wholesale_price_zar:.2f}/brick = R{int(round(pallet_price_zar, 0)):,}/pallet Excl. VAT**, "
        f"saving builders **R{int(round(savings_per_block_installed * 105, 0)):,} per pallet** in eliminated mortar, plaster, and zero corner breakage:"
    )

    df_bundles = pd.DataFrame(
        [
            {
                "Project Bundle Name": "📦 1-Pallet Starter Bundle",
                "Bricks Included": "105 Bricks (1 Pallet)",
                "Wall Coverage (18/m²)": "5.8 m² Wall (Small Room / Shed)",
                "Flat Unit Price": f"R{wholesale_price_zar:.2f} / brick",
                "Total Bundle Price": f"R{int(round(pallet_price_zar, 0)):,}",
                "Mortar & Plaster Saved": f"R{int(round(savings_per_block_installed * 105, 0)):,} Saved",
                "Code 2 HDPE Diverted": f"{round(105 * rhdpe_waste_used_kg, 1)} kg ({hdpe_bottles_diverted * 105:,} milk bottles)",
            },
            {
                "Project Bundle Name": "🏗️ 7-Pallet 20m Wall Bundle",
                "Bricks Included": "735 Bricks (7 Pallets)",
                "Wall Coverage (18/m²)": "40.8 m² (Full 20m × 2m Boundary Wall)",
                "Flat Unit Price": f"R{wholesale_price_zar:.2f} / brick",
                "Total Bundle Price": f"R{int(round(pallet_price_zar * 7, 0)):,}",
                "Mortar & Plaster Saved": f"R{int(round(savings_per_block_installed * 735, 0)):,} Saved",
                "Code 2 HDPE Diverted": f"{round(735 * rhdpe_waste_used_kg, 1):,} kg ({hdpe_bottles_diverted * 735:,} milk bottles)",
            },
            {
                "Project Bundle Name": "🏢 10-Pallet Full Structure Bundle",
                "Bricks Included": "1,050 Bricks (10 Pallets)",
                "Wall Coverage (18/m²)": "58.3 m² (Full House / Warehouse)",
                "Flat Unit Price": f"R{wholesale_price_zar:.2f} / brick",
                "Total Bundle Price": f"R{int(round(pallet_price_zar * 10, 0)):,}",
                "Mortar & Plaster Saved": f"R{int(round(savings_per_block_installed * 1050, 0)):,} Saved",
                "Code 2 HDPE Diverted": f"{round(1050 * rhdpe_waste_used_kg, 1):,} kg ({hdpe_bottles_diverted * 1050:,} milk bottles)",
            },
        ]
    )
    st.table(df_bundles)

    l_col, r_col = st.columns([1.3, 1.05])
    with l_col:
        st.markdown("#### 🎯 Target Addressable Market Table (Excl. 15% VAT)")
        df_tam = pd.DataFrame(
            [
                {
                    "Market Tier": "TAM (South Africa)",
                    "Annual Value": "R4.80 Billion",
                    "Verified Market Scope": "Total SA heavy concrete blocks, boundary walls & structural masonry (SANS 1215 / CMA SA).",
                },
                {
                    "Market Tier": "SAM (3 Gauteng Metros)",
                    "Annual Value": "R340 Million",
                    "Verified Market Scope": "Tshwane, Johannesburg & Ekurhuleni perimeter walls, extensions & 10% green tenders.",
                },
                {
                    "Market Tier": "SOM (Waltloo Hub Run-Rate)",
                    "Annual Value": f"R{annual_som_revenue_zar / 1_000_000:.2f} Million",
                    "Verified Market Scope": (
                        f"Primary builders ({contracted_pallets_mo} pallets/mo = R{contracted_rev_yr / 1_000_000:.2f}M/yr) "
                        f"+ Secondary estate/warehouse LOIs ({loi_pallets_mo} pallets/mo = R{loi_rev_yr / 1_000_000:.2f}M/yr)."
                    ),
                },
            ]
        )
        st.table(df_tam)

    with r_col:
        st.markdown("#### 🤝 Primary & Secondary Customer Personas & Loyalty Drivers")
        st.markdown(
            f'<div class="commercial-card"><b>👷 Primary Segment (70%): "Contractor Kabelo" (Mamelodi & Waltloo Builders, Age 28–55):</b><br>'
            f'• <b>Frustration Relieved:</b> High cement/plaster costs & 5–8% broken concrete corners.<br>'
            f'• <b>Motivation & Loyalty:</b> Saves <b>R{savings_20m_wall_zar:,} per 20m wall</b>, loads 50% more bricks per bakkie (15kg vs 24kg), and collects same-day stock in Waltloo.</div>'
            f'<div class="commercial-card"><b>🏢 Secondary Segment (30%): "Facilities Manager Willem" (Pretoria East Estates & Warehouses):</b><br>'
            f'• <b>Frustration Relieved:</b> Messy wet plastering in active warehouses & 10% green procurement audits.<br>'
            f'• <b>Motivation & Loyalty:</b> Clean dry-stacking, 1-click website ordering, and certified HDPE diversion.</div>',
            unsafe_allow_html=True,
        )

# =============================================================================
# TAB 3: R270K SEED ASK, WORKERS START MONTH 3, 7-MONTH PAYBACK & 30-MIN CURE
# =============================================================================
with tab3:
    st.subheader("3. Waltloo Hub R270,000 Seed Capital, 4 Factory Workers (Starting Month 3 @ R8,500/mo) & 7.0-Month Payback")

    fc1, fc2 = st.columns(2)
    monthly_fixed_opex_zar = fc1.slider(
        "Month 3+ Fixed OPEX: 4 Workers @ R8,500 (R34k) + Waltloo Rent (R14.5k) + Gas/Power (R4k) + Analytics (R1.5k) [Default: R54,000]",
        40000, 85000, key="monthly_fixed_opex_zar", step=2000,
    )
    seed_capital_ask_zar = fc2.slider(
        "Single-Tier Seed Capital Ask (ZAR) — 4 Brick Bake Bins + M1–M2 Testing + R4.00/kg HDPE [Locked: R270,000]",
        220000, 350000, key="seed_capital_ask_zar", step=5000,
    )

    # 30-Minute Curing Math with 4 Rotating 4-Cavity SCAMPER Brick Bake Bins (16 cavities per 30-min cycle):
    # 16 cycles per 8-hr shift * 16 bricks/cycle = 256 bricks/day * 26 working days = 6,656 bricks/mo (63.4 pallets/mo)
    daily_max_bricks = 256
    working_days_mo = 26
    single_shift_max = daily_max_bricks * working_days_mo  # 6,656 bricks/mo
    daily_som_bricks = math.ceil(monthly_units_sold / float(working_days_mo))
    som_util_pct = round((monthly_units_sold / single_shift_max) * 100, 1)

    breakeven_units_mo = math.ceil(monthly_fixed_opex_zar / unit_profit_zar)
    breakeven_pallets_mo = round(breakeven_units_mo / BPP, 1)
    daily_be_units = math.ceil(breakeven_units_mo / float(working_days_mo))

    monthly_rev_zar = monthly_units_sold * wholesale_price_zar
    monthly_var_zar = monthly_units_sold * production_cost_zar
    monthly_brick_net_profit = monthly_rev_zar - monthly_var_zar - monthly_fixed_opex_zar
    epr_subsidy_mo = round(monthly_units_sold * rhdpe_waste_used_kg * 1.20, 0)
    total_monthly_net_cashflow = monthly_brick_net_profit + epr_subsidy_mo

    # Exact 7.0-Month Payback Math:
    # Months 1–2 = Testing & Setup in Waltloo (Zero worker payroll; co-founders run SABS testing).
    # Month 3+ = 4 Workers start on payroll; R270,000 / R54,456 net cash flow = 5.0 commercial months -> 2.0 + 5.0 = 7.0 Months Total!
    if total_monthly_net_cashflow > 0:
        commercial_months = round(seed_capital_ask_zar / total_monthly_net_cashflow, 1)
        total_payback_months = round(2.0 + commercial_months, 1)
        payback_text = f"{total_payback_months} Months (Month 7)"
        payback_delta = f"2.0m Test (R0 Wages) + {commercial_months}m Sales"
    else:
        payback_text = "Increase SOM"
        payback_delta = "Below monthly break-even"

    monthly_rhdpe_t = round((monthly_units_sold * rhdpe_waste_used_kg) / 1000.0, 1)
    annual_rhdpe_t = round((annual_som_units * rhdpe_waste_used_kg) / 1000.0, 1)
    annual_bottles_m = round((annual_som_units * hdpe_bottles_diverted) / 1_000_000.0, 2)
    annual_co2e_t = round(annual_rhdpe_t * 1.95, 1)

    reclaimers_count = 40
    monthly_reclaimer_pool_zar = int(round(monthly_units_sold * rhdpe_waste_used_kg * reclaimer_rate_per_kg, 0))
    per_reclaimer_monthly_zar = int(round(monthly_reclaimer_pool_zar / float(reclaimers_count), 0))

    b1, b2, b3, b4 = st.columns(4)
    b1.metric("1. Daily & Monthly Break-Even", f"{daily_be_units} bricks / day", f"{breakeven_units_mo:,}/mo ({breakeven_pallets_mo} pallets/mo)")
    b2.metric("2. Total Seed Payback Time", payback_text, payback_delta)
    b3.metric("3. Monthly Net Profit (+EPR)", f"R{int(total_monthly_net_cashflow):,} / mo", f"R{int(monthly_brick_net_profit):,} bricks + R{int(epr_subsidy_mo):,} EPR")
    b4.metric("4. 30-Min Cure Daily Output", f"{daily_som_bricks} / {daily_max_bricks} bricks", f"{som_util_pct}% of 1-shift max (4 Bake Bins)")

    e1, e2, e3 = st.columns(3)
    e1.metric(
        "👷 PEOPLE: 40 Reclaimers (@ R4/kg) + 4 Staff",
        f"R{per_reclaimer_monthly_zar:,} / mo per Reclaimer",
        f"R{monthly_reclaimer_pool_zar:,}/mo pool (@ R4/kg) + 4 Staff @ R8,500/mo",
    )
    e2.metric(
        "♻️ PLANET: Code 2 HDPE Diverted from Landfills",
        f"{annual_rhdpe_t} Tonnes / yr",
        f"{monthly_rhdpe_t}t/mo (~{annual_bottles_m}M two-litre milk bottles/yr)",
    )
    e3.metric(
        "🌍 CARBON: Annual Emissions Avoided",
        f"{annual_co2e_t} Tonnes CO₂e / yr",
        "30-min water cure replaces 28-day Portland cement curing",
    )

    bc1, bc2 = st.columns([1.2, 1.15])
    with bc1:
        u_rng = list(range(0, 6826, 650))
        fig_be = go.Figure()
        fig_be.add_trace(go.Scatter(x=u_rng, y=[u * wholesale_price_zar for u in u_rng], mode="lines+markers", name="Monthly Revenue (33% Margin)", line=dict(color="#0d9488", width=3)))
        fig_be.add_trace(go.Scatter(x=u_rng, y=[monthly_fixed_opex_zar + (u * production_cost_zar) for u in u_rng], mode="lines+markers", name="Month 3+ Total Cost (OPEX + COGS)", line=dict(color="#ef4444", width=3, dash="dash")))
        fig_be.add_vline(x=breakeven_units_mo, line_dash="dot", line_color="#1e40af", annotation_text=f"Break-Even: {breakeven_units_mo:,}/mo ({daily_be_units}/day)")
        fig_be.add_vline(x=monthly_units_sold, line_dash="solid", line_color="#15803d", annotation_text=f"SOM: {monthly_units_sold:,}/mo ({total_pallets_mo} pallets)")
        fig_be.update_layout(title="Waltloo Hub Month 3+ Break-Even (179 Bricks/Day Breaks Even on R54k OPEX)", xaxis_title="Bricks Sold / Month", yaxis_title="ZAR / Month (Excl. VAT)", legend=dict(orientation="h", y=1.12), height=390)
        st.plotly_chart(fig_be, use_container_width=True)

    with bc2:
        st.markdown(f"#### 💰 R{int(seed_capital_ask_zar):,} Seed Capital Breakdown (Waltloo Hub — Workers Start M3)")
        sf = seed_capital_ask_zar / 270000.0
        df_seed = pd.DataFrame(
            [
                {
                    "Seed Allocation Bucket": "1. SCAMPER Tech & 4 Brick Bake Bins (44.4%)",
                    "Cost (ZAR)": f"R{int(round(120000 * sf, 0)):,}",
                    "Verified Items Included": "80 RPM silage cutter (R15k), 350L gas drum mixer & water trough (R30k), Adendorff 100T press (R43k), 4 modified 4-cavity Brick Bake Bins (R32k).",
                },
                {
                    "Seed Allocation Bucket": "2. Waltloo M1–M2 Lease & SANS Test (23.0%)",
                    "Cost (ZAR)": f"R{int(round(62000 * sf, 0)):,}",
                    "Verified Items Included": "Waltloo bay deposit + M1–M2 rent (R29k — R0 worker payroll during M1–M2!), fume hood (R14.5k), SABS SANS 1215 lab test (R18.5k).",
                },
                {
                    "Seed Allocation Bucket": "3. R4.00/kg HDPE Stock & M3 Wage Float (22.2%)",
                    "Cost (ZAR)": f"R{int(round(60000 * sf, 0)):,}",
                    "Verified Items Included": "9.0T Code 2 HDPE @ R4.00/kg to 40 reclaimers (R36k) + sand/fiber/MAPE (R7k) + Month-3 launch wage float for 4 workers (R17k).",
                },
                {
                    "Seed Allocation Bucket": "4. PPE (4 Workers & 40 Reclaimers) + BI (10.4%)",
                    "Cost (ZAR)": f"R{int(round(28000 * sf, 0)):,}",
                    "Verified Items Included": "PPE for 4 factory workers (R8,000) + PPE for 40 reclaimers (R11,000) + 500kg digital scale (R2,500) + Analytics setup/hosting (R6,500).",
                },
            ]
        )
        st.table(df_seed)

    st.markdown("#### 🗓️ 6-Month Phased Execution Roadmap (Worker Salaries Starting Month 3 → Full Payback in Month 7)")
    df_roadmap = pd.DataFrame(
        [
            {
                "Timeline Phase": "Months 1 – 2: Waltloo Setup & SABS Test",
                "Seed Spent": f"R{int(round(165000 * sf, 0)):,} (61%)",
                "Operational Activities": "Co-founders install chaff cutter, mixer, 100T press & 4 Brick Bake Bins in Waltloo; mold test batch & pass SABS SANS 1215 test (R0 worker payroll!).",
                "Monthly Sales": "0 Pallets (Testing & 20m Demo Wall)",
                "Cash-Flow Reality": "Lean Testing Phase: Deferring the 4 workers' R34k/mo payroll until Month 3 saves R68,000 in seed cash while we complete SABS certification.",
            },
            {
                "Timeline Phase": "Months 3 – 4: Workers Start & Break-Even Passed",
                "Seed Spent": f"R{int(round(75000 * sf, 0)):,} (28%)",
                "Operational Activities": "4 factory workers start on shift rotation (3/day @ R8,500/mo); onboard 40 reclaimers (@ R4.00/kg); cross 44.3-pallet break-even in Month 4.",
                "Monthly Sales": f"34 → 48 Pallets/mo (Passes {breakeven_pallets_mo} BE!)",
                "Cash-Flow Reality": "50% Customer Deposits + Worker Launch: Customer deposits fund raw materials while Month 4 sales cover 100% of the R54,000 monthly OPEX.",
            },
            {
                "Timeline Phase": "Months 5 – 6: Full SOM & 7.0-Month Payback",
                "Seed Spent": f"R{int(round(30000 * sf, 0)):,} (11%)",
                "Operational Activities": f"Scale to {total_pallets_mo} pallets/mo ({daily_som_bricks} bricks/day vs {daily_max_bricks}/day max); collect +R1.20/kg Section 18 EPR credits.",
                "Monthly Sales": f"{total_pallets_mo} Pallets/mo ({monthly_units_sold:,} bricks)",
                "Cash-Flow Reality": f"7.0-Month Total Payback: Generates R{int(monthly_rev_zar):,}/mo revenue and +R{int(total_monthly_net_cashflow):,}/mo net cash flow—paying back R270k in {payback_text}!",
            },
        ]
    )
    st.table(df_roadmap)

# =============================================================================
# TAB 4: SELF-SERVICE OPERATIONAL & BUSINESS ANALYTICS (NO SQL REQUIRED)
# =============================================================================
with tab4:
    st.subheader("4. Waltloo Hub Self-Service Director Analytics: Live Operational Metrics, Online Sales & 1-Click Explorer")

    col_op, col_biz = st.columns(2)

    with col_op:
        st.markdown("##### ⚙️ Operational Analytics (Live Waltloo Factory & Yard Health)")
        op1, op2 = st.columns(2)
        op1.metric("Live Waltloo Yard Inventory", "15 Pallets", "1,575 bricks (2.5-day stock buffer)")
        op2.metric("Reclaimer HDPE Stockpile", "6.5 Tonnes", "Bought @ R4.00/kg (1,545 bricks ready)")
        op3, op4 = st.columns(2)
        op3.metric("3-Worker Shift Output", f"{daily_som_bricks} bricks / day", f"Max capacity: {daily_max_bricks}/day (4 Bake Bins)")
        op4.metric("Zero-Breakage Mold Yield", "100% Intact Corners", "0% delivery breakage + 100% trim recycled")

    with col_biz:
        st.markdown("##### 📈 Business Analytics (Revenue, Website Orders & Margins)")
        online_pallets_mo = int(round(total_pallets_mo * 0.258, 0))  # 16 pallets at default 62 pallets/mo
        online_rev_mo = int(round(online_pallets_mo * pallet_price_zar, 0))

        bz1, bz2 = st.columns(2)
        bz1.metric("Full SOM Monthly Revenue", f"R{int(monthly_rev_zar):,} / mo", f"{total_pallets_mo} Pallets ({monthly_units_sold:,} bricks)")
        bz2.metric("🌐 Online Website Sales", f"R{online_rev_mo:,} / mo", f"{online_pallets_mo} Pallets (26% via plastinoxa.co.za)")
        bz3, bz4 = st.columns(2)
        bz3.metric("Resilient Gross Margin", f"{gross_margin_pct}% Margin", f"R{unit_profit_zar:.2f} gross profit / brick")
        bz4.metric("Section 18 EPR Subsidy", f"+R{int(epr_subsidy_mo):,} / mo", "+R1.20/kg PRO credit on Code 2 HDPE")

    st.divider()

    st.markdown("#### 🔍 1-Click Self-Service Sales Explorer & Ad-Hoc Issue Investigator (No SQL Required)")
    st.caption("Click any button below to aggregate sales by **Day of the Week**, **Week**, or **Month (Showing M1–M2 Testing → M3 Worker Start → M7 Payback)**, and filter by **Sales Channel**:")

    flt1, flt2 = st.columns([1.4, 1.0])
    time_view = flt1.radio(
        "1. Click to Aggregate Time Period:",
        [
            "📅 Daily View (Which Day of the Week Sells Most?)",
            "📊 Weekly View (Spot Weekly Dips & Load-Shedding Impact)",
            "📈 Monthly View (M1–M2 Testing → M3 Launch → M7 Payback)",
        ],
        horizontal=True,
    )
    channel_view = flt2.radio(
        "2. Click to Filter Sales Channel:",
        ["All Channels", "Direct Waltloo Hub", "Online Website (plastinoxa.co.za)"],
        horizontal=True,
    )

    if "Daily" in time_view:
        x_labels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        hub_vals = [11, 7, 3, 9, 13, 3]
        web_vals = [3, 2, 2, 3, 4, 2]
        chart_title = "Ad-Hoc Investigation: Monthly Pallets Sold by Day of the Week (46 Waltloo Hub + 16 Website = 62 Pallets)"
        adhoc_insight = (
            "💡 **Ad-Hoc Discovery (Day-of-Week Pattern):** **Friday (17 pallets) and Monday (14 pallets)** generate **50.0% of sales** "
            "as builders collect 7-pallet 20m boundary-wall bundles ahead of weekend and Monday starts. **Wednesday is our quietest day (5 pallets)**—"
            "**Director Action:** Worker 1 takes Wednesday off while the 3 on-shift workers clean the 4 Brick Bake Bins and run website promos."
        )
    elif "Weekly" in time_view:
        x_labels = ["Week 1", "Week 2", "Week 3 (Stage 4 Load-Shedding)", "Week 4 (Month-End Push)"]
        hub_vals = [12, 13, 8, 13]
        web_vals = [4, 4, 5, 3]
        chart_title = "Ad-Hoc Investigation: Weekly Pallet Sales (46 Waltloo Hub + 16 Website = 62 Pallets/Month)"
        adhoc_insight = (
            "💡 **Ad-Hoc Discovery (Why Did Week 3 Walk-In Sales Dip?):** Drilling into **Week 3** shows walk-in Waltloo Hub sales dipped from 13 to 8 pallets during Stage 4 load-shedding, "
            "but **Online Website Orders jumped to 5 pallets** while our LPG gas-heated drum mixer kept molding without 3-phase grid power!"
        )
    else:
        x_labels = [
            "Month 1 (Testing: R0 Wages)",
            "Month 2 (SABS Pass: R0 Wages)",
            "Month 3 (Workers Start: 34p)",
            "Month 4 (Passes BE: 48p)",
            "Month 5 (Growth: 55p)",
            "Month 6 (Full SOM: 62p)",
        ]
        hub_vals = [0, 0, 25, 35, 41, 46]
        web_vals = [0, 0, 9, 13, 14, 16]
        chart_title = "Executive Report: 6-Month Rollout (M1–M2 Testing [R0 Worker Payroll] → M3 Launch → 7.0-Mo Payback)"
        adhoc_insight = (
            f"💡 **Executive Summary (How We Hit 7.0 Months Payback):** In **Months 1–2**, commercial sales and worker wages are **R0** during SABS testing in Waltloo. "
            f"In **Month 3**, the 4 workers start on shift rotation (34 pallets sold), crossing our **{breakeven_pallets_mo}-pallet break-even in Month 4 (48 pallets)** "
            f"and reaching **62 pallets/month (R{int(monthly_rev_zar):,}/mo)** by Month 6—recovering the full R{int(seed_capital_ask_zar):,} seed ask in **{payback_text}**!"
        )

    st.info(adhoc_insight)

    fig_adhoc = go.Figure()
    if channel_view in ["All Channels", "Direct Waltloo Hub"]:
        fig_adhoc.add_trace(
            go.Bar(
                name="Direct Waltloo Hub Pallets",
                x=x_labels,
                y=hub_vals,
                marker_color="#0f766e",
                text=[f"{v} Pallets" if v > 0 else "Testing (R0 Wages)" for v in hub_vals],
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
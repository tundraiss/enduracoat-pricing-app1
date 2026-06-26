import streamlit as st
from dataclasses import dataclass

st.set_page_config(page_title="EnduraCoat Pricing App", page_icon="🧮", layout="centered")

st.title("🧮 EnduraCoat Pricing — Simple App")
st.caption("App-style front-end for your Excel pricing logic (flat area, steel kg, or circular).")

@dataclass
class Defaults:
    specific_gravity: float = 1.5
    thickness_microns: float = 120.0
    powder_price_area: float = 180.0      # R/kg (Option 1)
    powder_price_kg: float = 130.0        # R/kg (Option 2)
    market_min_m2_area: float = 230.0     # R/m² min
    market_price_m2_area: float = 250.0   # R/m² max/standard
    market_min_m2_kg: float = 230.0       # R/m² min (kg method)
    market_price_m2_kg: float = 250.0     # R/m² max/standard (kg method)
    density_steel: float = 8000.0         # kg/m³ (as used in your sheet)

D = Defaults()

def coverage_per_kg(sg: float, microns: float) -> float:
    # Excel: 1000/(sg*microns)
    if sg * microns == 0:
        return 0.0
    return 1000.0 / (sg * microns)

def option1_flat_area(length_cm: float, width_cm: float, sides: float, microns: float, sg: float, powder_price: float, hollow_factor: float):
    area_m2 = (length_cm * width_cm * sides) / 10000.0
    grams = (length_cm * width_cm * sides * microns * sg) / 10000.0
    if hollow_factor and hollow_factor != 0:
        grams = grams / hollow_factor
    powder_cost = grams * powder_price / 1000.0
    return area_m2, grams, powder_cost

def option2_steel_kg(steel_kg: float, thickness_mm: float, sides: float, microns: float, sg: float, powder_price: float, density_kg_m3: float):
    # Excel: kg/8000/mm*sides*1000  (equivalent to mass / (density * thickness_m))
    if thickness_mm == 0 or density_kg_m3 == 0:
        area_m2 = 0.0
    else:
        area_m2 = (steel_kg / density_kg_m3) / (thickness_mm / 1000.0) * sides
    grams = area_m2 * sg * microns
    powder_cost = grams * powder_price / 1000.0
    return area_m2, grams, powder_cost

def circular_area(radius_cm: float, sides: float, microns: float, sg: float, powder_price: float):
    import math
    area_m2 = (math.pi * (radius_cm ** 2)) / 10000.0 * sides
    grams = area_m2 * sg * microns
    powder_cost = grams * powder_price / 1000.0
    return area_m2, grams, powder_cost

with st.sidebar:
    st.header("Global inputs")
    sg = st.number_input("Specific gravity", min_value=0.0, value=float(D.specific_gravity), step=0.1, format="%.3f")
    microns = st.number_input("Coating thickness (microns)", min_value=0.0, value=float(D.thickness_microns), step=5.0)

    cov = coverage_per_kg(sg, microns)
    st.metric("Coverage (m² per kg)", f"{cov:,.3f}")

st.divider()
method = st.radio("Choose calculation method", ["Option 1 — Flat area (cm)", "Option 2 — Steel weight (kg)", "Circular — Radius (cm)"], horizontal=False)

if method.startswith("Option 1"):
    st.subheader("Option 1 — Flat surface (Area)")
    c1, c2 = st.columns(2)
    with c1:
        length_cm = st.number_input("Length (cm)", min_value=0.0, value=0.0, step=1.0)
        sides = st.number_input("Number of sides", min_value=1.0, value=2.0, step=1.0)
    with c2:
        width_cm = st.number_input("Width (cm)", min_value=0.0, value=0.0, step=1.0)
        hollow_factor = st.number_input("Non-solid factor (1 = solid, >1 reduces powder)", min_value=0.0, value=1.0, step=0.1)

    powder_price = st.number_input("Powder price (R/kg)", min_value=0.0, value=float(D.powder_price_area), step=5.0)
    market_min = st.number_input("Market MIN rate (R/m²)", min_value=0.0, value=float(D.market_min_m2_area), step=5.0)
    market_std = st.number_input("Market MAX/Std rate (R/m²)", min_value=0.0, value=float(D.market_price_m2_area), step=5.0)

    area_m2, grams, powder_cost = option1_flat_area(length_cm, width_cm, sides, microns, sg, powder_price, hollow_factor)
    sell_min = market_min * area_m2
    sell_max = market_std * area_m2

elif method.startswith("Option 2"):
    st.subheader("Option 2 — From steel weight (kg)")
    c1, c2 = st.columns(2)
    with c1:
        steel_kg = st.number_input("Steel weight (kg)", min_value=0.0, value=0.0, step=0.5)
        sides = st.number_input("Number of sides", min_value=1.0, value=2.0, step=1.0)
    with c2:
        thickness_mm = st.number_input("Steel thickness (mm)", min_value=0.0, value=1.6, step=0.1)
        density = st.number_input("Steel density (kg/m³)", min_value=0.0, value=float(D.density_steel), step=100.0)

    powder_price = st.number_input("Powder price (R/kg)", min_value=0.0, value=float(D.powder_price_kg), step=5.0)
    market_min = st.number_input("Market MIN rate (R/m²)", min_value=0.0, value=float(D.market_min_m2_kg), step=5.0)
    market_std = st.number_input("Market MAX/Std rate (R/m²)", min_value=0.0, value=float(D.market_price_m2_kg), step=5.0)

    area_m2, grams, powder_cost = option2_steel_kg(steel_kg, thickness_mm, sides, microns, sg, powder_price, density)
    sell_min = market_min * area_m2
    sell_max = market_std * area_m2

else:
    st.subheader("Circular — From radius (cm)")
    c1, c2 = st.columns(2)
    with c1:
        radius_cm = st.number_input("Radius (cm)", min_value=0.0, value=0.0, step=1.0)
    with c2:
        sides = st.number_input("Number of sides", min_value=1.0, value=1.0, step=1.0)

    powder_price = st.number_input("Powder price (R/kg)", min_value=0.0, value=float(D.powder_price_kg), step=5.0)
    market_min = st.number_input("Market MIN rate (R/m²)", min_value=0.0, value=float(D.market_min_m2_kg), step=5.0)
    market_std = st.number_input("Market MAX/Std rate (R/m²)", min_value=0.0, value=float(D.market_price_m2_kg), step=5.0)

    area_m2, grams, powder_cost = circular_area(radius_cm, sides, microns, sg, powder_price)
    sell_min = market_min * area_m2
    sell_max = market_std * area_m2

st.divider()
st.subheader("Results")

cA, cB, cC = st.columns(3)
cA.metric("Surface area (m²)", f"{area_m2:,.4f}")
cB.metric("Powder used (g)", f"{grams:,.1f}")
cC.metric("Powder cost (R)", f"{powder_cost:,.2f}")

c1, c2 = st.columns(2)
c1.metric("Selling price MIN (R)", f"{sell_min:,.2f}")
c2.metric("Selling price MAX/Std (R)", f"{sell_max:,.2f}")

with st.expander("Show calculation notes"):
    st.write(
        """
- Coverage (m²/kg) = 1000 / (specific_gravity × microns)  
- Flat area (m²) = (Length_cm × Width_cm × Sides) / 10,000  
- Steel kg method (m²) = (Mass_kg / Density) / Thickness_m × Sides  
- Powder grams = Area_m² × specific_gravity × microns (and divided by factor for non-solid products if provided)
        """
    )

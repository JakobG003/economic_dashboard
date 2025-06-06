import os

# Mapa kjer bodo tvoji data source fajli
data_sources_dir = "data_sources"

# Seznam imen datotek (brez .py)
modules = [
    "bitcoin_data",
    "inflation_data",
    "interest_rates_data",
    "employment_data",
    "commodities_data",
    "equities_data",
    "fund_flows_data",
    "real_estate_data",
    "supply_chains_data",
    "macro_themes_data"
]

# Ustvari mapo, če ne obstaja
os.makedirs(data_sources_dir, exist_ok=True)

# Ustvari prazne .py datoteke
for module in modules:
    path = os.path.join(data_sources_dir, f"{module}.py")
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(f"# {module.replace('_', ' ').title()} Module\n\n")
            f.write("def fetch_data():\n")
            f.write("    # TODO: Implement data fetching logic\n")
            f.write("    pass\n")
        print(f"Created: {path}")
    else:
        print(f"Already exists: {path}")

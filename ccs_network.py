import geopandas as gpd
from shapely.geometry import Point
import itertools
import networkx as nx
import matplotlib.pyplot as plt

GADM_FILE = r"C:\Users\rajrs\OneDrive\Desktop\AI for sustainability\gadm41_IND.gpkg"
GADM_LAYER = "ADM_ADM_1"
states = gpd.read_file(GADM_FILE, layer=GADM_LAYER)
gujarat = states[states["NAME_1"] == "Gujarat"]
if gujarat.empty:
    raise ValueError("Gujarat not found in GADM file")
gujarat = gujarat.to_crs(epsg=4326)
print("Loaded Gujarat boundary")
sources = [
    ("Plant_A", 22.30, 70.80),
    ("Plant_B", 23.02, 72.57),
    ("Plant_C", 21.17, 72.83)
]

points = []

for name, lat, lon in sources:
    points.append(
        {
            "name": name,
            "geometry": Point(lon, lat)
        }
    )

plants = gpd.GeoDataFrame(points, crs="EPSG:4326")
plants["inside_gujarat"] = plants.within(gujarat.geometry.iloc[0])

gujarat_proj = gujarat.to_crs(epsg=3857)
plants_proj = plants.to_crs(epsg=3857)

centroid = gujarat_proj.geometry.iloc[0].centroid

plants_proj["distance_km"] = plants_proj.geometry.distance(centroid) / 1000

def distance_to_cost(d, inside):

    if not inside:
        return 1.40

    if d < 100:
        return 1.00
    elif d < 200:
        return 1.10
    else:
        return 1.25


plants_proj["location_cost_factor"] = plants_proj.apply(
    lambda r: distance_to_cost(r["distance_km"], r["inside_gujarat"]),
    axis=1
)

print("\nLocation-based cost factors (using only GADM boundary):\n")

for _, row in plants_proj.iterrows():

    print(
        row["name"],
        "| inside Gujarat:", row["inside_gujarat"],
        "| distance from centre (km):", round(row["distance_km"], 2),
        "| cost factor:", row["location_cost_factor"]
    )
print("\nPairwise distance & cost matrix:\n")

pairwise_results = []

for (i, a), (j, b) in itertools.combinations(plants_proj.iterrows(), 2):

    d_km = a.geometry.distance(b.geometry) / 1000
    avg_factor = (a["location_cost_factor"] + b["location_cost_factor"]) / 2
    weighted_cost = d_km * avg_factor

    pairwise_results.append((a["name"], b["name"], d_km, weighted_cost))

    print(
        a["name"], "→", b["name"],
        "| distance (km):", round(d_km, 2),
        "| weighted cost:", round(weighted_cost, 2)
    )
G = nx.Graph()

for _, r in plants_proj.iterrows():
    G.add_node(r["name"])

for a_name, b_name, d_km, weighted_cost in pairwise_results:

    G.add_edge(
        a_name,
        b_name,
        distance_km=d_km,
        cost=weighted_cost
    )

mst = nx.minimum_spanning_tree(G, weight="cost")

print("\nMinimum cost CCS network (proxy):\n")

for u, v, data in mst.edges(data=True):
    print(u, "->", v, "| cost:", round(data["cost"], 2))
pos = nx.spring_layout(mst, seed=42)

plt.figure(figsize=(7, 5))

nx.draw(
    mst,
    pos,
    with_labels=True,
    node_size=2000,
    font_size=10
)

edge_labels = nx.get_edge_attributes(mst, "cost")
edge_labels = {k: round(v, 1) for k, v in edge_labels.items()}

nx.draw_networkx_edge_labels(
    mst,
    pos,
    edge_labels=edge_labels
)

plt.title("Minimum Cost CCS Network (Proxy)")
plt.tight_layout()
plt.show()
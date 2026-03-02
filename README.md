# Spatial Optimisation of a Carbon Capture and Storage (CCS) Transport Network in Gujarat

This project builds a spatial and network-based optimisation framework to design a
proxy carbon capture and storage (CCS) transport network for industrial emission
sources in Gujarat, India.

## Data
- Administrative boundary source: GADM – Global Administrative Areas
- Spatial unit: State boundary of Gujarat
- Emission sources: Hypothetical industrial point locations

## Methodology
- Loaded the Gujarat state boundary from GADM
- Created CO₂ source locations as geographic point features
- Re-projected spatial data for distance-based analysis
- Computed distances from the geographic centre of the state
- Assigned location-based cost factors based on distance and whether the source lies
  inside the state boundary
- Computed pairwise transport distances between all sources
- Constructed a weighted network graph using distance and cost factors

## Network optimisation
- Built an undirected weighted graph of all emission sources
- Computed the minimum spanning tree (MST) using transport cost as the edge weight
- The MST represents a minimum-cost proxy CCS transport network

## Key outcome
The project identifies the minimum-cost interconnection structure linking all CO₂
sources under spatial and location-based cost constraints.

## Notes
- Source locations are hypothetical and are used only to demonstrate the spatial
  optimisation framework.
- The cost function is a simplified proxy and does not represent real engineering
  or financial costs.

## How to run
1. Install required libraries:
   geopandas, shapely, networkx, matplotlib
2. Update the local path to the GADM geopackage file.
3. Run the Python script to reproduce the spatial processing and network results.

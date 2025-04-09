import solara
from ipyleaflet import Map, TileLayer, SplitMapControl, LayersControl, WidgetControl, GeoJSON, Popup
from ipywidgets import HTML, Output, Button
import geopandas as gpd
import json
from localtileserver import TileClient


@solara.component
def Page():
    # === Load shapefile ===
    gdf = gpd.read_file("C:/Users/gageb/documents/SLF_Climate_Local/shapefiles_geemap/ne_10m_admin_1_states_provinces.shp")
    geojson_data = json.loads(gdf.to_json())

    # === Tile clients ===
    client_1981 = TileClient("C:/Users/gageb/documents/.asc_to_.tif_conversion/slf_binarized_summed_1981-2010_with_crs.tif")
    client_ssp126 = TileClient("C:/Users/gageb/documents/.asc_to_.tif_conversion/slf_binarized_summed_2041-2070_ssp126_GFDL_with_crs.tif")
    client_ssp370 = TileClient("C:/Users/gageb/documents/.asc_to_.tif_conversion/slf_binarized_summed_2041-2070_ssp370_GFDL_with_crs.tif")
    client_ssp585 = TileClient("C:/Users/gageb/documents/.asc_to_.tif_conversion/slf_binarized_summed_2041-2070_ssp585_GFDL_with_crs.tif")

    # === Tile layers ===
    layer_1981 = TileLayer(url=client_1981.get_tile_url(), name="SLF 1981–2010")
    layer_ssp126 = TileLayer(url=client_ssp126.get_tile_url(), name="SLF SSP126")
    layer_ssp370 = TileLayer(url=client_ssp370.get_tile_url(), name="SLF SSP370")
    layer_ssp585 = TileLayer(url=client_ssp585.get_tile_url(), name="SLF SSP585")

    # === Create map (full screen height)
    m = Map(center=(40, -100), zoom=4, scroll_wheel_zoom=True, layout={"height": "100vh"})

    # === Add split map control
    split = SplitMapControl(left_layer=layer_1981, right_layer=layer_ssp126)
    m.add_control(split)

    # === Add extra layers (toggle manually)
    m.add_layer(layer_ssp370)
    m.add_layer(layer_ssp585)

    # === Add shapefile with click popup
    def on_click_feature(event, feature, **kwargs):
        name = feature["properties"].get("name", "Unknown")
        coords = feature["geometry"]["coordinates"][0][0]  # Grab first polygon coordinate
        popup = Popup(
            location=[coords[1], coords[0]],
            child=HTML(f"<b>{name}</b>"),
            close_button=True
        )
        m.add_layer(popup)

    geojson_layer = GeoJSON(
        data=geojson_data,
        name="States & Provinces",
        style={"color": "#1E90FF", "weight": 1, "fillOpacity": 0},
        hover_style={"fillOpacity": 0.2},
        on_click=on_click_feature
    )
    m.add_layer(geojson_layer)

    # === Legend HTML
    legend_html = """
    <div style="background:white;padding:10px;border-radius:5px;">
    <b>Risk Levels</b><br>
    <div><span style="background:#000000;width:12px;height:12px;display:inline-block;"></span> Low Risk</div>
    <div><span style="background:#D3D3D3;width:12px;height:12px;display:inline-block;"></span> Moderate Risk</div>
    <div><span style="background:#A9A9A9;width:12px;height:12px;display:inline-block;"></span> High Risk</div>
    <div><span style="background:#FFFFFF;width:12px;height:12px;display:inline-block; border: 1px solid #ccc;"></span> Extreme Risk</div>
    </div>
    """
    m.add_control(WidgetControl(widget=HTML(value=legend_html), position="topright"))

    # === Reset view button
    def reset_view(b):
        m.center = (40, -100)
        m.zoom = 4

    reset_button = Button(description="Reset View", layout={"width": "100px"})
    reset_button.on_click(reset_view)
    m.add_control(WidgetControl(widget=reset_button, position="bottomleft"))

    # === Layer toggle control
    m.add_control(LayersControl(position="topright"))

    # === Display map in Solara
    out = Output()
    with out:
        display(m)

    solara.Column(children=[out])

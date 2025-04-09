import solara
import geemap

# ✅ Raster file paths
rasters = {
    "SLF_1981-2010": "C:/Users/gageb/documents/.asc_to_.tif_conversion/slf_binarized_summed_1981-2010_with_crs.tif",
    "SLF_2041-2070_ssp126": "C:/Users/gageb/documents/.asc_to_.tif_conversion/slf_binarized_summed_2041-2070_ssp126_GFDL_with_crs.tif",
    "SLF_2041-2070_ssp370": "C:/Users/gageb/documents/.asc_to_.tif_conversion/slf_binarized_summed_2041-2070_ssp370_GFDL_with_crs.tif",
    "SLF_2041-2070_ssp585": "C:/Users/gageb/documents/.asc_to_.tif_conversion/slf_binarized_summed_2041-2070_ssp585_GFDL_with_crs.tif",
}

# ✅ Legend color values (DO NOT CHANGE COLORS)
legend_dict = {
    'Low Risk': '00008B',
    'Moderate Risk': 'FFA500',
    'High Risk': 'ADD8E6',
    'Extreme Risk': 'FF0000'
}

# ✅ Raster color palette (matches encoded values)
risk_palette = [
    "#00008B",  # Low Risk
    "#FFA500",  # Moderate Risk
    "#ADD8E6",  # High Risk
    "#FF0000",  # Extreme Risk
]

# ✅ Minimal map (no toolbar/inspector)
class SSPMap(geemap.Map):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_raster_layers()
        # self.add("layer_manager")  # ❌ hidden toolbar
        # self.add("inspector")      # ❌ no pixel inspection

    def add_raster_layers(self):
        for name, path in rasters.items():
            self.add_raster(
                path,
                colormap=risk_palette,
                layer_name=name
            )

# ✅ Styled legend box in bottom right corner
@solara.component
def LegendBox():
    with solara.Column(style={
        "position": "absolute",
        "bottom": "10px",
        "right": "10px",
        "background-color": "white",
        "padding": "6px",
        "border": "1px solid gray",
        "border-radius": "5px",
        "box-shadow": "2px 2px 10px rgba(0,0,0,0.2)",
        "z-index": "1000",
        "font-size": "12px",
        "line-height": "1.2",
        "min-width": "140px"
    }):
        solara.Text("Risk Levels", style={"font-weight": "bold", "font-size": "13px"})
        for label, color in legend_dict.items():
            with solara.Row(gap="6px"):
                solara.Markdown(
                    f"<div style='width:18px; height:14px; background-color:#{color}; border: 1px solid #ccc;'></div>"
                )
                solara.Text(label)

# ✅ Main fullscreen page with centered zoom
@solara.component
def Page():
    with solara.Column(style={"min-width": "100%", "padding": "0px"}):
        SSPMap.element(center=[40, 0], zoom=2, height="100vh")  # ⬅️ Adjusted zoom/center
        LegendBox()

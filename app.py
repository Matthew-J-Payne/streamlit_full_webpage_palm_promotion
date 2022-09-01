# conda env: deforestationdynamics
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
px.set_mapbox_access_token("pk.eyJ1IjoibWF0dGhld2pwYXluZSIsImEiOiJjbDN1NTk5dnEwZmVxM2VudnhmcWwwZm5yIn0.kT-2SV7qYLBV382pQJFtUw")

import streamlit as st
st.set_page_config(layout="wide")

#@st.cache
def graphing():
    
    palm = pd.read_csv("palm_areaYear2001-2015_timeseries_quadrat_25km2.csv")
    deforest = pd.read_csv("gfw_deforestation_with_distance_Year2001-2015_timeseries_quadrat_25km2.csv")


    palm_area_perYear = palm.groupby("year_plant", as_index = False)["areakm2"].sum()
    deforest_area_perYear = deforest.groupby("year", as_index = False)["areakm2"].sum()
            #deforest_mean_roadDist_perYear = deforest.groupby("year", as_index = False)["near_road"].mean()
            #deforest_mean_palmDist_perYear = deforest.groupby("year", as_index = False)["near_palm"].mean()

    traceDeforest = go.Scatter(
        x = deforest_area_perYear["year"], 
        y = deforest_area_perYear["areakm2"],
        name = "Non-oil palm deforestation",
        line = dict(color = "#DB0000")
        )
    tracePalm = go.Scatter(
        x = palm_area_perYear["year_plant"],
        y = palm_area_perYear["areakm2"],
        name = "Oil palm expansion",
        line = dict(color = "#F07605")
        )

    combined = [traceDeforest, tracePalm]


    layout = go.Layout(template = "plotly_white",
                    xaxis = dict(title = "Year", gridcolor = "#D3D3D3", linecolor = "Black", mirror = True, ticks = "outside", nticks = 8, tickfont = dict(size = 14)),
                    yaxis = dict(title = "Area (km<sup>2</sup>)", gridcolor = "#D3D3D3", linecolor = "Black", mirror = True, ticks = "outside"),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    height = 500,
                    width = 400,
                    font = dict(family = "Helvetica", color = "Black", size = 16),
                    legend = dict(orientation = "h", x = 0.05, y = -0.22),
                    #title = "Oil palm expansion and non-oil palm deforestation across the study site",
                    autosize = True
                    )
    fig = go.Figure(data = combined, layout = layout)
    return fig


@st.cache
def deforestation_function():
    # incorporating polygonal data into streamlit
    deforestation = gpd.read_file("deforestation_nonpalm.shp")
    deforestation = deforestation.to_crs(4326)
    loss = px.choropleth_mapbox(data_frame = deforestation,
                                    geojson = deforestation.geometry,
                                    locations = deforestation.index,
                                    color = "year",
                                    color_continuous_scale = "Reds",
                                    center = {"lat": -8.540459, "lon": -74.743779},
                                    mapbox_style = "satellite-streets",
                                    labels = {"year": "Year of forest loss"},
                                    zoom = 11,
                                    width = 800,
                                    height = 600
                                    )
    # quadrats = gpd.read_file("quadrats.shp")
    # quadrats = quadrats.to_crs(4326)
    # loss.add_choroplethmapbox(data_frame = quadrats,
    #                             geojson = quadrats.geometry,
    #                             locations = quadrats.index,
    #                             color = "Reds")
    loss.update_traces(marker_line_width = 0)
    #loss.update_layout(title_text = "Deforestation across the study area")
    
    return loss

@st.cache
def expansion_function():
    plantations = gpd.read_file("plantations_aged_mapped.shp")
    plantations = plantations.to_crs(4326)


    expansion = px.choropleth_mapbox(plantations,
                                        geojson = plantations.geometry,
                                        locations = plantations.index,
                                        color = "year_plant",
                                        hover_name = "year_plant",
                                        color_continuous_scale = "inferno",
                                        center = {"lat": -8.540459, "lon": -74.743779},
                                        mapbox_style = "satellite-streets",
                                        labels = {"year_plant": "Year Planted"},
                                        zoom = 10,
                                        width = 800,
                                        height = 600)
    expansion.update_traces(marker_line_width = 0)

    # # Modify tooltip
    # hover_trace = [t for t in expansion['data'] if 'text' in t][0]
    # for i, label in enumerate(hover_trace['text']):
    
    #     # Remove FIPS
    #     new_label = label.replace("FIPS: %s<br>" % Id[i], "")
    
    #     # Add a new value
    #     new_label += "<br>Other: %d" % values2[i]
    
    #     # Update trace text
    #     hover_trace['text'][i] = new_label
    #expansion.update_layout(title_text = "Oil palm expansion 2000 - 2015")

    return expansion
############################
# build streamlit dashboard
############################

#st.title("this is a test streamlit title!")
st.title("This is an companion dashboard for the poster:")
st.title("Oil palm promotes indirect land-use change in the Central Peruvian Amazon")#, in the Central Peruvian Amazon")
with st.expander("Click here for contact details"):
    st.markdown("Contact me at matthewjpayne1@gmail.com, if you're interested in collaborations or just want to chat!") # \n *I'll be sure to add more functionality to this dashboard in the future!*")

st.markdown("**Some contextual information about the dashboard**:  \n"
            "I thought this would be a good guide to familiarise any interested readers with the poster.  \n "
            "Hopefully, the poster speaks for itself.  \n But if not or you're just curious, read on..."
            "\n  \n **Research context:**  \n I am interested in exploring the promotion of indirect land-use change as deforestation by oil palm expansion.")#in the surrounding area, which is why the deforestation does not include forest that was cleared for oil palm development.")


column1, column2 = st.columns(2)

with column1:
    st.header("Non palm deforestation 2000 - 2015")
    st.write("This is deforestation derived from the Global Forest Watch dataset from Hansen et al., (2013).  \n **Source: Hansen/UMD/Google/USGS/NASA**")
    st.plotly_chart(deforestation_function(), use_container_width = True)

with column2:
    st.header("Oil palm expansion 2000 - 2015")
    st.markdown("...and this is oil palm delineated using photo-interpretation and age estimated")
    st.write("")
    st.write("") # padding for subplot placement
    st.plotly_chart(expansion_function(), use_container_width = True)


with st.expander("Click here for the deforestation data source"):
    st.markdown("Hansen, M. C., P. V. Potapov, R. Moore, M. Hancher, S. A. Turubanova, A. Tyukavina, D. Thau, S. V. Stehman, S. J. Goetz, T. R. Loveland, A. Kommareddy, A. Egorov, L. Chini, C. O. Justice, and J. R. G. Townshend. 2013. “High-Resolution Global Maps of 21st-Century Forest Cover Change.” Science 342 (15 November): 850–53. Data available on-line from: http://earthenginepartners.appspot.com/science-2013-global-forest. ")

# with st.expander("Click here for the age estimation data source"):
#     st.markdown("Málaga, N., Hergoualc’h, K., Kapp, G. et al. Variation in Vegetation and Ecosystem Carbon Stock Due to the Conversion of Disturbed Forest to Oil Palm Plantation in Peruvian Amazonia. Ecosystems 24, 351–369 (2021). Data available on-line from https://data.cifor.org/dataset.xhtml?persistentId=doi:10.17528/CIFOR/DATA.00196")

st.header("Sitewide non-oil palm deforestation is not significantly predicted by oil palm expansion")
st.write("From the graph below, it looks like there *isn't* a statistically valid relationship between oil palm and the non-palm deforestation in the map, and true there isn't.  \n  \n *...across the whole area in the same year.*  \n  \n Step in **spatially-fixed** and **time-fixed effects panel regression**, which can account for spatial and temporal variation in deforestation response.  \n  \n And that's it, for now. I'm intentionally withholding the model and plots until they are published in an academic paper.")
st.caption("*As a side note - I hope to code a way for this graph to poll the bounds of the above maps and reflect the values within.*")
#st.subheader("Oil palm expansion and non-oil palm deforestation across the study site")
# column3 = st.columns(1)
# with column3:
st.plotly_chart(graphing())

#st.markdown(
# """
# <link rel="stylesheet" href="https://mleibman.github.io/SlickGrid/slick.grid.css" type="text/css"/>
# <link rel="stylesheet" href="https://mleibman.github.io/SlickGrid/css/smoothness/jquery-ui-1.8.16.custom.css" type="text/css"/>
# <link rel="stylesheet" href="https://mleibman.github.io/SlickGrid/examples/examples.css" type="text/css"/>
# <table width="100%">
#   <tr>
#     <td valign="top" width="50%">
#       <div id="myGrid" style="width:600px;height:500px;"></div>
#     </td>
#     <td valign="top">
#       <h2>Demonstrates:</h2>
#       <ul>
#         <li>basic grid with minimal configuration</li>
#       </ul>
#         <h2>View Source:</h2>
#         <ul>
#             <li><A href="https://github.com/mleibman/SlickGrid/blob/gh-pages/examples/example1-simple.html" target="_sourcewindow"> View the source for this example on Github</a></li>
#         </ul>
#     </td>
#   </tr>
# </table>
# <script src="https://mleibman.github.io/SlickGrid/lib/jquery-1.7.min.js"></script>
# <script src="https://mleibman.github.io/SlickGrid/lib/jquery.event.drag-2.2.js"></script>
# <script src="https://mleibman.github.io/SlickGrid/slick.core.js"></script>
# <script src="https://mleibman.github.io/SlickGrid/slick.grid.js"></script>
# <script>
#   var grid;
#   var columns = [
#     {id: "title", name: "Title", field: "title"},
#     {id: "duration", name: "Duration", field: "duration"},
#     {id: "%", name: "% Complete", field: "percentComplete"},
#     {id: "start", name: "Start", field: "start"},
#     {id: "finish", name: "Finish", field: "finish"},
#     {id: "effort-driven", name: "Effort Driven", field: "effortDriven"}
#   ];
#   var options = {
#     enableCellNavigation: true,
#     enableColumnReorder: false
#   };
#   $(function () {
#     var data = [];
#     for (var i = 0; i < 500; i++) {
#       data[i] = {
#         title: "Task " + i,
#         duration: "5 days",
#         percentComplete: Math.round(Math.random() * 100),
#         start: "01/01/2009",
#         finish: "01/05/2009",
#         effortDriven: (i % 5 == 0)
#       };
#     }
#     grid = new Slick.Grid("#myGrid", data, columns, options);
#   })
# </script>
# """, unsafe_allow_html=True)
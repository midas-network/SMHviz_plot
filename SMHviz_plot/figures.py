import numpy as np
import plotly.express as px
from SMHviz_plot.utils import *


def add_scatter_trace(fig, data, legend_name, x_col="time_value", y_col="value", width=2, connect_gaps=True,
                      mode="lines+markers", color="rgb(110, 110, 110)", show_legend=True, subplot_coord=None,
                      hover_text=""):
    """ Add scatter trace to a Figure

    Add scatter trace on Figure object. By default, the hover text will be:

    ```
        "Value: {value}"

        "Epiweek: {time_value}"
    ```

    For more information on the parameters, please consult the plotly.graph_objects.Scatter() documentation

    :parameter fig: a Figure object to update
    :type fig: plotly.graph_objs.Figure
    :parameter data: a DataFrame containing the `x_col` and `y_col` columns
    :type data: pandas.DataFrame
    :parameter legend_name: Legend name of the associated trace (used also as legend group name)
    :type legend_name: str
    :parameter x_col: Name of the column to use for x-axis, by default `time_value`
    :type x_col: str
    :parameter y_col: Name of the column to use for y-axis, by default `value`
    :type y_col: str
    :parameter width: Width of the line, by default `2`
    :type width: float | int
    :parameter connect_gaps: Boolean to connect the gaps, by default `True`
    :type connect_gaps: bool
    :parameter mode: Drawing mode of this scatter trace, by default "lines+markers"
    :type mode: str
    :parameter color: Color of the trace to add, by default "rgb(110, 110, 110)"
    :type color: str
    :parameter show_legend: Boolean to show the legend; by default `True`
    :type show_legend: bool
    :parameter subplot_coord: For subplots, a list with 2 values: [row number, column number] indicating on which
        subplots to add the trace. `None` for non subplots object (default)
    :type subplot_coord: list | str
    :parameter hover_text: Appending text appearing on hover; by default, `""`
    :type hover_text: str
    :return: a plotly.graph_objs.Figure object with an added trace
    """
    if subplot_coord is None:
        subplot_coord = [None, None]
    fig.add_trace(go.Scatter(x=data[x_col],
                             y=data[y_col],
                             name=legend_name,
                             mode=mode,
                             marker=dict(color=color),
                             legendgroup=legend_name,
                             line=dict(width=width),
                             showlegend=show_legend,
                             hovertemplate=hover_text +
                             "<br>Value: %{y:,.2f}<br>Epiweek: %{x|%Y-%m-%d}<extra></extra>"),
                  row=subplot_coord[0], col=subplot_coord[1])
    fig.update_traces(connectgaps=connect_gaps)
    return fig


def make_proj_plot(fig_plot, proj_data, intervals=None, intervals_dict=None, x_col="target_end_date", y_col="value",
                   legend_col="model_name", legend_dict=None, line_width=2, color="rgba(0, 0, 255, 1)",
                   show_legend=True, point_value="median", opacity=None, connect_gaps=True, subplot_coord=None,
                   hover_text=""):
    """ Plot projection data on an existing Figure

    Plot projection data on an existing Figure for a specific tasks_id (scenario, target, location, model name, etc.)

    :parameter fig_plot:  a Figure object to update
    :type fig_plot: plotly.graph_objs.Figure
    :parameter proj_data: a DataFrame containing the `x_col` and `y_col` columns
    :type proj_data: pandas.DataFrame
    :parameter intervals: List of intervals to plot, by default `None`. If `None` ,it will be set to all possible
        values: `[0.95, 0.9, 0.8, 0.5]`
    :type intervals: list
    :parameter intervals_dict: Dictionary to translate `intervals` value into associated quantiles value, if "None"
        (default), will use internal dictionary:
            - 0.95: [0.025, 0.975]
            - 0.9: [0.05, 0.95]
            - 0.8: [0.1, 0.9]
            - 0.5: [0.25, 0.75]
    :type intervals_dict: dict
    :parameter x_col: Name of the column to use for x-axis, by default `target_end_date`
    :type x_col: str
    :parameter y_col: Name of the column to use for y-axis, by default `value`
    :type y_col: str
    :parameter point_value: To plot lines representing "median" (type_id = 0.5) or "point" value (type_id = NaN), "None"
        for no lines; by default "median".
    :type point_value: str
    :parameter legend_col: Name of the column to use for different traces (one trace per value), by default `model_name`
    :type legend_col: str
    :parameter legend_dict: a dictionary with value associated with `legend_col` variable (key, as in `proj_data`) and
        associated full name (value, for  legend purposes). If `None` (default), use information from the
        `legend_col` column for legend
    :type legend_dict: dict
    :parameter line_width: Width of the line, by default `2`
    :type line_width: float | int
    :parameter color: Color of the trace to add in a "rgba(X, Y, Z, 1)" format, (default) will use blue:
        `"rgba(0, 0, 255, 1)"`
    :type color: str
    :parameter show_legend: Boolean to show the legend; by default `True`
    :type show_legend: bool
    :parameter opacity: Opacity level of the intervals (ribbons); by default `None`, will generate opacity for each
        `intervals` value starting at 0.1 with a step of 0.1.
    :type opacity: list
    :parameter connect_gaps: Boolean to connect the gaps, by default `True`
    :type connect_gaps: bool
    :parameter subplot_coord: For subplots, a list with 2 values: [row number, column number] indicating on which
        subplots to add the trace. `None` for non subplots object (default)
    :type subplot_coord: list | str
    :parameter hover_text: Appending text appearing on hover; by default, `""`
    :type hover_text: str
    :return: a plotly.graph_objs.Figure object with an added trace
    """
    # Prerequisite
    # Subplot coordinate
    if subplot_coord is None:
        subplot_coord = [None, None]
    # Legend
    if legend_dict is not None:
        full_model_name = legend_dict[str(proj_data[legend_col].unique())]
    else:
        full_model_name = str(proj_data[legend_col].unique())
    # Order time value
    df_trace = proj_data.sort_values(x_col)
    # Figure add trace
    if point_value == "point":
        plot_df = df_trace[df_trace["type_id"].isna()]
    elif point_value == "median":
        plot_df = df_trace[df_trace["type_id"] == 0.5]
    else:
        plot_df = None
    # Opacity
    if intervals is not None and opacity is not None:
        if len(opacity) >= len(intervals):
            opacity.sort()
        else:
            val_opacity = opacity + [0.1, 0.1*len(intervals)]
            opacity = list(np.linspace(min(val_opacity), max(val_opacity), len(intervals)))
            opacity.sort()
    elif intervals is not None and opacity is None:
        val_opacity = [0.1, 0.1 * len(intervals)]
        opacity = list(np.linspace(min(val_opacity), max(val_opacity), len(intervals)))
        opacity.sort()
    else:
        opacity = [0.1]
    # Plot
    # Lines
    if plot_df is not None:
        fig_plot = add_scatter_trace(fig_plot, plot_df, full_model_name, x_col=x_col, y_col=y_col,
                                     mode="lines", width=line_width, connect_gaps=connect_gaps,
                                     show_legend=show_legend, color=color, subplot_coord=subplot_coord,
                                     hover_text=hover_text)
    # Intervals
    if intervals is not None:
        if len(intervals) == 1:
            quant_intervals = intervals_dict[intervals]
            fig_plot = ui_ribbons(fig_plot, df_trace, quant_intervals, full_model_name, x_col=x_col, y_col=y_col,
                                  color=color, opacity=opacity[0], subplot_coord=subplot_coord,
                                  hover_text=hover_text)
        elif len(intervals) > 1:
            intervals.sort(reverse=True)
            for i in range(0, len(intervals)):
                quant_intervals = intervals_dict[intervals[i]]
                fig_plot = ui_ribbons(fig_plot, df_trace, quant_intervals, full_model_name, x_col=x_col,
                                      y_col=y_col, color=color, opacity=opacity[i],
                                      subplot_coord=subplot_coord, hover_text=hover_text)
    return fig_plot


def make_scatter_plot(proj_data, truth_data, intervals=None, intervals_dict=None,
                      x_col="target_end_date", y_col="value", point_value="median", legend_col="model_name",
                      x_title="Horizon", y_title="N", subplot_var=None, subplot_title=None,
                      truth_legend_name="Truth Data", legend_dict=None, x_truth_col="time_value",
                      y_truth_col="value", viz_truth_data=True, hover_text="",
                      ensemble_name=None, ensemble_color=None, ensemble_view=False, line_width=2, connect_gaps=True,
                      color_dict=None, opacity=None, palette="turbo", title="", subtitle="", height=1000,
                      theme="plotly_white", notes=None, button=True, button_opt="all", v_lines=None, h_lines=None,
                      zoom_in_projection=None):
    """Create a Scatter Plot

    Create one plot for model projection output files. The function allows multiple view: adding truth data, projection
    one or multiple intervals, adding median lines, create subplots per a specific variable.

    Multiple layout parameters are also available:
        - highlight a specific value associated with a variable (for example a specific model)
        - specify colors for each specific plotting value or used a specific palette
        - change the opacity of the intervals
        - append the hover text
        - add a title, subtitle
        - change the theme and height of the output plot
        - add notes, button, horizon lines, vertical lines
        - specify a default zoom-in option

    By default, the intervals have for hover text:

    ```
        "{quant_sel[1] - quant_sel[0] * 100} % Intervals {value} - {value}"

        "Epiweek: {target_end_date}"
    ```

    the other traces have for hover text:

    ```
        "Value: {value}"

        "Epiweek: {target_end_date | time_value}"
    ```

    :parameter proj_data: Data frame containing the data to plot
    :type proj_data: pandas.DataFrame
    :parameter truth_data: Data frame containing the observed data to plot, set to None is no observed data plotted
    :type truth_data: pandas.DataFrame
    :parameter intervals: List of intervals to plot, by default `None`. If `None` ,it will be set to all possible
        values: `[0.95, 0.9, 0.8, 0.5]`
    :type intervals: list
    :parameter intervals_dict: Dictionary to translate `intervals` value into associated quantiles value, if "None"
        (default), will use internal dictionary:
            - 0.95: [0.025, 0.975]
            - 0.9: [0.05, 0.95]
            - 0.8: [0.1, 0.9]
            - 0.5: [0.25, 0.75]
    :type intervals_dict: dict
    :parameter x_col: Name of the column to use for x-axis, by default `target_end_date`
    :type x_col: str
    :parameter y_col: Name of the column to use for y-axis, by default `value`
    :type y_col: str
    :parameter point_value: To plot lines representing "median" (type_id = 0.5) or "point" value (type_id = NaN), "None"
        for no lines; by default "median".
    :type point_value: str
    :parameter legend_col: Name of the column to use for different traces (one trace per value), by default `model_name`
    :type legend_col: str
    :parameter x_title: Title of the x-axis
    :type x_title: str
    :parameter y_title: Title of the y-axis
    :type y_title: str
    :parameter subplot_var: Name of the column used to create the subplot (for example: subplot by list of
        scenario value associated with the column `scenario_id`)
    :type subplot_var: str
    :parameter subplot_title: Title(s) for each subplot. `None` for no titles.
    :type subplot_title: list | str
    :parameter truth_legend_name: Legend name of the associated trace (used also as legend group name), by default
        "Truth Data"
    :type truth_legend_name: str
    :parameter legend_dict: a dictionary with value associated with `legend_col` variable (key, as in `proj_data`) and
        associated full name (value, for  legend purposes). If `None` (default), use information from the
        `legend_col` column for legend
    :type legend_dict: dict
    :parameter x_truth_col: Name of the `truth_data` column to use for x-axis, by default `time_value`
    :type x_truth_col: str
    :parameter y_truth_col: Name of the `truth_data` column to use for y-axis, by default `value`
    :type y_truth_col: str
    :parameter: viz_truth_data: To view (`True`, default) or not (`False`) or in legend only (`"legendonly"`) the
        truth data
    :type viz_truth_data: bool | str
    :parameter hover_text: Appending text appearing on hover; by default, `""`
    :type hover_text: str
    :parameter ensemble_name: A`legend_col` value, if not `None, will be used to change the width (double) and the
        color (associated `ensemble_color` parameter) of the associated trace
    :type ensemble_name: str
    :parameter ensemble_color: Color name, if not `None`, will be used as color for the `legend_col` value associated
        with the parameter `ensemble_name`
    :type ensemble_color: str
    :parameter ensemble_view: To view (`True` or not (`False`, default)) only the `ensemble_name`, the other trace will
        be set to "legendonly"
    :type ensemble_view: bool
    :parameter line_width: Width of the line; double for `ensemble_name` (if not `None`), by default `2`
    :type line_width: float | int
    :parameter connect_gaps: Boolean to connect the gaps, by default `True`
    :type connect_gaps: bool
    :parameter color_dict: a dictionary with `legend_col` values (key) and associated color in the format
        "rgba(X, Y, Z, 1)" (value), if `None` (default) it will be created by using `palette`from
        plotly.express.colors scale.
    :type color_dict: dict
    :parameter opacity: Opacity level of the intervals (ribbons); by default `None`, will generate opacity for each
        `intervals` value starting at 0.1 with a step of 0.1.
    :type opacity: list
    :parameter palette: Name of the palette to create `color_dict` if `color_dict` is set to `None`. By default,
        "turbo". Value accepted should come from plotly.express.colors scale.
    :type palette: str
    :parameter title: Title of the plot, by default `""`
    :type title: str
    :parameter subtitle: Subtitle to add to the title, by default `""`
    :type subtitle: str
    :parameter height: Height of the output plot, by default `1000`px
    :type height: int
    :parameter theme: Plotly theme, by default `plotly_white`
    :type theme: str
    :parameter notes: Optional text to add at the bottom of the plot, on top of the legend
    :type notes: str
    :parameter button: if `True` (default), add a button on the top right of the plot, called "Ensemble" and allowing
        to display only one trace of interest (`ensemble_name`). Used only if `ensemble_name` is also not set to `None`.
    :type button: bool
    :parameter button_opt: if "all" (default), will add an "All" button, displaying all traces. Only if `button` is
        `True` and `ensemble_name` is not `None`
    :type button_opt: str
    :parameter v_lines: Dictionary containing the description of one or possible multiple vertical line on the plot,
        should be structured as: `v_lines = {"<name>":{"x": <value>, "line_width": <line width>,
        "line_color": <line color>, "line_dash": <line dash format>}}`, by default `None`
    :type v_lines: dict
    :parameter h_lines: Dictionary containing the description of one or possible multiple red dashed horizontal line
        on the plot, should be structured as: `h_lines = {"<name>":{"x": <value>, "text": <associated text>}}`;
        by default `None`
    :type h_lines: dict
    :parameter zoom_in_projection: Dictionary containing `x_min`, `x_max`, `y_min` and `y_max` value, to used as
        default zoom-in view, by default `None`
    :type zoom_in_projection: dict
    :return: a plotly.graph_objs.Figure object with model projection data
    """
    # Prerequisite
    # Figure preparation
    if subplot_var is not None:
        sub_var = proj_data[subplot_var].unique()
        fig_plot = prep_subplot(sub_var, subplot_title, x_title, y_title)
    else:
        sub_var = None
        fig_plot = go.Figure()
        fig_plot.update_layout(xaxis_title=x_title, yaxis_title=y_title)
    # Colorscale
    if color_dict is None:
        palette_list = px.colors.sample_colorscale(palette, len(proj_data[legend_col].unique()))
        for i in range(0, len(palette_list)):
            palette_list[i] = re.sub("\)", ", 1)", re.sub("rgb", "rgba", palette_list[i]))
        color_dict = dict(zip(proj_data[legend_col].unique(), palette_list))
    # Intervals
    if intervals_dict is None:
        intervals_dict = {0.95: [0.025, 0.975], 0.9: [0.05, 0.95], 0.8: [0.1, 0.9], 0.5: [0.25, 0.75]}
    # Plot
    # Figure with subplots
    in_legend = list()
    if sub_var is not None:
        for var in sub_var:
            df_facet = proj_data[proj_data[subplot_var] == var].drop(subplot_var, axis=1)
            subplot_coord = subplot_row_col(sub_var, var)
            if var == sub_var[0]:
                show_legend = True
            else:
                show_legend = False
            if truth_data is not None:
                fig_plot = add_scatter_trace(fig_plot, truth_data, truth_legend_name, show_legend=show_legend,
                                             hover_text=truth_legend_name, subplot_coord=subplot_coord,
                                             x_col=x_truth_col, y_col=y_truth_col, width=line_width,
                                             connect_gaps=connect_gaps)
            for mod_name in df_facet[legend_col].unique().sort():
                df_facet_trace = df_facet[df_facet[legend_col] == mod_name].drop(legend_col, axis=1)
                col_line = color_line_trace(color_dict, mod_name, ensemble_name=ensemble_name,
                                            ensemble_color=ensemble_color, line_width=line_width)
                if (mod_name not in in_legend) and (len(df_facet_trace) > 0):
                    in_legend.append(mod_name)
                    show_legend = show_legend
                else:
                    show_legend = False
                # Figure add trace
                fig_plot = make_proj_plot(fig_plot, proj_data, intervals=intervals, intervals_dict=intervals_dict,
                                          x_col=x_col, y_col=y_col, legend_col=legend_col, legend_dict=legend_dict,
                                          line_width=col_line[1], color=col_line[0], show_legend=show_legend,
                                          point_value=point_value, opacity=opacity, connect_gaps=connect_gaps,
                                          subplot_coord=subplot_coord, hover_text=hover_text)
    # Figure without subplots
    else:
        fig_plot = fig_plot
        if truth_data is not None:
            fig_plot = add_scatter_trace(fig_plot, truth_data, truth_legend_name, hover_text=truth_legend_name,
                                         x_col=x_truth_col, y_col=y_truth_col, width=line_width,
                                         connect_gaps=connect_gaps)
        for mod_name in proj_data[legend_col].unique().sort():
            df_trace = proj_data[proj_data[legend_col] == mod_name].drop(legend_col, axis=1)
            col_line = color_line_trace(color_dict, mod_name, ensemble_name=ensemble_name,
                                        ensemble_color=ensemble_color, line_width=line_width)
            # Figure add trace
            fig_plot = make_proj_plot(fig_plot, df_trace, intervals=intervals, intervals_dict=intervals_dict,
                                      x_col=x_col, y_col=y_col, legend_col=legend_col, legend_dict=legend_dict,
                                      line_width=col_line[1], color=col_line[0], show_legend=True,
                                      point_value=point_value, opacity=opacity, connect_gaps=connect_gaps,
                                      subplot_coord=[None, None], hover_text=hover_text)
    # View update
    to_vis = list()
    leg_only = list()
    if viz_truth_data is True:
        to_vis.append(truth_legend_name)
    elif viz_truth_data == "legendonly":
        leg_only.append(truth_legend_name)
    if ensemble_view is True:
        to_vis.append(ensemble_name)
        leg_only.append(proj_data[legend_col].unique())
        leg_only.remove(ensemble_name)
    else:
        to_vis.append(proj_data[legend_col].unique())
    for i in fig_plot.data:
        if i["name"] in to_vis:
            i["visible"] = True
        elif i["name"] in leg_only:
            i["visible"] = "legendonly"
        else:
            i["visible"] = False
    # Add notes
    if notes is not None:
        fig_plot.update_layout(legend={"title": {"text": notes + "<br>", "side": "top"}})
    # Add buttons
    if button is True and ensemble_name is not None:
        button = make_ens_button(fig_plot, viz_truth_data=viz_truth_data, truth_legend_name=truth_legend_name,
                                 ensemble_name=ensemble_name, button_name="Ensemble", button_opt=button_opt)
        fig_plot.update_layout(
            updatemenus=[dict(active=0, x=1.01, xanchor="left", type="buttons", buttons=button)]
        )
    # Add vertical lines
    if v_lines is not None:
        for v_name in v_lines:
            v_info = v_lines[v_name]
            fig_plot.add_vline(x=v_info["x"], line_width=v_info["line_width"], line_color=v_info["line_color"],
                               line_dash=v_info["line_dash"])
    # Add horizontal threshold
    if h_lines is not None:
        for h_name in h_lines:
            h_info = h_lines[h_name]
            fig_plot.add_hline(y=h_info["value"], line_width=1, line_color="red",
                               line_dash="dash", annotation=dict(font_size=10, font_color="red"),
                               annotation_position="bottom left",
                               annotation_text=h_info["text"])
    # Update layout
    fig_plot = subplot_fig_output(fig_plot, title=title, subtitle=subtitle, height=height, theme=theme)
    # Default Zoom-in
    if zoom_in_projection is not None:
        fig_plot.update_xaxes(range=[zoom_in_projection["x_min"], zoom_in_projection["x_max"]], autorange=False)
        fig_plot.update_yaxes(range=[zoom_in_projection["y_min"], zoom_in_projection["y_max"]], autorange=False)
    return fig_plot

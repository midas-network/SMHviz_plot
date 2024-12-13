from datetime import timedelta
import pandas as pd

from SMHviz_plot.utils import *
from utils_data import *


def add_scatter_trace(fig, data, legend_name, x_col="time_value", y_col="value", width=2, connect_gaps=None,
                      mode="lines+markers", color="rgb(110, 110, 110)", show_legend=True, subplot_coord=None,
                      hover_text="", line_width=0.0001, visible=True, dash=None, custom_data=None):
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
    :parameter connect_gaps: Boolean to connect the gaps, by default `None`
    :type connect_gaps: bool
    :parameter mode: Drawing mode of this scatter trace, by default "lines+markers"
    :type mode: str
    :parameter color: Color of the trace to add, by default "rgb(110, 110, 110)"
    :type color: str
    :parameter show_legend: Boolean to show the legend; by default `True`
    :type show_legend: bool | str
    :parameter subplot_coord: For subplots, a list with 2 values: [row number, column number] indicating on which
        subplots to add the trace. `None` for non subplots object (default)
    :type subplot_coord: list | str | None
    :parameter hover_text: Appending text appearing on hover; by default, `""`
    :type hover_text: str
    :parameter line_width: Line width of the markers
    :type line_width: float
    :parameter visible: Boolean or string indicating if the trace is visible or not or "legendonly"
    :type visible: bool | str
    :parameter dash: Option to print the line is dash, options include 'dash', 'dot', and 'dashdot'. By default, "None",
        no dash.
    :type dash: str | None
    :parameter custom_data: Add custom data
    :type dash: str | None | pandas.DataFrame
    :return: a plotly.graph_objs.Figure object with an added trace
    """
    if subplot_coord is None:
        subplot_coord = [None, None]
    fig.add_trace(go.Scatter(x=data[x_col],
                             y=data[y_col],
                             name=legend_name,
                             mode=mode,
                             marker=dict(color=color, line_width=line_width),
                             legendgroup=legend_name,
                             line=dict(width=width, dash=dash),
                             visible=visible,
                             showlegend=show_legend,
                             customdata=custom_data,
                             hovertemplate=hover_text +
                                           "Value: %{y:,.2f}<br>Epiweek: %{x|%Y-%m-%d}<extra></extra>"),
                  row=subplot_coord[0], col=subplot_coord[1])
    if connect_gaps is not None:
        fig.update_traces(connectgaps=connect_gaps)
    return fig


def add_bar_trace(fig, data, legend_name, x_col="time_value", y_col_max="max", y_col_min="min", width=7,
                  mode="lines", color="rgb(110, 110, 110)", show_legend=True, subplot_coord=None,
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
    :parameter y_col_max: Name of the column to use for y-axis, max value, by default `max`
    :type y_col_max: str
    :parameter y_col_min: Name of the column to use for y-axis, min value , by default `min`
    :type y_col_min: str
    :parameter width: Width of the line, by default `5`
    :type width: float | int
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
    for x_date in data[x_col].unique():
        if x_date == data[x_col].unique()[0]:
            show_leg = show_legend
        else:
            show_leg = False
        plot_data = data[data[x_col] == x_date]
        fig.add_trace(go.Scatter(x=[x_date, x_date],
                                 y=[plot_data[y_col_min][0], plot_data[y_col_max][0]],
                                 name=legend_name,
                                 mode=mode,
                                 legendgroup=legend_name,
                                 line=dict(width=width, color=color),
                                 showlegend=show_leg,
                                 hovertemplate=hover_text +
                                 "95% Interval: " + str(plot_data[y_col_min][0]) + " - " +
                                 str(plot_data[y_col_max][0]) + "<br>Epiweek: %{x|%Y-%m-%d}<extra></extra>"
                                 ),
                      row=subplot_coord[0], col=subplot_coord[1])
    fig.update_traces(connectgaps=False)
    return fig


def ui_ribbons(fig, df_plot, quant_sel, legend_name, x_col="target_end_date", y_col="value", color=None,
               opacity=0.1, subplot_coord=None, hover_text="", line_width=0.001, rm_second_hover=False,
               show_legend=False, special_hover=None):
    """ Add Intervals (ribbons) on Figure

    Add intervals information on Figure object. By default, the hover text will be:

    ```
        "{quant_sel[1] - quant_sel[0] * 100} % Intervals {value} - {value}"

        "Epiweek: {target_end_date}"
    ```

    :parameter fig: a Figure object to update
    :type fig: plotly.graph_objs.Figure
    :parameter df_plot: a DataFrame containing multiple columns: `type_id`: containing the quantiles value associated
        with the `quant_sel` parameter; `target_end_date`: date (x-axis) and `value`: value (y-axis)
    :type df_plot:  pandas.DataFrame
    :parameter quant_sel: list of at least 2 quantiles values to draw the interval
        (only the first 2 values will be used)
    :type quant_sel: list
    :parameter legend_name: Legend name of the associated trace (used also as legend group name)
    :type legend_name: str
    :parameter x_col: Name of the column to use for x-axis, by default `target_end_date`
    :type x_col: str
    :parameter y_col: Name of the column to use for y-axis, by default `value`
    :type y_col: str
    :parameter color: Color of the trace to add in a "rgba(X, Y, Z, 1)" format, if `None` (default) will use blue:
        "rgba(0, 0, 255, 1)"
    :type color: str
    :parameter opacity: Opacity level of the intervals (ribbons); by default `0.1`
    :type opacity: float | int
    :parameter subplot_coord: For subplots, a list with 2 values: [row number, column number] indicating on which
        subplots to add the trace. `None` for non subplots object (default)
    :type subplot_coord: list | str
    :parameter hover_text: Appending text appearing on hover; by default, `""`
    :type hover_text: str
    :parameter line_width: Width of the lines on the border of the intervals, by default `0.001`
    :type line_width: float | int
    :parameter rm_second_hover: Boolean to remove hover associated with the second `quant_sel` value; by default
        `FALSE`
    :type rm_second_hover: bool
    :parameter show_legend: Boolean to show the legend; by default `False`
    :type show_legend: bool
    :parameter special_hover: If not None, a dictionary contains the hover text for the ribbons with the keys: "first"
     and "second" indication the bottom and the top hover text of the ribbon, respectively. If not None will ignore
     all others "hover" parameters
    :type special_hover: dict | None
    :return: a plotly.graph_objs.Figure object with an added trace displaying intervals
    """
    # Prerequisite
    if subplot_coord is None:
        subplot_coord = [None, None]
    if color is None:
        color = "rgba(0, 0, 255, 1)"
    # Hover text
    if special_hover is None:
        second_hover_text = "<extra></extra>"
        if rm_second_hover is False:
            second_hover_text = hover_text + str(round((quant_sel[1] - quant_sel[0]) * 100)) + \
                                " % Interval: %{customdata:,.2f} - %{y:,.2f}<br>Epiweek: %{x|%Y-%m-%d}<extra></extra>"
        first_hover_text = (hover_text + str(round((quant_sel[1] - quant_sel[0]) * 100)) +
                            " % Interval: %{y:,.2f} - %{customdata:,.2f}<br>Epiweek: %{x|%Y-%m-%d}<extra></extra>")
    else:
        second_hover_text = special_hover["second"]
        first_hover_text = special_hover["first"]
    # Intervals
    fig.add_trace(go.Scatter(x=df_plot[df_plot["type_id"] == quant_sel[1]][x_col],
                             y=df_plot[df_plot["type_id"] == quant_sel[1]][y_col],
                             customdata=df_plot[df_plot["type_id"] == quant_sel[0]][y_col],
                             name=legend_name,
                             mode='lines',
                             line=dict(width=line_width),
                             marker=dict(color=re.sub(r", 1\)", ", " + str(opacity) + ")", color)),
                             legendgroup=legend_name,
                             showlegend=show_legend,
                             hovertemplate=second_hover_text),
                  row=subplot_coord[0], col=subplot_coord[1])
    fig.add_trace(
        go.Scatter(x=df_plot[df_plot["type_id"] == quant_sel[0]][x_col],
                   y=df_plot[df_plot["type_id"] == quant_sel[0]][y_col],
                   customdata=df_plot[df_plot["type_id"] == quant_sel[1]][y_col],
                   name=legend_name,
                   line=dict(width=line_width),
                   mode='lines',
                   marker=dict(color=re.sub(r", 1\)", ", " + str(opacity) + ")", color)),
                   legendgroup=legend_name,
                   showlegend=False,
                   fillcolor=re.sub(r", 1\)", ", " + str(opacity) + ")", color),
                   fill='tonexty',
                   hovertemplate=first_hover_text),
        row=subplot_coord[0], col=subplot_coord[1])
    return fig


def make_proj_plot(fig_plot, proj_data, intervals=None, intervals_dict=None, x_col="target_end_date", y_col="value",
                   legend_col="model_name", legend_dict=None, line_width=2, color="rgba(0, 0, 255, 1)",
                   show_legend=True, point_value="median", opacity=0.1, connect_gaps=True, subplot_coord=None,
                   hover_text=""):
    """ Plot projection data on an existing Figure

    Plot projection data on an existing Figure for a specific tasks_id (scenario, target, location, model name, etc.)

    :parameter fig_plot:  a Figure object to update
    :type fig_plot: plotly.graph_objs.Figure
    :parameter proj_data: a DataFrame containing the `x_col` and `y_col` columns
    :type proj_data: pandas.DataFrame
    :parameter intervals: List of intervals to plot, by default `None`. If `None` ,it will be set to all possible
        values: `[0.95, 0.9, 0.8, 0.5]`, please use an empty list for no intervals: `[]`
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
    :type opacity: int | float
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
        full_model_name = legend_dict[str(proj_data[legend_col].unique()[0])]
        proj_data_leg = proj_data.copy()
        proj_data_leg.loc[:, legend_col] = full_model_name
    else:
        full_model_name = "".join(list(proj_data[legend_col].unique()))
        proj_data_leg = proj_data.copy()
    # Order time value
    df_trace = proj_data_leg.sort_values(x_col)
    # Figure add trace
    if point_value == "point":
        plot_df = df_trace[df_trace["type_id"].isna()]
    elif point_value == "median":
        plot_df = df_trace[df_trace["type_id"] == 0.5]
    else:
        plot_df = None
    # Plot
    if len(re.findall("%{.+?}", hover_text)) > 0:
        hover_value = proj_data_leg[re.sub("%{|}", "",
                                           re.findall("%{.+?}", hover_text)[0])].unique()
        hover_value = list(hover_value)[0]
        hover_text = re.sub("%{.+?}", hover_value, hover_text)
    # Lines
    if plot_df is not None:
        fig_plot = add_scatter_trace(fig_plot, plot_df, full_model_name, x_col=x_col, y_col=y_col,
                                     mode="lines", width=line_width, connect_gaps=connect_gaps,
                                     show_legend=show_legend, color=color, subplot_coord=subplot_coord,
                                     hover_text=hover_text)
    # Intervals
    if intervals is not None:
        if isinstance(intervals, float | int):
            quant_intervals = intervals_dict[intervals]
            fig_plot = ui_ribbons(fig_plot, df_trace, quant_intervals, full_model_name, x_col=x_col, y_col=y_col,
                                  color=color, opacity=opacity, subplot_coord=subplot_coord,
                                  hover_text=hover_text)
        elif len(intervals) > 1:
            intervals.sort(reverse=True)
            for i in range(0, len(intervals)):
                if i == 0 and plot_df is None:
                    ui_show_legend = show_legend
                else:
                    ui_show_legend = False
                quant_intervals = intervals_dict[intervals[i]]
                fig_plot = ui_ribbons(fig_plot, df_trace, quant_intervals, full_model_name, x_col=x_col,
                                      y_col=y_col, color=color, opacity=opacity, show_legend=ui_show_legend,
                                      subplot_coord=subplot_coord, hover_text=hover_text)
    return fig_plot


def make_scatter_plot(proj_data, truth_data, intervals=None, intervals_dict=None,
                      x_col="target_end_date", y_col="value", point_value="median", legend_col="model_name",
                      x_title="Horizon", y_title="N", subplot_var=None, subplot_title=None, share_x="all",
                      share_y="all", truth_legend_name="Truth Data", legend_dict=None, x_truth_col="time_value",
                      y_truth_col="value", viz_truth_data=True, truth_data_type="scatter", truth_mode="lines+markers",
                      hover_text="", ensemble_name=None, ensemble_color=None, ensemble_view=False, line_width=2,
                      connect_gaps=True, color_dict=None, opacity=0.1, palette="turbo", title="", subtitle="",
                      height=1000, theme="plotly_white", notes=None, button=True, button_opt="all", v_lines=None,
                      h_lines=None, zoom_in_projection=None, specs=None, w_delay=None):
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
    :parameter share_x: Share x-axis in-between subplots. See `plotly.subplots.make_subplots()` for more information;
        by default `"all"`
    :type share_x: bool | str
    :parameter share_y: Share y-axis in-between subplots. See `plotly.subplots.make_subplots()` for more information;
        by default `"all"`
    :type share_y: bool | str
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
    :parameter truth_data_type: Type of plot for truth data: "scatter" or "bar" (vertical bar)
    :type truth_data_type: str
    :parameter truth_mode: Drawing mode of the truth data, only for scatter trace, by default "lines+markers"
    :type truth_mode: str
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
    :parameter opacity: Opacity level of the intervals (ribbons); by default `0.1`.
    :type opacity: int | float
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
        on the plot, should be structured as:
        h_lines = {"<name>":{"value": <value>, "text": <associated text>, "color": <associated color>,
                   "font_color":<associated font color>}, "font_size": <associated font size>}`;
        by default `None`
    :type h_lines: dict
    :parameter zoom_in_projection: Dictionary containing `x_min`, `x_max`, `y_min` and `y_max` value, to used as
        default zoom-in view, by default `None`
    :type zoom_in_projection: dict
    :parameter specs: Parameter `specs` as in the `plotly.subplots.make_subplots()` function. See
      plotly.subplots.make_subplots()` documentation for more details. Used only for plot with subplots.
    :type specs: list | None
    :parameter w_delay: For the truth data scatter plot, indicate a ending number of weeks to print in mode "markers"
      only . For example, if set to `4`, the last 4 weeks of the time series will be plotted in "markers" mode.
    :type w_delay: int | None
    :return: a plotly.graph_objs.Figure object with model projection data
    """
    # Prerequisite
    # Figure preparation
    if subplot_var is not None:
        sub_var = proj_data[subplot_var].unique()
        fig_plot = prep_subplot(sub_var, subplot_title, x_title, y_title, share_y=share_y, share_x=share_x,
                                sort=False, specs=specs)
    else:
        sub_var = None
        fig_plot = go.Figure()
        fig_plot.update_layout(xaxis_title=x_title, yaxis_title=y_title)
    # Colorscale
    if color_dict is None:
        color_dict = make_palette_sequential(proj_data, legend_col, palette=palette)
    # Intervals
    if intervals_dict is None:
        intervals_dict = {0.95: [0.025, 0.975], 0.9: [0.05, 0.95], 0.8: [0.1, 0.9], 0.5: [0.25, 0.75]}
    if intervals is None:
        intervals = [0.95, 0.9, 0.8, 0.5]
    # Plot
    # Figure with subplots
    in_legend = list()
    if sub_var is not None:
        for var in sub_var:
            df_facet = proj_data[proj_data[subplot_var] == var]
            if truth_data is not None:
                if subplot_var in truth_data.columns:
                    truth_facet = truth_data[truth_data[subplot_var] == var]
                else:
                    truth_facet = truth_data
            else:
                truth_facet = None
            subplot_coord = subplot_row_col(sub_var, var)
            if var == sub_var[0]:
                show_legend = True
            else:
                show_legend = False
            if truth_facet is not None:
                if truth_data_type == "scatter":
                    if w_delay is not None:
                        plot_truth_df = truth_facet[pd.to_datetime(truth_facet[x_truth_col]) <=
                                                    (max(pd.to_datetime(truth_facet[x_truth_col])) -
                                                     timedelta(weeks=w_delay))]
                    else:
                        plot_truth_df = truth_facet
                    fig_plot = add_scatter_trace(fig_plot, plot_truth_df, truth_legend_name, show_legend=show_legend,
                                                 hover_text=truth_legend_name + "<br>", subplot_coord=subplot_coord,
                                                 x_col=x_truth_col, y_col=y_truth_col, width=line_width,
                                                 connect_gaps=connect_gaps, mode=truth_mode)
                    if w_delay is not None:
                        plot_truth_df = truth_facet[pd.to_datetime(truth_facet[x_truth_col]) >
                                                    (max(pd.to_datetime(truth_facet[x_truth_col])) -
                                                     timedelta(weeks=w_delay))]
                        fig_plot = add_scatter_trace(fig_plot, plot_truth_df, truth_legend_name,
                                                     show_legend=False, hover_text=truth_legend_name + "<br>",
                                                     subplot_coord=subplot_coord, x_col=x_truth_col, y_col=y_truth_col,
                                                     width=line_width, connect_gaps=connect_gaps, mode="markers",
                                                     color="rgb(200, 200, 200)", line_width=0.5)
                elif truth_data_type == "bar":
                    fig_plot = add_bar_trace(fig_plot, truth_facet, truth_legend_name, show_legend=show_legend,
                                             hover_text=truth_legend_name + "<br>", subplot_coord=subplot_coord,
                                             x_col=x_truth_col)
                else:
                    fig_plot = fig_plot
            list_mod = list(df_facet[legend_col].unique())
            list_mod.sort()
            if ensemble_name in list_mod:
                list_mod.remove(ensemble_name)
                list_mod.append(ensemble_name)
            for mod_name in list_mod:
                df_facet_trace = df_facet[df_facet[legend_col] == mod_name]
                col_line = color_line_trace(color_dict, mod_name, ensemble_name=ensemble_name,
                                            ensemble_color=ensemble_color, line_width=line_width)
                if (mod_name not in in_legend) and (len(df_facet_trace) > 0):
                    in_legend.append(mod_name)
                    show_legend = show_legend
                else:
                    show_legend = False
                # Figure add trace
                fig_plot = make_proj_plot(fig_plot, df_facet_trace, intervals=intervals, intervals_dict=intervals_dict,
                                          x_col=x_col, y_col=y_col, legend_col=legend_col, legend_dict=legend_dict,
                                          line_width=col_line[1], color=col_line[0], show_legend=show_legend,
                                          point_value=point_value, opacity=opacity, connect_gaps=connect_gaps,
                                          subplot_coord=subplot_coord, hover_text=hover_text)
    # Figure without subplots
    else:
        fig_plot = fig_plot
        if truth_data is not None:
            if truth_data_type == "scatter":
                if w_delay is not None:
                    plot_truth_df = truth_data[pd.to_datetime(truth_data[x_truth_col]) <=
                                               (max(pd.to_datetime(truth_data[x_truth_col])) -
                                                timedelta(weeks=w_delay))]
                else:
                    plot_truth_df = truth_data
                fig_plot = add_scatter_trace(fig_plot, plot_truth_df, truth_legend_name, x_col=x_truth_col,
                                             hover_text=truth_legend_name + "<br>", y_col=y_truth_col, width=line_width,
                                             connect_gaps=connect_gaps, mode=truth_mode)
                if w_delay is not None:
                    plot_truth_df = truth_data[pd.to_datetime(truth_data[x_truth_col]) >
                                               (max(pd.to_datetime(truth_data[x_truth_col])) -
                                                timedelta(weeks=w_delay))]
                    fig_plot = add_scatter_trace(fig_plot, plot_truth_df, truth_legend_name, y_col=y_truth_col,
                                                 hover_text=truth_legend_name + "<br>", x_col=x_truth_col,
                                                 width=line_width, connect_gaps=connect_gaps, mode="markers",
                                                 color="rgb(200, 200, 200)", show_legend=False, line_width=0.5)
            elif truth_data_type == "bar":
                fig_plot = add_bar_trace(fig_plot, truth_data, truth_legend_name,
                                         hover_text=truth_legend_name + "<br>", x_col=x_truth_col)
            else:
                fig_plot = fig_plot
        list_mod = list(proj_data[legend_col].unique())
        list_mod.sort()
        if ensemble_name in list_mod:
            list_mod.remove(ensemble_name)
            list_mod.append(ensemble_name)
        for mod_name in list_mod:
            df_trace = proj_data[proj_data[legend_col] == mod_name]
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
    if viz_truth_data == True:
        to_vis.append(truth_legend_name)
    elif viz_truth_data == "legendonly":
        leg_only.append(truth_legend_name)
    if ensemble_view == True:
        to_vis.append(ensemble_name)
        leg_only = leg_only + list(proj_data[legend_col].unique())
        leg_only.remove(ensemble_name)
    else:
        if legend_dict is None:
            to_vis = to_vis + list(proj_data[legend_col].unique())
        else:
            for i in proj_data[legend_col].unique():
                to_vis.append(legend_dict[str(i)])
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
    if button == True and ensemble_name is not None:
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
            fig_plot.add_hline(y=h_info["value"], line_width=1, line_color=h_info["color"],
                               line_dash="dash", annotation=dict(font_size=h_info["font_size"],
                                                                 font_color=h_info["font_color"],
                                                                 font_family="Arial"),
                               annotation_position="top left",
                               annotation_text=h_info["text"])
    # Update layout
    fig_plot = subplot_fig_output(fig_plot, title=title, subtitle=subtitle, height=height, theme=theme)
    # Default Zoom-in
    if zoom_in_projection is not None:
        fig_plot.update_xaxes(range=[zoom_in_projection["x_min"], zoom_in_projection["x_max"]], autorange=False)
        fig_plot.update_yaxes(range=[zoom_in_projection["y_min"], zoom_in_projection["y_max"]], autorange=False)
    return fig_plot


def add_point_scatter(fig, df, ens_name, color_dict=None, multiply=1, symbol="circle", ens_symbol="diamond-wide",
                      size=20, opacity=0.7, legend_dict=None, show_legend=True, subplot_col=None, add_zero_line=True,
                      legend_col="model_name", palette="turbo"):
    """Add point scatter trace to a Figure

    Add point on Figure object.
    For more information on the parameters, please consult the plotly.graph_objects.Scatter() documentation

    :parameter fig: a Figure object to update
    :type fig: plotly.graph_objs.Figure
    :parameter df: Data frame containing the data to plot
    :type df: pandas.DataFrame
    :parameter ens_name: Name of the "Ensemble" variable, to plot on top of the other with a specific color
        (black) and symbol (see parameters `ens_symbol`). The name should be a value contains in the column
        defined via the `legend_col` parameter
    :type ens_name: str
    :parameter color_dict: Dictionary containing each legend value and the associated color, if `None` will
        be created by using the legend_col and palette parameter. Default, `None`
    :type color_dict: dict | str | None
    :parameter multiply: a value to multiply all the value. By default, 1
    :type multiply: int | float
    :parameter symbol: Marker symbol, by default "circle"
    :type symbol: str
    :parameter ens_symbol: "Ensemble" marker symbol. By default, "diamond-wide"
    :type ens_symbol: str
    :parameter size: Size of the markers
    :type size: int
    :parameter opacity: Opacity of the markers. By default, 0.7
    :type opacity: int | float
    :parameter legend_dict: a dictionary with value associated with `legend_col` variable (key, as in `df`) and
        associated full name (value, for  legend purposes). If `None` (default), use information from the
        `legend_col` column for legend
    :type legend_dict: dict
    :parameter show_legend: Boolean, to show the legend. By default, True
    :type show_legend: bool
    :parameter subplot_col: Name of the column used to create the subplot (for example: subplot by list of
        scenario value associated with the column `scenario_id`). By default, None (no subplot)
    :type subplot_col: int | None
    :parameter add_zero_line: Boolean, to add a dot horizontal line showing the 0 axis. By default, True
    :type add_zero_line: bool
    :parameter legend_col: Name of the column to use for the legend. By default, "model_name"
    :type legend_col: str
    :parameter palette: Name of the palette to apply, if `color_dict` is not set to None. By default, "turbo"
    :type palette: str
    :return: a plotly.graph_objs.Figure object
    """
    # prerequisite
    ens_marker = dict(symbol=ens_symbol, size=size, color="rgba(0,0,0," + str(opacity) + ")")
    multi = multiply
    if fig is None:
        fig = go.Figure()
    if subplot_col is None:
        subplot_col = 1
        # Colorscale
    if color_dict is None:
        color_dict = make_palette_sequential(df, legend_col, palette=palette)
    # figure
    df_comp_model = df[df[legend_col] != ens_name]
    for model in df_comp_model[legend_col].drop_duplicates():
        df_model = df_comp_model[df_comp_model[legend_col] == model]
        if legend_dict is not None:
            full_model_name = legend_dict[model]
        else:
            full_model_name = "".join(list(model))
        # prerequisite
        color_marker = color_line_trace(color_dict, model, line_width=0)
        color_marker = re.sub(r", 1\)", ", " + str(opacity) + ")", color_marker[0])
        model_marker = dict(size=20, color=color_marker, symbol=symbol)
        fig.add_trace(go.Scatter(x=df_model["full_x"],
                                 y=df_model["rel_change"] * multi,
                                 name=full_model_name,
                                 showlegend=show_legend,
                                 marker=model_marker,
                                 legendgroup=full_model_name,
                                 mode="markers",
                                 hovertemplate="%{x}: %{y:.1%}"),
                      row=1, col=subplot_col)
    df_comp_ens = df[df[legend_col] == ens_name]
    fig.add_trace(go.Scatter(x=df_comp_ens["full_x"],
                             y=df_comp_ens["rel_change"] * multi,
                             name=ens_name,
                             showlegend=show_legend,
                             marker=ens_marker,
                             legendgroup=ens_name,
                             mode="markers",
                             hovertemplate="%{x}: %{y:.1%}"),
                  row=1, col=subplot_col)
    # Add horizon line
    if add_zero_line is True:
        fig.add_hline(y=0, line_width=1, line_color="black", line_dash="dash")
    return fig


def make_point_comparison_plot(df, ens_name, plot_comparison=None, title=None, height=1000, theme="plotly_white",
                               color_dict=None, style="individual", x_col="target", x_dictionary=None,
                               x_order=None, subplot=False, subplot_col=None, subplot_titles=None, share_x="all",
                               share_y="all", legend_dict=None, legend_col="model_name", palette="turbo"):
    # Prerequisite
    if style == "inverse":
        multiply = -1
    else:
        multiply = 1
    # Prepare subplot
    if subplot is True:
        sub_var = df[subplot_col].unique()
        fig = prep_subplot(sub_var, subplot_titles, "", "", sort=False, share_x=share_x, share_y=share_y,
                           row_num=1)
    else:
        fig = go.Figure()
    # Plot
    if x_dictionary is not None:
        x_list = []
        for x_val in df[x_col]:
            x_list.append(x_dictionary[x_val])
    else:
        x_list = df[x_col]
    df_all = df.copy()
    df_all.loc[:, "full_x"] = x_list
    if x_order is not None:
        df_all["full_x"] = pd.CategoricalIndex(df_all["full_x"], ordered=True, categories=x_order)
        df_all = df_all.sort_values("full_x", ascending=True)
    if style == "individual":
        plot_comparison = list(df_all["comparison"].drop_duplicates())
        for comparison in plot_comparison:
            subplot_col = plot_comparison.index(comparison) + 1
            if comparison == plot_comparison[0]:
                show_legend = True
            else:
                show_legend = False
            df_comp = df_all[df_all["comparison"] == comparison]
            fig = add_point_scatter(fig, df_comp, ens_name, color_dict, legend_dict=legend_dict,
                                    show_legend=show_legend, subplot_col=subplot_col, add_zero_line=True,
                                    legend_col=legend_col, palette=palette, multiply=multiply)
    else:
        x_list_unique = []
        for x_val in x_list:
            if x_val not in x_list_unique:
                x_list_unique.append(x_val)
        x_axis_def = dict(zip(x_list_unique, range(1, len(x_list_unique) + 1)))
        tick_x1 = tick_label1 = tick_x2 = tick_label2 = []
        for targ in df_all["full_x"].drop_duplicates():
            df_sub = df_all[df_all["full_x"] == targ]
            for comp in plot_comparison:
                list_comparison = list(comp.keys())
                df_sub_c = df_sub[df_sub["comparison"].isin(list(list_comparison))].copy()
                subplot_col = list(plot_comparison).index(comp) + 1
                for comparison in list_comparison:
                    if comparison == list_comparison[0]:
                        x_axis = int(x_axis_def[targ]) + 0
                        if comp == list(plot_comparison)[0] and \
                                targ == list(df_all["full_x"].drop_duplicates())[0]:
                            show_legend = True
                        else:
                            show_legend = False
                    else:
                        x_axis = int(x_axis_def[targ]) + 0.65
                        show_legend = False
                    if comp == list(plot_comparison)[0]:
                        tick_x1.append(x_axis)
                        tick_label1.append(str(targ) + " - " + comparison)
                    else:
                        tick_x2.append(x_axis)
                        tick_label2.append(str(targ) + " - " + comparison)
                    df_sub_c["x_target"] = x_axis
                    fig = add_point_scatter(fig, df_sub_c, ens_name, color_dict, legend_dict=legend_dict,
                                            show_legend=show_legend, subplot_col=subplot_col, add_zero_line=True,
                                            legend_col=legend_col, palette=palette, multiply=multiply)
        fig.update_layout(xaxis1=dict(tickmode="array", tickvals=tick_x1, ticktext=tick_label1))
        fig.update_layout(xaxis2=dict(tickmode="array", tickvals=tick_x2, ticktext=tick_label2))
    # Update Layout
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True, tickangle=20)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True, tickformat=".1%")
    if isinstance(plot_comparison, dict):
        legend_param = dict(orientation="h", yanchor="top", xanchor="left", traceorder="grouped")
    else:
        legend_param = dict(orientation="v", yanchor="top", xanchor="left", traceorder="grouped")
    fig.update_layout(
        title=dict(text=title, font=dict(size=18), xanchor="center", xref="paper", x=0.5, yref="paper"),
        height=height, template=theme, legend=legend_param
    )
    return fig


def make_heatmap_plot(df, show_legend=True, subplot=False, subplot_col=None, subplot_titles=None, palette="ylorrd",
                      share_x="all", share_y="all", x_col="target_end_date", y_col="location_name", title=None,
                      height=1000, theme="plotly_white", sub_nrow=1, orientation="h"):
    if subplot is True:
        sub_var = list(df[subplot_col].unique())
        fig = prep_subplot(sub_var, subplot_titles, "", "", sort=False, share_x=share_x, share_y=share_y,
                           row_num=sub_nrow)
        for var in sub_var:
            df_plot = df[df[subplot_col] == var]
            if var == sub_var[0]:
                show_legend = show_legend
            else:
                show_legend = False
            plot_coord = subplot_row_col(sub_var, var, orientation=orientation)
            fig = fig.add_trace(
                go.Heatmap(z=df_plot["value"], x=df_plot[x_col], y=df_plot[y_col], coloraxis="coloraxis",
                           hovertemplate="x: %{x}<br>y: %{y}<br>z: %{z}<extra></extra>"),
                row=plot_coord[0], col=plot_coord[1])
    else:
        fig = go.Figure(data=go.Heatmap(z=df["value"], x=df[x_col], y=df[y_col], coloraxis="coloraxis"))
    fig.update_layout(
        title=dict(text=title, font=dict(size=18), xanchor="center", xref="paper", x=0.5, yref="paper"),
        height=height, template=theme, coloraxis={'colorscale': palette, 'colorbar': {'title': "Peak Probability"}})
    return fig


def add_box_plot(df_var, fig, x_col="model_name", y_col="type_id", box_value=None, color_dict=None,
                 box_orientation="h", show_legend=False, plot_coord=None):
    if plot_coord is None:
        plot_coord = [1, 1]
    if box_value is None:
        box_value = [0.01, 0.25, 0.5, 0.75, 0.99]
    for x_val in df_var[x_col].unique():
        df_plot = df_var[df_var[x_col] == x_val]
        if color_dict is None:
            color_x_val = "black"
        else:
            color_x_val = color_dict[x_val]
        fig = fig.add_trace(go.Box(
            orientation=box_orientation,
            y=df_plot[x_col].astype(str),
            lowerfence=df_plot[df_plot[y_col] == box_value[0]]["value"],
            q1=df_plot[df_plot[y_col] == box_value[1]]["value"],
            median=df_plot[df_plot[y_col] == box_value[2]]["value"],
            q3=df_plot[df_plot[y_col] == box_value[3]]["value"],
            upperfence=df_plot[df_plot[y_col] == box_value[4]]["value"],
            marker_color=color_x_val,
            name=x_val, showlegend=show_legend),
            row=plot_coord[0], col=plot_coord[1])
    return fig


def make_boxplot_plot(df, show_legend=False, subplot=False, subplot_col=None, subplot_titles=None, sub_nrow=1,
                      share_x="all", share_y="all", x_col="model_name", y_col="type_id", title=None, box_value=None,
                      height=1000, theme="plotly_white", sub_orientation="v", color_dict=None, box_orientation="h",
                      subplot_spacing=0.05):
    if subplot is True:
        sub_var = list(df[subplot_col].unique())
        fig = prep_subplot(sub_var, subplot_titles, "", "", sort=False, share_x=share_x, share_y=share_y,
                           row_num=sub_nrow, subplot_spacing=subplot_spacing)
        for var in sub_var:
            df_var = df[df[subplot_col] == var]
            if var == sub_var[0]:
                show_legend = show_legend
            else:
                show_legend = False
            plot_coord = subplot_row_col(sub_var, var, orientation=sub_orientation)
            fig = add_box_plot(df_var, fig, x_col=x_col, y_col=y_col, box_value=box_value, color_dict=color_dict,
                               box_orientation=box_orientation, show_legend=show_legend, plot_coord=plot_coord)
    else:
        fig = go.Figure()
        fig = add_box_plot(df, fig, x_col=x_col, y_col=y_col, box_value=box_value, color_dict=color_dict,
                           box_orientation=box_orientation, show_legend=show_legend, plot_coord=[1, 1])

    fig.update_layout(
        title=dict(text=title, font=dict(size=18), xanchor="center", xref="paper", x=0.5, yref="paper"),
        height=height, template=theme)
    return fig


def add_bar_plot(fig, df_var, df_other=None, truth_data=None, df_x="target_end_date", df_other_x="target_end_date",
                 truth_data_x="time_value", show_legend=True, obs_legend=True, title=None, height=1000, plot_coord=None,
                 var="Pathogen", other_var="Second Pathogen", truth_data_legend_name="Observed Data",
                 truth_data_tot_legend_name="Observed Data", theme="plotly_white", color='crimson',
                 color_other='deepskyblue', truth_data_tot_col="total_value"):
    if plot_coord is None:
        plot_coord = [1, 1]
    if truth_data is not None:
        fig.add_trace(go.Scatter(x=truth_data[truth_data_x], y=truth_data["value"],
                                 legendgroup="observed_data", name=truth_data_legend_name,
                                 marker=dict(color="black"), visible="legendonly", showlegend=obs_legend,
                                 hovertemplate=str(truth_data_legend_name) + ": %{y:,.2f}" + "<extra></extra>"),
                      row=plot_coord[0], col=plot_coord[1])
        if truth_data_tot_col in truth_data.columns:
            fig.add_trace(go.Scatter(x=truth_data[truth_data_x], y=truth_data[truth_data_tot_col],
                                     legendgroup="all_observed_data",
                                     name=truth_data_tot_legend_name,
                                     hovertemplate=str(truth_data_tot_legend_name) + ": %{y:,.2f}<extra></extra>",
                                     marker=dict(color="lightslategray"), visible="legendonly",
                                     showlegend=obs_legend),
                          row=plot_coord[0], col=plot_coord[1])
    fig.add_trace(
        go.Bar(x=df_var[df_x], y=df_var["value"], legendgroup=var, marker=dict(color=color),
               name=var, hovertemplate=str(var) + ": %{y:,.2f}<extra></extra>"),
        row=plot_coord[0], col=plot_coord[1])
    if df_other is not None:
        fig.add_trace(go.Bar(x=df_other[df_other_x], y=df_other["value"], legendgroup=other_var,
                             name=other_var, showlegend=show_legend,
                             marker=dict(color=color_other),
                             hovertemplate=str(other_var) + ": %{y:,.2f}<extra></extra>"),
                      row=plot_coord[0], col=plot_coord[1])
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig.update_layout(
        title=dict(text=title, xanchor="center", xref="paper", x=0.5, y=0.975, yanchor="middle"),
        height=height, template=theme, barmode="stack", hovermode="x",
        legend=dict(orientation="h", yanchor="top", xanchor="left", traceorder="grouped")
    )
    return fig


def make_bar_plot(df, df_other=None, truth_data=None, df_x="target_end_date", df_other_x="target_end_date",
                  truth_data_x="time_value", show_legend=True, subplot=False, title=None, height=1000,
                  subplot_col=None, truth_data_legend_name="Observed Data", truth_data_tot_legend_name="Observed Data",
                  df_legend_name="Pathogen", df_other_legend_name="Second Pathogen", subplot_titles=None,
                  share_x="all", share_y="all", x_title="", y_title="N", theme="plotly_white", color_dict=None,
                  palette=px.colors.qualitative.Plotly):
    if subplot is True:
        sub_var = list(df[subplot_col].unique())
        fig = prep_subplot(sub_var, subplot_titles, x_title, y_title, sort=False, share_x=share_x, share_y=share_y)
        if color_dict is None:
            color_dict = make_palette_sequential(df, subplot_col, palette=palette)
        for var in sub_var:
            df_var = df[df[subplot_col] == var]
            if var == sub_var[0]:
                show_legend = show_legend
                if truth_data is not None:
                    obs_legend = show_legend
                else:
                    obs_legend = False
            else:
                show_legend = False
                obs_legend = False
            plot_coord = subplot_row_col(sub_var, var)
            color = color_dict[var]
            other_var = list(df_other[subplot_col].unique())[0]
            fig = add_bar_plot(fig, df_var, df_other=df_other, truth_data=truth_data, df_x=df_x, df_other_x=df_other_x,
                               truth_data_x=truth_data_x, show_legend=show_legend, obs_legend=obs_legend,
                               title=title, height=height, plot_coord=plot_coord, var=var, other_var=other_var,
                               truth_data_legend_name=truth_data_legend_name, color=color,
                               truth_data_tot_legend_name=truth_data_tot_legend_name, theme=theme)

    else:
        fig = go.Figure()
        fig = add_bar_plot(fig, df, df_other=df_other, truth_data=truth_data, df_x=df_x, df_other_x=df_other_x,
                           truth_data_x=truth_data_x, show_legend=show_legend, obs_legend=show_legend,
                           title=title, height=height, plot_coord=[1, 1], var=df_legend_name,
                           other_var=df_other_legend_name,
                           truth_data_legend_name=truth_data_legend_name,
                           truth_data_tot_legend_name=truth_data_tot_legend_name, theme=theme)
    return fig


def add_spaghetti_plot(fig, df, color_dict, legend_dict=None,
                       legend_col="model_name", spag_col="type_id", show_legend=True, hover_text="", opacity=0.3,
                       subplot_coord=None, add_median=False, median=0.5):
    if add_median is True:
        df_med = df[df[spag_col] == median]
        df = df[df[spag_col] != median]
    else:
        df_med = None
    for leg in df[legend_col].drop_duplicates():
        # df_plot contains all data for a given model
        df_plot = df[df[legend_col] == leg].drop(legend_col, axis=1)
        if legend_dict is None:
            legend_name = leg
            col_line = color_line_trace(color_dict, leg)
        else:
            legend_name = legend_dict[leg]
            col_line = color_line_trace(color_dict, legend_name)
        # Prepare df with all trajectories in a model, separated by null rows
        # (which break up trajectories into different lines)
        temp = pd.DataFrame()
        traj_list = list(df_plot['type_id'].unique())
        temp.loc[:, 'value'] = [np.nan] * len(traj_list)
        temp.loc[:, 'type_id'] = traj_list
        temp.loc[:, 'target_end_date'] = [pd.NaT] * len(traj_list)
        all_traj_df = pd.concat([df_plot, temp], axis=0)
        all_traj_df = all_traj_df.sort_values(['type_id', 'target_end_date'])
        # Once Nan's are inserted between typeIDs, insert Nan in type ID col so hover text renders correctly
        all_traj_df.loc[pd.isna(all_traj_df['value']), 'type_id'] = np.nan

        # Add single trace
        color = re.sub(r", 1\)", ", " + str(opacity) + ")", col_line[0])
        fig = add_scatter_trace(fig, all_traj_df, legend_name, x_col="target_end_date",
                                mode="lines", color=color,
                                show_legend=show_legend, subplot_coord=subplot_coord,
                                custom_data=all_traj_df['type_id'],
                                hover_text=hover_text + "Model: " + legend_name + "<br>Type ID: %{customdata}<br>")
        if add_median is True and df_med is not None:
            df_plot_med = df_med[df_med[legend_col] == leg]
            add_scatter_trace(fig, df_plot_med, legend_name, x_col="target_end_date", show_legend=False,
                              mode="lines", subplot_coord=subplot_coord, width=4,
                              hover_text=hover_text + spag_col.title() + ": Median <br>", color=col_line[0])
    return fig


def add_spaghetti_plot_envelope(fig, df, color_dict, band_depth_limit, legend_dict=None,
                                legend_col="model_name", spag_col="type_id", show_legend=True,
                                hover_text="", opacity=0.3,
                                subplot_coord=None, add_median=False, median=0.5):
    """
    :param band_depth_limit: Show envelope around trajectories with band depth greater than X%
    """

    if add_median is True:
        df_med = df[df[spag_col] == median]
        df = df[df[spag_col] != median]
    else:
        df_med = None
    for leg in df[legend_col].drop_duplicates():
        # df_plot contains all data for a given model (and scenario and age group)
        df_plot = df[df[legend_col] == leg].drop(legend_col, axis=1)
        if legend_dict is None:
            legend_name = leg
            col_line = color_line_trace(color_dict, leg)
        else:
            legend_name = legend_dict[leg]
            col_line = color_line_trace(color_dict, legend_name)

        # Prepare df with all trajectories in a model, separated by null rows (which break up trajectories into different lines)
        temp = pd.DataFrame()
        traj_list = list(df_plot['type_id'].unique())
        temp.loc[:, 'value'] = [np.nan] * len(traj_list)
        temp.loc[:, 'type_id'] = traj_list
        temp.loc[:, 'target_end_date'] = [pd.NaT] * len(traj_list)
        all_traj_df = pd.concat([df_plot, temp], axis=0)
        all_traj_df = all_traj_df.sort_values(['type_id', 'target_end_date'])
        # Once Nan's are inserted between typeIDs, insert Nan in type ID col so hover text renders correctly
        all_traj_df.loc[pd.isna(all_traj_df['value']), 'type_id'] = np.nan
        band_depth_df = generate_band_depth_df(df_plot)
        all_traj_df = all_traj_df.merge(band_depth_df, how='left', on='type_id')

        # Add single trace
        connect_gaps = None
        color = re.sub(r", 1\)", ", " + str(opacity) + ")", col_line[0])
        fig.add_trace(go.Scatter(x=all_traj_df['target_end_date'],
                                 y=all_traj_df['value'],
                                 name=legend_name,
                                 mode='lines',
                                 marker=dict(color=color, line_width=0.0001),
                                 legendgroup=legend_name,
                                 line=dict(width=2, dash=None),
                                 visible=True,
                                 showlegend=show_legend,
                                 customdata=all_traj_df['type_id'],
                                 text=all_traj_df['band_depth'],
                                 hovertemplate=hover_text + f"Model: {legend_name}<br>"
                                                            "Type ID: %{customdata}<br>"
                                                            "Modified band depth: %{text:.2%}<br>"
                                                            "Value: %{y:,.2f}<br>Epiweek: %{x|%Y-%m-%d}<extra></extra>"
                                 ),
                      row=subplot_coord[0], col=subplot_coord[1])
        if connect_gaps is not None:
            fig.update_traces(connectgaps=connect_gaps)
        if add_median is True and df_med is not None:
            df_plot_med = df_med[df_med[legend_col] == leg]
            add_scatter_trace(fig, df_plot_med, legend_name, x_col="target_end_date",
                              show_legend=False,
                              mode="lines", subplot_coord=subplot_coord, width=4,
                              hover_text=hover_text + spag_col.title() + ": Median <br>",
                              color=col_line[0])

        # Add shaded region for trajectories with top X% of band depths
        band_depth_filtered = \
        band_depth_df.quantile(q=band_depth_limit, axis=0, interpolation='nearest').iloc[1]
        df_top_x_pctile = all_traj_df.loc[all_traj_df['band_depth'] >= band_depth_filtered, :]
        # shade region
        min_top_x_envelope = df_top_x_pctile.groupby('target_end_date')['value'].agg(
            'min').reset_index()
        max_top_x_envelope = df_top_x_pctile.groupby('target_end_date')['value'].agg(
            'max').reset_index()

        # Add trace for min
        fig.add_trace(go.Scatter(x=min_top_x_envelope['target_end_date'],
                                 y=min_top_x_envelope['value'],
                                 name=legend_name,
                                 mode='lines',
                                 legendgroup=legend_name,
                                 marker=dict(color=color, line_width=0.0001),
                                 line=dict(width=2, dash=None),
                                 visible=True,
                                 showlegend=False,
                                 ),
                      row=subplot_coord[0], col=subplot_coord[1])
        # Add trace for max
        fig.add_trace(go.Scatter(x=max_top_x_envelope['target_end_date'],
                                 y=max_top_x_envelope['value'],
                                 name=legend_name,
                                 mode='lines',
                                 legendgroup=legend_name,
                                 marker=dict(color=color, line_width=0.0001),
                                 line=dict(width=2, dash=None),
                                 visible=True,
                                 fill='tonexty',
                                 showlegend=False,
                                 ),
                      row=subplot_coord[0], col=subplot_coord[1])
    if connect_gaps is not None:
        fig.update_traces(connectgaps=connect_gaps)

    return fig


def make_spaghetti_plot(df, legend_col="model_name", spag_col="type_id", show_legend=True,
                        hover_text="", opacity=0.3,
                        subplot=False, title="", height=1000, subplot_col=None, subplot_titles=None,
                        palette="turbo",
                        share_x="all", share_y="all", x_title="", y_title="N", theme="plotly_white",
                        color_dict=None,
                        add_median=False, legend_dict=None, band_depth_limit=None):
    """
    :param band_depth_limit: if not None, must be a float X between 0 and 1 where the plot will
                             show envelope around trajectories with band depth greater than X%
    """

    # Colorscale
    if color_dict is None:
        color_dict = make_palette_sequential(df, legend_col, palette=palette)
    # Plot
    if subplot is True:
        sub_var = list(df[subplot_col].unique())
        fig = prep_subplot(sub_var, subplot_titles, x_title, y_title, sort=False, share_x=share_x,
                           share_y=share_y)
        for var in sub_var:
            df_var = df[df[subplot_col] == var].drop(subplot_col, axis=1)
            plot_coord = subplot_row_col(sub_var, var)
            if var == sub_var[0]:
                show_legend = show_legend
            else:
                show_legend = False
            if band_depth_limit and band_depth_limit >= 0 and band_depth_limit <= 1:
                add_spaghetti_plot_envelope(fig, df_var, color_dict=color_dict,
                                            legend_col=legend_col,
                                            spag_col=spag_col, show_legend=show_legend,
                                            hover_text=hover_text,
                                            opacity=opacity, subplot_coord=plot_coord,
                                            add_median=add_median,
                                            legend_dict=legend_dict,
                                            band_depth_limit=band_depth_limit)

            else:
                add_spaghetti_plot(fig, df_var, color_dict=color_dict, legend_col=legend_col,
                                   spag_col=spag_col, show_legend=show_legend,
                                   hover_text=hover_text,
                                   opacity=opacity, subplot_coord=plot_coord, add_median=add_median,
                                   legend_dict=legend_dict)
    else:
        fig = go.Figure()
        fig.update_layout(xaxis_title=x_title, yaxis_title=y_title)
        if band_depth_limit and band_depth_limit >= 0 and band_depth_limit <= 1:
            add_spaghetti_plot_envelope(fig, df, color_dict=color_dict, legend_col=legend_col,
                                        spag_col=spag_col, show_legend=show_legend,
                                        hover_text=hover_text,
                                        opacity=opacity, subplot_coord=None,
                                        add_median=add_median,
                                        legend_dict=legend_dict, band_depth_limit=band_depth_limit)

        else:
            add_spaghetti_plot(fig, df, color_dict=color_dict, legend_col=legend_col,
                               spag_col=spag_col, show_legend=show_legend, hover_text=hover_text,
                               opacity=opacity, subplot_coord=None, add_median=add_median,
                               legend_dict=legend_dict)
    subplot_fig_output(fig, title, subtitle="", height=height, theme=theme)
    return fig


def make_combine_multi_pathogen_plot(list_df, list_pathogen, truth_data=None, opacity=0.2, color=None, palette="turbo",
                                     intervals_dict=None, intervals=None, bar_interval=0.5, bar_calc="med", title=None,
                                     y_axis_title="", error_bar_pat=None):
    """Create the Multi-Pathogen Combined plot

    The Multi-pathogen Combined Plot contains 2 subplot representing the combination of multiple pathogens trajectories
    for a specific location, target and a subset of scenario selected by the user.

    The first subplot represents the 50%, 80%, 90% and 95% uncertainty intervals for the combination of all pathogen
    and for each pathogen (view updated with a button). It is possible to add the observed data (or truth data) on
    the plot via the `truth_data` parameter.

    The second subplot represents the median proportion of each selected pathogen on a stacked bar plot, with a
    50% uncertainty intervals (default value) error bars.

    The function `prep_multipat_plot_comb() outputs a dictionary with 2 objects: (1) "all":  median, 95%, 90%, 80%,
    and 50% quantiles for each "value" and "value_<pathogen>-<quantile>"columns and
    (2) "detail": median, 95%, 90%, 80%, and 50% quantiles for each "proportion_<pathogen>-<quantile>" columns.
    Each quantile is noted as: q1, q2, q3, q4, q5, q6, q7, q8, corresponding to: 0.025, 0.05, 0.1, 0.25, 0.75, 0.9,
    0.95, 0.975, respectively. The median and mean are noted as "med" and "mean", respectively.

    :parameter list_df: A dictionary with 2 DataFrame: (1) "all":  median, 95%, 90%, 80%, and 50% quantiles for the
     combined ("value" column) and for each pathogen ("value_<pathogen>" columns) and (2) "detail": median, 95%, 90%,
     80%, and 50% quantiles proportion for each pathogen ("proportion_<pathogen>" columns). Format in the same
     format as the output of the function `prep_multipat_plot_comb()`
    :type list_df: dict
    :parameter list_pathogen: list of pathogen represented in the plot
    :type list_pathogen: list
    :parameter truth_data: A DataFrame containing the observed data with the time in a `"time_value"` column, the
     main pathogen value in a `"value"` column and the combined observed value in a `"tot_value"` column. By default,
     `None`.
    :type truth_data: pd.DataFrame | None
    :parameter opacity: Opacity of the ribbons. By default, 0.2
    :type opacity: float
    :parameter color: A dictionary with the associated color for each pathogen and combined value with the name of the
     pathogen + "combined" as key and the color in "rgba(X,Y,Z,1)" format as value. If `"None"`, a dictionary will
     be created by using the palette parameter by default.
    :type color: dict | None
    :parameter palette: name of the palette or list of colors in rgb format. By default, "turbo"
    :type palette: list | str
    :parameter intervals_dict: Dictionary to translate `intervals` value into associated quantiles value, if "None"
        (default), will use internal dictionary:
            - 0.95: [q1, q8]
            - 0.9: [q2, q7]
            - 0.8: [q3, q6]
            - 0.5: [q4, q5]
    :type intervals_dict: dict
     :parameter intervals: List of intervals to plot in the first subplot, by default `None`. If `None` , all possible
        values: `[0.95, 0.9, 0.8, 0.5]` will be plotted
    :type intervals: list
    :parameter bar_interval: Interval to use for the error bar in the second subplot, by default `0.5`.
    :type bar_interval: float
    :parameter bar_calc: Value to use for the bar height, should match columns names. By default, "med"
    :type bar_calc: str
    :parameter title: Title of the plot, by default `None` (no title).
    :type title: str
    :parameter y_axis_title: Title of the first subplot, by default "".
    :type y_axis_title: str
    :parameter error_bar_pat: Name of the pathogen to draw at the bottom of the plot with error bar in the second
      subplot, by default `None`. If `None`, will take the first pathogen in the `list_pathogen` parameters
    :type error_bar_pat: str | None
    :return: a plotly.graph_objs.Figure object
    """
    # Preparation
    # Pathogen order/list
    if error_bar_pat is None:
        error_bar_pat = list_pathogen[0]
    elif error_bar_pat not in list_pathogen:
        print(error_bar_pat + " is not in `list_pathogen`. The first element of `list_pathogen` will be use instead.")
        error_bar_pat = list_pathogen[0]
    elif error_bar_pat != list_pathogen[0]:
        list_pathogen.remove(error_bar_pat)
        list_pathogen = [error_bar_pat] + list_pathogen
    low_list_pathogen = list()
    for pathogen in list_pathogen:
        low_list_pathogen.append(pathogen.lower())
    if intervals_dict is None:
        intervals_dict = {0.95: ["q1", "q8"], 0.9: ["q2", "q7"], 0.8: ["q3", "q6"], 0.5: ["q4", "q5"]}
        # Color preparation
        if color is None:
            color = make_palette_sequential(pd.DataFrame(data={"pathogen": ["Combined"] + list_pathogen}),
                                            "pathogen", palette=palette)
    # Subplot
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.05, shared_xaxes=True)
    # Scatter plot
    scatter_df = list_df["all"]
    col_value = ["value_" + pathogen for pathogen in low_list_pathogen] + ["value"]
    df_plot = pd.wide_to_long(scatter_df.reset_index(), col_value, j="type_id", i="target_end_date",
                              suffix="\\w+", sep="-").reset_index()
    df_plot.sort_values("target_end_date")
    if intervals is None:
        intervals = [0.95, 0.9, 0.8, 0.5]
    intervals.sort(reverse=True)
    for j in ["Combined"] + list_pathogen:
        if j == "Combined":
            col_name = ""
        else:
            col_name = "_" + j.lower()
        for i in range(0, len(intervals)):
            if i == 0:
                show_leg = True
            else:
                show_leg = False
            quant_sel = intervals_dict[intervals[i]]
            second_hover_text = (str(round(intervals[i] * 100)) +
                                 " % Interval: %{customdata:,.2f} - %{y:,.2f}<br>Epiweek: %{x|%Y-%m-%d}<extra></extra>")
            first_hover_text = (str(
                    round(intervals[i] * 100)) + " % Interval: %{y:,.2f} - %{customdata:,.2f}<br>Epiweek: %{x|%Y-%m-%d}"
                                                 + "<extra></extra>")
            fig = ui_ribbons(fig, df_plot, quant_sel, y_col="value" + col_name, legend_name=j, color=color[j],
                             show_legend=show_leg, opacity=opacity, subplot_coord=[1, 1],
                             special_hover={"first": first_hover_text, "second": second_hover_text})
            fig.for_each_trace(
                lambda trace: trace.update(visible=True) if trace.name == "Combined" else (),
            )
            fig.for_each_trace(
                lambda trace: trace.update(visible="legendonly") if trace.name != "Combined" else (),
            )
    if truth_data is not None:
        fig = add_scatter_trace(fig, truth_data, list_pathogen[0] + " Observed Data", subplot_coord=[1, 1],
                                hover_text=list_pathogen[0] + "<br>", color="rgba(0,0,0,1)", visible="legendonly")
        if "total_value" in truth_data.columns:
            fig = add_scatter_trace(fig, truth_data, " + ".join(list_pathogen) + "<br> Observed Data",
                                    y_col="total_value", subplot_coord=[1, 1], visible="legendonly",
                                    hover_text=" + ".join(list_pathogen) + "<br>")
    # Bar plot
    quant_sel = intervals_dict[bar_interval]
    bar_df = list_df["detail"]
    col_value = ["proportion_" + pathogen for pathogen in low_list_pathogen]
    df_plot = pd.wide_to_long(bar_df.reset_index(), col_value, j="type_id", i="target_end_date",
                              suffix="\\w+", sep="-").reset_index()
    bar_pathogen_list = list_pathogen.copy()
    bar_pathogen_list.reverse()
    med_point = pd.Series([1] * len(df_plot[df_plot["type_id"] == bar_calc]))
    for pathogen in bar_pathogen_list:
        med_val = df_plot[df_plot["type_id"] == bar_calc]["proportion_" + pathogen.lower()].reset_index(drop=True)
        med_point = med_point.subtract(med_val)
        fig.add_trace(go.Bar(
            x=df_plot["target_end_date"], marker=dict(color=color[pathogen]), showlegend=False,
            y=med_val, base=med_point, name="bar_" + pathogen), row=2, col=1)
        upper_bar = (
            df_plot[df_plot["type_id"] == quant_sel[1]]["proportion_" + pathogen.lower()].reset_index(drop=True))
        lower_bar = (
            df_plot[df_plot["type_id"] == quant_sel[0]]["proportion_" + pathogen.lower()].reset_index(drop=True))
        text_low_bar = round(lower_bar, 3)
        text_up_bar = round(upper_bar, 3)
        if pathogen == error_bar_pat:
            fig.update_traces(
                customdata=text_low_bar.astype(str) + " - " + text_up_bar.astype(str),
                hovertemplate="Epiweek: %{x|%Y-%m-%d}<br>" + bar_calc.title() + " " + pathogen +
                              ": %{y:,.3f}<br>" + str(bar_interval * 100) + "% Intervals: %{customdata}<extra></extra>",
                error_y=dict(type="data", symmetric=False, visible=True, array=list(upper_bar.subtract(med_val)),
                             arrayminus=list(med_val.subtract(lower_bar))),
                selector=dict(name="bar_" + pathogen))
        else:
            fig.update_traces(
                customdata=med_val,
                hovertemplate="Epiweek: %{x|%Y-%m-%d}<br>" + bar_calc.title() + " " + pathogen +
                              ": %{customdata:,.3f}<br>" + bar_calc.title() + " " +
                              " + ".join(bar_pathogen_list[bar_pathogen_list.index(pathogen):
                                                           len(bar_pathogen_list) + 1]) + ": %{y:,.3f}<extra></extra>",
                selector=dict(name="bar_" + pathogen))
    # Update layout
    # Button
    title_list_pathogen = list()
    for pathogen in list_pathogen:
        title_list_pathogen.append(pathogen)
    vis_list = list()
    comb_list = list()
    for i in fig.data:
        if i["yaxis"] == "y2":
            vis_list.append(True)
            comb_list.append(True)
        else:
            if i["name"] in title_list_pathogen:
                vis_list.append(True)
                comb_list.append("legendonly")
            elif i["name"] == "Combined":
                comb_list.append(True)
                vis_list.append("legendonly")
            else:
                comb_list.append("legendonly")
                vis_list.append("legendonly")
    button = list([
        dict(label="Combined",
             method="update",
             args=[{"visible": comb_list}])
    ])
    button = (button +
              list([
                  dict(label='Pathogens',
                       method='update',
                       args=[{'visible': vis_list}])
              ]))
    # Layout
    fig.update_layout(
        barmode="stack", height=1000, legend={"y": 0.5, "yanchor": "bottom", "itemsizing": "constant"},
        updatemenus=[dict(active=0, x=1.01, xanchor="left", type="buttons", buttons=button, showactive=True)],
        template="plotly_white", yaxis_title=y_axis_title, yaxis2_title="Proportion of Each Pathogen"
    )
    if title is not None:
        fig.update_layout(title=dict(text=title, font=dict(size=18), xanchor="center", xref="paper", x=0.5))
    return fig

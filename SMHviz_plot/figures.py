import pandas as pd

from SMHviz_plot.utils import *


def add_scatter_trace(fig, data, legend_name, x_col="time_value", y_col="value", width=2, connect_gaps=None,
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
    :parameter connect_gaps: Boolean to connect the gaps, by default `None`
    :type connect_gaps: bool
    :parameter mode: Drawing mode of this scatter trace, by default "lines+markers"
    :type mode: str
    :parameter color: Color of the trace to add, by default "rgb(110, 110, 110)"
    :type color: str
    :parameter show_legend: Boolean to show the legend; by default `True`
    :type show_legend: bool
    :parameter subplot_coord: For subplots, a list with 2 values: [row number, column number] indicating on which
        subplots to add the trace. `None` for non subplots object (default)
    :type subplot_coord: list | str | None
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
               opacity=0.1, subplot_coord=None, hover_text="", line_width=0, rm_second_hover=False,
               show_legend=False):
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
    :parameter line_width: Width of the lines on the border of the intervals, by default `0`
    :type line_width: float | int
    :parameter rm_second_hover: Boolean to remove hover associated with the second `quant_sel` value; by default
        `FALSE`
    :type rm_second_hover: bool
    :parameter show_legend: Boolean to show the legend; by default `False`
    :type show_legend: bool
    :return: a plotly.graph_objs.Figure object with an added trace displaying intervals
    """
    # Prerequisite
    if subplot_coord is None:
        subplot_coord = [None, None]
    if color is None:
        color = "rgba(0, 0, 255, 1)"
    # Hover text
    second_hover_text = "<extra></extra>"
    if rm_second_hover is False:
        second_hover_text = hover_text + str(round((quant_sel[1] - quant_sel[0]) * 100)) + \
                            " % Interval: %{customdata:,.2f} - %{y:,.2f}<br>Epiweek: %{x|%Y-%m-%d}<extra></extra>"
    # Intervals
    fig.add_trace(go.Scatter(x=df_plot[df_plot["type_id"] == quant_sel[1]][x_col],
                             y=df_plot[df_plot["type_id"] == quant_sel[1]][y_col],
                             customdata=df_plot[df_plot["type_id"] == quant_sel[0]][y_col],
                             name=legend_name,
                             mode='lines',
                             line=dict(width=line_width),
                             marker=dict(color=re.sub(", 1\)", ", " + str(opacity) + ")", color)),
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
                   marker=dict(color=re.sub(", 1\)", ", " + str(opacity) + ")", color)),
                   legendgroup=legend_name,
                   showlegend=False,
                   fillcolor=re.sub(", 1\)", ", " + str(opacity) + ")", color),
                   fill='tonexty',
                   hovertemplate=hover_text + str(round((quant_sel[1] - quant_sel[0]) * 100)) +
                        " % Interval: %{y:,.2f} - %{customdata:,.2f}<br>Epiweek: %{x|%Y-%m-%d}<extra></extra>"),
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
                if i is 0 and plot_df is None:
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
                      h_lines=None, zoom_in_projection=None):
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
                   "font_color":<associated font color>}}`;
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
        fig_plot = prep_subplot(sub_var, subplot_title, x_title, y_title, share_y=share_y, share_x=share_x,
                                sort=False)
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
                if truth_data_type is "scatter":
                    fig_plot = add_scatter_trace(fig_plot, truth_facet, truth_legend_name, show_legend=show_legend,
                                                 hover_text=truth_legend_name + "<br>", subplot_coord=subplot_coord,
                                                 x_col=x_truth_col, y_col=y_truth_col, width=line_width,
                                                 connect_gaps=connect_gaps, mode=truth_mode)
                elif truth_data_type is "bar":
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
            if truth_data_type is "scatter":
                fig_plot = add_scatter_trace(fig_plot, truth_data, truth_legend_name,
                                             hover_text=truth_legend_name + "<br>", x_col=x_truth_col,
                                             y_col=y_truth_col, width=line_width,
                                             connect_gaps=connect_gaps, mode=truth_mode)
            elif truth_data_type is "bar":
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
    if viz_truth_data is True:
        to_vis.append(truth_legend_name)
    elif viz_truth_data == "legendonly":
        leg_only.append(truth_legend_name)
    if ensemble_view is True:
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
            fig_plot.add_hline(y=h_info["value"], line_width=1, line_color=h_info["color"],
                               line_dash="dash", annotation=dict(font_size=10, font_color=h_info["font_color"]),
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
    :type subplot_col: str | None
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
        color_marker = re.sub(", 1\)", ", " + str(opacity) + ")", color_marker[0])
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
                      height=1000, theme="plotly_white", sub_orientation="v", color_dict=None, box_orientation="h"):
    if subplot is True:
        sub_var = list(df[subplot_col].unique())
        fig = prep_subplot(sub_var, subplot_titles, "", "", sort=False, share_x=share_x, share_y=share_y,
                           row_num=sub_nrow)
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
                 color_other='deepskyblue'):
    if plot_coord is None:
        plot_coord = [1, 1]
    if truth_data is not None:
        fig.add_trace(go.Scatter(x=truth_data[truth_data_x], y=truth_data["value"],
                                 legendgroup="observed_data", name=truth_data_legend_name,
                                 marker=dict(color="black"), visible="legendonly", showlegend=obs_legend,
                                 hovertemplate=str(truth_data_legend_name) + ": %{y:,.2f}" + "<extra></extra>"),
                      row=plot_coord[0], col=plot_coord[1])
        if "tot_value" in truth_data.columns:
            fig.add_trace(go.Scatter(x=truth_data[truth_data_x], y=truth_data["tot_value"],
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
        df_plot = df[df[legend_col] == leg].drop(legend_col, axis=1)
        if legend_dict is None:
            legend_name = leg
            col_line = color_line_trace(color_dict, leg)
        else:
            legend_name = legend_dict[leg]
            col_line = color_line_trace(color_dict, legend_name)
        for i in df_plot[spag_col].drop_duplicates():
            df_plot_i = df_plot[df_plot[spag_col] == i]
            df_plot_i = df_plot_i.sort_values("target_end_date")
            if i == list(df_plot[spag_col].drop_duplicates())[0]:
                show_legend_i = show_legend
            else:
                show_legend_i = False
            add_scatter_trace(fig, df_plot_i, legend_name, x_col="target_end_date", show_legend=show_legend_i,
                              mode="lines", subplot_coord=subplot_coord,
                              hover_text=hover_text + spag_col.title() + ": " + str(int(i)) + "<br>",
                              color=re.sub(", 1\)", ", " + str(opacity) + ")", col_line[0]))
        if add_median is True and df_med is not None:
            df_plot_med = df_med[df_med[legend_col] == leg]
            add_scatter_trace(fig, df_plot_med, legend_name, x_col="target_end_date", show_legend=False,
                              mode="lines", subplot_coord=subplot_coord, width=4,
                              hover_text=hover_text + spag_col.title() + ": Median <br>", color=col_line[0])
    return fig


def make_spaghetti_plot(df, legend_col="model_name", spag_col="type_id", show_legend=True, hover_text="", opacity=0.3,
                        subplot=False, title="", height=1000, subplot_col=None, subplot_titles=None, palette="turbo",
                        share_x="all", share_y="all", x_title="", y_title="N", theme="plotly_white", color_dict=None,
                        add_median=False, legend_dict=None):
    # Colorscale
    if color_dict is None:
        color_dict = make_palette_sequential(df, legend_col, palette=palette)
    # Plot
    if subplot is True:
        sub_var = list(df[subplot_col].unique())
        fig = prep_subplot(sub_var, subplot_titles, x_title, y_title, sort=False, share_x=share_x, share_y=share_y)
        for var in sub_var:
            df_var = df[df[subplot_col] == var].drop(subplot_col, axis=1)
            plot_coord = subplot_row_col(sub_var, var)
            if var == sub_var[0]:
                show_legend = show_legend
            else:
                show_legend = False
            add_spaghetti_plot(fig, df_var, color_dict=color_dict, legend_col=legend_col,
                               spag_col=spag_col, show_legend=show_legend, hover_text=hover_text,
                               opacity=opacity, subplot_coord=plot_coord, add_median=add_median,
                               legend_dict=legend_dict)
    else:
        fig = go.Figure()
        fig.update_layout(xaxis_title=x_title, yaxis_title=y_title)
        add_spaghetti_plot(fig, df, color_dict=color_dict, legend_col=legend_col,
                           spag_col=spag_col, show_legend=show_legend, hover_text=hover_text,
                           opacity=opacity, subplot_coord=None, add_median=add_median, legend_dict=legend_dict)
    subplot_fig_output(fig, title, subtitle="", height=height, theme=theme)
    return fig

import re
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def prep_subplot(sub_var, sub_title, x_title, y_title, sort=True, font_size=14, subplot_spacing=0.05, share_x="all",
                 share_y="all"):
    """ Prepare Plotly subplot object

    Prepared a Plotly Figure object with predefined subplots information:
        - column grid: 2 if length `sub_var` is superior to 1 (1 if not)
        - row grid: length of `sub_var` divided by 2 (+1 for odd number) or 1 if length of `sub_var` is lesser than 3

    :parameter sub_var: List of value associated with the variable used to create the subplot (for example: list of
        scenario value associated with the column `scenario_id`)
    :type sub_var: list
    :parameter sub_title: Title(s) for each subplot, should be of same length as `sub_var`. `None` for no titles.
    :type sub_title: list
    :parameter x_title: Title of the x-axis
    :type x_title: str
    :parameter y_title: Title of the y-axis
    :type y_title: str
    :parameter sort: Boolean to indicate if the `sub_var` should be sorted alphabetically, by default `True`
    :type sort: bool
    :parameter font_size:  Font size of the subplots annotation, by default `14`
    :type font_size: int
    :parameter subplot_spacing: Space between subplot rows and columns, must be a float between 0 and 1; by default
        `0.05`
    :type subplot_spacing: int | float
    :parameter share_x: Share x-axis in-between subplots. See `plotly.subplots.make_subplots()` for more information;
        by default `"all"`
    :type share_x: bool | str
    :parameter share_y: Share y-axis in-between subplots. See `plotly.subplots.make_subplots()` for more information;
        by default `"all"`
    :type share_y: bool | str
    :return: a Plotly subplots object; `plotly.graph_objs.Figure` with predefined subplots configured in 'layout
    """
    # Sort value
    if sort is True:
        sub_var.sort()
    # Row and Columns information
    if len(sub_var) > 2:
        col_num = 2
        if len(sub_var) % 2 == 0:
            row_num = len(sub_var) / 2
        else:
            row_num = (len(sub_var) + 1) / 2
    else:
        row_num = 1
        col_num = len(sub_var)
    # Subplots
    fig = make_subplots(rows=int(row_num), cols=int(col_num), subplot_titles=sub_title, shared_yaxes=share_y,
                        shared_xaxes=share_x, vertical_spacing=subplot_spacing, horizontal_spacing=subplot_spacing,
                        x_title=x_title, y_title=y_title)
    fig.update_annotations(font_size=font_size)
    return fig


def subplot_row_col(sub_var, var):
    """ Returns row and column information

    For a subplots Figure, returns the associated row and column information for a specific value for an object
    created with `prep_subplot()` function and containing less than 7 plots in the subplot object.

    :parameter sub_var: List of value associated with the variable used to create the subplot (for example: list of
        scenario value associated with the column `scenario_id`
    :type sub_var: list
    :parameter var: A specific value from the `sub_var` list
    :type var: str | float | int
    :return: a list with 2 values: [row number, column number] in the subplots
    """
    scen_order_dict = dict(zip(sub_var, list(range(len(sub_var)))))
    if scen_order_dict[var] < 2:
        n_row = 1
    elif scen_order_dict[var] < 4:
        n_row = 2
    else:
        n_row = 3
    if scen_order_dict[var] % 2 == 0:
        n_col = 1
    else:
        n_col = 2
    return [n_row, n_col]


def subplot_fig_output(fig, title, subtitle="", height=1000, theme="plotly_white"):
    """ Update Figure Layout

    For a Figure object, update the layout to include:
        - x and y axes with mirrored black line of width 1
        - a title with `title` + `subtitle` text, font 18, in a center position
        - a plot with: height (by default 1000), theme `plotly_white` (default) and a horizontal legend with grouped
        trace, at the bottom of the plot

    :parameter fig: a Figure object to update
    :type fig: plotly.graph_objs.Figure
    :parameter title: Title of the plot
    :type title: str
    :parameter subtitle: Subtitle to add to the title, by default `""`
    :type subtitle: str
    :parameter height: Height of the output plot, by default `1000`px
    :type height: int
    :parameter theme: Plotly theme, by default `plotly_white`
    :type theme:
    :return: a plotly.graph_objs.Figure object with updated layout properties
    """
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig.update_layout(
        title=dict(text=title + subtitle, font=dict(size=18), xanchor="center", xref="paper", x=0.5),
        height=height, template=theme, legend=dict(orientation="h", yanchor="top", xanchor="left", traceorder="grouped")
    )
    return fig


def make_blank_slider(x=0, y=-0.2, prefix="Date: ", font_color="gray", font_size=16, duration=300):
    """ Create the base for a slider

    Create a dictionary containing the "blank" base for a slider with:
        - "active" equal to 0
        - x and y location being set to 0 (default, x left), -0.2 (default, y top)
        - current value: with as prefix "Date: " (default); xanchor on the right and with a gray font size 16 (default)
        - transition: duration of 300 (default) and easing "cubic-in-out"
        - steps: empty list

    :parameter x: coordinates x of the slider location on the plot; by default `0`
    :type x: int | float
    :parameter y: coordinates y of the slider location on the plot; by default `-0.2`
    :type y: int | float
    :parameter prefix : Prefix to append to the selected value on the slider; by default `Date: `
    :type prefix: str
    :parameter font_color: Color of the selected value font; by default `gray`
    :type font_color: str
    :parameter font_size: Size of the selected value font; by default `gray`
    :type font_size: int
    :parameter duration: Slider duration transition; by default `300`
    :type duration: int
    :return: a dictionary with "blank" slider information
    """
    sliders_dict = {
        "active": 0,
        "x": x, "xanchor": "left", "y": y, "yanchor": "top",
        "currentvalue": {
            "prefix": prefix,
            "xanchor": "right",
            "font": {"size": font_size, "color": font_color}},
        "transition": {"duration": duration, "easing": "cubic-in-out"},
        "steps": []
    }
    return sliders_dict


def make_slider_buttons(x=-0.1, y=-0.25, redraw=False, duration=300):
    """ Create the base for a slider "Play/Pause" button

    Create a dictionary containing the basic information for a "play/pause" button to associate with a slider, with:
        - x and y location being set to -0.1 (default, x left), -0.25 (default, y bottom)
        - [play]
            - transition: duration of 300 (default) and easing "quadratic-in-out"
            - frame: duration 0f 200 (duration - 100)

    :parameter x: coordinates x of the slider location on the plot; by default `-0.1`
    :type x: int | float
    :parameter y: coordinates y of the slider location on the plot; by default `-0.25`
    :type y: int | float
    :parameter redraw: Boolean, button redraw associated information, by default `False`
    :parameter redraw: bool
    :parameter duration: Slider duration transition; by default `300`
    :type duration: int
    :return: a dictionary with "play/pause" button information to associate with a slider
    """
    button = [
        {'buttons': [{'args': [None, {'frame': {'duration': duration - 100, 'redraw': redraw}, 'fromcurrent': True,
                                      'transition': {'duration': duration, 'easing': 'quadratic-in-out'}}],
                      'method': 'animate', 'label': 'Play'},
                     {'args': [[None], {'frame': {'duration': 0, 'redraw': redraw}, 'mode': 'immediate',
                                        'transition': {'duration': 0}}],
                      'label': 'Pause', 'method': 'animate'}],
         "type": "buttons", "showactive": False,
         "x": x, "xanchor": "left", "y": -y, "yanchor": "bottom"
         }]
    return button


def make_ens_button(fig_plot, viz_truth_data=True, truth_legend_name="Truth Data", ensemble_name=None,
                    button_name="Ensemble", button_opt="all"):
    """ Ensemble button

    Create a button (called "Ensemble" by default), allowing to display only one trace of interest (`ensemble_name`),
    with the possibility to display truth data also (viz_truth_data, truth_legend_name). It is also possible to
    add a second "All" button, displaying all the traces in the plot.

    :parameter fig_plot:  a Figure object to update
    :type fig_plot: plotly.graph_objs.Figure
    :parameter: viz_truth_data: To view (`True`, default) or not (`False`) the truth_data
    :type viz_truth_data: bool
    :parameter truth_legend_name: Legend name of the associated trace, by default
        "Truth Data"
    :type truth_legend_name: str
    :parameter ensemble_name: A trace name value to display by default and when button `"Ensemble"` (default name) is
        clicked.
    :type ensemble_name: str
    :parameter button_name: Label name of the default button, by default "Ensemble"
    :type button_name: str
    :parameter button_opt: if "all", will add an "All" button, displaying all traces
    :type button_opt: str
    :return: a dictionary containing the button information to display only the "ensemble" (or all traces)
    """
    to_vis = list()
    vis_list = list()
    if viz_truth_data is True:
        to_vis.append(truth_legend_name)
    to_vis.append(ensemble_name)
    for i in fig_plot.data:
        if i["name"] in to_vis:
            vis_list.append(True)
        else:
            vis_list.append("legendonly")
    button = list([
        dict(label=button_name,
             method="update",
             args=[{"visible": vis_list}])
    ])
    if button_opt == "all":
        button = button + list([
            dict(label='All',
                 method='update',
                 args=[{'visible': [True]}])
        ])
    return button


def fig_error_message(text, height=500):
    """ Empty Figure with Error text

    Create an empty figure with an annotation text in the middle

    :parameter text: Text to display
    :type text: str
    :parameter height: Height of the output plot, by default `500` px
    :type height: int
    :return: an empty `plotly.graph_objs.Figure` with only a text displayed
    """
    fig = go.Figure()
    fig.update_yaxes(visible=False)
    fig.update_xaxes(visible=False)
    fig.update_layout(annotations=[{
        "text": text,
        "xref": "paper",
        "yshift": 90,
        "showarrow": False
    }], template="plotly_white", height=height)
    return fig


def color_line_trace(color_dict, mod_name, ensemble_name=None, ensemble_color=None, line_width=2):
    """ Returns the line and color for a particular key

    Returns the line and color for a particular key: if the ensemble name is equivalent to mod_name then
    `ensemble_color` will be used instead of `color_dict` for color and the line_width will be doubled.

    :parameter color_dict: a dictionary with keys and associated color in the format
        "rgba(X, Y, Z, 1)" (value)
    :type color_dict: dict
    :parameter mod_name: one of the key of `color_dict`
    :type mod_name: str
    :parameter ensemble_name: A`legend_col` value, if not `None, will be used to change the width (double) and the
        color (associated `ensemble_color` parameter) of the associated trace
    :type ensemble_name: str
    :parameter ensemble_color: Color name, if not `None`, will be used as color for the `legend_col` value associated
        with the parameter `ensemble_name`
    :type ensemble_color: str
    :param line_width: Width of the line, by default `2`
    :type line_width: float | int
    :return: a list with [color, line_width] information
    """
    if ensemble_name is not None and ensemble_color is not None and mod_name == ensemble_name:
        color = ensemble_color
        line_width = line_width * 2
    else:
        color = color_dict[mod_name]
        line_width = line_width
    return [color, line_width]


def make_palette(df, legend_col, palette="turbo"):
    if len(df[legend_col].unique()) > 1:
        palette_list = px.colors.sample_colorscale(palette, len(df[legend_col].unique()))
        for i in range(0, len(palette_list)):
            palette_list[i] = re.sub("\)", ", 1)", re.sub("rgb", "rgba", palette_list[i]))
        color_dict = dict(zip(df[legend_col].unique(), palette_list))
    else:
        color_dict = dict(zip(df[legend_col].unique(), "rgba(0, 0, 255, 1)"))
    return color_dict

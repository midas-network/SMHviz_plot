# Plot Description

This page contains a description of all the US Scenario 
Modeling Hub (SMH) plots used on the SMH websites.

All plots are written  in Plotly to allow interactivity.
For example, all the legends are 2 options:
- Double-click on a legend name to only display it
- Click on a legend name to display it or not on the plot

## Scenario Plot

### Plot:
To visualize all projections (ensembles and team-models projection) 
per scenario for a specific location, target.

Creates one subplot per scenario containing all the projections for 
the round plus the observed data associated with the selected target 
(if available) for a specific location.  

By default, only the default ensemble (in black) and the observed data 
for the round is viewed, other projections are accessible via the 
interactive legend, filters and buttons.
 
#### Vertical lines:

- Projection epiweek: the start week date of the projection is marked 
  by a vertical plain gray line
- Current week: the current week date is marked by a dotted vertical 
  gray line. If the current date is past the end date of the round, 
  this line will not appear on the plot.
 
#### Different possible views:

- Available filter: The plot can be filtered by multiple input:
  - Sidebar selection:
    - Scenario: one subplot for each selected scenario 
    - Location: the plot shows the value for one specific location 
    - Target: the plot shows the value for one specific target 
    - Uncertainty interval: multiple interval are possible:
      - Multi (optional):  displays 95% (quantiles 0.025 and 0.975),  
        90% (quantiles 0.05 and 0.95), 80% (quantiles 0.1 and 0.9), 
        and 50% (quantiles 0.25 and 0.75) uncertainty intervals, 
        shaded from lightest (95%) to darkest (50%). 
      - 95 %: displays 95%  uncertainty interval with the "main" 
        line (point or 0.5 quantile value)
      - 50 %: displays 50%  uncertainty interval with the "main"
        line (point or 0.5 quantile value)
      - None: displays the "main" line (point or 0.5 quantile value)
  - Plot specific filter:
      - Additional Ensemble: if a round contains multiple ensembles, 
        only the default ensemble is plotted. To add all the possible 
        ensembles, the "Show Additional Ensemble" checkbox needs to 
        be selected.
      - Plot interactivity:
        - Buttons: the plot contains a right side buttons with 2 options:
          - "Ensemble": only the default ensemble and observed data 
            are visible on the plot, all the other projections are 
            disable but available via the legend
          - "All": plot all projections and observed data (not 
            available if "multi" is selected for uncertainty level)
 
#### Optional Additions:

- Horizontal line: a red dotted line can be added to the plot to show 
past peak value or threshold information. The "peak" line is created by 
searching the maximum value in a specific time frame.

- Add Notes: a short note and a "\*" on specific legend name can be added 
via some specific parameters.

 
#### Default View:

- Plot "main" line:
  - Before round 17: the "point" value is used to draw the main line of 
  each projection, corresponds to the quantile 0.5 for all the ensembles
  - Starting round 17: the quantile 0.5 value is used to draw the main 
  line of each projection
- Scenario: all scenario selected, exception for the Round 11, only scenario
  A and B are selected
- Location: "US"
- Target:
  - Before Round 15: "Incident Cases"
  - Round 15 and ongoing: "Incident Hospitalization"
- Uncertainty level:
  - Before Round 11: "95%"
  - Round 11 and ongoing: "Multi"
- Zoom-in: By default the plot is zoomed-in to show the last 6 months of 
observed data (if available) and the complete round projection time frame 
on the x-axis. On the y-axis, the plot is zoomed-in to the maximum value 
found on the "zoom-in" x-axis time frame. It’s possible to zoom-out by 
using the Plotly controls.
 
## Model Specific Plot
 
### Plot:
Creates one subplot per target containing all the scenario projections 
for a specific projection plus the last 4 months of observed data (if 
available) for a specific location.  

By default, the default ensemble and the observed data for the round 
is viewed for all the weekly incident targets, other projections are 
accessible via the interactive legend, filters and buttons.
 
#### Different possible views:

- Available filter: The plot can be filtered by multiple input:
  - Sidebar selection:
    - Location: the plot shows the value for one specific location 
    - Uncertainty interval: multiple interval are possible:
      - 95 %: displays 95% (quantiles 0.025 and 0.975) uncertainty 
      interval with the "main" line (point or 0.5 quantile value)
      - 50 %: displays 50% (quantiles 0.25 and 0.75) uncertainty 
      interval with the "main" line (point or 0.5 quantile value)
      - None: displays the "main" line (point or 0.5 quantile value)
  - Plot specific filter:
    - Outcome type: If cumulative and incident target are included in 
    the round, the incident target will be plotted by default, but 
    the cumulative target are available to view by selecting "Cumulative"
    - Model Dropdown:  Select the model-team projection or ensemble 
    to plot (default ensemble, by default)
    - Additional Ensemble: if a round contains multiple ensembles, 
    only the default ensemble is included in the model dropdown. 
    To add all the possible ensembles, the "Show Additional Ensemble" 
    checkbox needs to be selected.
 
#### Default View:
Selected value:
- Plot "main" line:
  - Before round 17: the "point" value is used to draw the main line 
  of each projection, corresponds to the quantile 0.5 for all the 
  ensembles 
  - Starting round 17: the quantile 0.5 value is used to draw the 
  main line of each projection
- Scenario: all scenario included 
- Location: "US"
- Target: All "incident" target(s)
- Uncertainty level: "95%"
 
 
## Scenario Comparison
 
###  Plot:

Comparison is the excess percentage of each target in between two 
selected scenario per projection (default ensemble (in black) and 
team-model projection) for a specific location, and for the complete
required round time series.
 
### Calculation of excess percentage: 

The first step is to generate an "end value" for each specific scenario, 
location, target and projection.

Next, the relative change between two scenario (for example scenario 1 
and 2) can be calculated.

#### End Value:

Depending on the input it is calculated as:
- Incident projection:
  - End value is the sum of the incident value for the complete time 
  series {1, t}
  - `end value = sum(value{1, t})`
- "Zeroed" cumulative generated projection:
  - For the complete round time series:
    - End value is the value at the end of the round required time 
    series (T)
    - `end value = value{T}`
  - For each time point of the round time series:
    - End value at the time t is the difference between the value at 
    end of the  round required time series (T) and the value at the 
    time t
    - `end value{t} = value{T} - value{t}`
- Cumulative projection:
  - End value is the value at the end of the round required 
  time series (T)
  - `end value = value{T}`
 
#### Relative Change:

Is the ratio between te end value of scenario 1 and scenario 2, 
minus 1: `(end value{scenario 1} / end value{scenario2}) - 1`

### View

#### Different possible views:

- Available filter: The plot can be filtered by multiple input:
  - Sidebar selection:
    - Location: the plot shows the value for one specific location
  - External options:
    - Comparison: it is possible to add multiple comparison via a specific 
    parameter of the function use to generate the plot
 
#### Default View:

- Input data:
  - From Round 1 to 6: Incident Projection, the "point" value is 
  used to draw the main line of each projection, corresponds to the 
  quantile 0.5 for all the ensembles
  - From Round 7 to 16, except round 9: "Zeroed" cumulative generated 
  projection, with the end value calculated for the complete time series;
  the "point" value is used to draw the main line of each projection, 
  corresponds to the quantile 0.5 for all the projections (team-model and ensemble)
  - For Round 9:  "Zeroed" cumulative generated projection, with the end 
  value calculated for each week. A week slider is added to the plot to 
  be able to see the results for each time point. The "point" value is 
  used to draw the main line of each projection, corresponds to the 
  quantile 0.5 for all the projections (team-model and ensemble)
  - From Round 17:  Cumulative projection: the quantile 0.5 value is used to 
  draw the main line of each projection
- Location: "US"
 
## State Deviation
 
### Plot:

To visualize all the state variation by state (US and territories excluded) 
and by projections (default ensemble and team-models projection) for a 
specific scenario, incident target by time and normalized by population 
size by state.

For each state (x), at each time (t), a rate is calculated by applying the 
function:
`(Projection{x,t} * 100,000) / Population size{x}`
 with "Projection": "point" or 0.5 quantile value of the projection at a 
 time t for a state x.
 
#### Different possible views:

- Available filter: The plot can be filtered by multiple input:
  - Sidebar selection:
    - Scenario: the plot shows the value for one specific scenario 
    (scenario A selected by default)
    - Target: the plot shows the value for one specific target, 
    only the incident target are available
  - Plot specific filter:
    - Y-axis Scale: By default, the y-axis scale is linear, but it's 
    possible to change it to a log scale.
  - Plot interactivity:
    - Time slider: By default, the first week of the round time 
    series is plotted but all the weeks are available by using the 
    slider (either manually and automatically with the play/pause buttons)
 
#### Default View:

- "Projection" value:
  - Before round 17: the "point" value is used to calculate the rate, 
  corresponds to the quantile 0.5 for all the ensembles 
  - Starting round 17: the quantile 0.5 value is used to calculate 
  the rate of each projection 
- Scenario: Scenario A
- Target:
  - Before Round 15: "Incident Cases"
  - Round 15 and ongoing: "Incident Hospitalization"
  
## Trend Map

### Plot:
To visualize all the state variation by state (US and territories excluded) 
and by projections (default ensemble and team-models projection) for a specific 
scenario, incident target by time and normalized by population size by state, and 
with observed data (if available) in a map shaped plot. Each state shows the projection
with a 95% uncertainty interval and the associated observed data (if available).

For each state, at each time T, a rate is calculated by applying the function:
`(Projection{q,x,t} * 100,000) / Population size{x}`
 with "Projection": "point" or 0.5 quantile value, or quantile 0.025, 0.975 (q) of the 
projection at a time t for a state x.
 
#### Different possible views:

- Available filter: The plot can be filtered by multiple input:
  - Sidebar selection:
    - Scenario: the plot shows the value for one specific scenario 
    (scenario A selected by default)
    - Target: the plot shows the value for one specific target, 
    only the incident target are available
  - Plot specific filter:
    - Model Dropdown:  Select the model-team projection or 
    ensemble to plot (default ensemble, by default)
    - Additional Ensemble: if a round contains multiple ensembles, 
    only the default ensemble is  included in the model dropdown. 
    To add all the possible ensembles, the "Show Additional Ensemble" 
    checkbox needs to be selected.
    - Time slider: By default, the first 6 weeks of the round time 
    series are plotted but all the weeks are available by using the slider.
 
#### Default View:

- "Projection" value:
  - "Main" red line: 
    - Before round 17: the "point" value is used to calculate the rate, 
    corresponds to the quantile 0.5 for all the ensembles
    - Starting round 17: the quantile 0.5 value is used to calculate 
    the rate of each projection
  - Uncertain interval in light red:
    - 95% uncertainty interval (quantiles 0.025 and 0.975)
- Scenario: Scenario A 
- Target:
  - Before Round 15: "Incident Cases"
  - Round 15 and ongoing: "Incident Hospitalization"
- Time slider:
  - Projection: 6 first weeks. Except if the observed data is available 
  for the complete round time frame, then the complete round time 
  series is plotted.
  - Observed data: 3 weeks before round start date until round end date
  (as available)
 
## Risk Map

### Plot:
To visualize all the state variation by state (US and territories 
excluded) of the default ensemble for a specific scenario,  target by time 
and normalized by population size by state in a choropleth map of the US.

For each state, at each time T, a rate is calculated by applying the function:
`rate = (Projection{x,t} * 100,000) / Population size{x}`
with "Projection": "point" or 0.5 quantile value of the projection at a time t 
for a state x.
 
For rounds using "incident" target as input (see default view section for 
additional information), the cumulative rate per scenario, target, location 
for each time point will be calculated, by default. However, it's possible to
keep the incident rate and plot the incident rate instead of cumulative. 

 
#### Different possible views:
- Available filter: The plot can be filtered by multiple input:
  - Sidebar selection:
    - Scenario: the plot shows the value for one specific 
    scenario (scenario A selected by default)
    - Target: the plot shows the value for one specific target, 
    only the cumulative target are available
  - Plot interactivity:
    - Time slider: By default, the first week of the round time 
    series is plotted but all the weeks are available by using the 
    slider (either manually and automatically with the play/pause buttons)
 
#### Default View:

- "Projection" value:
  - For round 1 to round 6: the "point" value is used to calculate the 
  cumulative rate, corresponds to the quantile 0.5 for the default ensemble of the 
  corresponding incident target (for example, use "incident hospitalization", 
  if "cumulative hospitalization" is selected) and calculate the cumulative rate.
  - For round 7 to round 16: the "point" value is used to calculate the 
  cumulative rate, corresponding to the quantile 0.5 for the default ensemble 
  from the "zeroed" files of the corresponding selected target.
  - Starting round 17: the quantile 0.5 value is used to calculate the 
  incident rate of each projection of the corresponding selected target.
- Scenario: Scenario A
- Target:
  - Before Round 15: "Cumulative Cases"
  - Round 15 and ongoing: "Cumulative Hospitalizations"
    

## Model Distribution
 
### Plot:
Create one subplot per target and per scenario containing a boxplot of five 
selected quantiles: 0.01, 0.25, 0.5, 0.75, 0.99 for each projection (team-model 
(in gray) and default ensemble (in green)) for a specific location at a specific 
time.
 
#### Different possible views:
- Available filter: The plot can be filtered by multiple input:
  - Sidebar selection:
    - Scenario: one subplot for each selected scenario 
    - Location: the plot shows the value for one specific location
  - Plot specific filter:
    - Outcome type: If cumulative and incident target are included in the round, 
    the incident target will be plotted by default, but the cumulative target are 
    available to view by selecting "Cumulative"
    - Additional Ensemble: if a round contains multiple ensembles, only the default 
    ensemble is  included in the plot. To add all the possible ensembles (in green), 
    the "Show Additional Ensemble" checkbox needs to be selected.
    - Week selection: the plot can be drawn at two specific time points: mid-round time 
    (default) or at the end of the round required time series
 
#### Default View:
 Selected value:
- Scenario:
  - all scenario selected 
  - Exception: COVID-19 Round 11, only scenario A and B are selected
- Location: "US"
- Target: All "incident" target(s)
- Week selection: mid-round time

## Individual Trajectories
 
Only for rounds with individual trajectories required in the submission.

### Plot:
Create one subplot per scenario containing a sample of N individual trajectories 
for each team-model projections for a selected target and a specific location
 
#### Different possible views:
- Available filter: The plot can be filtered by multiple input:
  - Sidebar selection:
    - Scenario: one subplot for each selected scenario
    - Location: the plot shows the value for one specific location
    - Target: the plot shows the value for one specific target
  - Plot specific filter:
    - Number of trajectories to plot: Slider between 10 and 100 with a step 
    of 10 allowing to define the N, the  number of individual trajectories 
    for each team-model projection to plot.
    - Show median: To add a plain wider line showing the median (quantile 0.5) for 
    each team-model projections for a selected target (if available) and a specific location
 
#### Default View:

- Scenario: all scenario included
- Location: "US"
- Target: "Incident Hospitalization"
- Number of trajectories to plot: 10


## Multi-Pathogen Plot
 
### Plot:
Create one subplot per scenario containing default ensemble projection for 2 pathogens 
sharing multiple time points for the projections rounds time frame. 

The hub default pathogen will have all scenario presented for a specific quantile, location 
and incident target, and for a specific round in a bar plot format with the additional 
pathogen projection for a specific round, scenario, quantile, location and incident target 
will be stacked on top of each bar for the shared time frame. 

If available for the selected target, the observed data for the default pathogen and the 
sum of both pathogens observed data is available on the plot, by default in the interactive 
legend. 

#### Different possible views:

- Available filter: The plot can be filtered by multiple input:
  - Sidebar selection:
    - Scenario: one subplot for each selected scenario
    - Location: the plot shows the value for one specific location
    - Target: the plot shows the value for one specific incident target
  - Plot specific filter:
    - Default pathogen Quantile: quantile to plot, by default median (0.5)
      - Selection possibility: 0.05, 0.25, 0.5, 0.75, 0.095
    - Additional pathogen Round specific Scenario selection: scenario to plot for 
    the additional pathogen, by default scenario D
    - Additional pathogen Quantile: quantile to plot, by default median (0.5)
      - Selection possibility: 0.05, 0.25, 0.5, 0.75, 0.095

#### Default View:

- Scenario: all scenario included for the default pathogen and scenario D for the 
additional pathogen
- Location: "US"
- Target: "Incident Hospitalization"
- Quantiles: Median for both pathogen
- Round/Pathogen information:
  - Available on Round 15 with Round 1 of FLU 
  - Available on Round 16 with Round 2 of FLU

## Spatiotemporal Waves

TBD

## Projection Peaks

TBD

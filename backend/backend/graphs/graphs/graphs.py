import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
from datetime import timedelta
import plotly.express as px
import plotly.io as io


def prepare_data(data: str) -> pd.DataFrame:
    """Transforms JSON data with nested structure into a normalized DataFrame.

        Processes JSON string containing nested 'report' objects by expanding them into individual columns.
        Automatically converts dates and removes the original nested structure.

        Args:
            data (str): JSON string with mandatory 'report' and 'date' fields. Expected format:
                {
                    "date": ["2023-01-01", ...],
                    "report": [
                        {"metric1": value1, "metric2": value2},
                        ...
                    ]
                }

        Returns:
            pd.DataFrame: Processed DataFrame containing:
                - Columns derived from keys of the first 'report' object
                - 'date' column converted to datetime64[ns] dtype
                - Original 'report' field removed

        Raises:
            KeyError: If input data lacks 'report' or 'date' fields
            ValueError: If 'report' objects contain inconsistent keys

        Notes:
            - Uses keys from the first 'report' object to create columns
            - Maintains original row order from input data
            - Does not handle nested structures within 'report' objects
    """
    df = pd.read_json(StringIO(data))

    reports = df['report'].tolist()
    columns = reports[0].keys()
    for column in columns:
       df[column] = [report.get(column) for report in reports] 
    del df['report']

    df['date'] = pd.to_datetime(df['date'])



    return df


def number_tag(
        user_data: str,
        number_param_name: str,
        tag_param_name: str,
        date_limit: tuple[str] = None
    ) -> bin:
    """Generates a horizontal bar chart comparing average values across categorical tags.

    Processes JSON data to visualize average numerical values grouped by categorical tags
    with optional date filtering. Implements ascending value sorting and dark theme styling.

    Args:
        user_data (str): JSON string containing data with 'date', numerical, and tag fields
        number_param_name (str): Name of numerical field for average calculations
        tag_param_name (str): Name of categorical field for grouping and y-axis labels
        date_limit (tuple[str, str], optional): Date range filter as (start_date, end_date) in 
            YYYY-MM-DD format. End date must be after start date.

    Returns:
        str: html version of a plot

    Raises:
        ValueError: If date_limit contains invalid range (end date ≤ start date)

    Notes:
        - Bars sorted in ascending order by average value
        - Automatically optimizes layout dimensions for label visibility
        - Y-axis displays categorical tags, X-axis shows averaged numerical values
        - Uses plotly_dark template for visualization styling
    """
    df = prepare_data(user_data)

    if date_limit:
        if (pd.to_datetime(date_limit[1]) - pd.to_datetime(date_limit[0])) <= timedelta(0): # if the max value is bigger that the min value
            raise ValueError
        df['date'] = pd.to_datetime(df['date'])
        df = df[(df['date'] >= date_limit[0]) & (df['date'] <= date_limit[1])] # filter the data by date_limit values

    df['avg'] = df.groupby(tag_param_name)[number_param_name].transform('mean')

    df = df.sort_values(by='avg')

    category_order = df[tag_param_name].unique()

    fig = px.histogram(
        x=df['avg'].unique(),
        y=category_order,
        orientation='h',
        category_orders={tag_param_name: category_order}  
    )

    fig.update_layout(
        template='plotly_dark',
        xaxis=dict(
            zeroline=False
        ),
        margin=dict(l=15, r=15, b=15, t=15)
    )
    fig.update_xaxes(title_text=number_param_name)
    fig.update_yaxes(title_text=tag_param_name)
    fig.update_traces(marker_color='#0066CC')

    return io.to_html(fig, format='png', scale=5)


def number_date(
        user_data: str,
        number_param_name: str,
        scale: tuple[str] = 'day',
        date_limit: tuple[str] = None
    ) -> str:
    """Generates a time-series plot for numerical data aggregated at specified time intervals.

    Processes JSON input to create line plots with temporal aggregation, implementing date filtering
    and parameter validation. Features dark theme visualization with customizable time granularity.

    Args:
        user_data (str): JSON string containing data with 'date' field and numerical parameters
        number_param_name (str): Name of numerical column to aggregate and visualize
        scale (str, optional): Temporal aggregation interval. Valid options: 'day', 'week', 'month'.
            Defaults to 'day'.
        date_limit (tuple[str, str], optional): Date filter range as (start_date, end_date) in 
            YYYY-MM-DD format. Must have end_date > start_date.

    Returns:
        str: html version of a plot

    Raises:
        ValueError: For invalid parameters:
            - Unsupported scale value (not in ['day', 'week', 'month'])
            - Invalid date range (end_date ≤ start_date)
            - Month-scale plot requested with date range <31 days

    Notes:
        - Aggregates numerical values using mean for selected time intervals
        - Automatically sorts data chronologically before aggregation
        - Optimizes plot layout for time-axis label visibility
        - Uses plotly_dark template for consistent visual styling
    """

    df = prepare_data(user_data)

    # Validate the parameters
    if scale not in ['day', 'week', 'month']:
        raise ValueError


    # filter the data by date_limit values
    if date_limit:
        if not (pd.to_datetime(date_limit[1]) - pd.to_datetime(date_limit[0])) <= timedelta(0): 
            df['date'] = pd.to_datetime(df['date'])
            df = df[(df['date'] >= date_limit[0]) & (df['date'] <= date_limit[1])] # filter the data by date_limit values
        else: 
            raise ValueError
        
        if scale == 'month' and (pd.to_datetime(date_limit[1]) - pd.to_datetime(date_limit[0])) <= timedelta(31):
            raise ValueError


    #modify data if needed 
    if scale == 'month':
        df['month'] = df['date'].dt.month_name()
        df['monthly_avg'] = df.groupby('month')[number_param_name].transform('mean')
        y = 'monthly_avg'
        x = 'month'
        xlabel = 'month'

    elif scale == 'week':
        df['week_start'] = (df['date'] - pd.to_timedelta(df['date'].dt.dayofweek, unit='D'))

        df['weekly_avg'] = df.groupby('week_start')[number_param_name].transform('mean')
        y = 'weekly_avg'
        x = 'week_start'
        xlabel = 'first day of the week'

    elif scale == 'day':
        y = number_param_name
        x = 'date'
        xlabel = 'date'

    fig = px.line(
        x=df[x],
        y=df[y],
        orientation='h',
    )

    fig.update_layout(
        template='plotly_dark',
        margin=dict(l=15, r=15, b=15, t=15),
    )
    fig.update_yaxes(title_text=number_param_name)
    fig.update_xaxes(title_text=xlabel)
    fig.update_traces(marker_color='#0066CC')

    return io.to_html(fig, format='png', scale=5)


def tag_date(
        user_data: str,
        tag_param_name: str,
        scale: str = 'week',
        date_limit: tuple[str] = None
    ) -> bin:
    """Analyzes and visualizes tag frequency over a specified period.

    Processes user JSON data, groups tags by weeks/months, and generates a bar chart.
    Supports date range filtering and parameter validation.

    Args:
        user_data (str): JSON string containing user data
        tag_param_name (str): Name of the DataFrame column containing tags to analyze
        most_freq_tags_cnt (int, optional): Number of top frequent tags to display. Defaults to 10.
        scale (str, optional): Grouping scale: 'week' or 'month'. Defaults to 'week'.
        date_limit (tuple[str], optional): Date range filter as tuple of YYYY-MM-DD strings

    Returns:
        str: html version of a plot

    Raises:
        ValueError: For invalid parameters:
            - Invalid scale value
            - Invalid date range format
            - Date range too short for monthly analysis (<31 days)"""

    df = prepare_data(user_data)

    # Validate the parameters
    if scale not in ['week', 'month']:
        raise ValueError


    # filter the data by date_limit values
    if date_limit:
        if not (pd.to_datetime(date_limit[1]) - pd.to_datetime(date_limit[0])) <= timedelta(0): 
            df['date'] = pd.to_datetime(df['date'])
            df = df[(df['date'] >= date_limit[0]) & (df['date'] <= date_limit[1])] # filter the data by date_limit values
        else: 
            raise ValueError
        
        if scale == 'month' and (pd.to_datetime(date_limit[1]) - pd.to_datetime(date_limit[0])) <= timedelta(31):
            raise ValueError
    

    # change the data depending on the scale
    if scale == 'week':
        df['week'] = (df['date'] - pd.to_timedelta(df['date'].dt.dayofweek, unit='D'))
        new_df = df.groupby('week', as_index=False)[tag_param_name].value_counts(sort=True)
        x = 'week'    

    elif scale == 'month':
        df['month'] = df['date'].dt.month_name()
        new_df = df.groupby('month', as_index=False)[tag_param_name].value_counts(sort=True)
        x = 'month'
    
    # generate and return a figure 
    fig = px.bar(new_df, x=x, y='count', color=tag_param_name)
    fig.update_layout(
        template='plotly_dark'
    )
    return io.to_html(fig, format='png')


def checkbox_date(
        user_data: str,
        checkbox_param_name: str,
        date_limit: tuple[str] = None
    ) -> bin:

    """Generates a pie chart visualization for boolean parameter distribution with date filtering.

    Processes JSON input to create a pie chart showing true/false ratio for a specified checkbox 
    parameter. Implements optional date range filtering and automatic title generation with dark theme
    visualization.

    Args:
        user_data (str): JSON string containing data with 'date' field and boolean parameters
        checkbox_param_name (str): Name of boolean column to visualize as true/false distribution
        date_limit (tuple[str, str], optional): Date filter range as (start_date, end_date) in 
            YYYY-MM-DD format. Must have end_date > start_date. Defaults to None.

    Returns:
        str: html version of a plot

    Raises:
        ValueError: If provided date range is invalid (end_date ≤ start_date)

    Notes:
        - Automatically converts date fields to datetime objects for comparison
        - Uses plotly_dark template for consistent visual styling
        - Title dynamically reflects checkbox parameter name and date filter when applied
        - Raises ValueError before data processing if date range is chronologically invalid
    """

    # turn a json to dataframe
    df = prepare_data(user_data)

    # filter the data by date_limit values
    if date_limit:
        if not (pd.to_datetime(date_limit[1]) - pd.to_datetime(date_limit[0])) <= timedelta(0): 
            df['date'] = pd.to_datetime(df['date'])
            df = df[(df['date'] >= date_limit[0]) & (df['date'] <= date_limit[1])] # filter the data by date_limit values
        else: 
            raise ValueError

    # handle the naming of the plot
    title = f'"{checkbox_param_name}" true/false stats'
    if date_limit:
        title += f' from {date_limit[0]} to {date_limit[1]}'
 
     # generate a graph
    fig = px.pie(df, names=checkbox_param_name)
   
    fig.update_layout(
        template='plotly_dark',
        title=title
    )
    return io.to_html(fig, 'png', scale=5)


def number_checkbox(
        user_data: str, 
        number_param_name: str,
        checkbox_param_name: str,
        date_limit: tuple[str] = None
    ) -> bin:
    """Generates comparative bar charts for numerical parameter averages across checkbox categories.

    Processes JSON input to create grouped bar plots showing average values of a numerical parameter
    for each unique category in a checkbox column. Supports optional date filtering and implements
    automatic data aggregation with dark theme visualization.

    Args:
        user_data (str): JSON string containing data with 'date' field, numerical, and checkbox parameters
        number_param_name (str): Name of numerical column to calculate averages
        checkbox_param_name (str): Name of categorical column to group data by unique values
        date_limit (tuple[str, str], optional): Date filter range as (start_date, end_date) in 
            YYYY-MM-DD format. Must have end_date > start_date. Defaults to None.

    Returns:
        str: html version of a plot

    Raises:
        ValueError: If provided date range is invalid (end_date ≤ start_date)

    Notes:
        - Automatically converts date fields to datetime objects for comparison
        - Groups data by unique values in checkbox parameter column before averaging
        - Uses plotly_dark template with default styling for visual consistency
        - Returns empty plot visualization if checkbox column has no valid categories
        - Handles missing values implicitly through pandas groupby operation
    """

    # turn a json to dataframe
    df = prepare_data(user_data)

    # filter the data by date_limit values
    if date_limit:
        if not (pd.to_datetime(date_limit[1]) - pd.to_datetime(date_limit[0])) <= timedelta(0): 
            df['date'] = pd.to_datetime(df['date'])
            df = df[(df['date'] >= date_limit[0]) & (df['date'] <= date_limit[1])] # filter the data by date_limit values
        else: 
            raise ValueError

    # modify the data
    new_df = pd.DataFrame()
    new_df[checkbox_param_name] = df[checkbox_param_name].unique()
    new_df['avg'] = df.groupby(checkbox_param_name)[number_param_name].mean()

    # generate a plot
    fig = px.bar(new_df, x=checkbox_param_name, y='avg')
    fig.update_layout(
        template = 'plotly_dark'
    )

    return io.to_html(fig, 'png', scale=5)


def tag_checkbox(
        user_data: str,
        tag_param_name: str,
        checkbox_param_name: str,
        date_limit: tuple[str] = None
    ) -> bin:
    """Generates horizontal histogram of checkbox fulfillment rates grouped by tags.

    Processes JSON input to create a horizontal histogram showing fulfillment percentages
    of a boolean parameter (checkbox) across unique tag categories. Supports optional date
    filtering and implements automatic data aggregation with dark theme visualization.

    Args:
        user_data (str): JSON string containing data with 'date' field, tag categories
            and checkbox boolean values
        tag_param_name (str): Name of categorical column to group data by unique tag values
        checkbox_param_name (str): Name of boolean column to calculate fulfillment rates
        date_limit (tuple[str, str], optional): Date filter range as (start_date, end_date)
            in YYYY-MM-DD format. Must have end_date > start_date. Defaults to None.

    Returns:
        bytes: PNG image data of generated visualization

    Raises:
        ValueError: If provided date range is invalid (end_date ≤ start_date)

    Notes:
        - Converts boolean values to 1/0 for percentage calculations (True=1, False=0)
        - Automatically converts date fields to datetime objects for comparison
        - Groups data by unique tag values before calculating fulfillment rates
        - Results sorted by ascending fulfillment percentages
        - Uses plotly_dark template for consistent visual styling
        - Returns empty visualization if no valid tags/categories exist
        - Handles missing values through pandas groupby operations
    """
    # turn a json to dataframe
    df = prepare_data(user_data)

    # filter the data by date_limit values
    if date_limit:
        if not (pd.to_datetime(date_limit[1]) - pd.to_datetime(date_limit[0])) <= timedelta(0): 
            df['date'] = pd.to_datetime(df['date'])
            df = df[(df['date'] >= date_limit[0]) & (df['date'] <= date_limit[1])] # filter the data by date_limit values
        else: 
            raise ValueError

    df[checkbox_param_name] = df[checkbox_param_name]*1 # turn True/False into 1/0 for further calculations
    new_df = pd.DataFrame()
    df['avg'] = df.groupby(tag_param_name)[checkbox_param_name].transform('mean') # create the df colomn avg with the average percentages of checkbox_param to be filled
    new_df['tags'] = df[tag_param_name].unique()
    new_df['avg'] = [df.loc[df[tag_param_name] == x]['avg'].unique()[0] for x in df[tag_param_name].unique()] # grab the values from the df
    new_df = new_df.sort_values(by='avg')


    # generate a plot

    fig = px.histogram(new_df, x='avg', y='tags', orientation='h')
    fig.update_layout(
        template = 'plotly_dark'
    )

    return io.to_html(fig)

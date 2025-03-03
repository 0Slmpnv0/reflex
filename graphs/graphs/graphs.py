import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
from json import loads
from datetime import timedelta
import plotly.express as px
import plotly.io as io


def prepare_data(data: str) -> pd.DataFrame:
    """Transforms JSON data with nested structure into a normalized DataFrame.

    Processes JSON string containing nested 'report' objects by expanding them into
    individual columns. Handles datetime conversion for the 'date' field.

    Args:
        data: JSON string containing user data with mandatory 'report' and 'date' fields.
            Expected format:
            {
                "date": [dates...],
                "report": [{"metric1": val, "metric2": val...}, ...]
            }

    Returns:
        pd.DataFrame: Processed dataframe with:
            - Columns from original JSON's 'report' objects expanded as individual columns
            - 'date' column converted to datetime64[ns] dtype
            - Original 'report' column removed

    Notes:
        - Requires consistent keys in all 'report' objects (uses keys from first report)
        - Will raise KeyError if input data lacks 'report' or 'date' fields
        - Automatically converts date strings to pandas datetime objects
        - Maintains original row order while expanding report metrics
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
        user_data_json: str,
        number_param_name: str,
        tag_param_name: str,
        date_limit: tuple[str] = None
    ) -> bin:
    """Generates a horizontal bar chart comparing average values across categorical tags.

    Processes JSON data to show average numerical values grouped by categorical tags,
    with optional date filtering. Bars are sorted ascendingly by value. Uses dark theme.

    Args:
        user_data_json: JSON string containing data with 'date', numerical, and tag fields
        number_param_name: Name of numerical parameter to calculate averages
        tag_param_name: Name of categorical parameter for grouping and y-axis labels
        date_limit: Optional tuple (start_date, end_date) in YYYY-MM-DD format for filtering.
            End date must be after start date.

    Returns:
        Binary PNG image data of generated visualization.

    Raises:
        ValueError: If date_limit contains invalid range (end ≤ start)

    Notes:
        - Bars sorted ascending by average value
        - Automatically adjusts layout to fit category labels
        - Uses 800 DPI resolution for high-quality output
        - Dark theme background with white elements
        - Y-axis shows categorical tags, X-axis shows averaged numerical values
    """
    df = prepare_data(user_data_json)

    if date_limit:
        if (pd.to_datetime(date_limit[1]) - pd.to_datetime(date_limit[0])) <= timedelta(0): # if the max value is bigger that the min value
            raise ValueError
        df['date'] = pd.to_datetime(df['date'])
        df = df[(df['date'] >= date_limit[0]) & (df['date'] <= date_limit[1])] # filter the data by date_limit values

    df['avg'] = df.groupby(tag_param_name)[number_param_name].transform('mean') # create the column of the average num values per tags

    df = df.sort_values(by='avg')


    fig = px.histogram(
        x=df['avg'],
        y=df[tag_param_name],
        orientation='h'
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

    return io.to_image(fig, format='png', scale=5)


def number_date(
        user_data_json: str,
        number_param_name: str,
        scale: tuple[str] = 'day',
        date_limit: tuple[str] = None
    ) -> bin:
    """Generates a time-series plot for numerical data aggregated at specified time intervals.

    Processes JSON input data to create a line plot showing values aggregated by day/week/month.
    Supports date filtering and includes validation for input parameters. Uses dark theme styling.

    Args:
        user_data_json: JSON string containing user data with 'date' field and numerical parameters.
        number_param_name: Name of the numerical parameter/column to visualize.
        scale: Time aggregation scale. Must be one of ('day', 'week', 'month'). Defaults to 'day'.
        date_limit: Optional tuple of (start_date, end_date) strings (YYYY-MM-DD format) to filter data.
            For 'month' scale, date range must span ≥31 days.

    Returns:
        Binary PNG image data of the generated plot.

    Raises:
        ValueError: If any of these occur:
            - Invalid `scale` value provided
            - `date_limit` end date ≤ start date
            - `month` scale used with date range <31 days

    Notes:
        - X-axis labels rotate 90° except for monthly aggregations
        - For weekly scale, x-axis shows week start dates (MM-DD format)
        - Monthly aggregations use month names and horizontal labels
        - Plot uses constrained layout with 1500x1000px dimensions and 700 DPI
    """

    df = prepare_data(user_data_json)

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

    rotation = 90 # month scale will need to have a 0 rotation, so the rotation number is moved toa separate variable

    #modify data if needed 
    if scale == 'month':
        df['month'] = df['date'].dt.month_name()
        df['monthly_avg'] = df.groupby('month')[number_param_name].transform('mean')
        y = 'monthly_avg'
        x = 'month'
        xlabel = 'month'
        rotation = 0

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

    return io.to_image(fig, format='png', scale=5)


with open('/home/slmpnv/dev/pet/reflex/graphs/graphs/mock/mock_data_365.json') as file:
    data = file.read()


with open('res.png', 'wb') as file:
    bdata = number_date(data, number_param_name='Excercise time?', scale='month')
    file.write(bdata)

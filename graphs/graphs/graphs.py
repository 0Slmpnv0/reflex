import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO, StringIO
from json import loads


def prepare_data(data: str) -> pd.DataFrame:
    '''Turns a json string into a pandas dataframe, unpacks the report in separate columns
    Parameters:
        data (str):
            The json representation of user data
    Returns:
        DataFrame:
            The modified dataframe
    '''
    df = pd.read_json(StringIO(data))

    reports = df['report'].tolist()
    columns = reports[0].keys()
    for column in columns:
       df[column] = [report.get(column) for report in reports] 
    del df['report']

    df['date'] = pd.to_datetime(df['date'])

    return df


def number_tag(user_data_json: str, number_param_name: str, tag_param_name: str, date_limit: tuple[str] = None) -> bin:
    '''Function that returns a graph representing a correlation between the tag and number values.

    Parameters:
        user_data_json (str): 
            The JSON representation of user data.
        number_param_name (str): 
            The name of a parameter to treat as a number (x-axis).
        tag_param_name (str): 
            The name of a parameter to treat as a tag (y-axis).
        date_limit (tuple[str]): 
            A tuple of two strings: start ([0]) and end ([1]) dates. Only data from this period is used.

    Returns:
        bin: 
            Binary data of the **png** graph image.
    '''
    df = prepare_data(user_data_json)

    if date_limit:
        df['date'] = pd.to_datetime(df['date'])
        df = df[(df['date'] >= date_limit[0]) & (df['date'] <= date_limit[1])] # filter the data by date_limit values

    df['avg'] = df.groupby(tag_param_name)[number_param_name].transform('mean') # create the column of the average num values per tags

    df = df.sort_values(by='avg')

    plot_buff: bin = BytesIO() # create the buffer to save and return a plot binary  

    plt.style.use('dark_background') 
    plt.figure(constrained_layout=True) # autoscale a figure's size
    plt.barh(df[tag_param_name], df['avg'])
    plt.xlabel(number_param_name)
    plt.ylabel(tag_param_name)
    plt.savefig(plot_buff, format='png', dpi=700) # save a plot binary in the buffer

    return plot_buff.getvalue()


with open('/home/slmpnv/dev/pet/reflex/graphs/graphs/mock/mock_data_365.json') as file:
    data = file.read()


with open('res.png', 'wb') as file:
    bdata = number_tag(data, 'Productivity percentage', 'Mood', date_limit=('2023-01-01', '2023-02-01'))
    file.write(bdata)

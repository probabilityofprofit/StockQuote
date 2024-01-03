import numpy as np
import talib
from talib import abstract
import yfinance as yf
import pandas as pd 
import streamlit as st
import time

def pull_data():
    stock = st.text_input("Enter stock name like 'btc-usd: ")
    start_date = st.text_input("Enter start date like '2022-05-12: ") or '2022-04-04'
    end_date = st.text_input("Enter end date like '2022-05-15: ") or '2022-05-05'
    st.write("Valid intervals: [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]")
    date_frame = st.text_input("Enter date frame like '1h' for one hour: ")

    # Fetch data for the desired period
    data = yf.download(stock, start=start_date, end=end_date, interval=date_frame)
    data = data.drop(columns=["Adj Close"])
    data = data.rename(columns={'Open': 'open', 'High': 'high', 'Close': 'close', 'Low': 'low', 'Volume': 'volume'})

    st.write(f'The data is ready.')

    return data

def set_indi_config(indi):
    tool_config = {"name":indi,"parameters":[]}
    tool = abstract.Function(indi)

    if len(tool.parameters.items()) > 0:
        param_edit = st.selectbox("Do you want to change default parameters?", ["Yes", "No"])

        if param_edit == "Yes":
            for x, y in tool.parameters.items():
                new_val = st.text_input(f"Enter new {x} or press enter to leave it as default: ", value=str(y))
                if new_val != '':
                    tool_config["parameters"].append({x: int(new_val)})
                else:
                    tool_config["parameters"].append({x: int(y)})
    else:
        st.write("This indicator doesn't have parameters.")

    return tool_config

def calc_indi(indi, data):
    tool = abstract.Function(indi["name"])

    if len(indi["parameters"]) > 0:
        for param in indi["parameters"]:
            tool.set_parameters(param)

    output = tool(data)

    try:
        if isinstance(output, pd.DataFrame):
            output_columns = output.columns
            output_length = len(output_columns)
        else:
            output = pd.DataFrame(output)
            output_columns = output.columns
            output_length = len(output_columns)
    except Exception as e:
        st.error(str(e))
        output_length = 1

    if output_length > 1:
        for col in output_columns:
            col_name = indi["name"] + f"({col})"
            data[col_name] = output[col]
    else:
        data[indi["name"]] = output

    return data

def start_calc(list_indid, data):
    for ind in list_indid:
        data = calc_indi(ind, data)

    st.write("The results are displayed below:")
    st.dataframe(data)

def main():
    data = pull_data()
    status = True
    list_of_indi = []

    while status:
        st.write("Start the bot. Please choose the indicators.")

        all_indi = talib.get_functions()

        select = st.selectbox(f'Select indicator {len(list_of_indi) + 1}:', all_indi, key=f"selectbox_{len(list_of_indi)}")
        indi_config = set_indi_config(select)
        list_of_indi.append(indi_config)

        st.success("Done! Indicator is saved.")

        add_more = st.selectbox("Do you want to add more indicators?", ["Yes", "No"])

        if add_more == "No":
            status = False

    user_status = st.selectbox("Do you want to start calculation?", ["Yes, Start", "No, Restart Bot"])

    if user_status == "Yes, Start":
        start_calc(list_of_indi, data)

if __name__ == "__main__":
    main()

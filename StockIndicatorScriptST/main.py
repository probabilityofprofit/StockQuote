import numpy as np
import talib
from talib import abstract
import yfinance as yf
import pandas as pd 
from comand_colors import bcolors
import time


global task_name

task_name = ''

def pull_data():
    stock = input("enter stock name like 'btc-usd: ")
    task_name = stock
  
    start_date = input("enter start date loke '2022-05-12: ") or '2022-04-04'

    end_date = input("enter end date loke '2022-05-15: ") or '2022-05-05'
    print("Valid intervals: [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]")
    date_frame = input("enter date frame like '1h' for one hour: ")
    
    data = yf.download(stock, start=start_date, end=end_date, interval=date_frame)
    data = data.drop(columns=["Adj Close"])
    data = data.rename(columns={'Open': 'open', 'High': 'high', 'Close':'close', 'Low':'low' , 'Volume':'volume' })
    data.to_csv('input.csv')
    time.sleep(1)
    print(f' {bcolors.OKGREEN}the data is ready at inpit.csv {bcolors.ENDC} \n')

def set_indi_config(indi):
    pass
    """
    return indi with custome parameters
    """

    tool_config = {"name":indi,"parameters":[]}
    tool = abstract.Function(indi)



    if len(tool.parameters.items()) > 0:
        print("the defualt params is: \n")
        print(tool.parameters.items())

        param_edit = int(input(f" {bcolors.OKCYAN} need change defualt parameters: {bcolors.ENDC} \n {bcolors.OKGREEN} 1- YES {bcolors.ENDC} \n  {bcolors.FAIL} 2- NO USE DEFUALT: {bcolors.ENDC}"))
        
        if param_edit == 1:

            for x, y in tool.parameters.items():

                print("defualt: ",x, y)

                new_val = input(f"enter {bcolors.WARNING} new {x} {bcolors.ENDC} or press enter lave it {bcolors.OKBLUE} defualt: {bcolors.ENDC} ")
                if new_val == '':
                    tool_config["parameters"].append({x:int(y)})
                    

                else:
                    tool_config["parameters"].append({x:int(new_val)})
    else:
        print("this indcator dosent has pramiter ")
                
        
    return tool_config
            

def calc_indi(indi,data):
    pass
    tool = abstract.Function(indi["name"])

    if len(indi["parameters"]) > 0:
        for pram in indi["parameters"]:
            tool.set_parameters(pram)
        
    output = tool(data)

    try:
        
        output_columns = output.columns
        output_length = len(output_columns)

    except Exception as e:
        print(e)
        output_length = 1


    print(data)


    if output_length > 1:
        for col in output_columns:
            colom_name = indi["name"] + f"({col})"
            print(output[col])
            data[colom_name] = output[col]
    else:

        data[indi["name"]] = output
    
    print("indi id ready \n")

    return data


def start_calc(list_indid):

    file_name = task_name

    data = pd.read_csv("input.csv")

    for ind in list_indid:
        file_name += "("
        file_name += ind["name"]
        file_name += ")"
        data = calc_indi(ind,data)

    file_name += ".csv"
    
    
    data.to_csv(file_name)
    


pull_data()
status = True

while status:

    print("start the bot please choice the indicators: \n")
    all_indi = talib.get_functions()

    list_of_indi = []

    while True:

        for x,i in enumerate(all_indi):
            print(x,i)

        select = int(input(f'{bcolors.WARNING} enter index of indicators: {bcolors.ENDC}'))
        indi_config = set_indi_config(all_indi[select])
        list_of_indi.append(indi_config)

        print(f'{bcolors.OKGREEN} \n ###### DONE INDICATOR IS SAVE ###### \n {bcolors.ENDC}')

        add_more = int(input(f' {bcolors.WARNING} you need add more indicators ? {bcolors.ENDC} \n {bcolors.OKGREEN} 1- YES {bcolors.ENDC} \n {bcolors.FAIL} 2- CANCLE  {bcolors.ENDC} \n Enter 1 or 2: '))

        if add_more == 2:
            break


    print(f"{bcolors.OKGREEN} make sure before start calculte check your indicator selector{bcolors.ENDC}")
    for i in list_of_indi:

        print("#"*20)
        print(f"indicator name is {bcolors.WARNING} {i['name']} {bcolors.ENDC}\n")
        print(f" {bcolors.OKBLUE} parameters {bcolors.ENDC} \n")
        if len(i['parameters']) > 0:
            
            for x in i['parameters']:
                print(x)
        else:
            print(f" {bcolors.OKGREEN} use defualt {bcolors.ENDC}")
        
        print("\n \n ")
        

    user_status = int(input(f" {bcolors.WARNING} if you need start calculate: {bcolors.ENDC} \n {bcolors.OKGREEN} 1- YES START {bcolors.ENDC} \n {bcolors.FAIL} 2- NO RESTART BOT \n {bcolors.ENDC}"))

    if user_status == 1:
        status = False
        start_calc(list_of_indi)






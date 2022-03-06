#! /usr/bin/env python

import os
import argparse

import pandas as pd
import matplotlib.pyplot as plt

import PySimpleGUI as sg    


def write_new(weight):
    filepath = '/Users/bytedance/bin/resource/weight_tracer.csv'
    today = pd.Timestamp('today').strftime('%Y-%m-%d')
    if not os.path.isfile(filepath):
        df = pd.DataFrame([[weight, today]], columns = ['weight', 'date'])
    else:
        df = pd.read_csv(filepath, header=0, index_col=0)
        new_value = pd.Series([weight, today], index=df.columns)
        df = df.append(new_value, ignore_index=True)
    df.to_csv(filepath, header=True)


def show_stat():
    filepath = '/Users/bytedance/bin/resource/weight_tracer.csv'
    df = pd.read_csv(filepath, header=0, index_col=0)
    df['date']= pd.to_datetime(df['date'], format='%Y-%m-%d').dt.strftime('%Y-%m-%d')
    df.set_index('date').plot()
    plt.show()


def main():
    data = args.data or gui()
    if args.show:
        if args.write:
            write_new(data)
        show_stat()
    else:
        write_new(data)
        if not args.write:
            show_stat()

def gui():
    layout = [  [sg.Text("What's your weight?")],
                [sg.Input()],
                [sg.Button('Submit')] ]
    window = sg.Window('Weight Tracer', layout)
    event, values = window.read()
    window.close()
    return float(values[0])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('data', nargs='?', type=float)
    parser.add_argument('--show', '-s', action="store_true", help="show stats")
    parser.add_argument('--write', '-w', action="store_true",
                        help="write new value")
    args = parser.parse_args()
    main()
#! /Users/tianranmao/Projects/so1.0/venv/bin/python

import os
import re
import numpy as np
import pandas as pd
import smtplib
import time
from datetime import datetime

if __name__ == '__main__':

    LOG_FILE = './tradelog.txt'
    CSV_DIR = f"./csv/{datetime.today().strftime('%Y-%m-%d')}"

    pattern_trade = re.compile(r'^(BUY|SELL)\s+(\w+)\s+@\s+([.\d]+)\s+x\s+([\d]+)')

    PROF = {}
    BUY = {}
    SELL = {}
    COMBS = []

    with open(LOG_FILE, 'r') as rf:
        for line in rf:
            if line.split() == []:
                COMBS.append((BUY, SELL))
                BUY = {}
                SELL = {}
            else:
                match_trade = re.search(pattern_trade, line)
                op = match_trade.group(1)
                code = match_trade.group(2)
                price = float(match_trade.group(3))
                volume = int(match_trade.group(4))
                if op == 'BUY':
                    BUY.update({code:[price, volume, 'done']})
                elif op =='SELL':
                    SELL.update({code:[price, volume, 'done']})
        COMBS.append((BUY, SELL))

    for BUY, SELL in COMBS:
        for code in BUY:
            if code not in SELL:
                if code[6] == 'C':
                    SELL.update({code: [0, BUY[code][1], 'to be']})
                else:
                    SELL.update({code: [0, BUY[code][1], 'to be']})

        for code in SELL:
            if code not in BUY:
                if code[6] == 'C':
                    BUY.update({code: [0, SELL[code][1], 'to be']})
                else:
                    BUY.update({code: [0, SELL[code][1], 'to be']})

    def track(BUY, SELL):
        for code in BUY:
            if BUY[code][2] == 'to be':
                op_type = code[6]
                if op_type == 'C':
                    code2 = code.replace('C','_')
                elif op_type == 'P':
                    code2 = code.replace('P','_')
                code2 = code2.replace('M','_')
                df = pd.read_csv(f'{CSV_DIR}/{code2}.csv', index_col='time')
                df.dropna(inplace=True)
                ct = df.iloc[-1].name
                if op_type == 'C':
                    BUY[code][0] = round(df.iloc[-1, 0],4)
                elif  op_type == 'P':
                    BUY[code][0] = round(df.iloc[-1, 1],4)

        for code in SELL:
            if SELL[code][2] == 'to be':
                op_type = code[6]
                if op_type == 'C':
                    code2 = code.replace('C','_')
                elif op_type == 'P':
                    code2 = code.replace('P','_')
                code2 = code2.replace('M','_')
                df = pd.read_csv(f'{CSV_DIR}/{code2}.csv', index_col='time')
                df.dropna(inplace=True)
                ct = df.iloc[-1].name
                if op_type == 'C':
                    SELL[code][0] = round(df.iloc[-1, 0],4)
                elif  op_type == 'P':
                    SELL[code][0] = round(df.iloc[-1, 1],4)

        print(f'{ct:>10}', end='')
        for k in sorted(BUY.keys()):
            print(f'{k: >20}', end='')
        print(f'{"TOTAL": >20}', end='')
        print()

        print(f"{'BUY@':>10}", end='')
        for k in sorted(BUY.keys()):
            if BUY[k][2] == 'done':
                print(f'{BUY[k][0]: >20}', end='')
            else:
                print(f'{"*"+str(BUY[k][0]): >20}', end='')
        print()

        print(f"{'SELL@': >10}", end='')
        for k in sorted(BUY.keys()):
            if SELL[k][2] == 'done':
                print(f'{SELL[k][0]: >20}', end='')
            else:
                print(f'{"*"+str(SELL[k][0]): >20}', end='')
        print()

        print(f"{'EARNING':>10}", end='')
        tt = 0
        for k in sorted(BUY.keys()):
            tt += round(SELL[k][0]-BUY[k][0],4)
            print(f'{round(SELL[k][0] - BUY[k][0],4): >20}', end='')
        print(f'{round(tt,4): >20}')
        print()

    while True:
        time.sleep(5)
        for BUY, SELL in COMBS:
            track(BUY, SELL)
            print()


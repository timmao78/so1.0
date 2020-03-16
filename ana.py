#! /Users/tianranmao/Projects/so1.0/venv/bin/python

import cmd
import os
import re
import pandas as pd
import numpy as np
from bsm_option_class import call_option, put_option
from scipy import stats
from datetime import datetime

class Ana(cmd.Cmd):
    intro = 'Welcome to so shell.   Type help or ? to list commands.\n'
    df_dict = {}
    r = 0.025
    csv_dir = f"./csv/{datetime.today().strftime('%Y-%m-%d')}"

    def read_data(self):
        for f in os.listdir(self.csv_dir):
            pattern = re.compile(r'(\d+)_(\d+)_(\d+)+\.csv')
            match = re.search(pattern, f)
            if match!=None:
                dict_key = f'{match.group(1)}_{match.group(2)}_{match.group(3)}'
                self.df_dict.update({dict_key: pd.read_csv(f'{self.csv_dir}/{f}', index_col='time')})
        df = pd.read_csv(f'{self.csv_dir}/510050.csv', index_col='time')
        df.dropna(axis='index', how='any', inplace=True)
        self.df_dict.update({'510050': df})

        df = pd.read_csv(f'{self.csv_dir}/510300.csv', index_col='time')
        df.dropna(axis='index', how='any', inplace=True)
        self.df_dict.update({'510300': df})

    def get_K(self, S):
        if S < 3:
            low = '0'+str(int(S*1000 - S * 1000 % 50))
            high = '0'+str(int(S*1000 - S * 1000 % 50 + 50))
            return (low, high)
        elif S > 3:
            low = '0'+str(int(S*1000 - S * 1000 % 100))
            high = '0'+str(int(S*1000 - S * 1000 % 100 + 100))
            return (low, high)
        else:
            low = '03000'
            high = '03000'
            return (low, high)

    def pair_ana(self, pair):
        kc = float(pair[0][-5:])/1000.0
        kp = float(pair[1][-5:])/1000.0

        name_c = pair[0].replace('_', 'C')
        name_p = pair[1].replace('_', 'P')

        df = pd.read_csv(f'{self.csv_dir}/{pair[0][0:6]}.csv', index_col='time')
        df.dropna(axis='index', how='any', inplace=True)
        his_vol = stats.tstd(df['S'])*np.sqrt(250*4*60)

        su = df.iloc[-1]
        
        sc = pd.read_csv(f'{self.csv_dir}/{pair[0]}.csv', index_col='time').loc[su.name]
        sp = pd.read_csv(f'{self.csv_dir}/{pair[1]}.csv', index_col='time').loc[su.name]

        if sc['C'] == np.nan or sp['P']:
            su = df.iloc[-2]
            sc = pd.read_csv(f'{self.csv_dir}/{pair[0]}.csv', index_col='time').loc[su.name]
            sp = pd.read_csv(f'{self.csv_dir}/{pair[1]}.csv', index_col='time').loc[su.name]

        oc_real = call_option(su['S'], kc, sc['T'], self.r, 0.3)
        op_real =  put_option(su['S'], kp, sp['T'], self.r, 0.3)

        ivc = oc_real.imp_vol(sc['C'])
        ivp = op_real.imp_vol(sp['P'])

        if pair[0][-5:]==pair[1][-5:]:
            ir = np.log(kc/(su['S']+sp['P']-sc['C']))/sc['T']
            ir = round(ir, 3)
        else:
            ir = '-'

        oc_delta_1p = call_option(su['S']*1.005, kc, sc['T'], self.r, ivc)
        op_delta_1p =  put_option(su['S']*1.005, kp, sp['T'], self.r, ivp)
        oc_delta_1m = call_option(su['S']*0.995, kc, sc['T'], self.r, ivc)
        op_delta_1m =  put_option(su['S']*0.995, kp, sp['T'], self.r, ivp)
        oc_delta_2p = call_option(su['S']*1.01,  kc, sc['T'], self.r, ivc)
        op_delta_2p =  put_option(su['S']*1.01,  kp, sp['T'], self.r, ivp)
        oc_delta_2m = call_option(su['S']*0.99,  kc, sc['T'], self.r, ivc)
        op_delta_2m =  put_option(su['S']*0.99,  kp, sp['T'], self.r, ivp)
        oc_delta_3p = call_option(su['S']*1.02,  kc, sc['T'], self.r, ivc)
        op_delta_3p =  put_option(su['S']*1.02,  kp, sp['T'], self.r, ivp)
        oc_delta_3m = call_option(su['S']*0.98,  kc, sc['T'], self.r, ivc)
        op_delta_3m =  put_option(su['S']*0.98,  kp, sp['T'], self.r, ivp)

        oc_vega_m = call_option(su['S'], kc, sc['T'], self.r, ivc-0.01)
        op_vega_m =  put_option(su['S'], kp, sp['T'], self.r, ivp-0.01)

        delta_1p = oc_delta_1p.value() + op_delta_1p.value() - sc['C'] - sp['P']
        delta_1m = oc_delta_1m.value() + op_delta_1m.value() - sc['C'] - sp['P']
        delta_2p = oc_delta_2p.value() + op_delta_2p.value() - sc['C'] - sp['P']
        delta_2m = oc_delta_2m.value() + op_delta_2m.value() - sc['C'] - sp['P']
        delta_3p = oc_delta_3p.value() + op_delta_3p.value() - sc['C'] - sp['P']
        delta_3m = oc_delta_3m.value() + op_delta_3m.value() - sc['C'] - sp['P']
        vega_m = oc_vega_m.value() + op_vega_m.value() - sc['C'] - sp['P']

        print(f"{' ':>8}{su.name}{' ':>22}{name_c} + {name_p} {' ':15} HV: {round(his_vol, 2)}")
        print(f"{' ':>8}{'-'*148}")
        print(f"{' ':>8}{'C':>8}{'P':>8}{'S':>8}{'KC':>8}{'KP':>8}{'ivc':>8}{'ivp':>8}{'ir':>8}{' ':15}{'---':^10}{'--':^10}{'-':^10}{'vega':^10}{'+':^10}{'++':^10}{'+++':^10}")
        print(f"{' ':>8}{round(sc['C'],4):>8}{round(sp['P'],4):>8}{round(su['S'],3):>8}{kc:>8}{kp:>8}{round(ivc,3):>8}{round(ivp,3):>8}{ir:>8}{' ':15}{round(delta_3m,4):^10}{round(delta_2m,4):^10}{round(delta_1m,4):^10}{round(vega_m,4):^10}{round(delta_1p,4):^10}{round(delta_2p,4):^10}{round(delta_3p,4):^10}")
        print('\n')

    def do_run(self, arg):
        if arg=='':
            self.read_data()
            kl, kh = self.get_K(self.df_dict['510050'].iloc[-1]['S'])
            pair_list = []
            pair_list.append([f'510050_2004_{kl}', f'510050_2004_{kl}'])
            pair_list.append([f'510050_2004_{kl}', f'510050_2004_{kh}'])
            pair_list.append([f'510050_2004_{kh}', f'510050_2004_{kl}'])
            pair_list.append([f'510050_2004_{kh}', f'510050_2004_{kh}'])
            for pair in pair_list:
                self.pair_ana(pair)

            kl, kh = self.get_K(self.df_dict['510300'].iloc[-1]['S'])
            pair_list = []
            pair_list.append([f'510300_2004_{kl}', f'510300_2004_{kl}'])
            pair_list.append([f'510300_2004_{kl}', f'510300_2004_{kh}'])
            pair_list.append([f'510300_2004_{kh}', f'510300_2004_{kl}'])
            pair_list.append([f'510300_2004_{kh}', f'510300_2004_{kh}'])
            for pair in pair_list:
                self.pair_ana(pair)
        elif arg=='50':
            self.read_data()
            kl, kh = self.get_K(self.df_dict['510050'].iloc[-1]['S'])
            pair_list = []
            pair_list.append([f'510050_2004_{kl}', f'510050_2004_{kl}'])
            pair_list.append([f'510050_2004_{kl}', f'510050_2004_{kh}'])
            pair_list.append([f'510050_2004_{kh}', f'510050_2004_{kl}'])
            pair_list.append([f'510050_2004_{kh}', f'510050_2004_{kh}'])
            for pair in pair_list:
                self.pair_ana(pair)
        elif arg=='300':
            self.read_data()
            kl, kh = self.get_K(self.df_dict['510300'].iloc[-1]['S'])
            pair_list = []
            pair_list.append([f'510300_2004_{kl}', f'510300_2004_{kl}'])
            pair_list.append([f'510300_2004_{kl}', f'510300_2004_{kh}'])
            pair_list.append([f'510300_2004_{kh}', f'510300_2004_{kl}'])
            pair_list.append([f'510300_2004_{kh}', f'510300_2004_{kh}'])
            for pair in pair_list:
                self.pair_ana(pair)
        else:
            print('Usage: run 50/300')
        print()

    def help_run(self):
        print('Run a monitor on option(50/300) markets.')
        print('Usage: run 50/300')
        print()

    def do_exit(self, arg):
        print("Thank you. Bye.")
        print('')
        return True

    def help_exit(self):
        print('Quit program.')
        print('')

if __name__ == '__main__':
    Ana().cmdloop()

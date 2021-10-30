from datetime import datetime,date
import logging
import os
import requests 
import json

import telegram

from config import TELEGRAM_TOKEN, HTTPS_PROXY
from service import DB

URL = "http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=KZZ_LB2.0&token=70f12f2f4f091e459a279469fe49eca5&cmd=&st={sortType}&sr={sortRule}&p={page}&ps={pageSize}"

logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p',filename='bondcat.log', level=logging.INFO)



class BondFetchCat:
    def fetch_bonds(self, url: str = URL) -> [dict]:
        res =  requests.get(url)
        return res.json()

    def _select_all_bonds(self):
        db = DB()
        all_bonds = db.select_all_bonds()
        return all_bonds
    
    def filter_new_bonds(self, fetched_bonds):
        bonds_in_db = self._select_all_bonds()
        fetched_bonds_tuple = [(bond['CORRESNAME'], bond['STARTDATE']) for bond in fetched_bonds]
        new_bonds = [bond for bond in fetched_bonds_tuple if bond not in bonds_in_db]
        return new_bonds
    
    def save_bond_to_db(self, new_bonds):
        only_wanted_cols = [(bond[0], bond[1]) for bond in new_bonds]
        print(only_wanted_cols)
        db = DB()
        db.save_bonds(only_wanted_cols)
        

def convert_to_date(date_str):
    return datetime.strptime(date_str[0:10],"%Y-%m-%d").date()

def get_biding_bonds(url: str) -> [dict]:
    r =  requests.get(url)
    kezhuanzhai = r.json()
    return kezhuanzhai

def make_text(bonds):
    if bonds != []:
        text = ""
        for bond in bonds:
            text += f"{bond['SNAME']}将于{bond['STARTDATE']}申购。\n"
        text += "\n 💰💷💶💸💵💴💳"
        return text
    else:
        return

def send_message(message):
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id="202211787", text=message)

def remind_bot(kezhuanzhai):
    unpublic_kezhuanzhai = []
    for bond in kezhuanzhai:
        bond_date = convert_to_date(bond['STARTDATE'])
        if bond_date == date.today():
            unpublic_kezhuanzhai.append(bond)
    if unpublic_kezhuanzhai != []:
        message = make_text(unpublic_kezhuanzhai)
        send_message(message)
    else:
        logging.info("Bondcat is checked, there is no new bond today!")

def forcast_bot(kezhuanzhai):
    unpublic_kezhuanzhai = []
    for bond in kezhuanzhai:
        bond_date = convert_to_date(bond['STARTDATE'])
        if bond_date >= date.today():
            unpublic_kezhuanzhai.append(bond)
    if unpublic_kezhuanzhai != []:
        message = make_text(unpublic_kezhuanzhai)
        send_message(message)
    else:
        logging.info("Bondcat is checked, there is no new bond recently!")

def main():
    bonds = get_biding_bonds(URL)
    remind_bot(bonds)
    forcast_bot(bonds)
    
if __name__ == "__main__":
    # main()
    bondFetchCat = BondFetchCat()
    bonds_list = bondFetchCat.fetch_bonds()
    new_bonds = bondFetchCat.filter_new_bonds(bonds_list)
    bondFetchCat.save_bond_to_db(new_bonds)

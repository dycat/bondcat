from bondcat import get_biding_bonds, remind_bot, URL

def dailyBondCat():
    bonds = get_biding_bonds(URL)
    remind_bot(bonds)

if __name__ == "__main__":
    dailyBondCat()
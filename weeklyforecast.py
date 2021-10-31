from bondcat import get_biding_bonds, forcast_bot

def weeklyforecast():
    bonds = get_biding_bonds(URL)
    forcast_bot(bonds)

if __name__ == "__main__":
    weeklyforecast()
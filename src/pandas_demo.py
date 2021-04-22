import os
import pandas as pd
from datetime import timedelta, date

def main():
    current_path = os.path.dirname(__file__)
    dataset_path = os.path.join(current_path, f'../downloads/Precio de Oferta del Despacho-001.csv')
    df = pd.read_csv(dataset_path)
    codes = [
        "ACEG", "AXEG", "EPSG", "ARG1", "2S8G", "2VJS", "CIVG", "CRLG", "TBQ2",
        "BLL1", "BLL2", "CHN4", "CHN5", "CHN6", "CHN7", "CHN8", "TBS1", "TBS2",
        "TBS3", "TBS4", "TBSA", "TB22", "ST24", "DEPG", "UNIB", "EDNG", "BLVG",
        "CSP1", "CSP2", "CSP3", "CSP4", "CSP5", "CRDG", "ESSG", "PLQ4", "PLQ3",
        "ATLG", "ERO1", "ERO2", "ERO3", "ERO4", "ERO5", "ERO6", "ERO7", "ERO8",
        "LNN1", "LNN2", "LNN3", "LNN4", "RMAR", "ENDG", "EPFV", "CTG1", "CTG2",
        "CTG3", "CSLG", "EMGG", "EDQG", "EMUG", "URA1", "URAP", "EPMG", "JPR1",
        "EGPG", "EITG", "SPRG", "GECG", "TGJ1", "TGJ2", "GEC3", "GE32", "TMFG",
        "TFL1", "TFL4", "PRIG", "PRG1", "PRG2", "2S8I", "SOEG", "TBSG", "TBST",
        "TBQ3", "TBQ4", "TBQ1", "TCIG", "TCD1", "TCD2", "TCDG", "TRCG", "TRIG",
        "TMNG", "TRN1", "GNCG", "2Z66", "VESG", "2S9Q"
    ]
    code_filtered = df[df['Values_code'].isin(codes)]
    
    ## Generate column name list.
    cols = []
    for hour in range(1,25):
        formatted = str(hour).rjust(2, '0') 
        cols.append(f'Values_Hour{formatted}')

    df_cols = df[cols]
    code_filtered['mean'] = df_cols.mean(axis=1)

    col_filtered = code_filtered[['mean', 'Date']]

    bool_series = pd.isnull(col_filtered['mean'])
    filtered = col_filtered[bool_series]
    print(col_filtered.isna().any())
    print(col_filtered.loc[:, col_filtered.isna().any()])
    # print('-----')
    # print(filtered)
    # print('-----')
    # print(code_filtered)
    # print(df)

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)



def date_demo():
    start_date = date(2000, 1, 1)
    end_date = date(2021, 3, 31)
    next_end_date = end_date + timedelta(days=1)

    for single_date in daterange(start_date, next_end_date):
        print(single_date.strftime("%Y-%m-%d"))

if __name__ == '__main__':
    main()
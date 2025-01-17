# @title Leggo dataset; unisco il campo data e ora
import numpy as np
import pandas as pd
from datetime import datetime, time

file_csv = f"/content/drive/MyDrive/umidità_correzione/Ortles_2N.csv"

# Leggi il file CSV
df = pd.read_csv(file_csv, decimal=".", sep=";")

# Assicurati che entrambe le colonne siano di tipo stringa
df['date'] = df['date'].astype(str)
df['time'] = df['time'].astype(str)

df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], format='%Y-%m-%d %H:%M:%S')

df['PM2_5'] = df['PM2_5'].astype(np.float64)
df['PM10'] = df['PM10'].astype(np.float64)

df.info()

# @title Definisco le funzioni per correzione umidità K=livello di igroscopicità della particella

def chakrabarti_PM10(df):
    # Controllo che le colonne esistano nel DataFrame
    if 'PM10' in df.columns and 'hum' in df.columns:

        # sostituisco i valori di 'hum' pari a 100 con 99.9
        df.loc[:, 'hum_trasf'] = df['hum'].apply(lambda x: 99.9 if x == 100 else x) * 0.01

        # Applico la funzione
        df.loc[:, 'PM10_chakra'] = df.apply(
            lambda row: row['PM10'] / (1 + ((0.25 * row['hum_trasf']) / (-1 + (1/row['hum_trasf']))))
            if pd.notnull(row['PM10']) and row['hum_trasf'] > 0.4 else row['PM10'], axis=1
        )

    return df

def crilley_PM10(df):
    # Controllo che le colonne esistano nel DataFrame
    if 'PM10' in df.columns and 'hum' in df.columns:

        # sostituisco i valori di 'hum' pari a 100 con 99.9
        df.loc[:, 'hum_trasf'] = df['hum'].apply(lambda x: 99.9 if x == 100 else x) * 0.01

        # Applico la funzione
        df.loc[:, 'PM10_crilley'] = df.apply(
            lambda row: row['PM10'] / (1 + ((0.242424) / (-1 + (1/row['hum_trasf']))))
            if pd.notnull(row['PM10']) and row['hum_trasf'] > 0.4 else row['PM10'], axis=1
        )

    return df

def crilley_PM25(df):
    # Controllo che le colonne esistano nel DataFrame
    if 'PM2_5' in df.columns and 'hum' in df.columns:

        # sostituisco i valori di 'hum' pari a 100 con 99.9
        df.loc[:, 'hum_trasf'] = df['hum'].apply(lambda x: 99.9 if x == 100 else x)*0.01

        # Applico la funzione
        df.loc[:, 'PM2.5_crilley'] = df.apply(
            lambda row: row['PM2_5'] / (1 + ((0.242424) / (-1 + (1/row['hum_trasf']))))
            if pd.notnull(row['PM2_5']) and row['hum_trasf'] > 0.4 else row['PM2_5'], axis=1
        )

    return df

def chakrabarti_PM25(df):
    # Controllo che le colonne esistano nel DataFrame
    if 'PM2_5' in df.columns and 'hum' in df.columns:

        # sostituisco i valori di 'hum' con 99.9
        df.loc[:, 'hum_trasf'] = df['hum'].apply(lambda x: 99.9 if x == 100 else x) * 0.01

        # Applico la funzione
        df.loc[:, 'PM2.5_chakra'] = df.apply(
            lambda row: row['PM2_5'] / (1 + ((0.25 * row['hum_trasf']) / (-1 + (1/row['hum_trasf']))))
            if pd.notnull(row['PM2_5']) and row['hum_trasf'] > 0.4 else row['PM2_5'], axis=1
        )

    return df

def diAntonio_PM25(df):
    # Controllo che le colonne esistano nel DataFrame
    if 'PM2_5' in df.columns and 'hum' in df.columns:

        # sostituisco i valori di 'hum' con 99.9
        df.loc[:, 'hum_trasf_perc'] = df['hum'].apply(lambda x: 99.9 if x == 100 else x)*0.1

        # Applico la funzione
        df.loc[:, 'PM2.5_diAntonio'] = df.apply(
            lambda row: row['PM2_5'] / (1 + (0.62 / (-1 + (1/row['hum_trasf']))))
            if pd.notnull(row['PM2_5']) and row['hum_trasf'] > 0.4 else row['PM2_5'], axis=1
        )

    return df

# @title Applichiamo la funzione al dataset
df = chakrabarti_PM10(df)
df = crilley_PM10(df)
df = chakrabarti_PM25(df)
df = crilley_PM25(df)
df = diAntonio_PM25(df)

df.info()

# @title Andamenti a confronto
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Crea una figura con due subplot condividendo l'asse x (datetime)
fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                    subplot_titles=('PM10', 'PM10_chakrabarti', 'PM10_crilley'))

# Aggiungi
fig.add_trace(
    go.Scatter(x=df['datetime'], y=df['PM10'], mode='lines', name='PM10'),
    row=1, col=1
)

# Aggiungi
fig.add_trace(
    go.Scatter(x=df['datetime'], y=df['PM10_chakra'], mode='lines', name='PM10_chakrabarti'),
    row=2, col=1
)

# Aggiungi
fig.add_trace(
    go.Scatter(x=df['datetime'], y=df['PM10_crilley'], mode='lines', name='PM10_crilley'),
    row=3, col=1
)


# Aggiorna il layout per dare titoli e grandezza della finestra
fig.update_layout(height=800, width=1500, title_text='Andamenti di PM10 e PM10 corretto con algoritmi umidità Chakrabarti e Crilley',
                  xaxis_title='Datetime', yaxis_title='Concentrazione [µg/m3]')

# Mostra il grafico
fig.show()

# @title Andamenti a confronto
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Crea una figura con due subplot condividendo l'asse x (datetime)
fig = make_subplots(rows=4, cols=1, shared_xaxes=True,
                    subplot_titles=('PM2_5', 'PM2.5_chakrabarti', 'PM2.5_crilley', 'PM2.5_diAntonio'))

# Aggiungi
fig.add_trace(
    go.Scatter(x=df['datetime'], y=df['PM2_5'], mode='lines', name='PM2.5'),
    row=1, col=1
)

# Aggiungi
fig.add_trace(
    go.Scatter(x=df['datetime'], y=df['PM2.5_chakra'], mode='lines', name='PM2.5_chakrabarti'),
    row=2, col=1
)

# Aggiungi
fig.add_trace(
    go.Scatter(x=df['datetime'], y=df['PM2.5_crilley'], mode='lines', name='PM2.5_crilley'),
    row=3, col=1
)

# Aggiungi
fig.add_trace(
    go.Scatter(x=df['datetime'], y=df['PM2.5_diAntonio'], mode='lines', name='PM2.5_diAntonio'),
    row=4, col=1
)

# Aggiorna il layout per dare titoli e grandezza della finestra
fig.update_layout(height=800, width=1500, title_text='Andamenti di PM2.5 e PM2.5 corretto con algoritmi umidità Chakrabarti; Crilley; di Antonio',
                  xaxis_title='Datetime', yaxis_title='Concentrazione [µg/m3]')

# Mostra il grafico
fig.show()

# @title export excel

#creo un sottodataset con le colonne che mi interessano
sotto_df = df[['datetime', 'PM10','PM10_chakra', 'PM10_crilley', 'PM2_5', 'PM2.5_chakra', 'PM2.5_crilley', 'PM2.5_diAntonio']]

# Raggruppa per giorno e calcola la media delle colonne
medie_giornalieri = sotto_df.resample('D', on='datetime')[['PM10','PM10_chakra', 'PM10_crilley', 'PM2_5' , 'PM2.5_chakra', 'PM2.5_crilley', 'PM2.5_diAntonio']].mean().reset_index()

# Esporta il DataFrame in un file Excel
medie_giornalieri.to_excel('giornalieri_UMIDITà_Ortles2N_2022_2023.xlsx', index=False)

print("File Excel esportato con successo!")

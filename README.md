## Correzione Umidità e Analisi dei Dati di Particolato Atmosferico

### Descrizione del Progetto

Questo progetto si occupa della lettura, manipolazione e analisi di un dataset contenente misurazioni di PM10 e PM2.5, con l'obiettivo di correggere i valori in base all'umidità utilizzando vari algoritmi di correzione (Chakrabarti, Crilley, e di Antonio). Viene inoltre generato un report visivo e un file Excel contenente le medie giornaliere delle concentrazioni di particolato atmosferico.

### Struttura del Progetto

#### 1. Lettura del Dataset

Il file CSV è letto utilizzando pandas. Il dataset contiene colonne per data, ora, umidità relativa (hum), e concentrazioni di PM10 e PM2.5.

#### 2. Unione delle Colonne Data e Ora

Le colonne date e time vengono unite per creare una colonna datetime che rappresenta il timestamp completo per ogni misurazione.

#### 3. Correzione Umidità

Sono definite cinque funzioni per correggere le concentrazioni di PM10 e PM2.5 in base all'umidità relativa:

-chakrabarti_PM10

-crilley_PM10

-chakrabarti_PM25

-crilley_PM25

-diAntonio_PM25

Queste funzioni applicano formule specifiche per correggere i valori di particolato basandosi sull'umidità.

#### 4. Visualizzazione dei Risultati

Utilizzando plotly, vengono creati grafici per confrontare i valori originali e corretti di PM10 e PM2.5. I grafici mostrano le differenze tra i dati non corretti e quelli corretti usando i diversi algoritmi di correzione.


#### Note

Assicurarsi che i valori di umidità non superino il 100%. Nel caso in cui ciò accada, i valori vengono corretti a 99.9%.

La correzione si applica solo ai valori di umidità superiori al 40%.

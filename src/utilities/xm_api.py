import os
import json
import shutil
import requests
import pandas as pd
import datetime as dt
from pandas.io.json import json_normalize


class ReadDB:
    def __init__(self):
        self.url = "http://servapibi.xm.com.co/hourly"
        self.connection = None
        self.request = ''
        self.inventario_metricas = {
            'Gene': [
                (0, 'Generacion Real', 'Sistema', 'Horaria'),
                (1, 'Generacion Real por Recurso', 'Recurso', 'Horaria')], 
            'DemaCome': [
                (0, 'Demanda Comercial', 'Sistema', 'Horaria'),
                (1, 'Demanda Comercial por Agente', 'Agente', 'Horaria')], 
            'AporEner': [(0, 'Aportes Energia', 'Sistema', 'Diaria')], 
            'PrecEscaAct': [(0, 'Precio de Escasez de Activacion', 'Sistema', 'Diaria')], 
            'ConsCombustibleMBTU': [(0, 'Consumo Combustible Recursos pertenecientes al Despacho Central', 'Recurso', 'Horaria')], 
            'PrecOferDesp': [(0, 'Precio de Oferta del Despacho', 'Recurso', 'Horaria')], 
            'PrecBolsNaci': [(0, 'Precio de Bolsa Nacional', 'Sistema', 'Horaria')], 
            'MaxPrecOferNal': [(0, 'Máximo Precio de Oferta Nacional', 'Sistema', 'Horaria')], 
            'RestAliv': [(0, 'Restricciones Aliviadas', 'Sistema', 'Horaria')], 
            'GeneIdea': [
                (0, 'Generacion Ideal', 'Sistema', 'Horaria'),
                (1, 'Generacion Ideal', 'Recurso', 'Horaria')], 
            'VoluUtilDiarEner': [(0, 'Volumen Util Diario', 'Sistema', 'Diaria')], 
            'RemuRealIndiv': [(0, 'RRID', 'Sistema', 'Diaria')],
            'CapEfecNeta': [
                (0, 'Listado de recursos térmicos con su respectiva Capacidad Efectiva Neta por mes', 'Sistema', 'Anual'),
                (1,'Listado Recursos Generación','Recurso','Diaria')],
            'VentContEner': [
                (0,'Ventas en Contratos Energía','Sistema','Horaria'),
                (1,'Ventas en Contratos Energía por Agente','Agente','Horaria')],
            'CompContEner': [
                (0,'Compras en Contrato Energía','Sistema','Horaria'),
                (1,'Compras en Contrato Energía por Agente','Agente','Horaria')],
            'CompBolsNaciEner': [
                (0,'Compras en Bolsa Nacional Energía','Sistema','Horaria'),
                (1,'Compras en Bolsa Nacional Energía por Agente','Agente','Horaria')],
            'PrecPromContRegu': [(0,'Precio Promedio Contratos Regulado','Sistema','Diaria')],
            'PrecPromContNoRegu': [(0,'Precio Promedio Contratos No Regulado','Sistema','Diaria')],
            'ConsCombAprox': [(0,'Consumo Comb Aprox.','RecursoComb','Horaria')],
            'EmisionesCO2': [(0,'Emisiones CO2','RecursoComb','Horaria')],
            'EmisionesCH4': [(0,'Emisiones CH4','RecursoComb','Horaria')],
            'EmisionesN2O': [(0,'Emisiones N2O','RecursoComb','Horaria')],
            'EmisionesCO2Eq': [(0,'Emisiones CO2e','Recurso','Horaria')],
            'factorEmisionCO2e': [(0,'factor emision CO2e','Sistema','Horaria')],
            'ImpoEner': [(0,'Importaciones Energía','Sistema','Horaria')]
        }
        
    def get_collections(self, coleccion):
        return self.inventario_metricas[coleccion]

    def request_data(self, coleccion, metrica, start_date, end_date):
        """ request public server data from XM by the API

        Args:
            variable: one of this variables "DemaCome", "Gene", "GeneIdea", "PrecBolsNaci", "RestAliv"
            start_date: start date consult data
            end_date: end date consult data

        Returns: DataFrame with the raw Data

        """
        if coleccion not in self.inventario_metricas.keys():
            print('No existe la colección {}'.format(coleccion))
            return None
        if metrica > len(self.inventario_metricas[coleccion]):
            print('No existe la metrica')
            return None

        if self.inventario_metricas[coleccion][metrica][3] == 'Horaria':

            end = end_date
            condition = True
            aux = True
            data = None
            while condition:
                if (start_date - end_date).days < 30:
                    end = start_date + dt.timedelta(29)
                if end > end_date:
                    end = end_date
                
                self.request = {
                    "MetricId": coleccion,
                    "StartDate": "{}".format(str(start_date)),
                    "EndDate": "{}".format(str(end)),
                    'Entity': self.inventario_metricas[coleccion][metrica][2]
                }

                ## print(self.request) #TEMP

                self.connection = requests.post(self.url, json=self.request)
                
                data_json = json.loads(self.connection.content)
            
                temporal_data = json_normalize(data_json['Items'], 'HourlyEntities', 'Date', sep='_')
                
                if data is None:
                    data = temporal_data.copy()
                else:
                    data = data.append(temporal_data, ignore_index=True)
                
                start_date = start_date + dt.timedelta(30)

                if end == end_date:
                    aux = False
                condition = ((end - start_date).days > 30 | (end - end_date).days != 0) | aux
        elif self.inventario_metricas[coleccion][metrica][3] == 'Diaria' and coleccion == 'CapEfecNeta':
            end = end_date
            condition = True
            aux = True
            data = None
            while condition:
                if (start_date - end_date).days < 1:
                    end = start_date + dt.timedelta(0)
                if end > end_date:
                    end = end_date
                self.request = {"MetricId": coleccion,
                                "StartDate": "{}".format(str(start_date)),
                                "EndDate": "{}".format(str(end)),
                                'Entity': self.inventario_metricas[coleccion][metrica][2]}

                ## print(self.request) #TEMP

                self.url=self.url.replace('hourly','daily')
                self.connection = requests.post(self.url, json=self.request)
                
                data_json = json.loads(self.connection.content)
            
                temporal_data = json_normalize(data_json['Items'], 'DailyEntities', 'Date', sep='_')
                
                if data is None:
                    data = temporal_data.copy()
                else:
                    data = data.append(temporal_data, ignore_index=True)
                start_date = start_date + dt.timedelta(1)

                if end == end_date:
                    aux = False
                condition = ((end - start_date).days > 1 | (end - end_date).days != 0) | aux            
        elif self.inventario_metricas[coleccion][metrica][3] == 'Diaria':

            end = end_date
            condition = True
            aux = True
            data = None
            while condition:
                if (start_date - end_date).days < 30:
                    end = start_date + dt.timedelta(29)
                if end > end_date:
                    end = end_date

                self.request = {"MetricId": coleccion,
                                "StartDate": "{}".format(str(start_date)),
                                "EndDate": "{}".format(str(end)),
                                'Entity': self.inventario_metricas[coleccion][metrica][2]}

                ## print(self.request) #TEMP

                self.url=self.url.replace('hourly','daily')                
                self.connection = requests.post(self.url, json=self.request)
                data_json = json.loads(self.connection.content)
                temporal_data = json_normalize(data_json['Items'], 'DailyEntities', 'Date', sep='_')
                if data is None:
                    data = temporal_data.copy()
                else:
                    data = data.append(temporal_data, ignore_index=True)

                start_date = start_date + dt.timedelta(30)
                if end == end_date:
                    aux = False
                condition = ((end - start_date).days > 29 | (end - end_date).days != 0) | aux
        elif self.inventario_metricas[coleccion][metrica][3] == 'Anual':

            end = end_date
            condition = True
            aux = True
            data = None
            while condition:
                if (start_date - end_date).days < 366:
                    end = start_date + dt.timedelta(365)
                if end > end_date:
                    end = end_date

                self.request = {"MetricId": coleccion,
                                "StartDate": "{}".format(str(start_date)),
                                "EndDate": "{}".format(str(end)),
                                'Entity': self.inventario_metricas[coleccion][metrica][2]}

                ## print(self.request) #TEMP

                self.url=self.url.replace('hourly','annual')
                self.connection = requests.post(self.url, json=self.request)
                data_json = json.loads(self.connection.content)
                temporal_data = json_normalize(data_json['Items'], 'AnnualEntities', 'Code', sep='_')
                if data is None:
                    data = temporal_data.copy()
                else:
                    data = data.append(temporal_data, ignore_index=True)

                start_date = start_date + dt.timedelta(366)
                if end == end_date:
                    aux = False
                condition = ((end - start_date).days > 365 | (end - end_date).days != 0) | aux

        return data

def saveRequestAsCSV(output_directory, collection, metric, filename):
    consult = ReadDB()
    startDate = dt.date(2017, 12, 1)
    endDate = dt.date.today()
    df = consult.request_data(collection, metric, startDate, endDate)
    path = f'{output_directory}/{filename}'
    df.to_csv(path, index=False)

def format_horary(folder, filename):
    read_path = f'{folder}/{filename}'
    df = pd.read_csv(read_path)

    ## Decompose 'Date' column.
    df['year'] = df['Date'].map(lambda x: dt.datetime.strptime(x , '%Y-%m-%d').year)
    df['month'] = df['Date'].map(lambda x: dt.datetime.strptime(x , '%Y-%m-%d').month)
    df['day'] = df['Date'].map(lambda x: dt.datetime.strptime(x , '%Y-%m-%d').day)

    ## Generate column name list.
    cols = []
    for hour in range(1,25):
        formatted = str(hour).rjust(2, '0') 
        cols.append(f'Values_Hour{formatted}')

    df_cols = df[cols]
    df['mean'] = df_cols.mean(axis=1)

    df_filtered = df[['mean', 'Date', 'year', 'month', 'day']]

    save_path = f'{folder}/formatted_{filename}'
    df_filtered.to_csv(save_path, index=False)
    print(f'{filename} has been formatted as formatted_{filename}')

def format_horary_with_codes(folder, filename):
    # Not found via CTRL +F, on csv file:
    # "ACEG", "AXEG", "EPSG", "ARG1", "2S8G", "2VJS", "CIVG", "CRLG", "TBQ2",
    # "BLL1", "BLL2", "CHN4", "CHN5", "CHN6", "CHN7", "CHN8", "TBS1", "TBS2",
    # "TBS3", "TBS4", "TBSA", "TB22", "ST24", "DEPG", "UNIB", "EDNG", "BLVG",
    # "CSP1", "CSP2", "CSP3", "CSP4", "CSP5", "CRDG", "ESSG", "PLQ4", "ATLG",
    # "ERO1", "ERO2", "ERO3", "ERO4", "ERO5", "ERO6", "ERO7", "ERO8", "LNN1",
    # "LNN2", "LNN3", "LNN4", "RMAR", "ENDG", "EPFV", "EMGG", "EDQG", "EMUG",
    # "URAP", "EPMG", "JPR1", "EGPG", "EITG", "SPRG", "GECG", "TMFG", "PRIG",
    # "2S8I", "SOEG", "TBSG", "TBQ1", "TCIG", "TCDG", "TRCG", "TRIG", "TMNG",
    # "GNCG", "2Z66", "VESG", "2S9Q"

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

    read_path = f'{folder}/{filename}'
    df = pd.read_csv(read_path)

    df_code_filtered = df[df['Values_code'].isin(codes)]
    
    ## Generate column name list.
    cols = []
    for hour in range(1,25):
        formatted = str(hour).rjust(2, '0') 
        cols.append(f'Values_Hour{formatted}')

    df_cols = df[cols]
    df_code_filtered['mean'] = df_cols.mean(axis=1)

    df_filtered = df_code_filtered[['mean', 'Date']]
    
    final_df = df_filtered.groupby('Date')['mean'].mean().reset_index()
    final_df.columns = ['Date', 'Value']

    ## Decompose 'Date' column.
    final_df['year'] = final_df['Date'].map(lambda x: dt.datetime.strptime(x , '%Y-%m-%d').year)
    final_df['month'] = final_df['Date'].map(lambda x: dt.datetime.strptime(x , '%Y-%m-%d').month)
    final_df['day'] = final_df['Date'].map(lambda x: dt.datetime.strptime(x , '%Y-%m-%d').day)

    save_path = f'{folder}/formatted_{filename}'
    final_df.to_csv(save_path, index=False)
    print(f'{filename} has been formatted as formatted_{filename}')

def format_daily(folder, filename):
    read_path = f'{folder}/{filename}'
    df = pd.read_csv(read_path)

    ## Decompose 'Date' column.
    df['year'] = df['Date'].map(lambda x: dt.datetime.strptime(x , '%Y-%m-%d').year)
    df['month'] = df['Date'].map(lambda x: dt.datetime.strptime(x , '%Y-%m-%d').month)
    df['day'] = df['Date'].map(lambda x: dt.datetime.strptime(x , '%Y-%m-%d').day)

    df_filtered = df[['Value', 'Date', 'year', 'month', 'day']]

    save_path = f'{folder}/formatted_{filename}'
    df_filtered.to_csv(save_path, index=False)
    print(f'{filename} has been formatted as formatted_{filename}')

def main(output_directory, interval):
    ext = 'csv'
    test= str(interval).zfill(3)
    queries = [
        #('Gene', 0, f'Generacion Real-{test}.{ext}'),
        #('Gene', 1, f'Generacion Real por Recurso-{test}.{ext}'),
        #('DemaCome', 0, f'Demanda Comercial-{test}.{ext}'),
        #('DemaCome', 1, f'Demanda Comercial por Agente-{test}.{ext}'),    
        #('AporEner', 0, f'Aportes Energia-{test}.{ext}'),
        ('PrecEscaAct', 0, f'Precio de Escasez de Activacion.{ext}'), 
        ('PrecOferDesp', 0, f'Precio de Oferta del Despacho.{ext}'), 
        ('PrecBolsNaci', 0, f'Precio de Bolsa Nacional.{ext}'),  
        #('VoluUtilDiarEner', 0, f'Volumen Util Diario-{test}.{ext}'),  
        #('CompBolsNaciEner', 0, f'Compras en Bolsa Nacional Energía-{test}.{ext}'),  
        #('CompBolsNaciEner', 1, f'Compras en Bolsa Nacional Energía por Agente-{test}.{ext}')  
    ]

    for query in queries:
        print(f'fetching {query[2]} ...')
        saveRequestAsCSV(output_directory, query[0], query[1], query[2])
        print(f'{query[2]} has been saved!')
        if(query[0] == 'PrecBolsNaci'):
            format_horary(output_directory, query[2])
            print('')
        if (query[0] == 'PrecOferDesp'):
            format_horary_with_codes(output_directory, query[2])
            print('')
        if (query[0] == 'PrecEscaAct'):
            format_daily(output_directory, query[2])
            print('')

    original_names = [query[2] for query in queries]  
    
    # should be length 2
    file_names = [f'formatted_{query[2]}' for query in queries if (query[0] == 'PrecEscaAct' or query[0] == 'PrecOferDesp')]  
    print(original_names)
    print(file_names)

    # remove unnecesary files.
    for original_name in original_names:
        rm_path = f'{output_directory}/{original_name}'
        os.remove(rm_path)

    escasez_df = pd.read_csv(f'{output_directory}/{file_names[0]}')
    despacho_df = pd.read_csv(f'{output_directory}/{file_names[1]}')
    escasez_date = escasez_df.tail(1)['Date'].to_list()[0]
    despacho_date = despacho_df.tail(1)['Date'].to_list()[0]
    final_date = despacho_date if escasez_date > despacho_date else escasez_date
    sized_escasez = escasez_df[escasez_df['Date'] <= final_date]
    sized_despacho = despacho_df[despacho_df['Date'] <= final_date]
    sized_escasez.to_csv(f'{output_directory}/sized_{file_names[0]}', index=False)
    sized_despacho.to_csv(f'{output_directory}/sized_{file_names[1]}', index=False)

    # remove unnecesary files.
    for file_name in file_names:
        rm_path = f'{output_directory}/{file_name}'
        os.remove(rm_path)

def run():
    dirname = os.path.dirname(__file__)
    outdir = os.path.join(dirname, f'../../downloads')
    if os.path.exists(outdir):
        shutil.rmtree(outdir)
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    main(outdir, 1)

if __name__ == '__main__':
    run()
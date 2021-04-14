import os
import json
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
    startDate = dt.date(2017, 1, 1)
    endDate = dt.date.today()
    df = consult.request_data(collection, metric, startDate, endDate)
    path = f'{output_directory}/{filename}'
    df.to_csv(path, index=False)

def formatPrecioBolsa(folder, filename):
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

    df_filtered = df[['mean', 'year', 'month', 'day']]

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
        #('PrecEscaAct', 0, f'Precio de Escasez de Activacion-{test}.{ext}'), 
        ('PrecBolsNaci', 0, f'Precio de Bolsa Nacional-{test}.{ext}'),  
        #('VoluUtilDiarEner', 0, f'Volumen Util Diario-{test}.{ext}'),  
        #('CompBolsNaciEner', 0, f'Compras en Bolsa Nacional Energía-{test}.{ext}'),  
        #('CompBolsNaciEner', 1, f'Compras en Bolsa Nacional Energía por Agente-{test}.{ext}')  
    ]

    for query in queries:
        print(f'fetching {query[2]} ...')
        saveRequestAsCSV(output_directory, query[0], query[1], query[2])
        print(f'{query[2]} has been saved!')
        if(query[0] == 'PrecBolsNaci'):
            formatPrecioBolsa(output_directory, query[2])
            print('')

if __name__ == '__main__':
    dirname = os.path.dirname(__file__)
    outdir = os.path.join(dirname, f'../../downloads')
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    main(outdir, 1)
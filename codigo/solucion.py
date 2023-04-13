import pandas as pd
from difflib import SequenceMatcher


def main():
    ##archivo origen a pandas
    df_csv=pd.read_csv(r'.\csv\2023-04-11T04-36-02-388Zinstituciones_educativas.csv')
    df_js=pd.read_json(r'.\json\universidades.json')
    #Se crea nueva columna
    df_csv['universidad homologada']=''
    ##Quitar espacios en blanco en nombre de columnas
    df_js.columns =df_js.columns.str.strip()
    ##Convertir a mayúsculas
    df_js['Universidad']=df_js['Nombre'].str.upper()
    df_csv['Universidad']=df_csv['value'].str.upper()

    #Se quitan palabras comunes
    list_remove=['UNIVERSIDAD','NACIONAL','PRIVADA','DEL','DE','S.A.C.','S.A.','S.R.L.',' ']
    for i in list_remove:
        df_js['Universidad']=df_js['Universidad'].str.replace(i,'')
        df_csv['Universidad']=df_csv['Universidad'].str.replace(i,'')

    #Se crea estructura final de la tabla
    df_final=pd.DataFrame(columns=['nombre_universidad','sinonimos'])

    #Proceso de comparación para obtención de JSON
    for index,row_js in df_js.iterrows():
        list_parecidos=[]
        
        for index_y, row_csv in df_csv.iterrows():
            rt=SequenceMatcher(None,row_js['Universidad'],row_csv['Universidad'])
            ratio=rt.ratio()
            #se toma el ratio 0.7 para asumir parecidos razonables entre los textos
            if ratio>=0.70:
                if row_csv['value'] not in list_parecidos:
                    list_parecidos.append(row_csv['value'])
            rt2=SequenceMatcher(None,row_js['Siglas'],row_csv['Universidad'])
            ratio2=rt2.ratio()
            if ratio2>=0.70:
                if row_csv['value'] not in list_parecidos:
                    list_parecidos.append(row_csv['value'])
        
        df_final.loc[index]=[row_js['Nombre'],list_parecidos]

        
    df_final.to_json(r'.\resultado\sinonimo_universidades.json',orient='records')

    #Proceso de comparación para obtención de CSV
    for index,row_csv in df_csv.iterrows():
        
        
        for index_y, row_js in df_js.iterrows():
            rt=SequenceMatcher(None,row_js['Universidad'],row_csv['Universidad'])
            ratio=rt.ratio()
            rt2=SequenceMatcher(None,row_js['Siglas'],row_csv['Universidad'])
            ratio2=rt2.ratio()
            if ratio>=0.70:
                df_csv['universidad homologada'][index]=row_js['Nombre']
                break
            elif ratio2>=0.70:
                df_csv['universidad homologada'][index]=row_js['Nombre']
                break
            

    header=['candidateId','value','universidad homologada']      
    df_csv.to_csv(r'.\resultado\universidades_homologadas.csv',index=False,columns = header)       



def init():
    if __name__=='__main__':
        main()

init()
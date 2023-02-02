import requests
import pandas as pd
import json

def anrop(url : str, query : dict) -> pd.DataFrame:
    ''' Anropar och genomför mindre bearbetning av data från SCBs API.
    
        Argument:
            url   : Url för aktuell data, unikt för varje dataset
            query : Json med parametrar som kan användas för att filtrera data

        Returns:
            df    : DataFrame med något bearbetad data 
    '''

    # Laddar json-data från API
    session   = requests.Session()
    response  = session.post(url, json=query)
    json_data = json.loads(response.content)

    # Konverterar json-data till DataFrame
    _df = pd.json_normalize(json_data['data'])

    # Datan kommer i ett stökigt format och resulterar i en DataFrame med 
    # två kolumner, "key" och "values", där datan ligger inpackad i listor. 
    # Dessa packas upp till två separata DataFrames nedan
    df_key    = _df['key'].apply(pd.Series)
    df_values = _df['values'].apply(pd.Series)

    # Kombinera resultat till en ny DataFrame
    df = pd.concat([df_key, df_values], axis=1)

    # Under json_data['columns'] finns en lista med dicts för varje kolumn i 
    # datan. Under nyckeln "text" finns variabelnamnet
    _cols = [col['text'] for col in json_data['columns']]
    df.columns = _cols

    # I SCB's data representeras saknade värden med "..", dessa ersätts 
    # med det mer Python-vänliga None nedan
    df = df.mask(df=='..', None)

    return df




#FIXME - Ta bort, används för test
if __name__ == '__main__':
    url = "https://api.scb.se/OV0104/v1/doris/sv/ssd/START/FM/FM0103/FM0103A/FirENS2010ofKv"
  
    query = {
      "query": [
        {
          "code": "Sektor",
          "selection": {
            "filter": "item",
            "values": [
              "S14"
            ]
          }
        },
        {
          "code": "Kontopost",
          "selection": {
            "filter": "item",
            "values": [
              "BF9000",
              "FA0100",
              "FA5190",
              "FL0100"
            ]
          }
        },
        {
          "code": "Motsektor",
          "selection": {
            "filter": "item",
            "values": [
              "S0"
            ]
          }
        },
        {
          "code": "ContentsCode",
          "selection": {
            "filter": "item",
            "values": [
              "FM0103AS"
            ]
          }
        }
      ],
      "response": {
        "format": "json"
      }
    }
    
    df = anrop(url, query)
    print(df)

import pyodbc
import pandas as pd
import os
import xlsxwriter  
import re 
from datetime import datetime


current_path = os.path.dirname(os.path.abspath(__file__))
def select_empresas():
  conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={servidor};'
        f'DATABASE=master;UID={user};{senha}'
    )

  consulta_path = os.path.join(current_path, 'consulta')
  file = 'selectempresas.txt'
  consulta_empresas = os.path.join(consulta_path, file)
  with open(consulta_empresas, 'r') as query:
    consulta = query.read()
    
  cursor = conn.cursor() 
  cursor.execute(consulta)
  empresas = cursor.fetchall()
  
  return empresas

def nome_empresafunc(database,empresa):

    conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={servidor};'
        f'DATABASE=master;UID={user};{senha}'
    )

    
    print("Conexão Bem Sucedida")
    cursor = conn.cursor()

    query_nome_empresa = f"select razaosocial from empresas where cnpj = '{empresa} ' "
    try:
     cursor.execute(query_nome_empresa)   
     razao_social  = cursor.fetchall()
     if not razao_social:
       return 1
     else:
        return razao_social   
    except:
       pass 
      
def gerarconsulta(database, empresa, datainicio, datafim, consulta, filiais, multiquery):
    

           

    # Conexão com o banco de dados
    conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={servidor};'
        f'DATABASE=master;UID={user};{senha}'
    )

    print("Conexão Bem Sucedida")
    cursor = conn.cursor()

    taskfolders = os.path.join(current_path,'consulta')
    task = f'{consulta}.txt'
    pathtask = os.path.join(taskfolders, task)

    with open(pathtask, 'r') as query:
        sql_query = query.read()

    functions = sql_query.split('--##')
    raiz_cnpj = empresa[:8]
    query_nome_empresa = f"select cnpj from empresas where cnpj = '{empresa}' or cnpj like '%{raiz_cnpj}%' "
    try:
     cursor.execute(query_nome_empresa)   
     nome_empresa = cursor.fetchall()
     if not nome_empresa:
         
        return 1

     nomes_limpos = []
     for row in nome_empresa:
          
      nome_limpo = re.sub(r"[^\w\s\.]", " ",row[0])
      nomes_limpos.append(nome_limpo)

     
     nome_empresas = nomes_limpos[0]

    except Exception as e:
        print('erro',e)
    #Cria tabela
    try:
        criartabela  = functions[0]
        if filiais == True or filiais == 'True':
          raiz_cnpj_empresa = nome_empresas[:8]  
          criartabela = criartabela.format(empresa=raiz_cnpj_empresa, datainicio=datainicio, datafim=datafim)
        else: 
          criartabela = criartabela.format(empresa=empresa, datainicio=datainicio, datafim=datafim)   
         
        cursor.execute(criartabela)
        conn.commit()
        print('Tabelas criadas com sucesso')
    except Exception as e: 
        print('Não foi possível criar as tabelas',e)
        pass    
    

    try:
      
        if multiquery == 1:
          print('consulta de multi tabelas')
          try:   
            #Gera Consulta
            queries = functions[1].split(';')  
    
            queryfolder = os.path.join(current_path, 'planilhas')
            razao_social = nome_empresafunc(database,empresa)
            for row in razao_social:
              razao_social_distinct = row[0].replace(" ","")  
              razao_social_distinct = razao_social_distinct.replace(".","")   
            querypath = os.path.join(queryfolder, f'{consulta}_{razao_social_distinct}_{database}.xlsx')

                     
            with pd.ExcelWriter(querypath, engine='xlsxwriter') as writer:

                loop = 0
                for single_query in queries:
                    

                                       

                    if filiais == "True" or filiais == True:
                       print('Considera filiais')
                       raiz_cnpj_empresa = nome_empresas[:8]  
                       print(raiz_cnpj_empresa)
                       single_query = single_query.format(empresa=raiz_cnpj_empresa, datainicio=datainicio, datafim=datafim)
                    
                    else:
                        
                        print('Não considera filiais') 
                        single_query = single_query.format(empresa=empresa, datainicio=datainicio, datafim=datafim)

  

                    cursor.execute(single_query)
                    rows = cursor.fetchall()
                    columns = [column[0] for column in cursor.description]
                    
                        
                    df = pd.DataFrame.from_records(rows, columns=columns)
                    texto  = single_query
                    padrao = r'--(.*?)--'
                    resultados = re.findall(padrao, texto)

                    sheet_name = f'{resultados[0]}'


                    df.to_excel(writer, sheet_name=sheet_name, index=False)

                    coluna = 0
                    for column in df:
                       try:
                        coluna += 1

                        column_length = max(df[column].astype(str).map(len).max(), len(column))
                        col_idx = df.columns.get_loc(column)
                        writer.sheets[f'{sheet_name}'].set_column(col_idx, col_idx, column_length)

                       except Exception as e:
                           print ('erro',e) 
   
                   
                    loop += 1                       
                print("Arquivo Excel gerado com sucesso.")    

                    

          except Exception as e : 
           print('Erro ao gerar a consulta de multiplas abas', e)   
           pass                
        else:
          try:  
           queries = functions[1]
           texto  = queries
           padrao = r'--(.*?)--'
           resultados = re.findall(padrao, texto)
        
           queryfolder = os.path.join(current_path,'planilhas')
           razao_social = nome_empresafunc(database,empresa)
           for row in razao_social:
              razao_social_distinct = row[0].replace(" ","")  
              razao_social_distinct = razao_social_distinct.replace(".","")  
           querypath = os.path.join(queryfolder, f'{consulta}_{razao_social_distinct}_{database}.xlsx')
           if filiais == True or filiais == 'True':
            print("Considera filiais")   
            raiz_cnpj_empresa = nome_empresas[:8]  

            sql_query = queries.format(empresa=raiz_cnpj_empresa, datainicio=datainicio, datafim=datafim)

           else:
            print("Não considera filiais")   
            sql_query = queries.format(empresa=empresa, datainicio=datainicio, datafim=datafim)

           cursor.execute(sql_query)

           rows = cursor.fetchall()

           columns = [column[0] for column in cursor.description]
           df = pd.DataFrame.from_records(rows, columns=columns)
 
           df.to_excel(querypath, sheet_name=resultados[0], index = False)
           print("Arquivo Excel gerado com sucesso.")

          except Exception as e : 
           print('Erro ao gerar a consulta de aba única', e)    
           pass



    except Exception as e:
      print("Erro ao gerar a consulta", e)  
        #Dropar tabela criada
    try:
     dropartabela = functions[2]
     cursor.execute(dropartabela)
     conn.commit()
     print('Tabelas dropadas com sucesso')
    except Exception as e: 
     print('Não foi possível dropar as tabelas',e)
     pass   
   
    conn.close()

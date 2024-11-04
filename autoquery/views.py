from flask import render_template, request, redirect, session, flash, url_for, send_from_directory, jsonify, json, send_file
from BeaQuery import app, db
from models import Consultas
import os
import time 
from sqlalchemy import or_, and_
import uuid
from datetime import datetime
import redis
from queryexecute import gerarconsulta, nome_empresafunc, select_empresas
import re 
import pyodbc  
from trello import criartarefa, cards_list, delete_card


@app.route('/')
def query_auto():
 
  listaempresas = select_empresas()
  
  consultaslista = Consultas.query.order_by(Consultas.Task.asc()).all()
 
  return render_template('query.html', titulo='Solicitar consulta',  consultas = consultaslista, empresas =  listaempresas )




@app.route('/downloadquery', methods=['POST'])
def download_query():
    try:

        database = request.form.get('database')
        print(database)
        consulta = request.form.get('consulta')
        print(consulta)
        
        filiais = request.form.get('filiais')
        print(filiais)
        empresas = request.form.get('cnpj')
        empresa = re.sub('[^0-9]', '', empresas)
        print(empresa)
        datainicio = request.form.get('datainicio')
        print(datainicio)
        datafim = request.form.get('datafim')
        print(datafim)

        
        consultaslista = Consultas.query.filter_by(Task = consulta).first()
        multiquery = consultaslista.MultiplasAbas

        print(consulta)
        if filiais == 'on':
            filiais = True
        else:
            filiais = False

        print ('pedroPEDRO',filiais)
        try:
         returncode = gerarconsulta(database, empresa, datainicio, datafim, consulta, filiais, multiquery)
        except Exception as e:
         flash(f"Ocorreu um erro inesperado: {str(e)}")
       
        
        
        nome_empresa = []
        nome_empresass = nome_empresafunc(database, empresa)

        if nome_empresass == 1: 
            flash("Nenhuma empresa encontrada no ambiente selecionado")
        else: 
          for row in nome_empresass: 
            nome_empresa1 = re.sub(r"[^\w\s\.]", "", row[0])
            nome_empresa.append(nome_empresa1)
        print('rsrs',row[0])
        nomes_empresas = nome_empresa[0]
        nomes_empresas = nomes_empresas.replace(" ","")
        nomes_empresas = nomes_empresas.replace(".","")        
        data = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        queryfolder = os.path.join(r'planilhas')
        querypath = os.path.join(queryfolder, f'{consulta}_{nomes_empresas}_{database}.xlsx')

        return send_file(
        querypath,
        mimetype='text/xlsx',
        download_name=f'{consulta}_{nomes_empresas}_{database}.xlsx',
        as_attachment=True)
    
    
    
    except Exception as e:
       
        flash("Erro ao gerar a consulta, tente novamente")
        print('erro de consulta:', e)  
        
        
        
        return redirect(url_for('query_auto', titulo='Solicitar consulta', status = 'active',
    
         ))
 
 
 
@app.route('/trello')
def trello():
 
 
  cards = cards_list()
 
  return render_template('trello.html', titulo='Solicitação Requisitos', cards = cards, statustrello = 'active' )


@app.route('/criarcard', methods=['POST'])
def criar_tarefa():
 
   
 solicitante = request.form.get('solicitante') 
 titulo = request.form.get('titulo')
 descricao = request.form.get('descricao')
 arquivo = request.files.get('file')
 titulo = titulo + " - " + solicitante
 print(titulo,'GABIGOOOL')
 print(arquivo)
 try: 
  solicitacao = criartarefa(titulo,descricao, arquivo)
 except Exception as e:
     print('erro:', e)
 return redirect(url_for('trello', titulo = 'Solicitação Requisitos'))



@app.route('/deletarcard/<id>', methods=['POST'])
def deletar_tarefa(id):
 
 try: 
  deletar = delete_card(id)
 except Exception as e:
     print('erro:', e)
 return redirect(url_for('trello', titulo = 'Solicitação Requisitos'))



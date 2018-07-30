#################################################
##Codigo escrito por Ricardo Tosin################
##################################################
import socket
import sys
import datetime
import time
from thread import *

logServer2 = open('logServer2.txt','w') # Abre arquivo escrita do logServer2
datelog = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p") #Etiqueta de tempo para organizar log por data e hora

#VARIAVEL DE CONTROLE DE MODIFICACAO
pode_Alterar = False
storage_server = 0 #Variavel que armazena o valor a ser alterado

 
HOST = '127.0.0.1'   # Significa todas as interfaces disponiveis
PORT = 8887 # Porta Arbitraria nao Privilegiada
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket Criado'
 
#Binda o Socket para porta local
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Falha no Bind. Error Code : ' + str(msg[0]) + ' Mensagem: ' + msg[1]
    sys.exit()
     
print 'Socket bind SERVER 2 completo'
 
#Comeca a escutar o Socket de Rede
#Valor 10 s.listen() limita a conexao ate 10 ou seja a 11 ira ser recusada.
s.listen(10) 
print 'Escutando Socket'
logServer2.write(datelog + '---->' + 'Servidor 1 com IP :' + HOST + 'Iniciado na porta: ' + str(PORT) + '\n')
#Funcao para lidar com as conexoes e criar Threads
def clientthread(conn):
    global pode_Alterar
    #Enviando Mensagem ao Cliente Conectado.
    conn.send('ok') #Somente String
    #Loop Infinito, assim a thread nao termina.
    while True:
         
        #Recebendo do Cliente        
	data = conn.recv(1024)
	if (data == 'commit'):
		logServer2.write(datelog + '---->' + 'OK ENVIADO AO CLIENTE : '+ addr[0] + ':' + str(addr[1])+ '\n')
		pode_Alterar = True
		time.sleep(3)		
		reply = 'commit'
		conn.sendall(reply)
	   	break
	if (data == 'altera'):
		logServer2.write(datelog + '---->' + 'ALTERANDO DADOS PARA O CLIENTE: ' + addr[0] + ':' + str(addr[1]) + '\n')
		pode_Alterar = True
		time.sleep(3)
		storage_server = 1;
		logServer2.write(datelog + '---->' + 'DADO STORAGE MODIFICADO PARA CLIENTE: '+ addr[0] + ':' + str(addr[1]) + '\n' )
		reply = 'commit'
		break
	if (data == 'abort'):
		logServer2.write(datelog + '---->' + 'TENTATIVA DE ALTERAR FALHOU NO CLIENTE :'  + addr[0] + ':' + str(addr[1]) + '\n')
	elif not data:
            	break
    pode_Alterar = False		
    #Saindo do Loop
    conn.close()


#Continua Conectando com Clientes 
while 1:
    #Espera para aceitar a conexao - blocking call	
	if (pode_Alterar == True):
		conn, addr = s.accept()
		conn.send("NOK") # CASO JA EXISTA UMA CONEXAO ATIVA ENVIA ABORT AO CLIENTE
		conn.close()
	if (pode_Alterar == False):
		conn, addr = s.accept()
		logServer2.write(datelog + '---->' + 'ABERTA CONEXAO COM CLIENTE : ' + addr[0] + ':' + str(addr[1]) + '\n')
		print 'Connectado com ' + addr[0] + ':' + str(addr[1])
		#Inicia a Thread.
		pode_Alterar == True
		start_new_thread(clientthread, (conn,))
logServer2.close()	    
s.close()

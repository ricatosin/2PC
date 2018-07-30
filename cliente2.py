##########################################################
##Codigo cliente escrito por Ricardo Tosin ###############
##########################################################
 
import socket   
import sys  
import datetime
import time
 

logCli2 = open('logCli2.txt','w') # Abre arquivo escrita do logServer1
datelog = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p") #Etiqueta de tempo para organizar log por data e hora

 
host = '127.0.0.1';
port = 8886;

qnt_ok = 0 #VARIAVEL PARA TRATAR A QUESTAO DE QUANTOS OK O CLIENTE RECEBEU

while (port < 8889): #Loop para iterar a porta enviando a msg para os 3 servidores
	
	#TENTA CRIAR O SOCKET IVP4
	try:
	    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error:
	    print 'Falha ao Criar Socket'
	    sys.exit()
	     
	print 'Socket Criado'

	try:
	    remote_ip = socket.gethostbyname( host )
	 
	except socket.gaierror:
	    #ERRO NAO PODE RESOLVER O HOST
	    print 'Host nao pode ser resolvido... Saindo'
	    sys.exit()
	#Connect to remote server
	s.connect((remote_ip , port))
	logCli2.write(datelog + '---->' + 'CONECTADO AO SERVIDOR : ' + remote_ip + ':' + str(port)+ '\n')
	 
	print 'Socket Connectado em ' + host + ' no ip ' + remote_ip
	 
	#Envia Mensagem para SOLICITAR ALTERACAO o Servidor
	message = "commit"
	 
	try :
	    #Indica toda a Sequencia da mensagem
	    s.sendall(message)
	    time.sleep(1) # Variavel usada pra dar um tempo de 1 segundo antes de enviar para o proximo servidor	
	except socket.error:
	    #Caso falhe
	    print 'Falha no Envio'
	    sys.exit()
	 
	print 'Mensagem Enviada com sucesso'
	 
	#Recebe a resposta
	reply = s.recv(1024)
	if(reply == 'ok'):
		logCli2.write(datelog + '---->' + 'RECEBIDO OK DO SERVIDOR: '+ remote_ip + ':' + str(port)+ '\n')
		qnt_ok = qnt_ok + 1
		print qnt_ok
	print reply
	port = port + 1

######################## SE RECEVER UM OK DOS 3 SERVIDORES ENVIA UMA SOLICITACAO DE ALTERACAO PARA OS 3 ############################################

if(qnt_ok == 3):
	
	port = 8886;
	logCli2.write(datelog + '---->' + 'PREPARANDO PARA ALTERAR NO SERVIDOR: '+ remote_ip + ':' + str(port)+ '\n')
	while (port < 8889): #Loop para iterar a porta enviando a msg para os 3 servidores
		try:
		    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error:
		    print 'Falha ao Criar Socket'
		    sys.exit()
		     
		print 'Socket Criado'

		try:
		    remote_ip = socket.gethostbyname( host )
		 
		except socket.gaierror:
		    #could not resolve
		    print 'Host nao pode ser resolvido... Saindo'
		    sys.exit()
		#Connect to remote server
		s.connect((remote_ip , port))
		 
		print 'Socket Connectado em ' + host + ' no ip ' + remote_ip
		 
		#Envia Mensagem para o Servidor
		message = "altera"
		 
		try :
		    #Indica toda a Sequencia
		    s.sendall(message)
		    logCli2.write(datelog + '---->' + 'ALTERANDO VARIAVEL NO SERVIDOR : '+ remote_ip + ':' + str(port)+ '\n')
		    time.sleep(1) # Variavel usada pra dar um tempo de 1 segundo antes de enviar para o proximo servidor	
		except socket.error:
		    #Caso falhe
		    print 'Falha no Envio'
		    sys.exit()
		port = port + 1

######################## CASO RECEBA UM ABORT DE ALGUN DOS 3 ENVIA UM ABORT DA OPERACAO PARA TODOS ############################################

elif(qnt_ok < 3):

	
	port = 8886;
	logCli2.write(datelog + '---->' + 'NAO FOI POSSIVEL ALTERAR ABORTANDO NO SERVIDOR : '+ remote_ip + ':' + str(port)+ '\n')

	while (port < 8889): #Loop para iterar a porta enviando a msg para os 3 servidores
		try:
		    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error:
		    print 'Falha ao Criar Socket'
		    sys.exit()
		     
		print 'Socket Criado'

		try:
		    remote_ip = socket.gethostbyname( host )
		 
		except socket.gaierror:
		    #could not resolve
		    print 'Host nao pode ser resolvido... Saindo'
		    sys.exit()
		#Connect to remote server
		s.connect((remote_ip , port))
		 
		print 'Socket Connectado em ' + host + ' no ip ' + remote_ip
		 
		#Envia Mensagem para o Servidor
		message = "ABORT"
		 
		try :
		    #Indica toda a Sequencia
		    s.sendall(message)
		    time.sleep(1) # Variavel usada pra dar um tempo de 1 segundo antes de enviar para o proximo servidor	
		except socket.error:
		    #Caso falhe
		    print 'Falha no Envio'
		    sys.exit()
		port = port + 1
		
	
logCli2.close()

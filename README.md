# 2PC
Two-Phase Commit Python

Implementa uma versão simplificado do protocolo 2PC ("Two-Phase Commit") na linguagem Python. Cada servidor mantém um valor de uma variavel chamada de storage_server, onde este valor inicialmente é setado como '0' q significa nunca alterado,  como o objetivo do trabalho é mostrar a consistência de dados, para isso os clientes enviam requisições "commit", para todos os servidores automaticamente, sem a necessidade de escrever a mensagem se todos os servidores responde com o "OK" logo o cliente identifica que todos os servidores enviaram um OK e habilita ao cliente enviar a mensagem alterar, que altera a variavel storage_server de 0 para 1 ou para qualquer valor que esteja no cliente, caso haja tentativa de alterar e dentro destas tentativa a resposta seja um NOK, o cliente ABORTA a tentativa.
Cliente.py
Comando para Executar
$ python cliente.py
O clinte é inicializado automaticamente contem no codigo o ip do host e a porta do primeiro servidor que ele realizara a conexão, pode se utilizar 2 ou mais clientes do mesmo arquivo para testar, ou seja executar 3 arquivos cliente.py


host = '127.0.0.1';
port = 8886;
Os endereços dos três servidores farão parte de um while que incrementa a porta
a cada conexão, assim então abre-se um socket para enviar a mesma  mensagem para cada servidor a porta varia de 8886 ate 8888 totalizando 3 servidores


while (port < 8889): #Loop para iterar a porta enviando a msg para os 3 servidores
#TENTA CRIAR O SOCKET
try:
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
print 'Falha ao Criar Socket'
sys.exit()
Assim entao apos criar o socket o cliente envia a mensagem "commit" para cada servidor, que significa o pedido para alterar a variavel


message = "commit"
try :
#Indica toda a Sequencia da mensagem
s.sendall(message)
time.sleep(1) # Variavel usada pra dar um tempo de 1 segundo antes de                   enviar para o proximo servidor
except socket.error:
#Caso falhe
print 'Falha no Envio'
sys.exit()
print 'Mensagem Enviada com sucesso'
A cada mensagem enviada o cliente aguarda a resposta do servidor, caso a resposta seja um "ok" ele armazena a quantidades de "OK" na variável global
"qnt_ok", e incrementa em 1 a quantidade de OK

#Recebe a resposta
reply = s.recv(1024)
if(reply == 'ok'):
qnt_ok = qnt_ok + 1
print qnt_ok
print reply
port = port + 1
Se o Cliente Receber 3 "ok", ou seja se a "qnt_ok" for  = 3 então o cliente esta apto a alterar a variavel para  storage_server = 1, logo entao o cliente faz o mesmo procedimento explicado acima abre o socket em um loop while, porem agora enviando a mensagem "alterar" para todos os servidores que terão de alterar, a variável igualmente nos servidores replicados.
Caso o cliente receba um NOK de algum dos servidores, este ira enviar a mensagem "ABORT" a todos os servidores, indicando que esta abortando a operação.

Servidor
Para rodar o programa servidor1.py, servidor2.py, servidor3.py   basta executá-lo na linha de comando, escolhemos utilizar 3 servidores iguais ao invés de darmos como entrada a por linha de comando a porta para um mesmo servidor aberto 3 ou mais vezes  como podia ser feito, preferimos entao criar 3 servidores que diferem apenas na porta que utilizam e no arquivo de log que é criado para cada um
Executar
python servidor1.py
python servidor2.py
python servidor3.py

O servidor começa defindo em qual endereço e porta vai aguardar por conexões, assim como o limite de conexões que definimos para escutar no máximo 10.
HOST = '127.0.0.1' # Significa todas as interfaces disponiveis
PORT = 8886 # Porta Arbitraria nao Privilegiada
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(10)

Após a criação do socket o servidor entra em um loop ara aceitar conexões. Se o servidor recebeu uma requisição de alteração então ele verifica a variável. "pode_Alterar" Se ela for verdadeira, então o servidor já deu "OK" para algum outro cliente e deve enviar um "NOK" para a requisição atual e encerrar conexão. Caso contrário, o servidor salva a operação do cliente em operation, altera o valor da variável pode_Alterar para verdadeiro e cria uma thread para atender esse cliente.
while 1:
if (pode_Alterar == True):
conn, addr = s.accept()
conn.send("NOK")
conn.close()
if (pode_Alterar == False):
conn, addr = s.accept()
pode_Alterar == True
start_new_thread(clientthread, (conn,))
Assim a Thread criada aguarda uma resposta ("COMMIT" ou "ABORT") do cliente que solicitou a alteração. Se a resposta do cliente for "COMMIT" então a alteracao na variavel storage_server é realizada e o valor da variável "pode_Alterar "é alterada para falso. Se a resposta for "ABORT" então o servidor simplesmente seta "pode_Alterar" como falso.
def clientthread(conn):
    global pode_Alterar
    #Enviando Mensagem ao Cliente Conectado.
    conn.send('ok') #Somente String
    #Loop Infinito, assim a thread nao termina.
    while True:
         
        #Recebendo do Cliente        
	data = conn.recv(1024)
	if (data == 'commit'):
		logServer1.write(datelog + '---->' + 'OK ENVIADO AO CLIENTE : '+ addr[0] + ':' + str(addr[1])+ '\n')
		pode_Alterar = True
		time.sleep(3)		
		reply = 'commit'
		conn.sendall(reply)
		print pode_Alterar
		print 'entrei aki'
	   	break
	if (data == 'altera'):
		logServer1.write(datelog + '---->' + 'ALTERANDO DADOS PARA O CLIENTE: ' + addr[0] + ':' + str(addr[1]) + '\n')
		pode_Alterar = True
		time.sleep(3)
		storage_server = 1;
		logServer1.write(datelog + '---->' + 'DADO STORAGE MODIFICADO PARA CLIENTE: '+ addr[0] + ':' + str(addr[1]) + '\n' )
		print storage_server
		reply = 'commit'
		print pode_Alterar
		print data
		break
	if (data == 'abort'):
		logServer1.write(datelog + '---->' + 'TENTATIVA DE ALTERAR FALHOU NO CLIENTE :'  + addr[0] + ':' + str(addr[1]) + '\n')
	elif not data:
            	break

Log
logserver1, logserver2, logserver3  logcliente1 , logcliente2
No log esta contido as operações que cada servidor realizou e cada cliente
estas utilizam uma etiqueta de tempo, e indicam cada operacao realizada
com o respectiovo ip e porta do cliente dentro do servidor e no cliente o respectivo servidor e porta que ele esta conectando

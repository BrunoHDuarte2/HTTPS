import socket
import ssl
import re
import base64 
# Config para comunicação com o servidor
HOST = '127.0.0.1' # Host Local, já que está rodando localmente
PORT = 500 # Porta especificada no servidor, se for alterada lá então deve ser alterada aqui.
# Cria a estrutura com as configurações de SSL/TLS, quais cifras serão usadas ...
# Na forma como foi chamado essa função ele vai exigir um certificado válido pelo lado do servidor e o nome do host precisa bater com o do servidor
contextConfig = ssl.create_default_context() 
# Carrega o certificado do servidor para poder validar com quem se está comunicando
# Já que o certificado é autoassinado sem esse comando o programa não roda por segurança
contextConfig.load_verify_locations(cafile="keys/server.crt") 
# Comunicação 
# Socket TCP/IP tentando se conectar com 127.0.0.1:500
with socket.create_connection((HOST, PORT)) as sock:
    # Usa das configurações criadas pelo contextConfig para criar um tunel de comunicacao segura com TLS/SSL
    with contextConfig.wrap_socket(sock, server_hostname=HOST) as ssock:
        # Envia um get simples 
        ssock.sendall(b"GET / HTTP/Gengar\r\nHost: 127.0.0.1\r\n\r\n")
        # Recebe o resultado do get
        headerRecebido = ssock.recv(1024)
        # Mostra o resultado do get 
        #print(f"Dados recebidos: {data.decode()}")
        tamanhoDaImagem = int((re.search("Content-Length:\s*(\d+)",str(headerRecebido.decode())).group(1)))
        imagemRecebida = b""
        while len(imagemRecebida) < tamanhoDaImagem:
            imagemRecebida += ssock.recv(1024)
        imagemDecode = base64.b64decode(imagemRecebida.decode())
        with open('imagemRecebida.png', 'wb') as f:
            f.write(imagemDecode)
        print("Imagem Recebida com sucesso :)")
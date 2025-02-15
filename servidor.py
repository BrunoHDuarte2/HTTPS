import socket
import ssl
import base64
# Configs básicas do servidor
HOST = '127.0.0.1'
PORT = 500
# Estrutura TLS/SSL para criação do tunel de comunicação
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
# Certificado do servidor (autoassinado) e chave privada correspondente ao certificado
context.load_cert_chain(certfile="server.crt", keyfile="server.key")
# Socket criado e estabelecendo configs padrão: ip e porta de comunicação
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Define o ip e a porta
    sock.bind((HOST, PORT))
    sock.listen(5)
    print(f"Servidor HTTPS escutando em {HOST}:{PORT}...")
    # Utiliza do socket e das configurações de TLS/SSL para comunicação segura
    with context.wrap_socket(sock, server_side=True) as ssock:
        # Estabelece comunicação
        conn, addr = ssock.accept()
        with conn:
            print(f"Conexão estabelecida com {addr}")
            data = conn.recv(1024)
            print(f"Dados recebidos: {data.decode()}")
            with open('gengar.png', "rb") as f:
                imagem = base64.b64encode(f.read()).decode('utf8')
            header = (
                f"HTTP/1.1 200 OK\r\n"
                f"Content-Type: image/png\r\n"
                f"Content-Length: {len(imagem)}\r\n"
                f"\r\n"
            )
            # Como não dá pra enviar o pacote da imagem inteira de uma vez, quebra em tamanhos fixos de 1024 para envio
            # Dessa forma se envia vários pacotes e o cliente reconstrói a imagem.
            # ! importante dizer que por conta disso o Content-Lenght se torna mt importante :)
            conn.sendall(header.encode())
            chunk = 1024  
            for i in range(0, len(imagem), chunk):
                conn.sendall(imagem[i:i+chunk].encode())
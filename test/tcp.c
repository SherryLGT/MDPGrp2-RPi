#include <stdio.h>
#include <sys/socket.h>
#include <string.h>    //strlen
#include <arpa/inet.h> //inet_addr
#include <unistd.h>    //write
#include <pthread.h>   // thread

int CLIENT_SOCK, socket_desc, c, read_size;
struct sockaddr_in server, client;

int tcpConnection() {
    
    //Create socket
    socket_desc = socket(AF_INET , SOCK_STREAM , 0);
    if (socket_desc == -1)
    {
        printf("Unable to create socket");
    }
    puts("Socket created");
    
    //Prepare the sockaddr_in structure
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = INADDR_ANY;
    server.sin_port = htons( 1010 );
     
    //Bind
    if( bind(socket_desc,(struct sockaddr *)&server , sizeof(server)) < 0)
    {
        //print the error message
        perror("Error: Bind failed");
        return 1;
    }
    puts("Bind completed");
    
    //Listen
    listen(socket_desc , 3);
    
    //Accept and incoming connection
    puts("Waiting for incoming connections...");
    c = sizeof(struct sockaddr_in);
    
    //Accept connection from an incoming client
    CLIENT_SOCK = accept(socket_desc, (struct sockaddr *)&client, (socklen_t*)&c);
    if (CLIENT_SOCK < 0)
    {
        perror("Accept failed");
        return 1;
    }
    puts("Connection accepted");

    if(read_size == 0)
    {
        puts("Client disconnected");
        fflush(stdout);
    }
    else if(read_size == -1)
    {
        perror("Receiving failed");
    }
    
    return 0;
}

void tcpRead() {

    char client_message[2001];
    client_message[2000] = '\0';

    //Receive a message from client
    while( (read_size = recv(CLIENT_SOCK , client_message , 2000 , 0)) > 0 )
    {
        //Print client message
        puts(client_message);
    }
}

void tcpWrite(char message[]) {

    //Send the message back to client
    //write(client_sock , client_message , strlen(client_message));
    write(CLIENT_SOCK , message , strlen(message));
}

void main(int argc , char *argv[]){

    pthread_t tcpReadThread, tcpWriteThread;
    int conStatus;

    conStatus = tcpConnection();
    pthread_create(&tcpReadThread, NULL, tcpRead(), NULL);
    pthread_create(&tcpWriteThread, NULL, tcpRead(), NULL);
}
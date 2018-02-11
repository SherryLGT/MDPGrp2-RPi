#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

main()
{
	pthread_t tcpConThread, tcpReadThread;
	int tcpConret, tcpReadret;

	/* Create threads */
	tcpConret = pthread_create( &tcpConThread, NULL, tcpcon() , NULL);
	tcpReadret = pthread_create( &tcpReadThread, NULL, tcpread() , NULL);

	/* Wait for threads to finish */
	pthread_join(tcpConret, NULL);
	pthread_join(tcpReadret, NULL);
}

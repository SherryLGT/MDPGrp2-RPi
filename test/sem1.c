#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>

int g_var1 = 0;	// global variable
sem_t semM;

void *inc_gv()
{
	int i,j;

	for (i=0;i<10;i++)
	{
		g_var1++; // increment the global variable
		sem_wait(&semM);
		for (j=0; j<5000000;j++); // delay loop
		printf(" %d",g_var1); // print the value
		fflush(stdout);
		sem_post(&semM);
	}
}

main()
{
	sem_init(&semM,0,1);

	pthread_t TA, TB;
	int TAret, TBret;

	TAret = pthread_create(&TA, NULL, inc_gv, NULL);
	TBret = pthread_create(&TB, NULL, inc_gv, NULL);

	pthread_join(TAret, NULL);
	pthread_join(TBret, NULL);

	printf("\n pthread2 completed \n");
}

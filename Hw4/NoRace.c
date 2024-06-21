#include <stdio.h>
#include <pthread.h>

pthread_mutex_t mutex1 = PTHREAD_MUTEX_INITIALIZER;
#define LOOPS 100000
int Money = 100000;

void *Deposit()
{
  for (int i=0; i<LOOPS; i++) {
    pthread_mutex_lock( &mutex1 );
    Money = Money + 10;
    pthread_mutex_unlock( &mutex1 );
  }
  return NULL;
}

void *Withdraw()
{
  for (int i=0; i<LOOPS; i++) {
    pthread_mutex_lock( &mutex1 );
    Money = Money - 10;
    pthread_mutex_unlock( &mutex1 );
  }
  return NULL;
}


int main() 
{
  pthread_t thread1, thread2;

  pthread_create(&thread1, NULL, Deposit, NULL);
  pthread_create(&thread2, NULL, Withdraw, NULL);

  pthread_join( thread1, NULL);
  pthread_join( thread2, NULL);
  printf("Money=%d\n", Money);
}
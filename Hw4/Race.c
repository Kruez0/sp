#include <stdio.h>
#include <pthread.h>

#define LOOPS 100000000
int Money = 100000;

void *Deposit()
{
  for (int i=0; i<LOOPS; i++) {
    Money = Money + 10;
  }
  return NULL;
}

void *Withdraw()
{
  for (int i=0; i<LOOPS; i++) {
    Money = Money - 10;
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
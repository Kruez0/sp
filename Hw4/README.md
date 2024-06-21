# Multi-Threading by Producing Race Conditions
 > Done by myself and looking at laoshi's code and VERY much understand what im doing!
## Race Condition   

> Race condition means that the software behavior are related to timing of events for example in this program we use thread execution. Due to the lack of synchronization, the threads can interfere with each other or accessed simultaneously by multiple threads, leading to unpredictable and incorrect results. 

Race Program Explanation :     

    I have 100000 NTD and the program will deposit and withdraw 10 yuan at a time. The output of the program is as below:

```
PS C:\CSIE\SEM 4\System Programming\sp\Hw4> gcc Race.c -o Race
PS C:\CSIE\SEM 4\System Programming\sp\Hw4> ./Race
Money=614757010
```
The money we had , 100000, was updated either into 100010 (Deposited) or 99990 (Withdrawed). But because of the race condition, it is not updated correctly( either withdraw again or deposit again or neither). That is why after 1000000 loops the result is weird, 614757010.

## No Race Condition

No race means that the program is consistent regardless of the timing of the thread.   

No Race Program Explanation :   

The program is the same. I have 100000 NTD and the program will deposit and withdraw 10 yuan at a time. The output of the program is as below:

```
PS C:\CSIE\SEM 4\System Programming\sp\Hw4> gcc NoRace.c -o NoRace
PS C:\CSIE\SEM 4\System Programming\sp\Hw4> ./NoRace
Money=100000
```
The result is as above because the steps are consistent unlike race. So we had 100000 and then we begin thread 1 which adds 10 to it so 100010 and then withdraw -10 and so it becomes 100000 again. Do it for 10000000 times or billion times, the result will also be 100000 yuan because it is consistent.
#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    //let computer know that dollar is a float
    float dollar;
    do
    {
        dollar = get_float("Change needed:");
    }
    while (dollar <= 0);

    //convert dollars to cents
    int cents = round(dollar * 100);
    int coins = 0;
    //while loop for quarters
    while (cents >= 25)
    {
        cents -= 25; 
        coins++;
    }
    // while loop for dimes
    while (cents >= 10)
    {
        cents -= 10; 
        coins++;
    }
    // while loop for nickels
    while (cents >= 5)
    {
        cents -= 5;
        coins++;
    }
    // while loop for pennies
    while (cents >= 1)
    {
        cents -= 1; 
        coins++;
    }

    // print the number of coins needed for change
    printf("Coins needed: %i\n", coins);
}
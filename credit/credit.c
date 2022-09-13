#include <stdio.h>
#include <cs50.h>

int main(void)
{
    long card;
    do
    {
        card = get_long("Credit card number:");
    }
    while(card < 13 || card >16);
}

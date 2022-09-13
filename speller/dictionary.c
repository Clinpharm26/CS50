// Implements a dictionary's functionality

#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <strings.h>
#include <ctype.h>
#include <cs50.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 100000;
//initialise positive hash value
unsigned int hash_value;
//initialise hash table word count
unsigned int word_count;

// Hash table
node *table[N];


// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    //hash the word
    hash_value = hash(word);
    //access the linked list of the hash table
    node *cursor = table[hash_value];
    //iterate through the linked list
    while (cursor != NULL)
    {
        //if the word is a match
        if (strcasecmp(word, cursor -> word) == 0)
        {
            return true;
        }
        //move cursor to the next word
        cursor = cursor -> next;
    }
    return false;
}

// Hashes word to a number (credit: DJB2)
unsigned int hash(const char *word)
{
    // TODO

    unsigned long hash = 5381;
    int c;

    while ((c = toupper(*word++)))
    {
        hash = ((hash << 5) + hash) + c; /* hash * 33 + c */
    }

    return hash % N;

    return 0;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    //open dictionary file
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        printf("Unable to open %s\n", dictionary);
        return false;
    }
    //assign space for words
    char word[LENGTH + 1];
    //read strings from file
    while (fscanf(file, "%s", word) != EOF)
    {
        //create a new node for each word

        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }
        //pointer to the next node and word
        strcpy(n -> word, word);
        //hash the word & obtain the hash value
        hash_value = hash(word);
        //set pointer
        n -> next = table[hash_value];
        //set head to new pointer
        table[hash_value] = n;
        //increment the word count
        word_count++;
    }

    //close the file
    fclose(file);

    return true;
}

// Returns number of words in dictionary
unsigned int size(void)
{
    // TODO
    return word_count;

}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    //iterate through each node in each linked list of the hash table
    for (int i = 0; i < N; i++)
    {
        //set a pointer called cursor
        node *cursor = table[i];

        //if cursor is not NULL, free memory
        while (cursor != NULL)
        {
            //create a temp pointer
            node *temp = cursor;
            //now can move cursor to the next node
            cursor = cursor -> next;
            //now can free temp
            free(temp);
        }
        //if the cursor is NULL
        if (i == N - 1 && cursor == NULL)
        {
            return true;
        }
    }
    return false;
}

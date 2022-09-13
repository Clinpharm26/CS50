#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

#define BLOCKSIZE 512



typedef uint8_t BYTE;

//Pseudocode
//open memory card
//Repeat something... until end of card
//Read 512bytes into a buffer
//If start of new JPEG, do something...
//Else...do something else
//Else
//If already found JPEG, do something...
//Close any remaining files
//if used malloc, free memory

int main(int argc, char *argv[])
{
    char *input_file;
    FILE *file_ptr;

    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }
    else
    {
        input_file = argv[1];
        file_ptr = fopen(input_file, "r");
    }

    if (file_ptr == NULL)
    {
        printf("Error: Cannot open %s\n", input_file);
        return 2;
    }


    //initialise variables
    BYTE buffer[512];
    int count = 0;
    FILE *img_ptr = NULL;
    char filename[8]; // 000.jpg\0 = 8 char

    //Loop through the memory card

    while (fread(&buffer, sizeof(BYTE), BLOCKSIZE, file_ptr))
    {
        //if the start of a new JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            //if its not the 1st JPEG file, close the previous file
            if (!(count == 0))
            {
                fclose(img_ptr);
            }

            //initialise the new file
            sprintf(filename, "%03i.jpg", count);
            img_ptr = fopen(filename, "w");
            count++;
        }
        //if JPEG has been found, write to a new file
        if (!(count == 0))
        {
            fwrite(buffer, sizeof(buffer), 1, img_ptr);
        }
    }

    //close the files
    fclose(file_ptr);
    fclose(img_ptr);

    return 0;


}
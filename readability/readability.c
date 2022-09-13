# include <cs50.h>
# include <stdio.h>
# include <ctype.h>
# include <math.h>
# include <string.h>

int main(void)
{
    // get text from user
    string text = get_string("Text: ");

    //initialise letters, words and sentences

    int letters = 0;
    int words = 1;
    int sentences = 0;

    //count letters

    for (int i = 0, n = strlen(text); i < n; i++)
     while (text[i] != '\0')
      {
         if (isalpha(text[i++]))
          {
              letters++;
          }
      }
    {
        printf("Letters: %i\n", letters);
    }

    //count words

    for(int i = 0, n = strlen(text); i < n; i++)
    {

        if ((text[i] == 0 && text[i] != ' ') || (text[i] != n-1 && text[i] == ' ' && text[i+1] != ' ' ))
        {
          words++;
         }
    }
    {
        printf("Words: %i\n", words);
    }

    //count sentences

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences++;
        }
    }
    {
        printf("Sentences: %i\n", sentences);
    }

    //calculate average letters and sentences and cast int to float
    float L = (letters / (float) words) * 100;
    float S = (sentences / (float) words) * 100;

// calculate coleman liau index

    int index = round(0.0588 * L - 0.296 * S - 15.8);

    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 1 && index < 16)
    {
        printf("Grade %i\n", index);
    }
    else
    {
        printf("Grade 16+\n");
    }

}

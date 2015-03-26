#include <stdio.h>
#include <string.h>

int main(int argc, char* argv[])
{
  //default lennyface
  if (argc < 2)
    printf("( ͡° ͜ʖ ͡°)\n");
  else
  {
    //example for adding more option arguments
    if (strcmp(argv[1],"-o") == 0)
    {
      printf("( ͡o ͜ʖ ͡o)\n");
    }
    //or just format lennyface with your character here
    else if (strlen(argv[1]) == 1)
    {
      printf("( ͡%c ͜ʖ%c ͡)\n",argv[1][0],argv[1][0]);
    }
  }
  return 0;
}

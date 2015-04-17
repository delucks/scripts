#include <stdio.h>
#include <string.h>

//because, that's why
int main(int argc, char* argv[])
{
  //default lennyface
  if (argc < 2)
    printf("( ͡° ͜ʖ ͡°)\n");
  else
  {
    //specific ones
    if (strcmp(argv[1],"-t") == 0)
    {
      printf("(╯°□°）╯︵ ┻━┻\n");
    }
    else if (strcmp(argv[1],"-m") == 0)
    {
      printf("⊂(・(ェ)・)⊃\n");
    }
    else if (strcmp(argv[1],"-s") == 0)
    {
      printf("¯\\_(ツ)_/¯\n");
    }
    else if (strcmp(argv[1],"-d") == 0)
    {
      printf("ಠ_ಠ\n");
    }
    else if (strcmp(argv[1],"-T") == 0)
    {
      printf("(ノಠ益ಠ)ノ彡┻━┻\n");
    }
    //or just format lennyface with your character here
    else if (strlen(argv[1]) == 1)
    {
      printf("( ͡%c ͜ʖ ͡%c)\n",argv[1][0],argv[1][0]);
    }
    else
    {
      printf("( ͡%s ͜ʖ ͡%s)\n",argv[1],argv[1]);
    }
  }
  return 0;
}

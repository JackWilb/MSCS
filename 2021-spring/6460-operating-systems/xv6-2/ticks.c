#include "types.h"
#include "stat.h"
#include "user.h"

int
main(int argc , char **argv)
{

  if( argc != 2 ) {
    printf(1, "Usage: ticks <number of timer interupts to wait>");
    exit();
  }

  int initialUptime = uptime();
  int uptimeOffset = atoi(argv[1]);

  while (uptime() < initialUptime + uptimeOffset) {
    // busy-loop
  }

  int ticks = getticks();

  printf(1, "%d\n", ticks);
  exit();
}

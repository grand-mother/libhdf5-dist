#include <stdio.h>
#include <stdlib.h>

#include "hdf5.h"


int main()
{
        unsigned majnum, minnum, relnum;
        if (H5get_libversion(&majnum, &minnum, &relnum) < 0)
                exit(EXIT_FAILURE);

        printf("using libhdf5 version %u.%u.%u\n", majnum, minnum, relnum);

        exit(EXIT_SUCCESS);
}

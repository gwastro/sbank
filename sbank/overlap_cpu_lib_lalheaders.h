#include <fftw3.h>

 typedef struct tagCOMPLEX8FFTPlan
 {
   int32_t       sign; /**< sign in transform exponential, -1 for forward, +1 for reverse */
   uint32_t      size; /**< length of the complex data vector for this plan */
   fftwf_plan plan; /**< the FFTW plan */
 } COMPLEX8FFTPlan;

/* struct COMPLEX8FFTPlan; */

 typedef struct tagCOMPLEX8Vector {
     uint32_t length; /**< Number of elements in array. */
     float complex *data; /**< Pointer to the data array. */
 } COMPLEX8Vector;

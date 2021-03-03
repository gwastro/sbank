#include <fftw3.h>

 typedef struct tagCOMPLEX8FFTPlan
 {
   int32_t       sign; /**< sign in transform exponential, -1 for forward, +1 for reverse */
   uint32_t      size; /**< length of the complex data vector for this plan */
   fftwf_plan plan; /**< the FFTW plan */
 } COMPLEX8FFTPlan;

 typedef struct tagCOMPLEX8Vector {
     uint32_t length; /**< Number of elements in array. */
     float complex *data; /**< Pointer to the data array. */
 } COMPLEX8Vector;


 /** XLAL error numbers and return values. */
 enum XLALErrorValue {
     XLAL_SUCCESS = 0,      /**< Success return value (not an error number) */
     XLAL_FAILURE = -1,     /**< Failure return value (not an error number) */
 
     /* these are standard error numbers */
     XLAL_ENOENT = 2,        /**< No such file or directory */
     XLAL_EIO = 5,           /**< I/O error */
     XLAL_ENOMEM = 12,       /**< Memory allocation error */
     XLAL_EFAULT = 14,       /**< Invalid pointer */
     XLAL_EINVAL = 22,       /**< Invalid argument */
     XLAL_EDOM = 33,         /**< Input domain error */
     XLAL_ERANGE = 34,       /**< Output range error */
     XLAL_ENOSYS = 38,       /**< Function not implemented */
 
     /* extended error numbers start at 128 ...
 *       * should be beyond normal errnos */
 
     /* these are common errors for XLAL functions */
     XLAL_EFAILED = 128,     /**< Generic failure */
     XLAL_EBADLEN = 129,     /**< Inconsistent or invalid length */
     XLAL_ESIZE = 130,       /**< Wrong size */
     XLAL_EDIMS = 131,       /**< Wrong dimensions */
     XLAL_ETYPE = 132,       /**< Wrong or unknown type */
     XLAL_ETIME = 133,       /**< Invalid time */
     XLAL_EFREQ = 134,       /**< Invalid freqency */
     XLAL_EUNIT = 135,       /**< Invalid units */
     XLAL_ENAME = 136,       /**< Wrong name */
     XLAL_EDATA = 137,       /**< Invalid data */
 
     /* user-defined errors */
     XLAL_EUSR0 = 200,       /**< User-defined error 0 */
     XLAL_EUSR1 = 201,       /**< User-defined error 1 */
     XLAL_EUSR2 = 202,       /**< User-defined error 2 */
     XLAL_EUSR3 = 203,       /**< User-defined error 3 */
     XLAL_EUSR4 = 204,       /**< User-defined error 4 */
     XLAL_EUSR5 = 205,       /**< User-defined error 5 */
     XLAL_EUSR6 = 206,       /**< User-defined error 6 */
     XLAL_EUSR7 = 207,       /**< User-defined error 7 */
     XLAL_EUSR8 = 208,       /**< User-defined error 8 */
     XLAL_EUSR9 = 209,       /**< User-defined error 9 */
 
     /* external or internal errors */
     XLAL_ESYS = 254,        /**< System error */
     XLAL_EERR = 255,        /**< Internal error */
 
     /* specific mathematical and numerical errors start at 256 */
 
     /* IEEE floating point errors */
     XLAL_EFPINVAL = 256,      /**< IEEE Invalid floating point operation, eg sqrt(-1), 0/0 */
     XLAL_EFPDIV0 = 257,       /**< IEEE Division by zero floating point error */
     XLAL_EFPOVRFLW = 258,     /**< IEEE Floating point overflow error */
     XLAL_EFPUNDFLW = 259,     /**< IEEE Floating point underflow error */
     XLAL_EFPINEXCT = 260,     /**< IEEE Floating point inexact error */
 
     /* numerical algorithm errors */
     XLAL_EMAXITER = 261,      /**< Exceeded maximum number of iterations */
     XLAL_EDIVERGE = 262,      /**< Series is diverging */
     XLAL_ESING = 263,         /**< Apparent singularity detected */
     XLAL_ETOL = 264,          /**< Failed to reach specified tolerance */
     XLAL_ELOSS = 265,         /**< Loss of accuracy */
 
     /* failure from within a function call: "or" error number with this */
     XLAL_EFUNC = 1024         /**< Internal function call failed bit: "or" this with existing error number */
 };


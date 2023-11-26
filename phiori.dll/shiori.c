#include "emergency.h"
#include "phiori.h"
#include "shiori.h"
#include <stdlib.h>
#include <Windows.h>

int IS_LOADED;
int IS_ERROR;
char *ERROR_MESSAGE;
char *ERROR_TRACEBACK;
int SHOW_ERROR;

BOOL load(HGLOBAL h, long len) {
    int result = 0;
    result |= LOAD_Emergency(h, len);
    result |= LOAD(h, len);
    GlobalFree(h);
    return result;
}

BOOL unload(void) {
    int result = 0;
    result |= UNLOAD_Emergency();
    if (!IS_ERROR)
        result |= UNLOAD();
    return result;
}

HGLOBAL request(HGLOBAL h, long *len) {
    void *result = NULL;
    HGLOBAL gResult = NULL;
    if (!IS_ERROR)
        result = REQUEST(h, len);
    if (result == NULL)
        result = REQUEST_Emergency(h, len);
    GlobalFree(h);
    if (result) {
        gResult = GlobalAlloc(GMEM_FIXED, *len + 1);
        if (gResult)
            memcpy(gResult, result, *len + 1);
        free(result);
    }
    return gResult;
}

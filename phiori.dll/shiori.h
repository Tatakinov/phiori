#ifndef _SHIORI
#define _SHIORI 1

__declspec(dllexport) int __cdecl load(void *h, long len);
__declspec(dllexport) int __cdecl unload(void);
__declspec(dllexport) void *__cdecl request(void *h, long *len);

extern int IS_LOADED;
extern int IS_ERROR;
extern char *ERROR_MESSAGE;
extern char *ERROR_TRACEBACK;
extern int SHOW_ERROR;

#endif

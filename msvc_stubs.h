#ifndef MSVC_STUBS_H
#define MSVC_STUBS_H

/* integer types */
#define __int8   signed char
#define __int16  short
#define __int32  int
#define __int64  long long

/* calling conventions */
#define __cdecl
#define __stdcall
#define __fastcall
#define __thiscall
#define __vectorcall
#define __ptr32
#define __ptr64
#define __w64

/* inline keywords */
#define __inline inline
#define __forceinline inline

/* declspec/attributes */
#define __declspec(x) __attribute__((unused))
#define __attribute__(x) __attribute__((unused))
#define __unaligned __attribute__((unused))
#define __restrict __attribute__((unused))
#define __restrict__ __attribute__((unused))
#define __declspec_selectany __attribute__((unused))

/* intrinsics */
#define __assume(x)
#define __noop(...) 
#define __debugbreak()

/* analysis annotations */
#define __analysis_assume(x) __attribute__((unused))
#define __analysis_noreturn(x) __attribute__((unused))

/* SEH */
#define __try
#define __except(x)
#define __finally
#define __leave

/* varargs helpers */
#define __va_start(ap, x)
#define __crt_va_start(ap, x)
#define __va_arg(ap, t) ((t)0)
#define __va_end(ap)

/* misc intrinsics */
#define _AddressOfReturnAddress() ((void*)0)
#define _alloca(x) ((void*)0)
#define _alloca_dbg(x,y) ((void*)0)
#define __uuidof(x) 0

/* windows macros */
#define CALLBACK
#define WINAPI
#define APIENTRY

/* SAL annotations mapped to safe attributes */
#define __in __attribute__((unused))
#define __out __attribute__((unused))
#define __inout __attribute__((unused))
#define __in_opt __attribute__((unused))
#define __out_opt __attribute__((unused))
#define __success(x) __attribute__((unused))

/* misc helpers */
#define FIELD_OFFSET(type, field) ((size_t)&(((type *)0)->field))
#define UNREFERENCED_PARAMETER(x) (void)(x)

/* NULL */
#ifndef NULL
#define NULL ((void*)0)
#endif

#endif /* MSVC_STUBS_H */

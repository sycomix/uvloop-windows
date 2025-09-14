#ifndef UVLOOP_COMPAT_WIN_H
#define UVLOOP_COMPAT_WIN_H

#include <errno.h>
#include <stddef.h>
#include <signal.h>
#include "Python.h"
#include "uv.h"

#ifndef EWOULDBLOCK
#define EWOULDBLOCK EAGAIN
#endif

#define PLATFORM_IS_APPLE 0
#define PLATFORM_IS_LINUX 0

#define EPOLL_CTL_DEL 2
struct epoll_event {};
int epoll_ctl(int epfd, int op, int fd, struct epoll_event *event) {
    return 0;
};

// Windows doesn't have Unix domain sockets, so we provide a dummy implementation
struct sockaddr_un {
    unsigned short sun_family;
    char sun_path[108];  // UNIX_PATH_MAX
};

PyObject *
MakeUnixSockPyAddr(struct sockaddr_un *addr)
{
    PyErr_SetString(
        PyExc_NotImplementedError, "Unix domain sockets are not supported on Windows");
    return NULL;
}

#if PY_VERSION_HEX < 0x03070100

PyObject * Context_CopyCurrent(void) {
    return (PyObject *)PyContext_CopyCurrent();
};

int Context_Enter(PyObject *ctx) {
    return PyContext_Enter((PyContext *)ctx);
}

int Context_Exit(PyObject *ctx) {
    return PyContext_Exit((PyContext *)ctx);
}

#else

PyObject * Context_CopyCurrent(void) {
    return PyContext_CopyCurrent();
};

int Context_Enter(PyObject *ctx) {
    return PyContext_Enter(ctx);
}

int Context_Exit(PyObject *ctx) {
    return PyContext_Exit(ctx);
}

#endif

/* inlined from cpython/Modules/signalmodule.c
 * https://github.com/python/cpython/blob/v3.13.0a6/Modules/signalmodule.c#L1931-L1951
 * private _Py_RestoreSignals has been moved to CPython internals in Python 3.13
 * https://github.com/python/cpython/pull/106400 */

void
_Py_RestoreSignals(void)
{
#ifdef SIGPIPE
    PyOS_setsig(SIGPIPE, SIG_DFL);
#endif
#ifdef SIGXFZ
    PyOS_setsig(SIGXFZ, SIG_DFL);
#endif
#ifdef SIGXFSZ
    PyOS_setsig(SIGXFSZ, SIG_DFL);
#endif
}

#endif // UVLOOP_COMPAT_WIN_H
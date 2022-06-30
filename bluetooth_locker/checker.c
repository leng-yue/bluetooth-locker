#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <unistd.h>
#include <sys/socket.h>
#include <bluetooth/bluetooth.h>
#include <bluetooth/hci.h>
#include <bluetooth/hci_lib.h>

static PyObject *check(PyObject *self, PyObject *args)
{
    const char *address;

    if (!PyArg_ParseTuple(args, "s", &address))
        return NULL;

    int dev_id = hci_get_route(NULL);
    int sock = hci_open_dev(dev_id);
    if (dev_id < 0 || sock < 0)
    {
        return PyLong_FromLong(-2);
    }

    bdaddr_t baddr;
    char name[248] = {0};
    str2ba(address, &baddr);
    // Implement l2ping will be better
    int result = hci_read_remote_name(sock, &baddr, sizeof(name), name, 0);
    int current_time = time(NULL);
    while (result < 0 && time(NULL) - current_time < 5) {
        result = hci_read_remote_name(sock, &baddr, sizeof(name), name, 0);
        sleep(1);
    }
    close(sock);
    return PyLong_FromLong(result);
}


static PyMethodDef CheckerMethods[] = {
    {"check",  check, METH_VARARGS,
     "Check if bluetooth address is connectable."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef checkermodule = {
    PyModuleDef_HEAD_INIT,
    "checker",   /* name of module */
    NULL, /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    CheckerMethods
};

PyMODINIT_FUNC
PyInit_checker(void)
{
    return PyModule_Create(&checkermodule);
}

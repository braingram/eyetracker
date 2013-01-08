cimport numpy


# faster : 0.024
def calculate_O_and_M(numpy.ndarray[numpy.float_t, ndim=2] O,
        numpy.ndarray[numpy.float_t, ndim=2] M,
        numpy.ndarray[numpy.int_t, ndim=2] px,
        numpy.ndarray[numpy.int_t, ndim=2] py,
        numpy.ndarray[numpy.int_t, ndim=2] nx,
        numpy.ndarray[numpy.int_t, ndim=2] ny,
        numpy.ndarray[numpy.float_t, ndim=2] mag):
    cdef int rows = O.shape[0]
    cdef int cols = O.shape[1]
    cdef int r
    cdef int c
    cdef int xp
    cdef int xn
    cdef int yp
    cdef int yn
    cdef int cm = cols - 1
    cdef int rm = rows - 1
    for r in range(rows):
        for c in range(cols):
            xp = px[r, c]
            yp = py[r, c]
            xn = nx[r, c]
            yn = ny[r, c]
            if (xp < 0) or (xp > cm) or (yp < 0) or (yp > rm) or \
                    (xn < 0) or (xn > cm) or (yn < 0) or (yn > rm):
                continue

            O[yp, xp] += 1
            O[yn, xn] -= 1
            M[yp, xp] += mag[r, c]
            M[yn, xn] -= mag[r, c]

            #if (px[r, c] < 0) or (px[r, c] > (cols - 1)) or \
            #        (py[r, c] < 0) or (py[r, c] > (rows - 1)) or \
            #        (nx[r, c] < 0) or (nx[r, c] > (cols - 1)) or \
            #        (ny[r, c] < 0) or (ny[r, c] > (rows - 1)):
            #    continue
            #O[py[r, c], px[r, c]] += 1
            #O[ny[r, c], nx[r, c]] -= 1
            #M[py[r, c], px[r, c]] += mag[r, c]
            #M[ny[r, c], nx[r, c]] -= mag[r, c]
    return O, M


# slower: 0.045
def calculate_O_and_M_masked(numpy.ndarray[numpy.float_t, ndim=2] O,
        numpy.ndarray[numpy.float_t, ndim=2] M,
        numpy.ndarray[numpy.int_t, ndim=1] px,
        numpy.ndarray[numpy.int_t, ndim=1] py,
        numpy.ndarray[numpy.int_t, ndim=1] nx,
        numpy.ndarray[numpy.int_t, ndim=1] ny,
        numpy.ndarray[numpy.float_t, ndim=1] mag):
    cdef int N = px.shape[0]
    cdef int rows = O.shape[0]
    cdef int cols = O.shape[1]
    for i in range(N):
        if (px[i] < 0) | (px[i] > (cols - 1)) | \
                (py[i] < 0) | (py[i] > (rows - 1)) | \
                (nx[i] < 0) | (nx[i] > (cols - 1)) | \
                (ny[i] < 0) | (ny[i] > (rows - 1)):
            continue
        O[py[i], px[i]] += 1
        O[ny[i], nx[i]] -= 1

        M[py[i], px[i]] += mag[i]
        M[ny[i], nx[i]] -= mag[i]
    return O, M

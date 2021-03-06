#!/usr/bin/env python
# -*- coding: utf-8 -*-
import itertools
from ImageProcessingBackend import *
import scipy
from scipy.signal import sepfir2d, convolve2d
from stopwatch import clockit
import numpy


class VanillaBackend(ImageProcessingBackend):

    #@clockit : 0.0007
    def sobel3x3(self, im, **kwargs):
        return self.sobel3x3_separable(im)

    def sobel3x3_separable(self, image, **kwargs):

        sobel_c = array([-1., 0., 1.])
        sobel_r = array([1., 2., 1.])

        imgx = self.separable_convolution2d(image, sobel_c, sobel_r)
        imgy = self.separable_convolution2d(image, sobel_r, sobel_c)

        mag = sqrt(imgx ** 2 + imgy ** 2) + 1e-16

        return (mag, imgx, imgy)

    def separable_convolution2d(self, im, row, col, **kwargs):
        return sepfir2d(im, row, col)

    # borrowed with some translation from Peter Kovesi's fastradial.m
    #@clockit : 1.3
    # clocked with lprun
    #   - looping with mask : 1.8
    #   - histogram and mask : 0.25 seconds
    def fast_radial_transform(self, image, radii, alpha, **kwargs):

        gaussian_kernel_cheat = 1.

        (rows, cols) = image.shape

        use_cached_sobel = False
        cached_mag = None
        cached_x = None
        cached_y = None
        if 'cached_sobel' in kwargs:
            (cached_mag, cached_x, cached_y) = kwargs['cached_sobel']
            (sobel_rows, sobel_cols) = cached_sobel_mag.shape

            if sobel_rows == rows or sobel_cols == cols:
                use_cached_sobel = True

        if use_cached_sobel:
            mag = cached_mag
            imgx = cached_x
            imgy = cached_y
        else:
            (mag, imgx, imgy) = self.sobel3x3(image)

        #print "SM:", mag.shape, mag.max(), mag.min()
        #print "SX:", imgx.shape, imgx.max(), imgx.min()
        #print "SY:", imgy.shape, imgy.max(), imgy.min()

        # Normalise gradient values so that [imgx imgy] form unit
        # direction vectors.
        imgx = imgx / mag
        imgy = imgy / mag

        (y, x) = mgrid[0:rows, 0:cols]  # meshgrid(1:cols, 1:rows);

        S = zeros_like(image)

        for r in range(0, len(radii)):

            n = radii[r]

            M = zeros_like(image)
            O = zeros_like(image)
            F = zeros_like(image)

            # Coordinates of 'positively' and 'negatively' affected pixels
            posx = x + n * imgx
            posy = y + n * imgy

            negx = x - n * imgx
            negy = y - n * imgy

            # Clamp Orientation projection matrix values to a maximum of
            # +/-kappa,  but first set the normalization parameter kappa to the
            # values suggested by Loy and Zelinski
            kappa = 9.9
            if n == 1:
                kappa = 8

            posx = posx.round().astype(int)
            posy = posy.round().astype(int)
            negx = negx.round().astype(int)
            negy = negy.round().astype(int)

            # Clamp coordinate values to range [1 rows 1 cols]
            #posx[where(posx < 0)] = 0
            #posx[where(posx > cols - 1)] = cols - 1
            #posy[where(posy < 0)] = 0
            #posy[where(posy > rows - 1)] = rows - 1

            #negx[where(negx < 0)] = 0
            #negx[where(negx > cols - 1)] = cols - 1
            #negy[where(negy < 0)] = 0
            #negy[where(negy > rows - 1)] = rows - 1

            #for r in range(0, rows):
            #    for c in range(0, cols):
            #        O[posy[r, c], posx[r, c]] += 1
            #        O[negy[r, c], negx[r, c]] -= 1
            #        M[posy[r, c], posx[r, c]] += mag[r, c]
            #        M[negy[r, c], negx[r, c]] -= mag[r, c]
            mask = ~((posx < 0) | (posx > (cols - 1)) | (posy < 0) | \
                    (posy > (rows - 1)) | (negx < 0) | (negx > (cols - 1)) | \
                    (negy < 0) | (negy > (rows - 1)))
            #pm = ((posx > -1) & (posx < cols) & (posy > -1) & (posy < rows))
            #nm = ((negx > -1) & (negx < cols) & (negy > -1) & (negy < rows))
            # DOES NOT WORK WITH REPEATS
            #O[posy[mask].flatten(), posx[mask].flatten()] += 1
            #O[negy[mask].flatten(), negx[mask].flatten()] -= 1
            #M[posy[mask].flatten(), posx[mask].flatten()] += \
            #        mag[posy[mask].flatten(), posx[mask].flatten()]
            #M[negy[mask].flatten(), negx[mask].flatten()] -= \
            #        mag[negy[mask].flatten(), negx[mask].flatten()]
            # 1.8 seconds
            #for (px, py, nx, ny, m) in itertools.izip( \
            #        posx[mask].flat, posy[mask].flat, \
            #        negx[mask].flat, negy[mask].flat, \
            #        mag[mask].flat):
            #    # 15% of time
            #    O[py, px] += 1
            #    # 15% of time
            #    O[ny, nx] -= 1
            #    # 11% of time
            #    M[py, px] += m
            #    # 11% of time
            #    M[ny, nx] -= m
            # 22%
            pH, _, _ = numpy.histogram2d(posy[mask], posx[mask], posy.shape)
            # 22%
            pM, _, _ = numpy.histogram2d(posy[mask], posx[mask], posy.shape,
                    weights=mag[mask])
            # 22%
            nH, _, _ = numpy.histogram2d(negy[mask], negx[mask], negy.shape)
            # 22%
            nM, _, _ = numpy.histogram2d(negy[mask], negx[mask], negy.shape,
                    weights=mag[mask])
            O = pH - nH
            M = pM - nM

            #MM = zeros_like(image)
            #OO = zeros_like(image)
            # 1.3 seconds?
            #for (px, py, nx, ny, m) in itertools.izip( \
            #        posx.flat, posy.flat, negx.flat, negy.flat, \
            #        mag.flat):
            #    # 38% of time !!!!
            #    if px < 0 or px > (cols - 1) or py < 0 or py > (rows - 1) \
            #        or nx < 0 or nx > (cols - 1) or ny < 0 or ny > (rows - 1):
            #        continue
            #    # 15% of time
            #    OO[py, px] += 1
            #    # 15% of time
            #    OO[ny, nx] -= 1

            #    # 11% of time
            #    MM[py, px] += m
            #    # 11% of time
            #    MM[ny, nx] -= m
            #print 'O', O.shape, O.max(), O.min()
            #print O[:3, :3]
            #print O[-3:, -3:]
            #print 'M', M.shape, M.max(), M.min()
            #print M[:3, :3]
            #print M[-3:, -3:]

            #if any(abs(O - OO) > 1.) or any(abs(M - MM) > 1.):
            #    raise Exception
            O[where(O > kappa)] = kappa
            O[where(O < -kappa)] = -kappa
            #print 'O', O.shape, O.max(), O.min()

            # Unsmoothed symmetry measure at this radius value
            F = M / kappa * (abs(O) / kappa) ** alpha
            #print "-- Radius: %i --" % n
            #print "F:", F.shape, F.max(), F.min()

            # Generate a Gaussian of size proportional to n to smooth
            # and spread
            # the symmetry measure.  The Gaussian is also scaled in magnitude
            # by n so that large scales do not lose their relative weighting.
            # A = fspecial('gaussian',[n n], 0.25*n) * n;
            # S = S + filter2(A,F);
            width = round(gaussian_kernel_cheat * n)
            # print width
            if mod(width, 2) == 0:
                width += 1
            gauss1d = scipy.signal.gaussian(width, 0.25 * n)

            thisS = self.separable_convolution2d(F, gauss1d, gauss1d)
            #print "S:", thisS.shape, thisS.max(), thisS.min()
            S += thisS
            #print "S:", S.shape, S.max(), S.min()

        S = S / len(radii)  # Average
        #print "S:", S.shape, S.max(), S.min()

        return S

    # 0.0006
    def find_minmax(self, image, **kwargs):

        # print "here (vanilla)"
        if image is None:
            return ([0, 0], [0])

        #min_coord = nonzero(image == min(image.ravel()))
        #max_coord = nonzero(image == max(image.ravel()))

        # @clockit : 0.0045
        #return ([min_coord[0][0], min_coord[1][0]], [max_coord[0][0],
        #        max_coord[1][0]])

        return (numpy.unravel_index(image.argmin(), image.shape), \
                numpy.unravel_index(image.argmax(), image.shape))

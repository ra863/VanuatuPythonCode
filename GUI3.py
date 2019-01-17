"""
GUI 3 - Graph containing fitted curves e.c.t.
"""
from pylab import *
from math import log


def fitExponent(tList, yList, ySS=0):
    '''
    This function finds a
        tList in sec
        yList - measurements
        ySS - the steady state value of y
    returns
        amplitude of exponent
        tau - the time constant
    '''
    bList = [log(max(y - ySS, 1e-6)) for y in yList]
    b = matrix(bList).T
    rows = [[1, t] for t in tList]
    A = matrix(rows)
    # w = (pinv(A)*b)
    (w, residuals, rank, sing_vals) = lstsq(A, b)
    tau = -1.0 / w[1, 0]
    amplitude = exp(w[0, 0])
    return (amplitude, tau)


if __name__ == '__main__':
    import random

    tList = arange(0.0, 1.0, 0.001)
    tSamples = arange(0.0, 1.0, 0.2)
    random.seed(0.0)
    tau = 0.3
    amplitude = 3
    ySS = 3
    yList = amplitude * (exp(-tList / tau)) + ySS
    ySamples = amplitude * (exp(-tSamples / tau)) + ySS
    yMeasured = [y + random.normalvariate(0, 0.05) for y in ySamples]
    # print yList
    (amplitudeEst, tauEst) = fitExponent(tSamples, yMeasured, ySS)
    print('Amplitude estimate = %f, tau estimate = %f'
          % (amplitudeEst, tauEst))

    yEst = amplitudeEst * (exp(-tList / tauEst)) + ySS

    figure(1)
    plot(tList, yList, 'b')
    plot(tSamples, yMeasured, '+r', markersize=12, markeredgewidth=2)
    plot(tList, yEst, '--g')
    xlabel('seconds')
    legend(['True value', 'Measured values', 'Estimated value'])
    grid(True)
    show()

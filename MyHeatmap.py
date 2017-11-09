import numpy as np
import seaborn as sns
import math
import matplotlib.pyplot as plt


def logNorm(num, maxValue):
    return np.sign(num) * math.log(abs(num) + 1) / math.log(maxValue + 1)


def linear(num, maxValue):
    return num / float(maxValue)


def applytransform(arr, func, args):
    m, n = arr.shape
    arr = arr.astype('float')
    for i in range(m):
        for j in range(n):
            arr[i][j] = func(arr[i][j], *args)
    return arr

# take in numbers in original space, return a mapping from original space to bin index (interpolate input)
def logToBinIndex(maxValue, deltaD, n, transformFunc):
    #maxValue = arr.max()
    current = 0.0
    eps = 0.0001  # a very small number to deal with the boundary of the range
    xp = []
    fp = []
    bins = []
    unifrom = False  # a flag to tell if the the following bins are of the same size
    for i in range(n):
        if unifrom == False:
            lb = transformFunc(i * deltaD, maxValue)
            rb = transformFunc((i + 1) * deltaD, maxValue)
            width = max(rb - lb, float(1 - current) / (n - i))
            # print width
            if (rb - lb < float(1 - current) / (n - i)):
                unifrom = True
                # print i
        else:
            width = float(1 - current) / (n - i)
            # print width

        # closed left interval, open right interval
        xp.append(current)
        fp.append(i)
        xp.append(current + width - eps)
        fp.append(i)
        bins.append(current)
        current = current + width
    # deal with the end point
    xp.append(1)
    fp.append(n - 1)
    bins.append(1)
    return xp, fp, bins


def logToBinIndexUni(n):
    current = 0.0
    eps = 0.0001  # a very small number to deal with the boundary of the range
    xp = []
    fp = []
    bins = []
    width = 1.0 / n
    for i in range(n):
        xp.append(current)
        fp.append(i)
        xp.append(current + width - eps)
        fp.append(i)
        bins.append(current)
        current = current + width
    return xp, fp, bins


def mapToBinCenter(xp, fp, arr, n):
    dim1, dim2 = arr.shape
    binLabel = np.zeros_like(arr)
    arr = arr.astype('float')
    for i in range(dim1):
        for j in range(dim2):
            index = math.ceil(np.interp(arr[i][j], xp, fp))
            binLabel[i][j] = index
            arr[i][j] = (index + 0.5) / n
    return arr, binLabel

# draw a log-scaled Heatmap


def drawHeatMap(name, transformFunc, cmap='RdBu_r', nonNegative=False, outName=None, dpi=None):
    arr = np.load(name).astype('float')
    dim1, dim2 = arr.shape
    maxValue = arr.max()

    arr = arr.clip(0) if nonNegative else arr

    arr = applytransform(arr, logNorm, [maxValue])

    plt.figure(figsize=(5, 5))
    # plot heatmap
    sns.heatmap(arr, square=True, center=0, vmin=-1, vmax=1,
                xticklabels=False, yticklabels=False, cbar=False, cmap=cmap)
    plt.tight_layout(pad=0)

    if (outName != None):
        plt.savefig(outName + '.png', pad_inches=0, dpi=dpi / 5.0)

# draw a log-scale heatmap with the smoothing technique using binned
# colormap and deltaD correlation


def drawHeatMapSmooth(name, binNum, transformFunc, deltaD, uniformBin=False, cmap=None, nonNegative=True, outName=None, dpi=None, showHist=True):
    arr = np.load(name).astype('float')
    dim1, dim2 = arr.shape
    maxValue = arr.max()
    assert (math.ceil(maxValue / deltaD) >=
            binNum), "maxValue/deltaD < binNum, choose a smaller bin number"

    arr = arr.clip(0) if nonNegative else arr

    arr = applytransform(arr, transformFunc, [maxValue])

    if (uniformBin):
        xp, fp, bins = logToBinIndexUni(binNum)
    else:
        xp, fp, bins = logToBinIndex(maxValue, deltaD, binNum, transformFunc)

    arrBin, binLabel = mapToBinCenter(xp, fp, arr, binNum)

    if showHist:
        plt.figure(figsize=(10, 5))
        # plot heatmap
        plt.subplot(1, 2, 1)
        sns.heatmap(arrBin, square=True, vmin=0, vmax=1,
                    xticklabels=False, yticklabels=False, cbar=False, cmap=cmap)

        # Plot histograms
        plt.subplot(1, 2, 2)    

        cm = plt.cm.get_cmap(cmap)
        n, bins, patches = plt.hist(arr.ravel(), bins, range=[
                                    0, 1], orientation="horizontal")
        for c, p in zip(range(len(patches)), patches):
            plt.setp(p, 'facecolor', cm((c + 0.5) / binNum))

        n2, bins2, patches2 = plt.hist(
            arr.ravel(), binNum * 9, range=[0, 1], orientation="horizontal")
        bin_centers2 = 0.5 * (bins2[:-1] + bins2[1:])
        indices = np.interp(bin_centers2, xp, fp)
        for c, p in zip(indices, patches2):
            plt.setp(p, 'facecolor', cm((math.ceil(c) + 0.5) / binNum))

    else:
        plt.figure(figsize=(5, 5))
        # plot heatmap only 
        sns.heatmap(arrBin, square=True, vmin=0, vmax=1,
                    xticklabels=False, yticklabels=False, cbar=False, cmap=cmap)

    plt.xticks(rotation='vertical')
    plt.tight_layout(pad=0)

    if (outName != None):
        plt.savefig(outName + '.png', pad_inches=0, dpi=dpi / 5.0)

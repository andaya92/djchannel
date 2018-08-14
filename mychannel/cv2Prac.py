import cv2 as cv
import numpy as np
from multiprocessing.pool import ThreadPool
from common import mosaic, clock
from numpy.linalg import norm


SZ = 20 # size of each digit is SZ x SZ
CLASS_N = 10
DIGITS_FN = '../digits.png'

def split2d(img, cell_size, flatten=True):
    h, w = img.shape[:2]
    sx, sy = cell_size
    cells = [np.hsplit(row, w//sx) for row in np.vsplit(img, h//sy)]
    cells = np.array(cells)
    if flatten:
        cells = cells.reshape(-1, sy, sx)
    return cells

def load_digits(fn):
    print('loading "%s" ...' % fn)
    digits_img = cv.imread(fn, 0)
    digits = split2d(digits_img, (SZ, SZ))
    labels = np.repeat(np.arange(CLASS_N), len(digits)/CLASS_N)
    return digits, labels

def deskew(img):
    m = cv.moments(img)
    if abs(m['mu02']) < 1e-2:
        return img.copy()
    skew = m['mu11']/m['mu02']
    M = np.float32([[1, skew, -0.5*SZ*skew], [0, 1, 0]])
    img = cv.warpAffine(img, M, (SZ, SZ), flags=cv.WARP_INVERSE_MAP | cv.INTER_LINEAR)
    return img

class StatModel(object):
    def load(self, fn):
        self.model.load(fn)  # Known bug: https://github.com/opencv/opencv/issues/4969
    def save(self, fn):
        self.model.save(fn)

class KNearest(StatModel):
    def __init__(self, k = 3):
        self.k = k
        self.model = cv.ml.KNearest_create()

    def train(self, samples, responses):
        self.model.train(samples, cv.ml.ROW_SAMPLE, responses)

    def predict(self, samples):
        _retval, results, _neigh_resp, _dists = self.model.findNearest(samples, self.k)
        return results.ravel()

class SVM(StatModel):
    def __init__(self, C = 1, gamma = 0.5):
        self.model = cv.ml.SVM_create()
        self.model.setGamma(gamma)
        self.model.setC(C)
        self.model.setKernel(cv.ml.SVM_RBF)
        self.model.setType(cv.ml.SVM_C_SVC)

    def train(self, samples, responses):
        self.model.train(samples, cv.ml.ROW_SAMPLE, responses)

    def predict(self, samples):
        return self.model.predict(samples)[1].ravel()


def evaluate_model(model, digits, samples, labels):
    resp = model.predict(samples)
    err = (labels != resp).mean()
    print('error: %.2f %%' % (err*100))

    confusion = np.zeros((10, 10), np.int32)
    for i, j in zip(labels, resp):
        confusion[i, int(j)] += 1
    print('confusion matrix:')
    print(confusion)
    print()

    vis = []
    for img, flag in zip(digits, resp == labels):
        img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
        if not flag:
            img[...,:2] = 0
        vis.append(img)
    return mosaic(25, vis)

def preprocess_simple(digits):
    return np.float32(digits).reshape(-1, SZ*SZ) / 255.0

def preprocess_hog(digits):
    samples = []
    for img in digits:
        gx = cv.Sobel(img, cv.CV_32F, 1, 0)
        gy = cv.Sobel(img, cv.CV_32F, 0, 1)
        mag, ang = cv.cartToPolar(gx, gy)
        bin_n = 16
        bin = np.int32(bin_n*ang/(2*np.pi))
        bin_cells = bin[:10,:10], bin[10:,:10], bin[:10,10:], bin[10:,10:]
        mag_cells = mag[:10,:10], mag[10:,:10], mag[:10,10:], mag[10:,10:]
        hists = [np.bincount(b.ravel(), m.ravel(), bin_n) for b, m in zip(bin_cells, mag_cells)]
        hist = np.hstack(hists)

        # transform to Hellinger kernel
        eps = 1e-7
        hist /= hist.sum() + eps
        hist = np.sqrt(hist)
        hist /= norm(hist) + eps

        samples.append(hist)
    return np.float32(samples)





def run():
	digits, labels = load_digits(DIGITS_FN)

	print('preprocessing...')
	# shuffle digits
	rand = np.random.RandomState(321)
	shuffle = rand.permutation(len(digits))
	digits, labels = digits[shuffle], labels[shuffle]

	digits2 = list(map(deskew, digits))
	samples = preprocess_hog(digits2)

	train_n = int(0.9*len(samples))
	cv.imshow('test set', mosaic(25, digits[train_n:]))
	digits_train, digits_test = np.split(digits2, [train_n])
	samples_train, samples_test = np.split(samples, [train_n])
	labels_train, labels_test = np.split(labels, [train_n])


	print('training KNearest...')
	model = KNearest(k=4)
	model.train(samples_train, labels_train)
	vis = evaluate_model(model, digits_test, samples_test, labels_test)
	cv.imshow('KNearest test', vis)

	print('training SVM...')
	model = SVM(C=2.67, gamma=5.383)
	model.train(samples_train, labels_train)
	vis = evaluate_model(model, digits_test, samples_test, labels_test)
	cv.imshow('SVM test', vis)
	print('saving SVM as "digits_svm.dat"...')
	model.save('digits_svm.dat')

	cv.waitKey(0)
	cv.waitKey(0) & 0xFF		
	cv.destroyAllWindows()

if "__main__" == __name__ :
	run()

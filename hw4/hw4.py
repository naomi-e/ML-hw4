import numpy as np
import pandas as pd
from scipy.stats import norm
import matplotlib.pyplot as plt

PLOT_WIDTH_IN_SIGMA = 3


# code for ploting the original distribution with the one that we found with the EM
def plot_pred_vs_actual(df):
    plt.figure(figsize=(10, 7))
    mu_hat1 = df['x'][df['z'] == 0].mean()
    sigma_hat1 = df['x'][df['z'] == 0].std()
    x_hat1 = np.linspace(mu_hat1 - PLOT_WIDTH_IN_SIGMA * sigma_hat1, mu_hat1 + PLOT_WIDTH_IN_SIGMA * sigma_hat1, 1000)
    y_hat1 = norm.pdf(x_hat1, mu_hat1, sigma_hat1)

    mu_hat2 = df['x'][df['z'] == 1].mean()
    sigma_hat2 = df['x'][df['z'] == 1].std()
    x_hat2 = np.linspace(mu_hat2 - PLOT_WIDTH_IN_SIGMA * sigma_hat2, mu_hat2 + PLOT_WIDTH_IN_SIGMA * sigma_hat2, 1000)
    y_hat2 = norm.pdf(x_hat2, mu_hat2, sigma_hat2)

    plt.plot(x_hat1, y_hat1, color='red', lw=1, ls='-', alpha=0.5)
    plt.plot(x_hat2, y_hat2, color='blue', lw=1, ls='-', alpha=0.5)

    plt.xlim(min(mu_hat1 - PLOT_WIDTH_IN_SIGMA * sigma_hat1, mu_hat2 - 3 * sigma_hat2),
             max(mu_hat1 + PLOT_WIDTH_IN_SIGMA * sigma_hat1, mu_hat2 + PLOT_WIDTH_IN_SIGMA * sigma_hat2))

    mu1 = -1
    sigma1 = 1
    x1 = np.linspace(mu1 - PLOT_WIDTH_IN_SIGMA * sigma1, mu1 + PLOT_WIDTH_IN_SIGMA * sigma1, 1000)
    y1 = norm.pdf(x1, mu1, sigma1)

    mu2 = 5
    sigma2 = 2
    x2 = np.linspace(mu2 - PLOT_WIDTH_IN_SIGMA * sigma2, mu2 + PLOT_WIDTH_IN_SIGMA * sigma2, 1000)
    y2 = norm.pdf(x2, mu2, sigma2)

    plt.plot(x1, y1, color='red', lw=1, ls='--', alpha=0.5)
    plt.plot(x2, y2, color='blue', lw=1, ls='--', alpha=0.5)

    plt.xlim(min(mu1 - PLOT_WIDTH_IN_SIGMA * sigma1, mu2 - PLOT_WIDTH_IN_SIGMA * sigma2),
             max(mu1 + PLOT_WIDTH_IN_SIGMA * sigma1, mu2 + PLOT_WIDTH_IN_SIGMA * sigma2))

    plt.legend(['Predicted - 1st gaussian', 'Predicted - 2nd gaussian',
                'Original - 1st gaussian', 'Original - 2nd gaussian'])

    plt.show()
    print ("mu_1: %s ,predicted mu_1: %s\nsigma_1: %s, predicted sigma_1: %s" % (mu1, mu_hat1, sigma1, sigma_hat1))
    print ("mu_2: %s ,predicted mu_2: %s\nsigma_2: %s, predicted sigma_2: %s" % (mu2, mu_hat2, sigma2, sigma_hat2))


def get_num_of_gaussians():
    k = None

    ###########################################################################
    # TODO: Implement the function.                                           #
    ###########################################################################
    k=4
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

    return k


def init(points_list, k):
    """
    :param points_list: the entire data set of points. type: list.
    :param k: number of gaussians. type: integer.
    :return the initial guess of w, mu, sigma. types: array
    """
    w = np.array([0.0])
    mu = np.array([0.0])
    sigma = np.array([0.0])
    ###########################################################################
    # TODO: Implement the function. compute init values for w, mu, sigma.     #
    ###########################################################################
    w=np.ones(k) / k
    w[-1] = w[-1] + (1 - w.sum())
    sigma = np.ones(k)
    points_list_np = np.array(points_list)
    mu_unit = (points_list_np.max() - points_list_np.min())/(k+1)
    mu = np.linspace(points_list_np.min()+mu_unit,points_list_np.max()-mu_unit,k)
    
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

    return w, mu, sigma


def normal_pdf(x, mean, std):
    """
    Calculate normal desnity function for a given x, mean and standrad deviation.
 
    Input:
    - x: A value we want to compute the distribution for.
    - mean: The mean value of the distribution.
    - std:  The standard deviation of the distribution.
 
    Returns the normal distribution pdf according to the given mean and var for the given x.    
    """
    
    normal = 1 / (np.sqrt( 2 * np.pi * np.power(std, 2))) * np.exp( - np.power((x - mean), 2) / (2 * np.power(std, 2) ))
    #print(normal)
    return normal

def expectation_2(points_list, mu, sigma, w):
    """
    :param points_list: the entire data set of points. type: list.
    :param mu: expectation of each gaussian. type: array
    :param sigma: std for of gaussian. type: array
    :param w: weight of each gaussian. type: array
    :return likelihood: dividend of ranks matrix (likelihood). likelihood[i][j] is the likelihood of point i to belong to gaussian j. type: array
    """
    likelihood = np.array([0.0])
    ###########################################################################
    # TODO: Implement the function. compute likelihood array                  #
    ###########################################################################
    likelihood = np.empty(shape =[len(points_list), w.size])
    #gaus_set = np.array([mu, sigma, w])
    for i in range (len(points_list)):
        for j in range (w.size):
            normal = normal_pdf(points_list[i], mu[j], sigma[j])
            #print(normal)
            likelihood[i][j] = w[j]*normal
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

    return likelihood


def expectation(points_list, mu, sigma, w):
    """
    :param points_list: the entire data set of points. type: list.
    :param mu: expectation of each gaussian. type: array
    :param sigma: std for of gaussian. type: array
    :param w: weight of each gaussian. type: array
    :return likelihood: dividend of ranks matrix (likelihood). likelihood[i][j] is the likelihood of point i to belong to gaussian j. type: array
    """
    likelihood = np.array([0.0])
    ###########################################################################
    # TODO: Implement the function. compute likelihood array                  #
    ###########################################################################
    likelihood = np.empty(shape =[len(points_list), w.size])
    
    normal = lambda t, mean, std, w: w*normal_pdf(t, mean, std)
    vfunc = np.vectorize(normal)
    
    #gaus_set = np.array([mu, sigma, w])
    #for i in range (len(points_list)):
#     print("likelihood.shape:" ,likelihood.shape)
#     print("likelihood[:,0].shape: ", likelihood[:,0].shape)
    for j in range (w.size):
        #normal = normal_pdf(points_list[i], mu[j], sigma[j])
        #print(normal)
        #likelihood[:][j] = w[j]*normal
        likelihood_return = vfunc(points_list, mu[j], sigma[j], w[j])
#         print("likelihood_return.shape: ", likelihood_return.shape)
#         print("likelihood.shape:" ,likelihood.shape)
#         print("likelihood[:,j].shape: ", likelihood[:,j].shape)
        likelihood[:,j] = np.transpose(likelihood_return)
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

    return likelihood


def maximization(points_list, ranks):
    """
    # :param data: the complete data
    :param points_list: the entire data set of points. type: list.

    :param ranks: ranks matrix- r(x,k)- responsibility of each data point x to gaussian k
    :return w_new: new weight parameter of each gaussian
            mu_new: new expectation parameter of each gaussian
            sigma_new: new std parameter of each gaussian
    """

    w_new = np.array([0.0])
    mu_new = np.array([0.0])
    sigma_new = np.array([0.0])

    ###########################################################################
    # TODO: Implement the function. compute w_new, mu_new, sigma_new          #
    ###########################################################################
    pass
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

    return w_new, mu_new, sigma_new


def calc_max_delta(old_param, new_param):
    """
    :param old_param: old parameters to compare
    :param new_param: new parameters to compare
    :return maximal delta between each old and new parameter
    """
    max_delta = 0.0

    ###########################################################################
    # TODO: find the maximal delta between each old and new parameter         #
    ###########################################################################
    pass
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

    return max_delta


# helper function for plotting
def plot_gmm(k, res, mu, sigma, points_list, iter_num=-1):
    data = pd.DataFrame(points_list, columns=['x'])
    res = pd.DataFrame(res, columns=['x'])
    for k in range(k):
        res_bin = res[res == k]
        dots = data["x"][res_bin.index]
        plt.scatter(dots.values, norm.pdf(dots.values, loc=mu[k], scale=sigma[k]),
                    label="mu=%.2f, Sigma=%.2f" % (mu[k], sigma[k]), s=10)
    plt.ylabel('probability')
    if iter_num >= 0:
        plt.title('Expectation Maximization - GMM - iteration {}'.format(iter_num))
    else:
        plt.title('Expectation Maximization - GMM')
    plt.legend()
    plt.ylim(0, 0.5)
    plt.show()


def expectation_maximization(points_list, k, max_iter, epsilon):
    """
    :param points_list: the entire data set of points. type: list.
    :param k: number of gaussians. type: integer
    :param max_iter: maximal number of iterations to perform. type: integer
    :param epsilon: minimal change in parameters to declare convergence. type: float
    :return res: gaussian estimation for each point. res[i] is the gaussian number of the i-th point. type: list
            mu: mu values of each gaussian. type: array
            sigma: sigma values of each gaussian. type: array
            log_likelihood: a list of the log likelihood values each iteration. type: list


    """
    w = np.array([0.0])
    mu = np.array([0.0])
    sigma = np.array([0.0])
    # TODO: init values and then remove the 3 lines above

    # Loop until convergence
    delta = np.infty
    iter_num = 0

    log_likelihood = []
    while delta > epsilon and iter_num <= max_iter:

        # E step
        likelihood = None  # TODO: compute likelihood array

        likelihood_sum = likelihood.sum(axis=1)
        log_likelihood.append(np.sum(np.log(likelihood_sum), axis=0))

        # M step
        ranks = None  # TODO: compute ranks array using the likelihood array

        w_new, mu_new, sigma_new = None, None, None   # TODO: compute w_new, mu_new, sigma_new

        # Check significant change in parameters
        delta = max(calc_max_delta(w, w_new), calc_max_delta(mu, mu_new), calc_max_delta(sigma, sigma_new))

        # TODO: below, set the new values for w, mu, sigma

        if iter_num % 10 == 0:
            res = ranks.argmax(axis=1)
            plot_gmm(k, res, mu, sigma, points_list, iter_num)
        iter_num += 1

    plt.show()

    res = ranks.argmax(axis=1)

    # Display estimated Gaussian:
    plot_gmm(k, res, mu, sigma, points_list, iter_num)

    return res, mu, sigma, log_likelihood

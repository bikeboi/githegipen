---
title: "Quadratic Mutual Information in brief"
date: 2023-02-01
draft: false
math: true
draft: false
---

Information theory is great -- in theory. In practice, many of the quantities are tricky to compute. Most of them revolve around entropy

\\[
H(X) = -\sum\_{i=1}^N \log p\_j,
\\]

which is fine for discrete systems for which we know all possible states _and_ the distribution over those states. Most often this is far from the case, so we have to be clever about how we use these measures.

Thankfully, the work of past clever people cascades down to the rest of us, and we can reap the efforts of their cleverness. In 1994, Jagat Narain Kapur published a treatise: _Measures of Information and their Application_ [1] in which he formulated alternative forms of mutual information with varying uses. Of note, to us, is what later developers of the theory called: Quadratic Mutual Information (QMI) [2]. The idea is that replacing Kullback-Liebler (KL) divergence in QMI with a 'Quadratic Divergence' results in a form that's _much_ easier to estimate in a differentiable way. The trade-off is that the raw QMI quantity isn't meaningful the same way MI is, but here's the kicker: the same distributions that maximise QMI also maximise MI. So we can optimise QMI, a differentiable and computationally-cheap-to-estimate quantity, as a proxy to MI. How great!


## Deriving QMI {#deriving-qmi}

Both Jose Principe's book _Information Theoretic Learning_ [2] and Kari Torkkola's paper [3] have well-expounded derivations of QMI and its estimator. Here I'll re-elaborate on what has already been done there.

Mutual information between two random variables \\(X\\) and \\(Y\\) can be thought of as the KL-divergence between their joint distribution, and the product of their marginals,
\\[
I(X; Y) = D\_{KL}(P\_{X,Y}\\|P\_XP\_Y) = \iint\log\frac{p(x,y)}{p(x)p(y)}\\:dxdy.
\\]

With QMI we replace KL-divergence and replace it with something that looks similar to Euclidean distance,

\\[
I\_Q(X; Y) = \iint(p(x,y) - p(x)p(y))^2\\:dxdy.
\\]

Expanding this we get a three-term quadratic-looking expression,

\begin{align\*}
I\_Q(X; Y) = \iint p(x,y)^2 - 2p(x,y)p(x)p(y) + p(x)^2p(y)^2.\tag{1}
\end{align\*}

And so there it is, quadratic mutual information. Yet still not as useful in practice. We're still stuck with those gnarly integrals and density functions we have to somehow estimate. In comes the second step: the QMI estimator.


## The QMI estimator {#the-qmi-estimator}

First, we use [Kernel Density Estimation](https://www.wikiwand.com/en/Kernel_density_estimation) (KDE) to approximate the density functions. Given dataset of \\(N\\) samples \\(\\{(x\_i,y\_i)|i=1...N\\}\\), we estimate the densities using a Gaussian kernel with bandwidth \\(\sigma\\):

\begin{align\*}
\hat{p}\_{X,Y}(x, y) &= \frac{1}{N}\sum\_{i=1}^N G\_\sigma(x-x\_i)G\_\sigma(y-y\_i)\tag{2}\\\\
\hat{p}\_X(x) &= \frac{1}{N}\sum\_{i=1}^NG\_\sigma(x-x\_i),\tag{3}\\\\
\hat{p}\_Y(y) &= \frac{1}{N}\sum\_{i=1}^NG\_\sigma(y-y\_i),\tag{4}
\end{align\*}

where \\(G\_\sigma(x)\\) is the Gaussian density function with \\(\mu=0\\) and \\(\sigma\\) standard deviation. Before we plug the KDE estimates into (1), we note the following property of convolved Gaussian functions:

\\[
\int G\_\sigma(x-x')G\_\sigma(y-y')\\:dx'dy' = G\_{\sigma\sqrt{2}}(x' - y').
\\]

This neat simplification _vanquishes_ the scary integrals of \\((1)\\){{<sidenote>}}This is why we use the Gaussian kernel in particular.{{</sidenote>}},
leaving us with pleasant sums-of-sums that we can compute exactly. In this manner, each of three terms in \\((1)\\) becomes an _information potential_ (IP): the joint-, marginal-, and cross-information potentials respectively,
\\[
\hat{I}\_Q(X; Y) = \hat{V}\_J + \hat{V}\_M - 2\hat{V}\_C,\\\\
\\]

where the IPs work out to:

\begin{align\*}
\hat{V}\_J &= \frac{1}{N^2}\sum\_{i=1}^N\sum\_{j=1}^N G\_{\sigma\sqrt2}(x\_i - x\_j)G\_{\sigma\sqrt2}(y\_i - y\_j)\tag{5}\\\\
\hat{V}\_M &= \bigg(\frac{1}{N^2}\sum\_{i=1}^N\sum\_{j=1}^N G\_{\sigma\sqrt2}(x\_i-x\_j)\bigg)\bigg(\frac{1}{N^2}\sum\_{i=1}^N\sum\_{j=1}^N G\_{\sigma\sqrt2}(y\_i-y\_j)\bigg)\tag{6}\\\\
\hat{V}\_C &= \frac{1}{N}\sum\_{i=1}^N
\bigg( \frac{1}{N}\sum\_{j=1}^N G\_{\sigma\sqrt{2}}(x\_i - x\_j) \bigg)
\bigg( \frac{1}{N}\sum\_{j=1}^N G\_{\sigma\sqrt{2}}(y\_i - y\_j) \bigg).\tag{7}
\end{align\*}


## Computation {#computation}

If you squint a little you'll see that \\((5)-(7)\\) revolve around inter-sample differences \\(x\_i-x\_j\\) and \\(y\_i-y\_j\\). This means we can compute all of these _once_ and just re-use them for each IP, bringing the time complexity of QMI into the \\(\mathcal{O}(N^2)\\) range. Let \\(X \in \mathbb{R}^{N\times N}\\) be the _difference matrix_ for \\(x\\)-samples such that \\(X\_{ij} = G\_{\sigma\sqrt{2}}(x\_i - x\_j\\), and similarly for \\(Y\\). We can then rewrite the IPs  with Einstein notation:

\begin{align\*}
\hat{V}\_J &= N^{-2} X\_{ij}Y\_{ij}\\\\
\hat{V}\_M &= N^{-4} (\mathbf{1}\_{ij}X\_{ij})(\mathbf{1}\_{kl}Y\_{kl}) \\\\
\hat{V}\_C &= N^{-3} (\mathbf{1}\_jX\_{ij})(\mathbf{1}\_kY\_{ik}),
\end{align\*}

where summation over the indices is implied and \\(\mathbf{1}\\) is the vector/matrix of all ones (either/or implied by the number of indices); \\(\mathbf{1}\_{ij}A\_{ij}\\) is shorthand for summing over all the elements in \\(A\_{ij}\\). The notation might be a little obtuse at first but it serves to show how simple the calculations really are.

The above translates to Python quite smoothly:

```python
def qmi(x, y):
    """Compute QMI
    Args:
        x and y: Length N ndarrays (samples from random variables X and Y)
    """
    # Compute difference matrix (G is the elementwise univariate Gaussian pdf)
    X = G( x[:,None] - x )
    Y = G( y[:,None] - y )

    # Compute information potentials
    Vj = (X * Y).mean()
    Vm = X.mean() * Y.mean()
    Vc = (X.mean(axis=1) * Y.mean(axis=1)).mean()

    # QMI
    return Vj + Vm - 2*Vc
```


## Applications {#applications}

Here we've gone over the QMI formulation where both \\(x\\) and \\(y\\) are continuous-valued. This form is the most general and, fortunately, the most straightforward. In his 2002 paper, Torkkola [3] formulated QMI for the discrete-continuous case. There, one variable was class labels and the other a continuous (possibly multivariate) value. In that context QMI becomes a way to do feature selection: maximising the QMI between a transformation \\(z = f\_\theta(x)\\) and the class labels, w.r.t. parameters \\(\theta\\), puts \\(z\\) in a space where same-class samples cluster and differing-class ones are far apart -- effectively, classification.

QMI has been used this way in neuroscience [4,5]. The binary class labels become the presence/absence of a spike in a single neuron, \\(x\\) is whichever stimulus was used, and the transformation (often linear) projects the stimulus into a space where its samples are separated by whether they evoked a spike or not. Thus, the parameters of the transformation are the neuron's receptive field: the stimulus that it's sensitive to.

Though useful so far, QMI, as far as I can tell, seems to be relatively untapped. I mean, this is an easy way to optimise mutual information, we could use it in loads of places{{<sidenote>}}Caveat: the particular way QMI is optimised is important, particularly how bandwidth $\sigma$ is adjusted. This is worth talking about in a future article.{{</sidenote>}}. For instance, we could apply the same receptive-field mapping procedure to neurons/layers in a deep neural net and do something like [feature visualisation](https://distill.pub/2017/feature-visualization/). It would be great to see this used more.


## References {#references}

[1] Kapur, J.N. (1994). _Measures of information and their applications._

[2] Xu, D., Erdogmuns, D. (2010). _Renyi’s Entropy, Divergence and Their Nonparametric Estimators. In: Information Theoretic Learning. Information Science and Statistics._

[3] Torkkola, K. (2002). _On feature extraction by mutual information maximization._

[4] Mu, Z., Nikolic, K., Schultz, S.R. (2021). _Quadratic Mutual Information estimation of mouse dLGN receptive fields reveals asymmetry between ON and OFF visual pathways._

[5] Katz, M., Viney, T., Nikolic, K. (2016). _Receptive Field Vectors of Genetically-Identified Retinal Ganglion Cells Reveal Cell-Type-Dependent Visual Functions._

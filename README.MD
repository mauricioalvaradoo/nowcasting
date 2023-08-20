# Nowcasting peruvian GDP

## Methodology
### Model
The dynamic factor model with mixed monthly/quarterly data is based in Bańbura et al. (2011) and Bańbura and Modugno (2014). We define a stationary $𝑛$−dimensional process $𝑦_𝑡 = [𝑦_{1,𝑡}, 𝑦_{2,𝑡}, ..., 𝑦_{n,𝑡}]', \ 𝑡 = 1, ... 𝑇$, standardized with zero mean and variance  unitary. It is assumed that $𝑦_t$ follows the following factor model representation:

$$ y_t = \Lambda f_t + ϵ_t $$

where $𝑓_t$ is a vector of common factors of $𝑟 × 1^5$ dimension and where the idiosyncratic errors $ϵ_𝑡 = [ϵ_{1,𝑡}, ϵ_{2,𝑡}, ..., ϵ_{𝑛,𝑡}]'$ are not correlated with lags and leads of $𝑓_t$. The matrix $\Lambda$ ​​of dimension $𝑛 × 𝑟$ contains the factor coefficients.

Nevertheless, it is allowed that the idiosyncratic disturbances to be serially correlated. Also, I can define a different autoregressive process for each group of series. An AR(1) process for the disturbances is as the following:

$$e_{i,t} = \rho_i e_{i,t-1} + e_{i,t}, \ \ \ e_{i,t} \sim N(0,\sigma^2_i) $$

The common factors $𝑓_t$ are defined to follow a VAR process of order $𝑝$ as the following:

$$ f_t = A_1 f_{t-1} + A_2 f_{t-2} + ... + A_𝑝 f_{t-p} + u_t, \ \ \ u_t \sim i.i.d. N(0, Q) $$

where $A_1, A_2, ... A_p$ are autoregressive matrixes of dimension $𝑟 × 𝑟$.

### EM algorithm
The estimation is achieved by the Expectation-Maximization (EM) algorithm in line with estimating the coefficients for different patterns of missing data. This methodology adapts to the estimation of indicators in countries that have series that their registration started late, so some of these are only available recently. 

In the first stage, the EM algorithm fits the pattern of missing values ​​and "fills-in" it. In the second stage, the coefficients are estimated by maximum likelihood (ML), with fewer difficulties since the lack of data has already been solved. The jointly $\log$-likelihood of $y_t$ and $f_t$ is define by $l(Y, F; \theta)$, where $Y=[y_1, y_2, ... y_T]$ and $F=[f_1, f_2, ... f_T]$. The steps are the following:
1. **E-step**: The expectation of the $\log$-likelihood conditional to the data is calculated using the estimation of a previous iteration: 
$$L(\theta, \theta(j)) = E_{\theta(j)} [l(Y, F; \theta)|\Omega_t]$$

2. **M-step**: The parameters are estimated through the maximization of the expected $\log$-likelihood with respect to $\theta$:
$$\theta(j+1) = arg max L(\theta, \theta(j))$$


## Data
I use 129 monthly variables and 1 quarterly variable (GDP Growth) from three principal sources:
- Central Reserve Bank of Peru
- Federal Reserve Bank of St. Louis
- Yahoo Finance

The series are obtained using the library [econdata](https://github.com/mauricioalvaradoo/econdata). They are divided in the following groups:
```
                        Series
Group                         
Output                      12
Labor Market                21
Juncture                    14
Prices                      13
Government                  11
Balance of Trade            17
Finance                     24
Stock Market                6
Quotes                      11
-------------------------------
Total                      129
```

To get stationary time series, which is an assumption of the model, I transformate them following this criterias:

```
1: Levels
2: First Difference to the Levels
3: Logarithm
4: First Difference to the Logarithm
+ : Season-Trend decomposition using LOESS (STL)
```

Then, all one them are standarized $y_t = \dfrac{(y_t - \hat{y_t})}{\sigma_y}$


## References
1. Bańbura, M., and Modugno, M. (2014). Maximum likelihood estimation of factor models on datasets with arbitrary pattern of missing data. _Journal of Applied Econometrics_ **29(1)**, 133-160. [link](https://onlinelibrary.wiley.com/doi/abs/10.1002/jae.2306?casa_token=tX0xS_49OXcAAAAA%3Aocw-egTRztTVg643NCHRCQUs_OGCPMTS78Qds4gk2nN6ViFjOMZYSDVip-0eeDwQCpvaTOTqjof5_wKI).
2. Bańbura, M., Giannone, D., and Reichlin, L. (2011). Nowcasting. _ECB Working Paper_ **1275**. [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1717887).

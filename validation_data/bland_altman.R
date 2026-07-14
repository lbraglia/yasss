## An implementation of  Lu, M.J.,Zhong, W.H.,
## Liu, Y.X., Miao, H.Z., Li, Y.C., Ji, M.H. 2016. 'Sample Size for Assessing
## Agreement between Two Methods of Measurement by Bland-Altman Method.' The
## International Journal of Biostatistics.  Article 20150039. (Published online
## See also https://www.kuan-liu.com/posts/2021/08/sample-size-and-power-calculation-for-bland-altman-method-comparing-two-sets-of-measurements-in-r/
## ------------------------------------------------

power_ba <- function(n,      # available sample size
                     D = 0.5,  # meani of difference
                     SD = 2.5, # expected sd of difference
                     delta = 7, # target clinical agreement limit
                     gamma = 0.05, # confidence level of Loa
                     alpha = 0.05 # confidence level of CI of loa
                   )
{
  zgamma <- qnorm(1 - gamma / 2)
  se_loas <- SD * sqrt((1/n) + ((zgamma^2) / (2 * (n-1))))
  tau_1 <- (delta - D - zgamma * SD) / se_loas
  tau_2 <- (delta + D - zgamma * SD) / se_loas
  suppressWarnings(
    the_t <- qt(1 - alpha / 2, df = n - 1)
  )
  beta_1 <- 1 - pt(the_t, df = n - 1, ncp = tau_1, lower.tail = FALSE) # eq 3
  beta_2 <- 1 - pt(the_t, df = n - 1, ncp = tau_2, lower.tail = FALSE) # eq 4
  1 - (beta_1 + beta_2) # power: eq 5
}

bland_altman <- function(power = 0.8, ...){
  searched_samples <- 1:25000 # looking at lu's table ..
  params <- c(list("n" = searched_samples), list(...))
  pows <- do.call(power_ba, params)
  res <- cbind(data.frame("n" = searched_samples, "power" = pows),
               data.frame(...))
  res <- na.omit(res)
  head(res[res$power > power, ], n = 1)
}

# simple usage
bland_altman(D = 0.5, SD = 1, delta = 7)


## ------------------------------------------------------------------
## sample size: Example 1 pass
pass_cases <- expand.grid(
  "power" = c(0.8, 0.9),
  "D" = 0.5,
  "SD" = c(2.5, 2.6, 2.7),
  "delta" = 7
)
pass_cases <- pass_cases[with(pass_cases, order(power, SD)), ]

pass_cases$ss <- apply(cases, 1, function(x){
  desired_power <- x[1]
  the_SD <- x[2]
  sample_sizes <- 50:200
  real_pows <- power_ba(sample_sizes, D=0.5, SD=the_SD, delta=7)
  results <- data.frame("n"=sample_sizes, "pows"=real_pows)
  head(results[real_pows > desired_power, ], n=1)$n
})
cases

pass_res <- lapply(split(pass_cases, seq_len(nrow(pass_cases))), function(par){
  bland_altman(power = par$power,
              D = par$D,
              SD = par$SD,
              delta = par$delta)
})
(pass_res <- do.call(rbind, pass_res))



## ---------------------------------------------------------------
## lu et al table 1

lu_et_al_cases <- expand.grid(
  delta_over_sigma = seq(2, 3, by = 0.1),
  beta = c(0.2, 0.1),
  mu_over_sigma = seq(0, 0.9, by = 0.1)
)

lu_et_al_res <- lapply(
  split(lu_et_al_cases, seq_len(nrow(lu_et_al_cases))),
  function(par){
    SD <- 1
    mu <- SD * par$mu_over_sigma
    delta <- SD * par$delta_over_sigma
    power <- 1 - par$beta
    bland_altman(power = power, D = mu, SD = SD, delta = delta)
  }
)
(lu_etal_res <- do.call(rbind, lu_et_al_res))
## as PASS put it: we traced the problem to their equation (6) which is an
## approzimation. In PASS we use their formula 5 which gives the exact
## answer. Because of this problem we found several entries in table 1 that
## were slightly off

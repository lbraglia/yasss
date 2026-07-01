import math
from scipy import stats
from scipy import optimize


def test_power(n, p1, p2, alpha, alternative):
    tside = 2 if alternative.startswith("t") else 1
    
    # two sided
    def two_sided_power():
        # equivalent of power.prop.test with strict=TRUE
        qu = stats.norm.ppf(1 - alpha/2)
        d = math.fabs(p1 - p2)
        q1 = 1 - p1
        q1 = 1 - p1
        q2 = 1 - p2
        pbar = (p1 + p2)/2
        qbar = 1 - pbar
        v1 = p1 * q1
        v2 = p2 * q2
        vbar = pbar * qbar
        lower = (math.sqrt(n) * d - qu * math.sqrt(2 * vbar))/math.sqrt(v1 + v2)
        upper = (math.sqrt(n) * d + qu * math.sqrt(2 * vbar))/math.sqrt(v1 + v2)
        return stats.norm.cdf(lower) + (1 - stats.norm.cdf(upper))

    # one sided power
    def one_sided_power():
        pass

    if tside == 2:
        return two_sided_power
    else:
        return one_sided_power
    

    
def solve_for(what, pow_f, power=0.8, **kwargs):
    w = what.lower()
    if w.startswith("p"):  #power
        return pow_f(**kwargs)()
    elif w.startswith("n"):  # sample size
        return optimize.brentq(lambda n: pow_f(n=n, **kwargs)() - power, 1, 1e5)


# >  power.prop.test(n=10,p1=0.1, p2=0.2, sig.level=0.05, alternative="two",strict=TRUE)
#      Two-sample comparison of proportions power calculation

#               n = 10
#              p1 = 0.1
#              p2 = 0.2
#       sig.level = 0.05
#           power = 0.09349
#     alternative = two.sided
# NOTE: n is number in *each* group

p = solve_for(what="power", pow_f=test_power,
              n=10,
              p1=0.1,
              p2=0.2,
              alpha=0.05,
              alternative="two.sided")
p

# > power.prop.test(power=0.8,p1=0.1, p2=0.2, sig.level=0.05, alternative="two",strict=TRUE)

#      Two-sample comparison of proportions power calculation

#               n = 199
#              p1 = 0.1
#              p2 = 0.2
#       sig.level = 0.05
#           power = 0.8
#     alternative = two.sided

# NOTE: n is number in *each* group
n = solve_for("n", pow_f=test_power,
              p1=0.1,
              p2=0.2,
              alpha=0.05,
              power=0.8,
              alternative="two.sided")

n

from algo import prefix_tree


def simpl(TS): # расчет метрики простота
    S, E, T, s0, AS = TS
    return (len(E) + 1) / (len(T) + len(S))


def recalc_state_precision(s, nu, teta, pprec):
    if s not in nu:
        nu[s] = 0
    if s not in teta:
        teta[s] = 0
    stPrec = nu[s] * teta[s]
    teta[s] += 1
    nu[s] = (stPrec + pprec) / teta[s]


def s_point(state, T):
    res = set()
    for t in T:
        st, at, s_t = t
        if st == state:
            res.add(t)
    return res


def exist_t1_in_T1(s1, a, T1):
    for t1 in T1:
        st1, at1, s_t1 = t1
        if st1 == s1 and a == at1:
            return s_t1
    return False


def calc_state_precision(s, s1, TS, TS1, nu, teta):
    S, E, T, s0, AS = TS
    S1, E1, T1, s0, AS1 = TS1
    pen = 0
    for t in s_point(s, T):
        _, a, s_ = t
        if exist_t1_in_T1(s1, a, T1):
            s1_ = exist_t1_in_T1(s1, a, T1)
            calc_state_precision(s_, s1_, TS, TS1, nu, teta)
        else:
            pen += 1
    otn = len(s_point(s, T))
    if s in AS:
        otn += 1
        if s1 not in AS1:
            pen += 1
    if otn != 0:
        part_part_prec = (otn - pen) / otn
        recalc_state_precision(s, nu, teta, part_part_prec)


def sum_partial_precisions(TS, nu):
    S, E, T, s0, AS = TS
    sum = 0
    for s in S:
        sum += nu[s]
    res = sum / len(S)
    return res


def prec(TS, L, A): # расчет метрики точность
    nu = dict()
    teta = dict()
    S, E, T, s0, AS = TS
    TS1, f = prefix_tree(L, A)
    calc_state_precision(s0, s0, TS, TS1, nu, teta)
    return sum_partial_precisions(TS, nu)

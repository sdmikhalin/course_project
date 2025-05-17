def prefix_tree(L, A):  # этап 1: построение префиксного дерева для журнала событий L
    s0 = (" ",) # нулевое состояние
    AS, S, E, T = set(), set(), A, set()
    S.add(s0)
    f = dict()
    for trace in L:
        s = s0
        for i in range(len(trace)):
            s_ = tuple(trace[:i + 1])
            t = (s, trace[i], s_)
            if t not in T:
                T.add(t)
                f[t] = 1
            else:
                f[t] += 1
            S.add(s_)
            if i == len(trace) - 1:
                AS.add(s_)
            s = s_
    TS = (S, E, T, s0, AS)
    return TS, f


def condense(L, TS1, f, Treshold):  # этап 2: построение конденсированной системы переходов
    f1 = round(len(L) * Treshold) - 1
    S1, E1, T1, s0, AS1 = TS1
    S2, E2, T2, AS2 = set(), E1, set(), AS1
    for t in T1:
        if f[t] > f1:
            T2.add(t)
    S2.add(s0)
    for t in T2:
        s, a, s_ = t
        S2.add(s_)
    TS2 = (S2, E1, T2, s0, AS2)
    return TS2, f


def calculate_s_d(s, activity):  # временное состояние для каждого перехода
    return "".join(s) + "X" + "".join(activity)


def exist_event(s, activity, S3, T3):
    for s_ in S3:
        if (s, activity, s_) in T3:
            return s_
    return False


def replay_trace(trace, TS3, f, complete_traces, dzeta, TT):  # этап 1 алгоритма восстановления: проигрывание трассы
    S3, E3, T3, s0, AS3 = TS3
    if tuple(trace) in complete_traces:
        return True
    s = s0
    for i in range(len(trace)):
        s_ = exist_event(s, trace[i], S3, T3)
        s_d = calculate_s_d(s, trace[i])
        if s_:
            if s_ == s_d:
                t = (s, trace[i], s_d)
                f[t] += 1
                dzeta[tuple(trace)] = (i, s)
                return False
            s = s_
        else:
            S3.add(s_d)
            t = (s, trace[i], s_d)
            T3.add(t)
            TT.add(t)
            f[t] = 1
            dzeta[tuple(trace)] = (i, s)
            return False
    dzeta[tuple(trace)] = (len(trace), s)
    complete_traces.add(tuple(trace))
    return True


def restate_TS(L, TS3, f, complete_traces, dzeta, V_wsc, TT):  # этап 2 алгоритма восстановления: реконструкия системы переходов
    S3, E3, T3, s0, AS3 = TS3
    s0_swc = ("XXXXXXXXXXX",) # состояние ловушка
    max_wind_size = 0
    for el in L:
        max_wind_size = max(max_wind_size, len(el))
    for trace in L:
        i, s = dzeta[tuple(trace)]
        if i == len(trace):
            continue
        s_d = calculate_s_d(s, trace[i])
        t = (s, trace[i], s_d)
        if t not in TT:
            continue
        wnd_size = round(max_wind_size * f[t] * V_wsc / len(L))
        if wnd_size == 0:
            s_ = s0_swc
        else:
            s_ = tuple(trace[i - wnd_size + 1: i + 1])
        t_ = (s, trace[i], s_)
        S3.remove(s_d)
        S3.add(s_)
        T3.remove(t)
        T3.add(t_)
        TT.remove(t)
        f[t_] = f[t]
        if i == len(trace):
            AS3.add(s_)
    return


def reduce(L, TS3, f, V_wsc):  # этап 3: построение редуцированной системы переходов
    complete_traces = set()
    TT = set()
    dzeta = dict()
    while True:
        unreplayable_traces = False
        for trace in L:
            if not replay_trace(trace, TS3, f, complete_traces, dzeta, TT):
                unreplayable_traces = True
        if unreplayable_traces:
            restate_TS(L, TS3, f, complete_traces, dzeta, V_wsc, TT)
        if not unreplayable_traces:
            break
    return TS3


def reduction_algorythm(L, A, Treshold, V_wsc): # полный алгоритм
    TS1, f = prefix_tree(L, A)
    TS2, f = condense(L, TS1, f, Treshold)
    TS3 = reduce(L, TS2, f, V_wsc)
    return TS3


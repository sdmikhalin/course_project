import pandas as pd
import pm4py
from algo import reduction_algorythm
from metrics import prec, simpl
from examples import L1, L2, A1, A2


print("Введите путь к файлу: ", end="") # L3.csv
file_path = input()

df = pd.read_csv(file_path).head(10000)

print("Введите название колонки case_id в файле: ", end="") # Case ID
input_case_id = input()
print("Введите название колонки activity в файле: ", end="") # activityNameNL
input_activity = input()
print("Введите название колонки timestamp в файле: ", end="") # Complete Timestamp
input_timestamp = input()

event_log = pm4py.format_dataframe(
    df,
    case_id=input_case_id,
    activity_key=input_activity,
    timestamp_key=input_timestamp
)

L = [] # журнал событий в ввиде списка трасс
for case in pm4py.convert_to_event_log(event_log):
    trace_activities = [event['concept:name'] for event in case] # каждая трасса - список событий
    L.append(trace_activities)

print("Введите параметр Treshold: ", end="")
input_treshold = float(input())
print("Введите параметр Vwsc: ", end="")
input_vwsc = float(input())


A = pm4py.get_event_attribute_values(L, "concept:name") # множество уникальных активностей
TS = reduction_algorythm(L, A, input_treshold, input_vwsc)
S, E, T, s0, AS = TS
print("Состояния перехода: ")
for el in T:
    print(el)
print("Точность:", prec(TS, L, A))
print("Простота:", simpl(TS))


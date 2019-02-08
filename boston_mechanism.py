"""
Boston Mechanism customized for ICU,s graduate research advisor selection system
Author: Someya Naoki
2019/1/30
This source code is written by Python3.
"""
import numpy as np
import collections
import sys
import random
import time
import copy
import pandas as pd
from collections import Counter

studs = []
labs = []
capa = []
studs_list = {}
labs_list = {}
student_ninki = []
labo_ninki = []
labo_sample_distribution = [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,5,5,5,5,5,6,6,6,6,6,6,6,6,7,7,7,7,7,7,8,8,8,8,8,9,9,9,9,10,10,10,10,11,12,13,13,13,14,15,15,15,15,18,19,21,24,24,27,28,33,36]

def python_list_add(in1, in2):
    wrk = np.array(in1) + np.array(in2)
    return wrk.tolist()

def merge_dict_add_values(d1, d2):
    return dict(Counter(d1) + Counter(d2))

def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]

def create_list(STUDENT_NUM,LABO_NUM,TEIIN,STUDENT_LIST_NUM):

    # 引数の数だけ学生を用意
    students = np.arange(STUDENT_NUM)
    students = students.tolist()
    global studs
    studs = students

    global student_ninki
    student_ninki = []
    for student in students:
        student_ninki.append(student + 1)

    student_ninki = np.sqrt(student_ninki)
    student_ninki_round = []
    for ninki in student_ninki:
        student_ninki_round.append(int(round(ninki)))
    student_ninki = student_ninki_round
    print("\n▼ 学生の人気分布\n", student_ninki)

    # 引数の数だけ教員を用意
    labos = np.arange(LABO_NUM)
    labos = labos.tolist()
    global labs
    labs = labos

    global labo_ninki
    labo_ninki = []
    global labo_sample_distribution
    for key in labos:
        for var in range(labo_sample_distribution[key]):
            labo_ninki.append(key)
    print("\n▼ 教員の人気分布\n", labo_ninki)

    # 学生の希望順位表を作成
    students = {key: None for key in students}
    for student in students:
        student_pref = []
        labo_ninki_neo = labo_ninki
        # 学生の選好リストを入力値まで作成
        for var in range(0,STUDENT_LIST_NUM):
            first = random.choice(labo_ninki_neo)
            student_pref.append(first)
            for num in labo_ninki_neo:
                if num == first:
                    labo_ninki_neo = remove_values_from_list(labo_ninki_neo, num)
        students[student] = student_pref

    global studs_list
    studs_list = students
    print("\n▼ 学生の選好順位リスト\n",studs_list)

    global firststuds_list
    firststuds_list = studs_list.copy()


    # 教員の希望順位表を作成
    labos = {key: None for key in labos}
    for labo in labos:
        labo_pref = []
        labo_chozen_count = 0;
        student_ninki_neo = []
        for key in studs_list.keys():
            for value in studs_list[key]:
                if labo == value:
                    labo_chozen_count += 1
                    for var in range(0, student_ninki[key]):
                        student_ninki_neo.append(key)
        for var in range(0,labo_chozen_count):
            labo_choice = random.choice(student_ninki_neo)
            labo_pref.append(labo_choice)
            for num in student_ninki_neo:
                if num == labo_choice:
                    student_ninki_neo = remove_values_from_list(student_ninki_neo, num)
        labos[labo] = labo_pref

    global labs_list
    labs_list = labos
    print("\n▼ 教員の選好順位リスト\n",labs_list)

    # 教員の選好リストの平均人数を算出
    semi_list_sum = 0;
    i = 0;
    for key in labs_list:
        semi_list_sum += len(labs_list[key])
        i += 1
    global labo_list_average
    labo_list_average = semi_list_sum / i
    print('\n▼ 初回マッチングの教員の選好リストの平均人数\n',labo_list_average)


    global capa
    capa = {key: None for key in labos}
    for item in capa:
        capa[item] = TEIIN

def boston_mechanism(studs, labs, capa, studs_list, labs_list):
    labos_addmitted = [-1 for i in studs_list] # The school each student has been admitted to.
    student_count = [0 for i in studs] # The number of students each school has been admitted.
    unadmitted = [i for i in range(len(studs_list)) if labos_addmitted[i] == -1]
    choice = 0 # The current choice level
    # While there are students left without admitted schools
    admit_count = 1;
    while admit_count > 0:
        admit_count = 0;
        print("#" * 50)
        print("Choice level: {}".format(choice+1))
        # For each school...
        for labo in range(len(labs)):
            # ...with empty spots left
            if student_count[labo] == capa[labo]:
                continue
            # Consider the students who who rather choose a null school at this
            # choice level
            # if choice < 4:
            null_students = [i for i in unadmitted if len(studs_list[i]) > choice and studs_list[i][choice] == -1]
            # Assign those school to a null school
            for ns in null_students:
                labos_addmitted[ns] = -100
                # print("Student {} gets admitted to a null labo.".format(studs[ns]))
            # print("Students with null choice at choice level {}: {}".format(choice+1, [I[i] for i in null_students]))
            # Consider only the students who listed the current school as their current choice
            choiced_students = [i for i in unadmitted if len(studs_list[i]) > choice and studs_list[i][choice] == labo]
            # print("Students with choice {} at school {}: {}".format(choice+1,
            #     C[sc], [I[i] for i in students]))
            # Assign seats to the school following the priority order of the
            # students at the school until there are no spots left at the school
            # or no students left that put the school as their top priority
            i = 0
            while not student_count[labo] == capa[labo] and len(labs_list[labo]) > i:
                # Check if the student on the school's priority list are in the
                # group of unadmitted students
                if labs_list[labo][i] in choiced_students:
                    # Assign the student to the school
                    labos_addmitted[labs_list[labo][i]] = labo
                    student_count[labo] += 1
                    print("Student {} admitted to labo {}.".format(studs[labs_list[labo][i]], labs[labo]))
                    admit_count += 1;
                i += 1
        # Get the new group of unadmitted students
        unadmitted = [i for i in range(len(studs_list)) if labos_addmitted[i] == -1]
        choice += 1
        # for student, school in enumerate(labos_addmitted):
        #     print("{}:  {}.".format(studs[student], labs[school] if school > -1 else "Null school"))
    return labos_addmitted


def boston_mechanism_add(studs_add, labs_add, capa_add, studs_list_add, labs_list_add):
    labos_addmitted = [-1 for i in studs_list_add] # The school each student has been admitted to.
    student_count = [0 for i in labs_add] # The number of students each school has been admitted.
    unadmitted = [i for i in range(len(studs_list_add)) if labos_addmitted[i] == -1]
    choice = 0 # The current choice level
    # While there are students left without admitted schools
    admit_count = 1;
    while admit_count > 0:
        admit_count = 0;
        print("#" * 50)
        print("Choice level: {}".format(choice+1))
        # For each school...
        for labo in range(len(labs_add)):
            # ...with empty spots left
            if student_count[labo] == capa_add[labo]:
                continue
            # Consider the students who who rather choose a null school at this
            # choice level
            # if choice < 4:
            null_students = [i for i in unadmitted if len(studs_list_add[i]) > choice and studs_list_add[i][choice] == -1]
            # Assign those school to a null school
            for ns in null_students:
                labos_addmitted[ns] = -100
                print("Student {} gets admitted to a null labo.".format(studs_add[ns]))
            # print("Students with null choice at choice level {}: {}".format(choice+1, [I[i] for i in null_students]))
            # Consider only the students who listed the current school as their current choice
            choiced_students = []
            for i in unadmitted:
                if len(studs_list_add[i]) > choice:
                    if studs_list_add[i][choice] == labo:
                        choiced_students.append(i)
            # choiced_students = [i for i in unadmitted if len(studs_list_add[i]) > choice and studs_list_add[i][choice] == labo]
            # print("Students with choice {} at school {}: {}".format(choice+1,
            #     C[sc], [I[i] for i in students]))
            # Assign seats to the school following the priority order of the
            # students at the school until there are no spots left at the school
            # or no students left that put the school as their top priority
            i = 0
            while not student_count[labo] == capa_add[labo] and len(labs_list_add[labo]) > i:
                # Check if the student on the school's priority list are in the
                # group of unadmitted students
                if labs_list_add[labo][i] in choiced_students:
                    # Assign the student to the school
                    labos_addmitted[labs_list_add[labo][i]] = labo
                    student_count[labo] += 1
                    print("Student {} admitted to labo {}.".format(studs[labs_list_add[labo][i]], labs_add[labo]))
                    admit_count += 1;
                i += 1
        # Get the new group of unadmitted students
        unadmitted = [i for i in range(len(studs_list_add)) if labos_addmitted[i] == -1]
        choice += 1
        # for student, school in enumerate(labos_addmitted):
        #     print("{}:  {}.".format(studs[student], labs[school] if school > -1 else "Null school"))
    return labos_addmitted

if __name__ == '__main__':
    start = time.time()
    trials = []
    STUDENT_NUM = int(sys.argv[1])
    LABO_NUM = int(sys.argv[2])
    TEIIN = int(sys.argv[3])
    STUDENT_LIST_NUM = int(sys.argv[4])
    TRIAL_NUM = int(sys.argv[5])
    # 計算回数
    count = 0;
    # 試行回数
    loop = 0;
    # 評価
    sum_stability = [];
    sum_strategy = [];
    sum_student_rank_rate = {}
    sum_student_utility = 0;
    sum_labo_utility = 0;
    sum_count = 0;
    sum_labo_rank_rate_mean = 0;
    sum_labo_rank_rate_std = 0;
    sum_labo_rank_rate_mean = 0;
    sum_labo_list_num = [0 * LABO_NUM];
    average_student_rank_list = []
    average_labo_rank_list = []
    sum_under_student_num_list = []

    for var in range(0, TRIAL_NUM):
        count = 1

        print("#" * 50)
        print("ここから%s回目"%(count))
        print("#" * 50)

        create_list(STUDENT_NUM,LABO_NUM,TEIIN,STUDENT_LIST_NUM)

        labos_addmitted = boston_mechanism(studs, labs, capa, studs_list, labs_list)
        print("*" * 50)
        std = np.arange(len(studs))
        std = std.tolist()
        std = {key: None for key in std}
        for value in std:
            std[value] = labos_addmitted[value]
        print("\n▼ マッチング結果\n",std)

        #############################################################

        #2回目のマッチングに臨む学生
        nomatch_students = []
        adjust_student_list = []
        adjust_labo_list = []
        for value in std:
            if std[value] == -1:
                nomatch_students.append(value)
        nomatch_students_list = copy.deepcopy(nomatch_students)
        nomatch_students = {key: None for key in nomatch_students}
        studs_add = []
        studs_add = np.arange(len(nomatch_students))
        studs_add = studs_add.tolist()

        # もしマッチできなかった学生がいたら以下を実行
        if studs_add != []:

            count += 1
            print("#" * 50)
            print("ここから%s回目"%(count))
            print("#" * 50)

            print("\n▼ マッチできなかった学生\n",nomatch_students)
            print("\n▼ マッチできなかった学生(index)\n",studs_add)

            #2回目のマッチングに臨む教員
            for key in std:
                value = std[key]
                if value != -1:
                    capa[value] -= 1;
            for key in list(capa):
                if capa[key] == 0:
                    del capa[key]
            print("\n▼ 定員にまだ空きのある教員with定員\n",capa)
            free_labos = []
            for key in capa:
                free_labos.append(key)
            print("\n▼ 定員にまだ空きのある教員\n",free_labos)
            labs_add = []
            labs_add = np.arange(len(capa))
            labs_add = labs_add.tolist()
            print("\n▼ 定員にまだ空きのある教員(index)\n",labs_add)

            # 定員にまだ空きのある教員の残り定員
            capa_add = []
            for key in capa:
                capa_add.append(capa[key])
            print("\n▼ 定員にまだ空きのある教員の残り定員\n",capa_add)

            # labo_ninkiを更新
            for var in labo_ninki:
                if var >= len(labs_add):
                    labo_ninki = remove_values_from_list(labo_ninki, var)

            # 2回目の学生の選考リストを作る
            studs_list_add = {key: None for key in studs_add}
            for applicant in studs_list_add:
                student_pref = []
                labo_ninki_neo = labo_ninki
                for var in range(0,STUDENT_LIST_NUM):
                    first = random.choice(labo_ninki_neo)
                    student_pref.append(first)
                    for num in labo_ninki_neo:
                        if num == first:
                            labo_ninki_neo = remove_values_from_list(labo_ninki_neo, num)
                studs_list_add[applicant] = student_pref
            print("\n▼ マッチできなかった学生の新たな選考リスト\n",studs_list_add)

            # 2回目の教員の選考リストを作る
            labs_list_add = {key: None for key in labs_add}
            for program in labs_list_add:
                labo_pref = []
                labo_chozen_count = 0;
                student_ninki_neo = []
                for key in studs_list_add.keys():
                    for value in studs_list_add[key]:
                        if program == value:
                            labo_chozen_count += 1
                            for var in range(0, student_ninki[key]):
                                student_ninki_neo.append(key)
                for var in range(0,labo_chozen_count):
                    labo_choice = random.choice(student_ninki_neo)
                    labo_pref.append(labo_choice)
                    for num in student_ninki_neo:
                        if num == labo_choice:
                            student_ninki_neo = remove_values_from_list(student_ninki_neo, num)
                labs_list_add[program] = labo_pref
            print("\n▼ 今回のマッチングでまだ空きのある教員の新たな選考リスト\n",labs_list_add)

            labos_list_add = {}
            labo_count = 0;
            for key in labs_list_add:
                if labs_list_add[key] != []:
                    labos_list_add.update({labo_count:labs_list_add[key]})
                    labo_count += 1;

            labos_addmitted = boston_mechanism_add(studs_add, labs_add, capa_add, studs_list_add, labs_list_add)
            print("*" * 50)
            std_add = np.arange(len(studs_add))
            std_add = std_add.tolist()
            std_add = {key: None for key in std_add}
            for value in std_add:
                std_add[value] = labos_addmitted[value]
            print("\n▼ マッチング結果\n",std_add)
            print("*" * 50)

            free_labos_index = 0;
            for i, v in enumerate(nomatch_students):
                print(std_add[i])
                if std_add[i] == -1:
                    print("free_labos_index", free_labos_index)
                    free_labos_index = -1
                    print("free_labos_index", free_labos_index)
                else:
                    free_labos_index = std_add[i]
                nomatch_students[v] = free_labos[free_labos_index]
            print("マッチング結果（学生側）：", nomatch_students)
            # 学生の選好順位リスト
            adjust_student_list = sorted(nomatch_students.items())
            adjust_student_list = dict(adjust_student_list)
            for i, v in enumerate(adjust_student_list):
                student_list_index = studs_list_add[i]
                for var in range(len(student_list_index)):
                    i = student_list_index[var]
                    student_list_index[var] = free_labos[i]
                adjust_student_list[v] = student_list_index
            print("index調整済み学生の選好順序リスト", adjust_student_list)

            # 教員の選好順位リスト
            adjust_labo_list = {key: [] for key in free_labos}
            for i, v in enumerate(adjust_labo_list):
                labo_list_index = labs_list_add[i]
                for var in range(len(labo_list_index)):
                    ll_index = labo_list_index[var]
                    ns_count = 0
                    for key in nomatch_students:
                        if ns_count == ll_index:
                            labo_list_index[var] = key
                        ns_count += 1
                adjust_labo_list[v] = labo_list_index
            print("index調整済み教員の選好順序リスト", adjust_labo_list)

        loop += 1
        print("\n")
        print("#" * 50)
        print("%s周目結果"%(loop))
        print("#" * 50)
        print("\n全ての学生がマッチするまでの計算回数：%s回 "%(count))
        trials.append(count)

        # 第1回目のマッチング結果(学生側)
        std.update(nomatch_students)
        studentMatchs = std
        print("\n▼ 第%s回目のマッチング結果(学生側)\n"%(loop),studentMatchs)

        # 最終的な選好順序リスト(学生側)
        for key in adjust_student_list:
            for var in studs_list:
                if key == var:
                    studs_list[var].extend(adjust_student_list[key])
        print("\n▼ 最終的な選好順序リスト(学生側)\n",studs_list)

        programMatchs = np.arange(LABO_NUM)
        programMatchs = programMatchs.tolist()
        programMatchs = {key: [] for key in programMatchs}
        for key in programMatchs:
            for var in studentMatchs:
                if key == studentMatchs[var]:
                    programMatchs[key].append(var)
        print("\n▼ 第%s回目のマッチング結果(教員側)\n"%(loop),programMatchs)

        # 最終的な選好順序リスト(学生側)
        for key in adjust_labo_list:
            for var in labs_list:
                if key == var:
                    labs_list[var].extend(adjust_labo_list[key])
        print("\n▼ 最終的な選好順序リスト(教員側)\n",labs_list)

        # 学生のランク
        students_rank = np.arange(STUDENT_NUM)
        students_rank = students_rank.tolist()
        students_rank = {key: None for key in students_rank}
        i = 0;
        for s_rank in students_rank:
            i = studentMatchs[s_rank]
            students_rank[s_rank] = studs_list[s_rank].index(i)
        print("\n▼ 学生のランク\n", students_rank)

        # 教員のランク
        labo_rank = np.arange(LABO_NUM)
        labo_rank = labo_rank.tolist()
        labo_rank = {key: [] for key in labo_rank}
        for l_rank in labo_rank:
            for v in programMatchs[l_rank]:
                labo_rank[l_rank].append(labs_list[l_rank].index(v))
        print("\n▼ 教員のランク\n", labo_rank)

    #############################################################

        print("#" * 50)
        print("評価軸")
        print("#" * 50)

        # (a)安定性
        stability = 0;
        envy = 0;
        for sr_key in students_rank:
            if students_rank[sr_key] >= 1:
                for i in range (0, students_rank[sr_key]):
                    envy = studs_list[sr_key][i]
                    for var in programMatchs[envy]:
                        if labs_list[envy].index(sr_key) < programMatchs[envy].index(var):
                            stability += 1;
                            break;
        print("\n(a)安定性：", stability)

        # (b)耐戦略性
        strategy = 0;
        strategy_option = 0;
        swith = 0;
        for sr_key in students_rank:
            if students_rank[sr_key] >= 1:
                for i in range (0, students_rank[sr_key]):
                    strategy_option = studs_list[sr_key][i]
                    if swith == 1:
                        swith = 0
                    else:
                        for var in programMatchs[strategy_option]:
                            if labs_list[strategy_option].index(sr_key) < programMatchs[strategy_option].index(var):
                                strategy += 1;
                                swith = 1;
                                break;
        print("\n(b)耐戦略性：", strategy)

        # (c)効率性
        student_max_rank = max(students_rank.values())
        student_rank_rate = np.arange(student_max_rank + 1)
        student_rank_rate = student_rank_rate.tolist()
        student_rank_rate = {key: 0 for key in student_rank_rate}
        for key in student_rank_rate:
            for sr_key in students_rank:
                if students_rank[sr_key] == key:
                    student_rank_rate[key] += 1;
        print("\n(c)効率性：")
        print("student_rank_rate: ", student_rank_rate)
        for key in student_rank_rate:
            print("第%s希望の教員とマッチした学生数：%s （%s）"%(key + 1, student_rank_rate[key], student_rank_rate[key] / STUDENT_NUM * 100))

        print(sum_student_rank_rate)
        sum_student_rank_rate = merge_dict_add_values(sum_student_rank_rate, student_rank_rate)
        print(sum_student_rank_rate)

        average_student_rank = 0
        for key in student_rank_rate:
            rank_num = key + 1
            average_student_rank += rank_num * student_rank_rate[key]
        average_student_rank = average_student_rank/STUDENT_NUM
        print("=>学生の効率性：", average_student_rank)

        average_labo_rank = 0
        for l_rank in labo_rank:
            for value in labo_rank[l_rank]:
                rank_num = value + 1
                average_labo_rank += rank_num
        average_labo_rank = average_labo_rank/LABO_NUM
        print("=>教員の効率性：", average_labo_rank)

        # (d)衡平性
        kakusa_list = []
        for key in students_rank:
            kakusa_list.append(students_rank[key])
        kakusa_list_nparray = np.array(kakusa_list)
        kakusa_list_nparray += 1;
        kakusa_list_df = pd.DataFrame(pd.Series(kakusa_list_nparray.ravel()).describe()).transpose()
        print("\n(d)格差：\n", kakusa_list_df)
        print("・平均順位：", kakusa_list_df.mean()["mean"])
        print("・順位の標準偏差：", kakusa_list_df.mean()["std"])

        # (e)実現可能性
        print("\n(e)実現可能性：")
        print("・完了までの回数：", count)
        labo_list_num = [] # 各教員の選好リスト数
        labo_list_average = 0; # 教員の選好リスト数の平均
        for key in labs_list:
            labo_list_num.append(len(labs_list[key]))
        labo_list_num.sort()
        sum_labo_list_num = python_list_add(sum_labo_list_num, labo_list_num)
        labo_list_num_nparray = np.array(labo_list_num)
        labo_list_num_df = pd.DataFrame(pd.Series(labo_list_num_nparray.ravel()).describe()).transpose()
        print("・教員の選好リストの数\n", labo_list_num_df)


        sum_stability.append(stability)
        sum_strategy.append(strategy)
        sum_student_utility += average_student_rank
        average_student_rank_list.append(average_student_rank)
        sum_labo_utility += average_labo_rank
        average_labo_rank_list.append(average_labo_rank)
        sum_count += count
        sum_labo_rank_rate_mean += kakusa_list_df.mean()["mean"]
        sum_labo_rank_rate_std += kakusa_list_df.mean()["std"]

        sum_under_student_num = 0
        for key in student_rank_rate:
            if key > 1:
                print(student_rank_rate[key])
                sum_under_student_num += student_rank_rate[key]
        sum_under_student_num_list.append(sum_under_student_num)
        print(sum_under_student_num_list)

    #############################################################

    print("#" * 50)
    print("最終結果")
    print("#" * 50)

    print("\n(a)安定性：", sum_stability)
    sum_stability_nparray = np.array(sum_stability)
    sum_stability_df = pd.DataFrame(pd.Series(sum_stability_nparray.ravel()).describe()).transpose()
    print(sum_stability_df)
    print("・平均値：", sum_stability_df.mean()["mean"])
    print("・標準偏差：", sum_stability_df.mean()["std"])

    print("\n(b)耐戦略性：", sum_strategy)
    sum_strategy_nparray = np.array(sum_strategy)
    sum_strategy_df = pd.DataFrame(pd.Series(sum_strategy_nparray.ravel()).describe()).transpose()
    print(sum_strategy_df)
    print("・平均値：", sum_strategy_df.mean()["mean"])
    print("・標準偏差：", sum_strategy_df.mean()["std"])

    print("\n")
    for key in sum_student_rank_rate:
            print("第%s希望の教員とマッチした学生数の平均：%s （%s）"%(key + 1, sum_student_rank_rate[key]/TRIAL_NUM, sum_student_rank_rate[key] / STUDENT_NUM * 100/TRIAL_NUM))
    print("\n(c)学生の効率性：")
    print(average_student_rank_list)
    print("・平均順位：", sum_labo_rank_rate_mean/TRIAL_NUM)
    print("・順位の標準偏差：", sum_labo_rank_rate_std/TRIAL_NUM)

    print("\n(d)教員の効率性：")
    print(average_labo_rank_list)
    print("・平均順位：", sum_labo_utility/TRIAL_NUM)
    average_labo_rank_list_nparray = np.array(average_labo_rank_list)
    average_labo_rank_list_df = pd.DataFrame(pd.Series(average_labo_rank_list_nparray.ravel()).describe()).transpose()
    print("・順位の標準偏差：", average_labo_rank_list_df.mean()["std"])

    print("\n(e)学生間の格差：")
    print("・第3希望以下の教員に所属した学生数：", sum_under_student_num_list)
    sum_under_student_num_list_nparray = np.array(sum_under_student_num_list)
    sum_under_student_num_list_df = pd.DataFrame(pd.Series(sum_under_student_num_list_nparray.ravel()).describe()).transpose()
    print(sum_under_student_num_list_df)
    print("・平均値：", sum_under_student_num_list_df.mean()["mean"])
    print("・標準偏差：", sum_under_student_num_list_df.mean()["std"])

    average_labo_list_num = []
    for v in sum_labo_list_num:
        v /= TRIAL_NUM
        average_labo_list_num.append(v)
    print("\n(f)教員の負担：")
    print('・各教員の選好リスト数の平均(昇順)')
    print(average_labo_list_num)
    average_labo_list_num_nparray = np.array(average_labo_list_num)
    average_labo_list_num_df = pd.DataFrame(pd.Series(average_labo_list_num_nparray.ravel()).describe()).transpose()
    print(average_labo_list_num_df)

    print("\n(g)実現可能性：")
    print(trials)
    print("・平均計算回数：", sum_count/TRIAL_NUM)
    average = sum_count / loop
    trials_nparray = np.array(trials)
    df = pd.DataFrame(pd.Series(trials_nparray.ravel()).describe()).transpose()
    print(df)

    elapsed_time = time.time() - start
    print("\n・アルゴリズム計算時間の平均")
    print("{0}".format(elapsed_time/TRIAL_NUM) + "[秒]\n")
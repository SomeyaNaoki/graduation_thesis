"""
DA Algorithm customized for ICU,s graduate research advisor selection system
Author: Someya Naoki
2019/1/30
This source code is written by Python3.
"""
import numpy as np
import random
import pandas as pd
import sys
import time
import collections
import copy
from collections import Counter

# 学生の選好リスト
rankApplicant = {}
firstRankApplicant = {}
# ゼミの選好リスト
rankProgram = {}
# 各ゼミの定員
positionProgram = {}
# 最終的な組み合わせ
programMatchs   = {}
# 暫定ゼミを有していない学生の集合
freeApplicant   = []
# checkApplicant  = copy.deepcopy(rankApplicant)
checkApplicant = {}
# 今回のマッチングでどのゼミともマッチできなかった学生の集合
nomatchApplicant = []
# evaluation_vars
entire_student_pref_list = {}
akiaruProgram = []
simekiriProgram = []
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
    students = np.arange(STUDENT_NUM)
    students = students.tolist()
    print("\n▼ 学生一覧\n",students)

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

    labos = np.arange(LABO_NUM)
    labos = labos.tolist()
    print("\n▼ ゼミ一覧\n",labos)

    global labo_ninki
    labo_ninki = []
    global labo_sample_distribution
    for key in labos:
        for var in range(labo_sample_distribution[key]):
            labo_ninki.append(key)
    print("\n▼ ゼミの人気分布\n", labo_ninki)

    # 学生の希望順位表を作成
    students = {key: None for key in students}
    for student in students:
        student_pref = []
        labo_ninki_neo = labo_ninki
        for var in range(0,STUDENT_LIST_NUM):
            first = random.choice(labo_ninki_neo)
            student_pref.append(first)
            for num in labo_ninki_neo:
                if num == first:
                    labo_ninki_neo = remove_values_from_list(labo_ninki_neo, num)
        students[student] = student_pref

    global rankApplicant
    rankApplicant = students
    print("\n▼ 学生の選好順位リスト\n",rankApplicant)

    global firstRankApplicant
    firstRankApplicant = rankApplicant.copy()

    global entire_student_pref_list
    entire_student_pref_list = rankApplicant.copy()

    # ゼミの希望順位表を作成
    labos = {key: None for key in labos}
    for labo in labos:
        labo_pref = []
        labo_chozen_count = 0;
        student_ninki_neo = []
        for key in rankApplicant.keys():
            for value in rankApplicant[key]:
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

    global rankProgram
    rankProgram = labos
    print("\n▼ ゼミの選好順位リスト\n",rankProgram)

    # ゼミの定員リストを作成
    labos = {key: None for key in labos}
    for labo in labos:
        labos[labo] = TEIIN

    global positionProgram
    positionProgram = labos
    print("\nゼミの定員リスト\n",positionProgram)

    global checkApplicant
    checkApplicant  = copy.deepcopy(rankApplicant)

def matching(applicant):
  '''Find the free program available to a applicant '''
  # 学生Xのマッチング開始
  print('\n')
  print("Matching Student %s"%(applicant))
  # 学生Xの選好リストを最新状態にする
  rankApplicant[applicant] = list(checkApplicant[applicant])
  '''If Applicant not have program again, remove from free Applicant '''
  # もし学生Xの選好リストが空の場合
  if(len(rankApplicant[applicant])==0):
    # 暫定ゼミがなくマッチ希望の学生の集合から学生Xを消す
    freeApplicant.remove(applicant)
    nomatchApplicant.append(applicant)
    # 学生Xはどのゼミともマッチしなかった
    print('- Student %s does not have program to check again '%(applicant))
  # もし学生Xの選好リストにゼミがある場合
  else:
    # 学生Xの先行順位表の中のゼミそれぞれに対して以下を実行
    for program in rankApplicant[applicant]:
      #Cek whether program is full or not
      # もしその候補ゼミの定員に空きがあれば
      if len(programMatchs[program]) < positionProgram[program]:
        # もし学生Xの名前が候補ゼミの選考リストに存在しなかったら
        if applicant not in rankProgram[program]:
          # 「学生Xは候補ゼミの選考リストに存在しなかった」と表示
          print('- Student %s does not exist in list applicant in labo %s '%(applicant,program))
          # 学生Xの選考リストから候補ゼミの名前を消す
          checkApplicant[applicant].remove(program)
        # もし学生Xの名前が候補ゼミの選考リストに存在したら
        else:
          # 学生Xは候補ゼミとマッチする
          programMatchs[program].append(applicant)
          # 暫定ゼミがなくマッチ希望の学生の集合から学生Xを消す
          freeApplicant.remove(applicant)
          # 「学生Xは暫定ゼミとマッチし、暫定ゼミがなくマッチ希望の学生ではない」と表示
          print('- Student %s is no longer a free applicant and is now tentatively get labo %s'%(applicant, program))
          break
      # もしその候補ゼミの定員に空きがなければ
      else:
        # 「候補ゼミの定員に空きがない」と表示
        print('- labo %s is full (%s participant) '%(program,positionProgram[program]))
        # もし学生Xの名前が候補ゼミの選考リストに存在しなかったら
        if applicant not in rankProgram[program]:
          # 「学生Xは候補ゼミの選考リストに存在しなかった」と表示
          print('- Student %s does not exist in list applicant in labo %s '%(applicant,program))
          # 学生Xの選考リストから候補ゼミの名前を消す
          checkApplicant[applicant].remove(program)
        # もし学生Xの名前が候補ゼミの選考リストに存在したら
        else :
          # get applicant who can remove,
          # 学生XをapplicantRemoveとする
          applicantRemove = applicant
          # 候補ゼミの暫定学生それぞれに対して以下を実行
          for applicantMatch in programMatchs[program]:
            # もし学生Xのほうが暫定学生よりも候補ゼミにとって希望順位が高かったら
            if rankProgram[program].index(applicantRemove) < rankProgram[program].index(applicantMatch):
              # 繰り返しにより、最も希望順位の低い学生が不採用学生となる
              applicantRemove = applicantMatch
          # もし不採用学生がいまだ学生Xだったら
          if applicantRemove==applicant:
            # 「候補ゼミの選考リストにおける学生Xの順位は他の暫定学生よりも低い」と表示
            print('- Rank Applicant %s in labo %s is bigger then other current applicant match '%(applicant,program))
            # 学生Xの選考リストから候補ゼミの名前を消す
            checkApplicant[applicant].remove(program)
          # もし不採用学生が学生Xではなかったら
          else:
            # 「学生Xは不採用学生よりも候補ゼミにとって希望順位が高い」と表示
            print('- Student %s is better than Student %s'%(applicant, applicantRemove))
            # 「不採用学生を暫定学生から外し、新しく学生Xと候補ゼミがマッチした」と表示
            print('- Making Student %s free again.. and tentatively match Student %s and labo %s'%(applicantRemove, applicant, program))

            #The new applicant have match
            # 暫定ゼミがなくマッチ希望の学生の集合から学生Xを消す
            freeApplicant.remove(applicant)
            # 学生Xは候補ゼミとマッチする
            programMatchs[program].append(applicant)

            #The old applicant is now not match anymore
            # 不採用学生を暫定ゼミがなくマッチ希望の学生の集合に加える
            freeApplicant.append(applicantRemove)
            # 不採用学生を暫定学生から外す
            programMatchs[program].remove(applicantRemove)

            break

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
        # init all applicant free and not have program
        for applicant in rankApplicant.keys():
            freeApplicant.append(applicant)
        # init programMatch
        for program in rankProgram.keys():
            programMatchs[program]=[]
        # Matching algorithm until stable match terminates
        while (len(freeApplicant) > 0):
            for applicant in freeApplicant:
                matching(applicant)
        print("\n▼ 第%s回目のマッチング結果\n"%(count),programMatchs)
        print("\n▼ 第%s回目のマッチングでどのゼミともマッチできなかった学生の人数\n"%count,len(nomatchApplicant))

        while (len(nomatchApplicant) > 0):
            count += 1
            print("#" * 50)
            print("ここから%s回目"%(count))
            print("#" * 50)
            # まだ所属ゼミが決まっていない学生の集合
            rankApplicant = {key: None for key in nomatchApplicant}
            print("\n▼ 第%s回目のマッチングの時点でまだ所属ゼミが決まっていない学生の集合\n"%count,rankApplicant)
            # 各ゼミの残り定員数
            for program in positionProgram:
                positionProgram[program] = positionProgram[program] - len(programMatchs[program])
                if positionProgram[program] == 0:
                    simekiriProgram.append(program)
                else:
                    akiaruProgram.append(program)
            # １回目のマッチを終えてのそれぞれのゼミの残り定員数
            print("\n▼ 各ゼミの残り定員数\n",positionProgram)
            print("\n▼ 募集を締め切ったゼミ\n",simekiriProgram)
            for key in list(positionProgram):
                if positionProgram[key] == 0:
                    del(positionProgram[key])
                    for var in labo_ninki:
                        if var == key:
                            labo_ninki = remove_values_from_list(labo_ninki, var)
            akiaruProgram = positionProgram.keys()
            print("\n▼ 定員にまだ空きのあるゼミ\n",akiaruProgram)
            print("\n▼ 定員にまだ空きのあるゼミの残り定員数\n",positionProgram)
            # positionProgramを初期化
            for key in positionProgram:
                positionProgram[key] = TEIIN
            if len(akiaruProgram) < 3:
                STUDENT_LIST_NUM = len(akiaruProgram)
            # 2回目の学生の選考リストを作る
            for applicant in rankApplicant:
                student_pref = []
                labo_ninki_neo = labo_ninki
                for var in range(0,STUDENT_LIST_NUM):
                    first = random.choice(labo_ninki_neo)
                    student_pref.append(first)
                    for num in labo_ninki_neo:
                        if num == first:
                            labo_ninki_neo = remove_values_from_list(labo_ninki_neo, num)
                student_priority = student_pref
                rankApplicant[applicant] = student_priority
            print("\n▼ マッチできなかった学生の新たな選考リスト\n",rankApplicant)

            for key in rankApplicant:
                for var in entire_student_pref_list:
                    if key == var:
                        entire_student_pref_list[var].extend(rankApplicant[key])

            # 2回目のゼミの選考リストを作る
            for program in rankProgram:
                labo_pref = []
                labo_chozen_count = 0;
                student_ninki_neo = []
                for key in rankApplicant.keys():
                    for value in rankApplicant[key]:
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
                rankProgram[program].extend(labo_pref)
            print("\n▼ 今回のマッチングでまだ空きのあるゼミの新たな選考リスト\n",rankProgram)
            checkApplicant  = copy.deepcopy(rankApplicant)
            # init all applicant free and not have program
            for applicant in rankApplicant.keys():
                freeApplicant.append(applicant)

            nomatchApplicant = []
            akiaruProgram = []
            simekiriProgram = []
            labo_ninki = labo_ninki

            # Matching algorithm until stable match terminates
            while (len(freeApplicant) > 0):
                for applicant in freeApplicant:
                    matching(applicant)
            print("\n▼ 第%s回目のマッチング結果(ゼミ)\n"%(count),programMatchs)
            print("\n▼ 第%s回目のマッチングでどのゼミともマッチできなかった学生の人数\n"%count,len(nomatchApplicant))

        loop += 1
        print("\n")
        print("#" * 50)
        print("%s周目結果"%(loop))
        print("#" * 50)
        print("\n全ての学生がマッチするまでの計算回数：%s回 "%(count))
        trials.append(count)

        student_num_of_each_labo = []
        for key in programMatchs:
            student_num_of_each_labo.append(len(programMatchs[key]))
        print("\n▼ 各ゼミの学生数)\n", student_num_of_each_labo)
        student_num_of_each_labo_nparray = np.array(student_num_of_each_labo)
        student_num_of_each_labo_df = pd.DataFrame(pd.Series(student_num_of_each_labo_nparray.ravel()).describe()).transpose()
        print(student_num_of_each_labo_df)

        print("\n▼ 第%s回目のマッチング結果(ゼミ側)\n"%(loop),programMatchs)
        print("\n▼ 最終的な選好順序リスト(ゼミ側)\n",rankProgram)
        studentMatchs = np.arange(STUDENT_NUM)
        studentMatchs = studentMatchs.tolist()
        studentMatchs = {key: None for key in studentMatchs}
        for key in studentMatchs:
            for var in programMatchs:
                for value in programMatchs[var]:
                    if key == value:
                        studentMatchs[key] = var
        print("\n▼ 第%s回目のマッチング結果(学生側)\n"%(loop),studentMatchs)
        print("\n▼ 最終的な選好順序リスト(学生側)\n",entire_student_pref_list)


        # ゼミの人気分布を再度作成
        labos_neo = np.arange(LABO_NUM)
        labos_neo = labos_neo.tolist()
        for key in labos_neo:
            for var in range(labo_sample_distribution[key]):
                labo_ninki.append(key)

        # 学生のランク
        students_rank = np.arange(STUDENT_NUM)
        students_rank = students_rank.tolist()
        students_rank = {key: None for key in students_rank}
        for s_rank in students_rank:
            for key in programMatchs:
                for value in programMatchs[key]:
                    if value == s_rank:
                        for frav in firstRankApplicant[s_rank]:
                            if frav == key:
                                rank = firstRankApplicant[value].index(key)
                                students_rank[s_rank] = rank
        for s_rank in students_rank:
            if students_rank[s_rank] is None:
                students_rank[s_rank] = 3
        print("\n▼ 学生のランク\n", students_rank)

        # ゼミのランク
        labo_rank = np.arange(LABO_NUM)
        labo_rank = labo_rank.tolist()
        labo_rank = {key: [] for key in labo_rank}
        for l_rank in labo_rank:
            for pm_value in programMatchs[l_rank]:
                labo_rank[l_rank].append(rankProgram[l_rank].index(pm_value))
        print("\n▼ ゼミのランク\n", labo_rank)

        #############################################################

        print("#" * 50)
        print("%s周目評価軸"%(loop))
        print("#" * 50)

        # (a)安定性
        stability = 0;
        envy = 0;
        for sr_key in students_rank:
            if students_rank[sr_key] >= 1:
                for i in range (0, students_rank[sr_key]):
                    envy = entire_student_pref_list[sr_key][i]
                    for var in programMatchs[envy]:
                        if rankProgram[envy].index(sr_key) < programMatchs[envy].index(var):
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
                    strategy_option = entire_student_pref_list[sr_key][i]
                    if swith == 1:
                        swith = 0;
                    else:
                        for var in programMatchs[strategy_option]:
                            if rankProgram[strategy_option].index(sr_key) < programMatchs[strategy_option].index(var):
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
        for key in student_rank_rate:
            print("第%s希望のゼミとマッチした学生数：%s （%s）"%(key + 1, student_rank_rate[key], student_rank_rate[key] / STUDENT_NUM * 100))
        sum_student_rank_rate = merge_dict_add_values(sum_student_rank_rate, student_rank_rate)

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

        kakusa_list = []
        for key in students_rank:
            kakusa_list.append(students_rank[key])
        kakusa_list_nparray = np.array(kakusa_list)
        kakusa_list_nparray += 1;
        kakusa_list_df = pd.DataFrame(pd.Series(kakusa_list_nparray.ravel()).describe()).transpose()
        print("\n(d)格差：\n", kakusa_list_df)
        print("・平均順位：", kakusa_list_df.mean()["mean"])
        print("・順位の標準偏差：", kakusa_list_df.mean()["std"])
        # (g)実現可能性
        print("\n(e)実現可能性：")
        print("・完了までの回数：", count)
        labo_list_num = [] # 各ゼミの選好リスト数
        labo_list_average = 0; # ゼミの選好リスト数の平均
        # ゼミの選好リストの人数を算出
        for key in rankProgram:
            labo_list_num.append(len(rankProgram[key]))
        labo_list_num.sort()
        sum_labo_list_num = python_list_add(sum_labo_list_num, labo_list_num)
        labo_list_num_nparray = np.array(labo_list_num)
        labo_list_num_df = pd.DataFrame(pd.Series(labo_list_num_nparray.ravel()).describe()).transpose()
        print("・ゼミの選好リストの数\n", labo_list_num_df)

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
            print("第%s希望のゼミとマッチした学生数の平均：%s （%s）"%(key + 1, sum_student_rank_rate[key]/TRIAL_NUM, sum_student_rank_rate[key] / STUDENT_NUM * 100/TRIAL_NUM))
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
    print("・第3希望以下のゼミに所属した学生数：", sum_under_student_num_list)
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
    print('・各ゼミの選好リスト数の平均(昇順)')
    print(average_labo_list_num)
    average_labo_list_num_nparray = np.array(average_labo_list_num)
    average_labo_list_num_df = pd.DataFrame(pd.Series(average_labo_list_num_nparray.ravel()).describe()).transpose()
    print(average_labo_list_num_df)

    print("\n(g)実現可能性：")
    print(trials)
    print("・平均計算回数：", sum_count/TRIAL_NUM)
    average = sum_count / loop
    trials_nparray = np.array(trials)
    # print(trials_nparray)
    df = pd.DataFrame(pd.Series(trials_nparray.ravel()).describe()).transpose()
    print(df)

    elapsed_time = time.time() - start
    print("\n・アルゴリズム計算時間の平均")
    print("{0}".format(elapsed_time/TRIAL_NUM) + "[秒]\n")
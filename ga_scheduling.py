# -*- coding: utf-8 -*-
import random
from scoop import futures

from deap import base
from deap import creator
from deap import tools
from deap import cma

NEED_PEOPLE =[]

# Class of Employees
class Employee(object):
  def __init__(self, no, name, age, manager, wills):
    self.no = no
    self.name = name
    self.age = age
    self.manager = manager

    # will is Time zone, 1 is Morning、2 is %%!Noon、3 is Night。
    # 例）mon_1 is Monday Morning
    self.wills = wills

  def is_applicated(self, box_name):
    return (box_name in self.wills)

# Class of Shift
# 3(Morning,Noon,Night) * 7day * 10person = 210 dimension tuple
class Shift(object):
  # Definision of frame
  SHIFT_BOXES = [
    'mon_1', 'mon_2', 'mon_3',
    'tue_1', 'tue_2', 'tue_3',
    'wed_1', 'wed_2', 'wed_3',
    'thu_1', 'thu_2', 'thu_3',
    'fri_1', 'fri_2', 'fri_3',
    'sat_1', 'sat_2', 'sat_3',
    'sun_1', 'sun_2', 'sun_3']

  # Anticipated people
  REQUIRED_PEOPLE = NEED_PEOPLE

  def __init__(self, list):
    if list == None:
      self.make_sample()
    else:
      self.list = list
    self.employees = []

  # Generate random data
  def make_sample(self):
    sample_list = []
    for num in range(210):
      sample_list.append(random.randint(0, 1))
    self.list = tuple(sample_list)

  # Divide tuple by user
  def slice(self):
    sliced = []
    start = 0
    for num in range(10):
      sliced.append(self.list[start:(start + 21)])
      start = start + 21
    return tuple(sliced)

  # Assign frame by user
  def print_inspect(self):
    user_no = 0
    for line in self.slice():
      print("ユーザ%d" % user_no)
      print(line)
      user_no = user_no + 1

      index = 0
      for e in line:
        if e == 1:
          print(self.SHIFT_BOXES[index])
        index = index + 1

  # CSV assign
  def print_csv(self):
    for line in self.slice():
      print(','.join(map(str, line)))

  def get_boxes_by_user(self, user_no):
    line = self.slice()[user_no]
    return self.line_to_box(line)

  def line_to_box(self, line):
    result = []
    index = 0
    for e in line:
      if e == 1:
        result.append(self.SHIFT_BOXES[index])
      index = index + 1
    return result

  def get_user_nos_by_box_index(self, box_index):
    user_nos = []
    index = 0
    for line in self.slice():
      if line[box_index] == 1:
        user_nos.append(index)
      index += 1
    return user_nos

  def get_user_nos_by_box_name(self, box_name):
    box_index = self.SHIFT_BOXES.index(box_name)
    return self.get_user_nos_by_box_index(box_index)

  def abs_people_between_need_and_actual(self):
    result = []
    index = 0
    for need in self.REQUIRED_PEOPLE:
      actual = len(self.get_user_nos_by_box_index(index))
      result.append(abs(need - actual))
      index += 1
    return result

  def not_applicated_assign(self):
    count = 0
    for box_name in self.SHIFT_BOXES:
      user_nos = self.get_user_nos_by_box_name(box_name)
      for user_no in user_nos:
        e = self.employees[user_no]
        if not e.is_applicated(box_name):
          count += 1
    return count

  def few_work_user(self):
    result = []
    for user_no in range(10):
      e = self.employees[user_no]
      ratio = float(len(self.get_boxes_by_user(user_no))) / float(len(e.wills))
      if ratio < 0.5:
        result.append(e)
    return result

  def no_manager_box(self):
    result = []
    for box_name in self.SHIFT_BOXES:
      manager_included = False
      user_nos = self.get_user_nos_by_box_name(box_name)
      for user_no in user_nos:
        e = self.employees[user_no]
        if e.manager:
          manager_included = True
      if not manager_included:
        result.append(box_name)
    return result

  def three_box_per_day(self):
    result = []
    for user_no in range(10):
      boxes = self.get_boxes_by_user(user_no)
      wdays = []
      for box in boxes:
        wdays.append(box.split('_')[0])
      wday_names = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
      for wday_name in wday_names:
        if wdays.count(wday_name) == 3:
          result.append(wday_name)
    return result

day_of_week = ["Monday","Tuesday","Wednesday","Thurday","Friday","Saturday","Sunday"]
day_time = ["Morning","Noon","Evening"]

for i in range(len(day_of_week)):
    exec("""NEED_PEOPLE.append(int(input("Input required number of persons on " + day_of_week[i] + " " + day_time[0] + ":")))""")
    exec("""NEED_PEOPLE.append(int(input("Input required number of persons on " + day_of_week[i] + " " + day_time[1] + ":")))""")
    exec("""NEED_PEOPLE.append(int(input("Input required number of persons on " + day_of_week[i] + " " + day_time[2] + ":")))""")
    

e0 = Employee(0, "George Washington", 40, False, ['mon_1', 'tue_1', 'wed_1', 'thu_1', 'fri_1', 'sat_1', 'sun_1'])
e1 = Employee(1, "John Adams", 21, False, ['mon_1', 'mon_2', 'mon_3', 'wed_1', 'wed_2', 'wed_3','fri_1', 'fri_2', 'fri_3'])
e2 = Employee(2, "Thomas Jefferson", 18, False, ['sat_1', 'sat_2', 'sat_3', 'sun_1', 'sun_2', 'sun_3'])
e3 = Employee(3, "James Madison", 35, True, ['mon_1', 'mon_2', 'mon_3',
                                     'tue_1', 'tue_2', 'tue_3',
                                     'wed_1', 'wed_2', 'wed_3',
                                     'thu_1', 'thu_2', 'thu_3',
                                     'fri_1', 'fri_2', 'fri_3',
                                     'sat_1', 'sat_2', 'sat_3',
                                     'sun_1', 'sun_2', 'sun_3'
                                    ])
e4 = Employee(4, "James Monroe", 19, False, ['mon_3', 'tue_3', 'wed_3', 'thu_3', 'fri_3', 'sat_3', 'sun_3'])
e5 = Employee(5, "John Quincy Adams", 43, True, ['mon_1', 'mon_2', 'mon_3',
                                     'tue_1', 'tue_2', 'tue_3',
                                     'wed_1', 'wed_2', 'wed_3',
                                     'thu_1', 'thu_2', 'thu_3',
                                     'fri_1', 'fri_2', 'fri_3'
                                    ])
e6 = Employee(6, "Andrew Jackson", 25, False, ['fri_1', 'fri_2', 'fri_3',
                                     'sat_1', 'sat_2', 'sat_3',
                                     'sun_1', 'sun_2', 'sun_3'
                                    ])
e7 = Employee(7, "Martin Van Buren", 22, False, ['mon_2', 'tue_2', 'wed_2', 'thu_2', 'fri_2', 'sat_2', 'sun_2'])
e8 = Employee(8, "William Henry Harrison", 18, False, ['mon_3', 'tue_3', 'wed_3', 'thu_3', 'fri_3', 'sat_3', 'sun_3'])
e9 = Employee(9, "John Tyler", 30, True, ['thu_1', 'thu_2', 'thu_3',
                                     'fri_1', 'fri_2', 'fri_3',
                                     'sat_1', 'sat_2', 'sat_3',
                                     'sun_1', 'sun_2', 'sun_3'
                                    ])

employees = [e0, e1, e2, e3, e4, e5, e6, e7, e8, e9]

creator.create("FitnessPeopleCount", base.Fitness, weights=(-10.0, -100.0, -1.0, -100.0, -10.0))
creator.create("Individual", list, fitness=creator.FitnessPeopleCount)

toolbox = base.Toolbox()

toolbox.register("map", futures.map)

toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, 210)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalShift(individual):
  s = Shift(individual)
  s.employees = employees

  people_count_sub_sum = sum(s.abs_people_between_need_and_actual()) / 210.0
  not_applicated_count = s.not_applicated_assign() / 210.0
  few_work_user = len(s.few_work_user()) / 10.0
  no_manager_box = len(s.no_manager_box()) / 21.0
  three_box_per_day = len(s.three_box_per_day()) / 70.0
  return (not_applicated_count, people_count_sub_sum, few_work_user, no_manager_box, three_box_per_day)

toolbox.register("evaluate", evalShift)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)

toolbox.register("select", tools.selTournament, tournsize=3)

if __name__ == '__main__':
    pop = toolbox.population(n=300)
    CXPB, MUTPB, NGEN = 0.6, 0.5, 500 # Crossing probability, Mutation probability, Loop count of the evolution computation

    print("Evolution Start")

    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):  #zip function is variables Simultaneous loop (In this code, it's pop and fitnesses.)
        ind.fitness.values = fit

    print("  %i 's evaluation'" % len(pop))

    for g in range(NGEN):
        print("-- %i generation --" % g)
        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))

        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        print("  %i 's evaluation'" % len(invalid_ind))

        pop[:] = offspring

        index = 1
        for v in ind.fitness.values:
          fits = [v for ind in pop]

          length = len(pop)
          mean = sum(fits) / length
          sum2 = sum(x*x for x in fits)
          std = abs(sum2 / length - mean**2)**0.5

          print(("* parameter%d") % index)
          print(("  Min %s" % min(fits)))
          print(("  Max %s" % max(fits)))
          print(("  Avg %s" % mean))
          print(("  Std %s" % std))
          index += 1

    print("-- Evolution Complete --")

    best_ind = tools.selBest(pop, 1)[0]
    s = Shift(best_ind)
    s.print_csv()

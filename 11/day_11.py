import pprint
from functools import reduce

pp = pprint.PrettyPrinter(indent=4)

# NUM_ROUNDS = 20 # part 1
NUM_ROUNDS = 10000 # part 2


def run():
  with open('day_11/input_example.txt') as f:

    # parse monkey input
    input = [m.strip() for m in f.read().split('Monkey ') if m]
    monkeys = {}
    for i, data in enumerate(input):
      monkeys[i] = {}
      items, op, divisible_test, true_dest, false_dest = [
        l.split(': ')[1] for l in data.split('\n')[1:]
      ]
      items = [int(i) for i in items.split(', ')]
      monkeys[i]['items'] = items
      monkeys[i]['op'] = op.split(' ')[2:]
      monkeys[i]['divisible_test'] = int(divisible_test.split(' ')[2])
      monkeys[i]['true_dest'] = int(true_dest.split(' ')[3])
      monkeys[i]['false_dest'] = int(false_dest.split(' ')[3])
      monkeys[i]['count'] = 0

    safe_modulo = reduce((lambda x, y: x * y), [m['divisible_test'] for m in monkeys.values()])

    for round in range(1, NUM_ROUNDS + 1):
      print(f'Round {round}')
      # loop through monkeys
      for k in sorted(monkeys.keys()):
        m = monkeys[k]
        print(f'-->Monkey {k}: {m}')

        # loop through items
        while m['items']:
          m['count'] += 1
          worry_level = m['items'].pop(0)
          # print(f'item: {worry_level}')
          new_worry_level = worry_level
          op = [worry_level if s == 'old' else s for s in m['op']]
          if op[1] == '*':
            # new_worry_level = int((int(op[0]) * int(op[2])) / 3) # Part 1
            new_worry_level = int(op[0]) * int(op[2]) # Part 2
          elif op[1] == '+':
            # new_worry_level = int((int(op[0]) + int(op[2])) / 3) # Part 1
            new_worry_level = int(op[0]) + int(op[2]) # Part 2

          new_worry_level = new_worry_level % safe_modulo
          dest_monkey_id = m['true_dest'] if new_worry_level % m['divisible_test'] == 0 else m['false_dest']
          monkeys[dest_monkey_id]['items'].append(new_worry_level)

    # Get 2 highest monkeys, multiple for monkey bizniz
    print('finding n highest')
    n_largest = sorted(monkeys.items(), key=lambda item: item[1]['count'])[::-1][:2]
    counts = [m[1]['count'] for m in n_largest]
    monkey_business = reduce((lambda x, y: x * y), counts)

    pp.pprint(monkey_business)

if __name__ == '__main__':
    run()


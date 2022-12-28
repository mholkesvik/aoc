def run():
    with open('day_10/input.txt') as f:
      input = f.read().strip().split("\n")
      x = 1
      x_arr = []
      for cmd in input:
        if cmd == 'noop':
          x_arr.append(x)
        else:
          # cmd: addx
          x_arr.append(x)
          x_arr.append(x)
          add_val = int(cmd.split(' ')[1])
          x += add_val
    
    # part 1
    # special_cycles = list(range(20, len(x_arr), 40))
    # print([(i, x_arr[i]) for i in special_cycles])
    # print(sum([(i*x_arr[i]) for i in special_cycles]))

    # part 2
    msg = ''
    for cycle, x in enumerate(x_arr):
      cycle = cycle % 40
      sprite = ['.'] * 41
      sprite[x] = '#'
      sprite[min(40, x+1)] = '#'
      sprite[min(40, x+2)] = '#'
      msg += sprite[cycle+1]

      if cycle == 39:
        msg += '\n'

    print(msg)
      
import sys
import heapq
# runs on python3.8.1
# initiating fringe
fringe = []
closed = []
nodes_expanded = 0
nodes_generated = 1

# find_route input_filename origin_city destination_city heuristic_filename
# read input file(s)
# input_file = 'input1.txt'
# origin_city = 'Bremen'
# destination_city = 'Kassel'
# heuristic_filename = 'h_kassel.txt'

input_file = sys.argv[1]
origin_city = sys.argv[2]
destination_city = sys.argv[3]
if len(sys.argv) > 4:
  heuristic_filename = sys.argv[4]  
else:
  heuristic_filename = None
lines = open(input_file,'r').read().split('\n')
s = {}
for i in lines:
  if i == 'END OF INPUT':
    break
  x = i.rfind(' ')
  s[i[:x]] = float(i[x+1:])
h = {}
if heuristic_filename:
  heuristics = open(heuristic_filename,'r').read().split('\n')
  for i in heuristics:
    if i == 'END OF INPUT':
      break
    x = i.split(' ')
    h[x[0]] = float(x[1])

# get heuristic cost
def get_heuristic_cost(city):
  if city in h.keys():
    return h[city]
  return 0

# get connected city cost
def get_cost(city1, city2):
  if (city1+' '+city2) in s.keys():
    cost = s[city1+' '+city2]
  elif (city2+' '+city1) in s.keys():
    cost = s[city2+' '+city1]
  else:
    cost = -1
  return cost

# expand city
def expand_city(city):
  city_name = city['city']
  if city_name in closed:
    return None
  results = []
  for i in lines:
    if i == 'END OF INPUT':
      break
    if city_name in i:
      c = i.split(' ')
      if city_name == c[0]:
        results.append({'city': c[1], 'parent':city, 'total_cost': city['total_cost'] + get_cost(c[1],city_name), 'heuristic_cost': get_heuristic_cost(c[1])})
      else:
        results.append({'city': c[0], 'parent':city,'total_cost': city['total_cost'] + get_cost(c[0],city_name), 'heuristic_cost': get_heuristic_cost(c[0])})
  add_results_to_fringe(results)
  closed.append(city_name)
  return results

# add to fringe
def add_results_to_fringe(results):
  for result in results:
    heapq.heappush(fringe, (result['total_cost'] + result['heuristic_cost'], result))

# get node to expand
def get_next_node():
  return heapq.heappop(fringe)

# print output
def print_output(node):
  l =[]
  while node is not None:
    if node['parent'] == None:
      break
    l.append(node['parent']['city'] + " to " +node['city'] +", "+str(node['total_cost'] - node['parent']['total_cost']) + " km")
    node = node['parent']
  print('\n'.join(l[::-1]))

# begin logic
start = {'city': origin_city, 'parent': None, 'total_cost': 0, 'heuristic_cost': get_heuristic_cost(origin_city)}
add_results_to_fringe([start])

found = False
while len(fringe) > 0:
  nodes_expanded +=1
  node = get_next_node()
  if node:
    node = node[1]
  if node['city'] == destination_city:
    found = True
    break
  l = expand_city(node)
  if l is not None:
    nodes_generated += len(l)
print('nodes expanded:',nodes_expanded)
print('nodes generated:',nodes_generated)
if found:  
  print('distance:',node['total_cost'])
  print('route:')
  print_output(node)
if not found:
  print('distance: infinity')
  print('route:\nnone')

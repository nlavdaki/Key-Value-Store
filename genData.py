import argparse
import random
import string
import pandas as pd
import os
import json



# Define a function that converts a data type string to the corresponding data type
def convert_type(type_str):
    if type_str == 'int':
        return int
    elif type_str == 'str':
        return str
    elif type_str == 'float':
        return float




#data func
def create_database(keyFile, d, n, m, l):
# read the keyfile
  z = pd.read_csv(keyFile,delimiter=" ", usecols=['keys','keystype'])
  dk = pd.DataFrame(z)
# dk is the df which contains the possible nesteing keys and their types nest_key is the name of the keys and type_nest_key their types
  dk['keystype'] = dk['keystype'].apply(convert_type)
  nest_key = dk['keys']
  type_nest_key = dk['keystype']
  keys = nest_key.to_dict()
  keys_list = list(keys.values())
  keys_length = len(keys_list)

  database = {}

#n : number of lines
  for row in range(n):
    current = {}
#m maximum number of keys in every value
    for i in range(0,m):
#this is a process to link the random key generated for each value to the type of its value generated for it
      dk_indexed = dk.reset_index()

      value_key = keys_list[random.randint(0, keys_length - 1)]

      row_index = dk_indexed[dk_indexed['keys'] == value_key]['index'].iloc[0]
      n_value_type = type_nest_key.loc[row_index]
      value_type = n_value_type
#value data generation for each type
      ll = random.randint(0, l)
      if value_type == int:
        value = random.randint(0, 10 ** l)
      elif value_type == float:
        value = random.uniform(0, 10 ** l)
      elif value_type == str:
        value = "".join(random.choices(string.ascii_lowercase, k=ll)) or ' '
      else:
        value = ' '
      current_nested = current
#d: the depth aka the maximum number of nests in each value
      for depth in range(0,d):
        new_key = keys_list[random.randint(0, keys_length - 1)]
        if new_key not in current_nested:
          current_nested[new_key] = {}
        current_nested = current_nested[new_key]
      current_nested[value_key] = value

    database['key' + str(row + 1)] = current
  return database




def main(args):
    # call create_database function
    result = create_database(keyFile=args.keyFile, d=args.d, n=args.n, m=args.m, l=args.l)

    keyFile_dir = os.path.dirname(args.keyFile)
    datafile_path = os.path.join(keyFile_dir, 'dataToIndex.txt')



    with open(datafile_path, "w") as f:
        for key, value in result.items():
            json_str = json.dumps(value, separators=(',', ': '))
            f.write('"{}": {}'.format(key, json_str))
            f.write('\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--keyFile", help="path to key file", type=str, required=True)
    parser.add_argument("-n", help="number of lines", type=int, required=True)
    parser.add_argument("-d", help="depth", type=int, required=True)
    parser.add_argument("-l", help="length", type=int, required=True)
    parser.add_argument("-m", help="maximum number of keys in every value", type=int, required=True)

    args = parser.parse_args()


    print("The process has Started!")
    main(args=args)
    print(f"The process has Finished!")




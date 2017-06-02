import os
import re
import sys
from copy import copy

from pyth.plugins.plaintext.writer import PlaintextWriter
from pyth.plugins.rtf15.reader import Rtf15Reader

try:
   os.chdir(os.path.dirname(sys.argv[0]))  # change work directory
except:
   pass


def main():
   file_list = os.listdir('./doc')
   rtf_files = list()
   for file_name in file_list:
      if file_name.split('.')[-1] == 'rtf':
         rtf_files.append(file_name)

   print('Select file: (0 to exit)')
   for index, rtf_file in enumerate(rtf_files):
      print('{} {}'.format(index + 1, rtf_file))
   try:
      selection = int(input('\n'))
   except:
      sys.exit(1)
   if selection == 0:
      sys.exit(0)

   with open('./doc/' + rtf_files[selection - 1]) as f:
      lines = parse_rtf(f)

   parsed = parse_doc(lines)

   print(parsed['Chapter'])
   for item in parsed['Multiple Choice']:
      print(item['Q'])
      print(item['A'])
      print(item['B'])
      print(item['C'])
      print(item['D'])
      raw_input('\n')
      print(item['Ans'])
      print(item['Section'])
      print(item['Difficulty'])
      raw_input('\n')
   for item in parsed['Essay']:
      print(item['Q'])
      raw_input('\n')
      print(item['Ans'])
      print(item['Section'])
      print(item['Difficulty'])
      raw_input('\n')
   for item in parsed['True/False']:
      print(item['Q'])
      raw_input('\n')
      print(item['Ans'])
      print(item['Section'])
      print(item['Difficulty'])
      raw_input('\n')


def parse_rtf(file):
   doc = Rtf15Reader.read(file)
   return PlaintextWriter.write(doc).getvalue().split('\n')


def parse_doc(lines):
   result = {
      'Chapter': '',
      'Multiple Choice': [],
      'Essay': [],
      'True/False': []
   }

   parse_flag = ''
   model_mc = {
      'Q': '',
      'A': '',
      'B': '',
      'C': '',
      'D': '',
      'Ans': '',
      'Section': '',
      'Difficulty': ''
   }
   model_e_or_tf = {
      'Q': '',
      'Ans': '',
      'Section': '',
      'Difficulty': ''
   }
   for line in lines:
      if line == 'Multiple Choice':
         parse_flag = 'mc'
      elif line == 'Essay':
         parse_flag = 'e'
      elif line == 'True/False':
         parse_flag = 'tf'
      elif re.match(r'Chapter: Chapter \d*', line):
         result['Chapter'] = line.split(': ')[-1]
      else:

         if parse_flag == 'mc':
            if re.match(r'^\d{1,2}\.[\w ]*', line):
               model_mc['Q'] = line
            elif re.match('^A\)[\w ]*', line):
               model_mc['A'] = line
            elif re.match('^B\)[\w ]*', line):
               model_mc['B'] = line
            elif re.match('^C\)[\w ]*', line):
               model_mc['C'] = line
            elif re.match('^D\)[\w ]*', line):
               model_mc['D'] = line
            elif re.match('^Ans:[ ]*[A-Z]', line):
               model_mc['Ans'] = line
            elif re.match('^(Section|Feedback):? \d{1,2}\.\d{1,2}.*', line):
               model_mc['Section'] = line
            elif re.match('^Difficulty: \w*', line):
               model_mc['Difficulty'] = line
               mc = copy(model_mc)
               result['Multiple Choice'].append(mc)


         elif parse_flag == 'e':
            if re.match(r'^\d{1,2}\.[\w ]*', line):
               model_e_or_tf['Q'] = line
            elif re.match('^Ans:[\w ]*', line):
               model_e_or_tf['Ans'] = line
            elif re.match('^(Section|Feedback):? \d{1,2}\.\d{1,2}.*', line):
               model_e_or_tf['Section'] = line
            elif re.match('^Difficulty: \w*', line):
               model_e_or_tf['Difficulty'] = line
               e = copy(model_e_or_tf)
               result['Essay'].append(e)

         elif parse_flag == 'tf':
            if re.match(r'^\d{1,2}\.[\w ]*', line):
               model_e_or_tf['Q'] = line
            elif re.match('^Ans:[\w ]*', line):
               model_e_or_tf['Ans'] = line
            elif re.match('^(Section|Feedback):? \d{1,2}\.\d{1,2}.*', line):
               model_e_or_tf['Section'] = line
            elif re.match('^Difficulty: \w*', line):
               model_e_or_tf['Difficulty'] = line
               e = copy(model_e_or_tf)
               result['True/False'].append(e)

   return result


if __name__ == '__main__':
   while True:
      main()

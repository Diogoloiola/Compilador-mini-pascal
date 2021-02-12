from typing import Text
import sys
from lexico import analisadorLexico

if __name__ == "__main__":
   lexico = analisadorLexico('main.pas')
   lexico.criaTabela()
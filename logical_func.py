from itertools import permutations
import pandas as pd

class LogicalTable:
    def __init__(self, letters, true='T', false='F'):
        self.letters = letters
        self.true = true
        self.false = false
        self.table = self.create_table(len(self.letters), self.letters)
    
    def __str__(self):
        return self.table
    
    def __repr__(self):
        return f'{self.table.to_string(index=False)}'

    def create_table(self, n, letters):
        a = set(list(permutations(self.false*n+self.true*n, n)))
        t = set(a)
        table = pd.DataFrame(t, columns=letters)
        return table.sort_values(letters, ascending=False)
    
    def logical_table(self):
        return self.table.replace({
            f'{self.true}': True,
            f'{self.false}': False
        })
    
    #return with parenthesis if is an expression
    #return without parenthesis if as preposition
    def return_with_parenthesis(self, x):
        if(len(x) == 1):
            return f'{x}'
        elif((x[0] == '~' or x[0] == ')') and x[-1] == ')'):
            return f'{x}'
        else:
            return f'({x})'
            
    def AND(self, x, y):
        x_title = self.return_with_parenthesis(x)
        y_title = self.return_with_parenthesis(y)
        lt = self.logical_table()
        lt[f'{x_title} ^ {y_title}'] = lt.apply(lambda w: w[f'{x}'] and w[f'{y}'], axis=1)
        self.table = lt.replace({
            True: f'{self.true}',
            False: f'{self.false}'
        })
    
    def OR(self, x, y):
        x_title = self.return_with_parenthesis(x)
        y_title = self.return_with_parenthesis(y)
        lt = self.logical_table()
        lt[f'{x_title} v {y_title}'] = lt.apply(lambda w: w[f'{x}'] or w[f'{y}'], axis=1)
        self.table = lt.replace({
            True: f'{self.true}',
            False: f'{self.false}'
        })
    
    def NOT(self, x):
        lt = self.logical_table()
        x_title = self.return_with_parenthesis(x)
        lt[f'~{x_title}'] = lt.apply(lambda w: not w[f'{x}'], axis=1)
        self.table = lt.replace({
            True: f'{self.true}',
            False: f'{self.false}'
        })
        
    def arrow(self, x, y):
        lt = self.logical_table()
        lt[f'{x} => {y}'] = lt.apply(lambda w: not w[f'{x}'] or w[f'{y}'], axis=1)
        self.table = lt.replace({
            True: f'{self.true}',
            False: f'{self.false}'
        })
    
    def double_arrow(self, x, y):
        lt = self.logical_table()
        lt[f'{x} <=> {y}'] = lt.apply(lambda w: w[f'{x}'] == w[f'{y}'], axis=1)
        self.table = lt.replace({
            True: f'{self.true}',
            False: f'{self.false}'
        })
        
    def generate_complete_table(self, x, y):
        self.AND(x, y)
        self.OR(x, y)
        self.NOT(x)
        self.NOT(y)
        self.arrow(x, y)
        self.double_arrow(x, y)
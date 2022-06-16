import re
import numpy as np


def variables(equation_list):
    """
    determines different type of variables used in the equations.
    """
    variables = {}
    pattern_var = re.compile(r'[a-zA-Z]+')
    for equation in equation_list:
        vars = re.findall(pattern_var, equation)
        for elmnt in vars:
            if elmnt not in variables:
                variables[elmnt] = []
    num_var = len(variables)
    return num_var, variables

def coeff(equation_list, variables):

    coeff = []

    for eq in equation_list:
        # coeff_element = []
        for var in variables:
            pattern_term = re.compile(r'[-]?\d*'+var)
            lhs_limit = eq.index("=")
            # var_coeff = pattern_term.finditer(eq)
            indx = {}
            for idx,obj in enumerate(pattern_term.finditer(eq)):
                indx[idx] = obj.span()
            coeff_sum = []
            # print(eq, var)
            for elements in indx:
                start_idx = indx[elements][0]
                end_idx = indx[elements][1]
                if indx[elements][0] < lhs_limit:
                    try:
                        coeff_sum.append(int(eq[start_idx:end_idx].strip(var)))
                    except:
                        coeff_sum.append(1)
                elif indx[elements][0] > lhs_limit:
                    try:
                        coeff_sum.append(-int(eq[start_idx:end_idx].strip(var)))
                    except:
                        coeff_sum.append(1)
            coeff_sum_1 = sum(coeff_sum)
            variables[var].append(coeff_sum_1)
        
    
    for keys in variables:
        coeff.append(variables[keys])
    transposed_tuples = list(zip(*coeff))
    transposed = [list(sublist) for sublist in transposed_tuples]

    return transposed, variables.keys()

def solve_equation(coeff):
    solution = {}
    return solution

def dict_append(eq):
    for i in eq:
        # print(i)
        if 'x' in coeff:
            coeff['x'].append(int(re.findall(pattern_x, i)[0]) if re.findall(pattern_x, i)[0] not in ["+","-"] else 1)
        else:
            coeff['x'] = [int(re.findall(pattern_x, i)[0]) if re.findall(pattern_x, i)[0] not in ["+","-"] else 1]
        
        if 'y' in coeff:
            coeff['y'].append(int(re.findall(pattern_y, i)[0]) if re.findall(pattern_y, i)[0] not in ["+","-"] else 1)
        else:
            coeff['y'] = [int(re.findall(pattern_y, i)[0]) if re.findall(pattern_y, i)[0] not in ["+","-"] else 1]
        
        if 'z' in coeff:
            coeff['z'].append(int(re.findall(pattern_z, i)[0]) if re.findall(pattern_z, i)[0] not in ["+","-"] else 1)
        else:
            coeff['z'] = [int(re.findall(pattern_z, i)[0]) if re.findall(pattern_z, i)[0] not in ["+","-"] else 1]

        cons.append(re.findall(pattern_number, i))
    # print(x)


class equation():

    def __init__(self, eq):
        self.eq = eq
        self.variables_1 = self.variables(self.eq)
        self.coeff_variables = self.coeff(self.eq, self.variables_1)
        self.coeff = self.coeff_variables[0]
        self.variables = self.coeff_variables[1]
        self.constants = self.coeff_variables[2]
    
    def variables(self, equation_list):
        variables = {}
        pattern_var = re.compile(r'[a-zA-Z]+')

        for equation in equation_list:
            vars = re.findall(pattern_var, equation)
            for elmnt in vars:
                if elmnt not in variables:
                    variables[elmnt] = []
        
        num_var = len(variables)
        if num_var > len(equation_list):
            raise SystemExit("**Error**: Number of variables more than the number of equations")
        
        return variables
    
    def coeff(self, equation_list, variables):

        coeff = []
        cons = []
        cons_pattern_1 = re.compile(r'(-?\d+)\W')
        # cons_pattern_1_1 = re.compile(r'(-?\d+)\W')
        cons_pattern_2 = re.compile(r'-?\d+$')
        for eq in equation_list:
            try:
                lhs_limit = eq.index("=")
            except ValueError:
                raise SystemExit(f"**Error** Invalid equation '{eq}'")
                
            # coeff_element = []
            for var in variables:
                pattern_term = re.compile(r'[-]?\d*'+var)
                # var_coeff = pattern_term.finditer(eq)
                indx = {}
                for idx,obj in enumerate(pattern_term.finditer(eq)):
                    indx[idx] = obj.span()
                coeff_sum = []
                # print(eq, var)
                for elements in indx:
                    start_idx = indx[elements][0]
                    end_idx = indx[elements][1]
                    if indx[elements][0] < lhs_limit:
                        try:
                            coeff_sum.append(int(eq[start_idx:end_idx].strip(var)))
                        except:
                            coeff_sum.append(1)
                    elif indx[elements][0] > lhs_limit:
                        try:
                            coeff_sum.append(-int(eq[start_idx:end_idx].strip(var)))
                        except:
                            coeff_sum.append(-1)
                coeff_sum_1 = sum(coeff_sum)
                variables[var].append(coeff_sum_1)

            #finding the constant terms and aggregating them
            sub_cons = []
            for obj in re.finditer(cons_pattern_1, eq):
                if obj.span()[0]<lhs_limit:
                    sub_cons.append(-int(obj.groups()[0]))
                else:
                    sub_cons.append(int(obj.groups()[0]))
            for obj in re.findall(cons_pattern_2, eq):
                sub_cons.append(int(obj))
            
            sub_cons = sum(sub_cons)
            # print(obj.groups()[0], obj.span(), eq[obj.span()[0]:obj.span()[1]-1])
            # if len(re.findall(cons_pattern_1, eq)) != 0:
            #     sub_cons.extend(re.findall(cons_pattern_1, eq))
            # if len(re.findall(cons_pattern_2, eq)) != 0:
            #     sub_cons.extend(re.findall(cons_pattern_2, eq))
            # sub_cons.append(re.findall(cons_pattern_2,eq))
            #print(sub_cons)
            cons.append(sub_cons)

        for keys in variables:
            coeff.append(variables[keys])
        transposed_tuples = list(zip(*coeff))
        transposed = [list(sublist) for sublist in transposed_tuples]

        return transposed, variables.keys(), cons

    def solve(self, coeff, constants):
        a = coeff
        b = constants
        x = np.linalg.solve(a,b)
        return x


if __name__ == '__main__':   
    eq = ['x+6y+8z=34','5x+55-9y-3z=6']

    eq1 = equation(eq)
    print(eq1.coeff)
    print(eq1.constants)
    print(eq1.solve(eq1.coeff, eq1.constants))

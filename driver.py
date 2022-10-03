from problog.logic import Term, Clause
from problog.program import PrologString
from problog.learning import lfi
import random
import itertools

def add_learning_params(model, nfeats, nranks):
    feats = ['f({})'.format(i) for i in range(nfeats)]
    permus = list(itertools.combinations_with_replacement(range(1,nranks+1), nfeats))
    for j in range(len(permus)):
        permu = permus[j]
        comb = []
        for i in range(len(permu)):
            comb.append('f({})'.format(i))
            comb.append(permu[i])
        if j < len(permus) - 1:
            model += 't(_)::rank_assignment({});\n'.format(comb).replace("'","")
        else:
            model += 't(_)::rank_assignment({}).\n'.format(comb).replace("'", "")
    return model

def add_ethical_features(model, nfeats, nsits):
    for i in range(nfeats):
        model += '''
        type(f({}), '-').
        '''.format(i)
    for j in range(nsits):
        model += '''
        has_plan(go(right), s({})).
        has_plan(go(left), s({})).
        '''.format(j,j)
        for i in range(nfeats):
            if random.choice([True, False]):
                model += '''
                has_feature(f({}), go(right), s({})).
                '''.format(i,j)
            else:
                model += '''
                has_feature(f({}), go(left), s({})).
                '''.format(i, j)
    return model

def add_ranks(model,nranks):
    ranks = '''
    rank(R) :- between(1, {}, R).
    '''.format(nranks)
    return model + ranks

def get_opinions(nopis,nsits):
    opinions = []
    for i in range(nopis):
        opi = []
        for j in range(nsits):
            right = random.choice([True,False])
            left = not right
            opi.append((Term('best',Term('go',Term('right')), Term('s',Term(str(j)))),right))
            opi.append((Term('best',Term('go',Term('left')), Term('s',Term(str(j)))),left))
            # opi.append((Term('best(go(left), s({}))'.format(j)), left))
        opinions.append(opi)
    return opinions

def get_base_model():
    with open('experiments/model.pl', 'r') as file:
        return file.read()

def get_model(nfeats,nranks,nsits):
    model = get_base_model()
    model = add_ethical_features(model,nfeats,nsits)
    model = add_ranks(model,nranks)
    model = add_learning_params(model,nfeats,nranks)
    return model

def run_test(model,opinions):
    score, weights, atoms, iteration, lfi_problem = lfi.run_lfi(
        PrologString(model), opinions)

    print(lfi_problem.get_model())


def main():
    nsits = 20
    nfeats = 20
    nranks = 2
    nopis = 5
    random.seed(0)
    model = get_model(nfeats,nranks,nsits)
    opinions = get_opinions(nopis,nsits)
    run_test(model,opinions)


if __name__ == "__main__":
    main()

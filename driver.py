from problog.program import PrologString
from problog.learning import lfi
import random
import itertools
import time
import contextlib

# Default values
nsits = 5
nfeats = 4
nfeats_plan = 2
nranks = 2
nopis = 10
time_limit = 180

model_file = 'experiments/exp_model.pl'
opi_file = 'experiments/exp_opinions.pl'
base_file = 'experiments/base.pl'

def add_learning_params(model, nfeats, nranks):
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

def add_ethical_features(model, nfeats, nsits, nfeats_plan):
    for i in range(nfeats):
        model += '''
        type(f({}), '-').
        '''.format(i)
    for j in range(nsits):
        model += '''
        has_plan(go(right), s({})).
        has_plan(go(left), s({})).
        '''.format(j,j)
        feats = random.sample(range(nfeats), nfeats_plan*2)
        for i in feats[:nfeats_plan]:
            model += '''
            has_feature(f({}), go(right), s({})).
            '''.format(i,j)
        for i in feats[nfeats_plan:]:
            model += '''
            has_feature(f({}), go(left), s({})).
            '''.format(i, j)
    return model

def add_ranks(model,nranks):
    ranks = '''
    rank(R) :- between(1, {}, R).
    max_rank({}).
    '''.format(nranks,nranks)
    return model + ranks

def get_opinions(nopis,nsits):
    opinions = ''
    for i in range(nopis):
        for j in range(nsits):
            right = random.choice([True,False])
            left = not right
            opinions += 'evidence(best(go(right),s({})),{}).\n'.format(j,right)
            opinions += 'evidence(best(go(left),s({})),{}).\n'.format(j,left)
        if i < nopis - 1:
            opinions += '---\n'
    return opinions

def get_base_model():
    with open(base_file, 'r') as file:
        return file.read()

def get_model(nfeats, nranks, nsits, nfeats_plan):
    model = get_base_model()
    model = add_ethical_features(model, nfeats, nsits, nfeats_plan)
    model = add_ranks(model,nranks)
    model = add_learning_params(model,nfeats,nranks)
    return model

def run_test(nfeats,nranks,nsits,nfeats_plan,nopis):
    random.seed(0)
    model = get_model(nfeats, nranks, nsits, nfeats_plan)
    random.seed(0)
    opinions = get_opinions(nopis, nsits)
    write_input_files(model, opinions)
    with contextlib.redirect_stdout(None):
        lfi.main([model_file, opi_file])

def write_input_files(model,opinions):
    with open(model_file, "w") as text_file:
        text_file.write(model)
    with open(opi_file, "w") as text_file:
        text_file.write(opinions)


def test_features(nfeats_plan):
    min_features = 2*nfeats_plan
    max_features = 100
    print('Testing features')
    print('features,time')
    for i in range(min_features, max_features+1):
        start = time.time()
        run_test(i, nranks, nsits, nfeats_plan, nopis)
        end = time.time()
        elapsed = end - start
        print('{},{}'.format(i, elapsed))
        if elapsed > time_limit:
            return


def test_ranks():
    min_ranks = 2
    max_ranks = 100
    print('Testing ranks')
    print('ranks,time')
    for i in range(min_ranks, max_ranks+1):
        start = time.time()
        run_test(nfeats, i, nsits, nfeats_plan, nopis)
        end = time.time()
        elapsed = end - start
        print('{},{}'.format(i, elapsed))
        if elapsed > time_limit:
            return

def test_opis():
    min_opis = 1
    max_opis = 1000
    print('Testing opis')
    print('opis,time')
    for i in range(min_opis, max_opis+1):
        start = time.time()
        run_test(nfeats, nranks, nsits, nfeats_plan, i)
        end = time.time()
        elapsed = end - start
        print('{},{}'.format(i, elapsed))
        if elapsed > time_limit:
            return


def main():
    test_features(1)
    test_features(2)
    test_features(3)
    test_ranks()
    test_opis()



if __name__ == "__main__":
    main()

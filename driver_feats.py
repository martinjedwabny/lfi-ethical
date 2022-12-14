from problog.program import PrologString
from problog.learning import lfi
import random
import itertools
import time
import contextlib
import os

# Default values
nsits = 5
nfeats = 4
nfeats_plan = 2
nranks = 4
nopis = 10
time_limit = 180

model_file = 'experiments/exp_model.pl'
opi_file = 'experiments/exp_opinions.pl'
base_file = 'experiments/base_feats.pl'

def add_learning_params(model, nfeats, nranks, max_asgs=100000000):
    model += '\n'
    for i in range(nfeats):
        for j in range(nranks):
            if j < nranks - 1:
                model += 't(_)::has_rank(f({}),{});\n'.format(i,j+1).replace("'","")
            else:
                model += 't(_)::has_rank(f({}),{}).\n\n'.format(i,j+1).replace("'","")
    return model


def add_ethical_features(model, nfeats, nsits, nfeats_plan):
    model += '\n\n'
    for i in range(nfeats):
        model += "type(f({}), '-').\n".format(i)
    model += 'ethical_features({}).\n'.format(['f({})'.format(i) for i in range(nfeats)]).replace("'","")
    for j in range(nsits):
        model += 'has_plan(go(right), s({})).\n'.format(j)
        model += 'has_plan(go(left), s({})).\n'.format(j)
        feats = random.sample(range(nfeats), nfeats_plan*2)
        for i in feats[:nfeats_plan]:
            model += 'has_feature(f({}), go(right), s({})).\n'.format(i,j)
        for i in feats[nfeats_plan:]:
            model += 'has_feature(f({}), go(left), s({})).\n'.format(i, j)
    return model

def add_ranks(model,nranks):
    ranks = 'rank(R) :- between(1, {}, R).\n'.format(nranks)
    ranks += 'max_rank({}).\n'.format(nranks)
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


def get_model(nfeats, nranks, nsits, nfeats_plan, max_asgs=100000000):
    model = get_base_model()
    model = add_ethical_features(model, nfeats, nsits, nfeats_plan)
    model = add_ranks(model,nranks)
    model = add_learning_params(model,nfeats,nranks,max_asgs)
    return model


def run_test(nfeats, nranks, nsits, nfeats_plan, nopis, max_asgs=100000000):
    random.seed(0)
    model = get_model(nfeats, nranks, nsits, nfeats_plan, max_asgs)
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


# def test_ranks(nfeats):
#     min_ranks = 2
#     max_ranks = 100
#     print('Testing ranks')
#     print('ranks,time')
#     for i in range(min_ranks, max_ranks+1):
#         start = time.time()
#         run_test(nfeats, i, 20, int(nfeats/2), nopis)
#         end = time.time()
#         elapsed = end - start
#         print('{},{}'.format(i, elapsed))
#         if elapsed > time_limit:
#             return

def test_rank_asgs():
    min_asgs = 2
    max_asgs = 1024
    print('Testing asgs')
    print('asgs,time')
    for i in range(min_asgs, max_asgs+1, 10):
        start = time.time()
        run_test(10, nranks, 4, int(nfeats/2), 5, i)
        end = time.time()
        elapsed = end - start
        print('{},{}'.format(i, elapsed))
        if elapsed > time_limit:
            return

def test_opis(nfeats):
    min_opis = 1
    max_opis = 1000
    print('Testing opis')
    print('opis,time')
    for i in range(min_opis, max_opis+1, 10):
        start = time.time()
        run_test(nfeats, nranks, 20, int(nfeats/2), i)
        end = time.time()
        elapsed = end - start
        print('{},{}'.format(i, elapsed))
        if elapsed > time_limit:
            return


def main():
    if (os.nice(-19)==-19):
        print('OS.nice OK.')
    test_features(1)
    # test_features(2)
    # test_features(3)
    # test_features(5)
    # test_features(10)
    # test_features(15)
    # test_ranks(2)
    # test_rank_asgs()
    # test_opis(4)
    # test_opis(6)
    # test_opis(8)
    # test_opis(10)
    # test_opis(15)
    return



if __name__ == "__main__":
    main()

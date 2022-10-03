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

def opinions_to_evidence(opinions):
    example = ""
    for line in opinions:
        if line.strip().startswith("---"):
            pl = PrologString(example)
            atoms = lfi.extract_evidence(pl)
            if len(atoms) > 0:
                yield atoms
            example = ""
        else:
            example += line
    if example:
        pl = PrologString(example)
        atoms = lfi.extract_evidence(pl)
        if len(atoms) > 0:
            yield atoms

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
    with open('experiments/model.pl', 'r') as file:
        return file.read()


def get_model(nfeats, nranks, nsits, nfeats_plan):
    model = get_base_model()
    model = add_ethical_features(model, nfeats, nsits, nfeats_plan)
    model = add_ranks(model,nranks)
    model = add_learning_params(model,nfeats,nranks)
    return model

def run_test():
    lfi.main(['experiments/exp_model.pl', 'experiments/exp_opinions.pl'])

def write_input_files(model,opinions):
    with open("experiments/exp_model.pl", "w") as text_file:
        text_file.write(model)
    with open("experiments/exp_opinions.pl", "w") as text_file:
        text_file.write(opinions)

def main():
    nsits = 10
    nfeats = 5
    nranks = 3
    nopis = 10
    nfeats_plan = 2
    random.seed(0)
    model = get_model(nfeats, nranks, nsits, nfeats_plan)
    opinions = get_opinions(nopis,nsits)
    write_input_files(model,opinions)
    run_test()



if __name__ == "__main__":
    main()

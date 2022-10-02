:- use_module(library(aggregate)).
0.281427747318699::rank_assignment([danger(agent), 1, danger(c1), 1, danger(c2), 1, responsible(agent), 1]); 0.04244114096646::rank_assignment([danger(agent), 1, danger(c1), 1, danger(c2), 1, responsible(agent), 2]); 0.010678487452607::rank_assignment([danger(agent), 1, danger(c1), 2, danger(c2), 2, responsible(agent), 1]); 0.072823894422998::rank_assignment([danger(agent), 1, danger(c1), 2, danger(c2), 2, responsible(agent), 2]); 0.323127403277696::rank_assignment([danger(agent), 2, danger(c1), 1, danger(c2), 1, responsible(agent), 1]); 0.200735781945672::rank_assignment([danger(agent), 2, danger(c1), 1, danger(c2), 1, responsible(agent), 2]); 0.002320025221626::rank_assignment([danger(agent), 2, danger(c1), 2, danger(c2), 2, responsible(agent), 1]); 0.066445519394241::rank_assignment([danger(agent), 2, danger(c1), 2, danger(c2), 2, responsible(agent), 2]).
amount_of_ethical_features_of_rank(R,N) :- rank(R), rank_assignment(RA), amount_of_ethical_features_of_rank(R,N,RA).
amount_of_ethical_features_of_rank(R,0,[]) :- rank(R).
amount_of_ethical_features_of_rank(R,N,[F, R1 | RA]) :- rank(R), R=R1, amount_of_ethical_features_of_rank(R,N1,RA), N is N1+1.
amount_of_ethical_features_of_rank(R,N,[F, R1 | RA]) :- rank(R), R\=R1, amount_of_ethical_features_of_rank(R,N,RA).
amount_satisfied_of_rank(A,S,R,N) :- has_plan(A,S), rank(R), rank_assignment(RA), amount_satisfied_of_rank(A,S,R,N,RA).
amount_satisfied_of_rank(A,S,R,0,[]) :- has_plan(A,S), rank(R).
amount_satisfied_of_rank(A,S,R,N,[F, R1 | RA]) :- has_plan(A,S), rank(R), R=R1, satisfies(F,A,S), amount_satisfied_of_rank(A,S,R,N1,RA), N is N1+1.
amount_satisfied_of_rank(A,S,R,N,[F, R1 | RA]) :- has_plan(A,S), rank(R), R=R1, not(satisfies(F,A,S)), amount_satisfied_of_rank(A,S,R,N,RA).
amount_satisfied_of_rank(A,S,R,N,[F, R1 | RA]) :- has_plan(A,S), rank(R), R\=R1, amount_satisfied_of_rank(A,S,R,N,RA).
min_rank(0).
max_rank(2).
rank(R) :- min_rank(Min), max_rank(Max), between(Min,Max,R).
max_val(0,0).
max_val(R,V) :- rank(R), R>0, amount_of_ethical_features_of_rank(R,N), val(R,V1), R1 is R-1, max_val(R1,V2), V is V1*N+V2.
val(0,0).
val(R,V) :- rank(R), R>0, R1 is R-1, max_val(R1,V1), V is V1+1.
val_until_rank(A,S,0,0).
val_until_rank(A,S,R,N) :- rank(R), R>0, amount_satisfied_of_rank(A,S,R,N1), val(R,V), R1 is R-1, val_until_rank(A,S,R1,N2), N is N1*V+N2.
val(A,S,N) :- max_rank(R), val_until_rank(A,S,R,N).
satisfies(F,A,S) :- has_feature(F,A,S), type(F,'+').
satisfies(F,A,S) :- type(F,'-'), not(has_feature(F,A,S)).
best(A,S) :- action(A), situation(S), has_plan(A,S), val(A,S,R), not((has_plan(B,S), A\=B, val(B,S,R1), R1>R)).
action(go(right)).
action(go(left)).
situation(s1).
situation(s2).
situation(s3).
situation(s4).
situation(s5).
situation(s6).
car(agent).
car(c1).
car(c2).
ethical_feature(danger(C)) :- car(C).
ethical_feature(responsible(agent)).
type(danger(C),'-') :- car(C).
type(responsible(agent),'-').
has_plan(go(right),s1).
has_plan(go(left),s1).
has_feature(danger(c1),go(left),s1).
has_feature(danger(c2),go(left),s1).
has_feature(danger(agent),go(left),s1).
has_plan(go(right),s2).
has_plan(go(left),s2).
has_feature(danger(c1),go(right),s2).
has_feature(danger(c2),go(right),s2).
has_feature(danger(agent),go(left),s2).
has_plan(go(right),s3).
has_plan(go(left),s3).
has_feature(danger(c1),go(right),s3).
has_feature(danger(c2),go(left),s3).
has_plan(go(right),s4).
has_plan(go(left),s4).
has_feature(danger(agent),go(right),s4).
has_feature(responsible(agent),go(right),s4).
has_feature(danger(c1),go(right),s4).
has_feature(danger(c1),go(left),s4).
has_feature(danger(c2),go(left),s4).
has_plan(go(right),s5).
has_plan(go(left),s5).
has_feature(danger(agent),go(right),s5).
has_feature(responsible(agent),go(right),s5).
has_feature(danger(agent),go(left),s5).
has_plan(go(right),s6).
has_plan(go(left),s6).
has_feature(danger(c1),go(right),s6).
has_feature(danger(c2),go(right),s6).
has_feature(danger(c1),go(left),s6).

action(go(right)).
action(go(left)).

% % max_val(?R,?V)
max_val(0,0).
max_val(R,V) :- rank(R), R > 0, amount_of_ethical_features_of_rank(R,N), val(R,V1), R1 is R-1, max_val(R1,V2), V is V1*N+V2.

% % val(?R,?V)
val(0,0).
val(R,V) :- rank(R), R > 0, R1 is R-1, max_val(R1,V1), V is V1+1.

% val_until_rank(?A,?S,?R,+N)
val_until_rank(A,S,0,0).
val_until_rank(A,S,R,N) :- rank(R), R > 0, amount_satisfied_of_rank(A,S,R,N1), val(R,V), R1 is R-1, val_until_rank(A,S,R1,N2), N is N1*V+N2.

% val(A?,S?)
val(A,S,N) :- max_rank(R), val_until_rank(A,S,R,N).

% satisfies(?F,?A,?S)
satisfies(F,A,S) :-
    has_feature(F,A,S),
    type(F,'+').
satisfies(F,A,S) :-
    type(F,'-'),
    not(has_feature(F,A,S)).

amount_of_ethical_features_of_rank(R,N) :- 
    rank(R), 
    ethical_features(Fs), 
    amount_of_ethical_features_of_rank(R,N,Fs).
amount_of_ethical_features_of_rank(R,0,[]) :- rank(R).
amount_of_ethical_features_of_rank(R,N,[F|Fs]) :- 
    rank(R), 
    has_rank(F,R),
    amount_of_ethical_features_of_rank(R,N1,Fs), 
    N is N1+1.
amount_of_ethical_features_of_rank(R,N,[F|Fs]) :- 
    rank(R), 
    has_rank(F,R1),
    R \= R1, 
    amount_of_ethical_features_of_rank(R,N,Fs).

amount_satisfied_of_rank(A,S,R,N) :- 
    has_plan(A,S), 
    rank(R), 
    ethical_features(Fs), 
    amount_satisfied_of_rank(A,S,R,N,Fs).
amount_satisfied_of_rank(A,S,R,0,[]) :- 
    has_plan(A,S), 
    rank(R).
amount_satisfied_of_rank(A,S,R,N,[F|Fs]) :- 
    has_plan(A,S), 
    rank(R), 
    has_rank(F,R),
    satisfies(F,A,S), 
    amount_satisfied_of_rank(A,S,R,N1,Fs), 
    N is N1+1.
amount_satisfied_of_rank(A,S,R,N,[F|Fs]) :- 
    has_plan(A,S), 
    rank(R), 
    has_rank(F,R),
    not(satisfies(F,A,S)), 
    amount_satisfied_of_rank(A,S,R,N,Fs).
amount_satisfied_of_rank(A,S,R,N,[F|Fs]) :- 
    has_plan(A,S), 
    rank(R), 
    has_rank(F,R1),
    R \= R1, 
    amount_satisfied_of_rank(A,S,R,N,Fs).

% best(?A,?S)
best(A,S) :-
    action(A),
    has_plan(A,S),
    val(A,S,R),
    not((has_plan(B,S), A \= B, val(B,S,R1), R1 > R)).
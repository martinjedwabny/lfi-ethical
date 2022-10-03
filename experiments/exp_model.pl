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
    rank_assignment(RA), 
    amount_of_ethical_features_of_rank(R,N,RA).
amount_of_ethical_features_of_rank(R,0,[]) :- rank(R).
amount_of_ethical_features_of_rank(R,N,[F,R1|RA]) :- 
    rank(R), 
    R = R1, 
    amount_of_ethical_features_of_rank(R,N1,RA), 
    N is N1+1.
amount_of_ethical_features_of_rank(R,N,[F,R1|RA]) :- 
    rank(R), 
    R \= R1, 
    amount_of_ethical_features_of_rank(R,N,RA).

amount_satisfied_of_rank(A,S,R,N) :- 
    has_plan(A,S), 
    rank(R), 
    rank_assignment(RA), 
    amount_satisfied_of_rank(A,S,R,N,RA).
amount_satisfied_of_rank(A,S,R,0,[]) :- 
    has_plan(A,S), 
    rank(R).
amount_satisfied_of_rank(A,S,R,N,[F,R1|RA]) :- 
    has_plan(A,S), 
    rank(R), 
    R = R1, 
    satisfies(F,A,S), 
    amount_satisfied_of_rank(A,S,R,N1,RA), 
    N is N1+1.
amount_satisfied_of_rank(A,S,R,N,[F,R1|RA]) :- 
    has_plan(A,S), 
    rank(R), 
    R = R1, 
    not(satisfies(F,A,S)), 
    amount_satisfied_of_rank(A,S,R,N,RA).
amount_satisfied_of_rank(A,S,R,N,[F,R1|RA]) :- 
    has_plan(A,S), 
    rank(R), 
    R \= R1, 
    amount_satisfied_of_rank(A,S,R,N,RA).

% best(?A,?S)
best(A,S) :-
    action(A),
    has_plan(A,S),
    val(A,S,R),
    not((has_plan(B,S), A \= B, val(B,S,R1), R1 > R)).
        type(f(0), '-').
        
        type(f(1), '-').
        
        type(f(2), '-').
        
        type(f(3), '-').
        
        has_plan(go(right), s(0)).
        has_plan(go(left), s(0)).
        
            has_feature(f(3), go(right), s(0)).
            
            has_feature(f(1), go(left), s(0)).
            
        has_plan(go(right), s(1)).
        has_plan(go(left), s(1)).
        
            has_feature(f(0), go(right), s(1)).
            
            has_feature(f(1), go(left), s(1)).
            
        has_plan(go(right), s(2)).
        has_plan(go(left), s(2)).
        
            has_feature(f(3), go(right), s(2)).
            
            has_feature(f(1), go(left), s(2)).
            
        has_plan(go(right), s(3)).
        has_plan(go(left), s(3)).
        
            has_feature(f(2), go(right), s(3)).
            
            has_feature(f(1), go(left), s(3)).
            
        has_plan(go(right), s(4)).
        has_plan(go(left), s(4)).
        
            has_feature(f(2), go(right), s(4)).
            
            has_feature(f(3), go(left), s(4)).
            
    rank(R) :- between(1, 2, R).
    max_rank(2).
    t(_)::rank_assignment([f(0), 1, f(1), 1, f(2), 1, f(3), 1]);
t(_)::rank_assignment([f(0), 1, f(1), 1, f(2), 1, f(3), 2]);
t(_)::rank_assignment([f(0), 1, f(1), 1, f(2), 2, f(3), 2]);
t(_)::rank_assignment([f(0), 1, f(1), 2, f(2), 2, f(3), 2]);
t(_)::rank_assignment([f(0), 2, f(1), 2, f(2), 2, f(3), 2]).

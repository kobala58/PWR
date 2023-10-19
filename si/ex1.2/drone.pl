:- consult('getyesno.pl').  % Use ensure_loaded if available.

%
% Main control procedures
%

start :-
   write('Ten program sprawdzi dlaczego nie możesz wystartować dronem.'),nl,
   write('Odpowiedz T lub N na pytania.'),nl,
   clear_stored_answers,
   try_all_possibilities.

try_all_possibilities :-     % Backtrack through all possibilities...
   defect_may_be(D),
   explain(D),
   fail.

try_all_possibilities.       % ...then succeed with no further action.


%
% Diagnostic knowledge base
%   (conditions under which to give each diagnosis)
%

defect_may_be(niepodlaczona_bateria) :-
   user_says(battery_is_connectes,no).

defect_may_be(uszkodzona_bateria) :-
   user_says(battery_is_connectes,yes),
   user_says(sound,no).

defect_may_be(sparowanie_radia) :-
   user_says(battery_is_connectes,yes),
   user_says(sound,yes),
   user_says(flashing_lights,yes).

defect_may_be(zly_kanal) :-
   user_says(battery_is_connectes,yes),
   user_says(sound,yes),
   user_says(flashing_lights,no),
   user_says(gogles_are_connected,no).

defect_may_be(rozladowana_bateria) :-
   user_says(battery_is_connectes,yes),
   user_says(sound,yes),
   user_says(flashing_lights,no),
   user_says(gogles_are_connected,yes),
   user_says(battery_is_not_full,yes).

defect_may_be(nierowno) :-
   user_says(battery_is_connectes,yes),
   user_says(sound,yes),
   user_says(flashing_lights,no),
   user_says(gogles_are_connected,yes),
   user_says(battery_is_not_full,no),
   user_says(correct_angle,no).


%
% Case knowledge base
%   (information supplied by the user during the consultation)
%

:- dynamic(stored_answer/2).

   % (Clauses get added as user answers questions.)


%
% Procedure to get rid of the stored answers
% without abolishing the dynamic declaration
%

clear_stored_answers :- retract(stored_answer(_,_)),fail.
clear_stored_answers.


%
% Procedure to retrieve the user's answer to each question when needed,
% or ask the question if it has not already been asked
%

user_says(Q,A) :- stored_answer(Q,A).

user_says(Q,A) :- \+ stored_answer(Q,_),
                  nl,nl,
                  ask_question(Q),
                  get_yes_or_no(Response),
                  asserta(stored_answer(Q,Response)),
                  Response = A.


%
% Texts of the questions
%

ask_question(battery_is_connectes) :-
   write('Is battery connected to drone via XT30 connector? :'),nl,

ask_question(sound) :-
   write('Does drone emited sound after connecting battery?'),nl.

ask_question(flashing_lights) :-
   write('Are some lights flashing at the tail?'),nl.

ask_question(gogles_are_connected) :-
   write('Turn on your goggles. Are you able to see image from drone camera?'),nl.

ask_question(battery_is_not_full) :-
   write('Are you seeing "BATT < FULL" at the bottom of goggles image?'),nl.

ask_question(correct_angle) :-
   write('Are you seeing "ANGLE" at the bottom of goggles image?'),nl.


%
%  Explanations for the various diagnoses
%

explain(uszkodzona_bateria) :-
   nl,
   write('Bateria jest uszkodzona. Zutylizuj ją i podłącz inną.'),nl.

explain(niepodlaczona_bateria) :-
   nl,
   write('Bateria jest niepodłączona, podłącz ją.'),nl.

explain(sparowanie_radia) :-
   nl,
   write('Twoje radio nie jest sparowanie.'),nl,
   write('Naciśnij przycisk na dronie który znajduje się z pobliżu migających świateł.'),nl,
   write('Na radiu odnajdź przycisk "pair" i naciśnij go.'),nl,
   write('Poczekaj aż światła przestaną migać.'),nl.

explain(zly_kanal) :-
   nl,
   write('Gogle są ustawione na inny kanał odbioru.'),nl,
   write('Użyj opcji automatycznego wyszukiwania lub manualnie przejdź przez kanały aż do uzyskania baterii'),nl.

explain(rozladowana_bateria) :-
   nl,
   write('Bateria nie jest w pełni naładowna'),nl,
   write('Naładuj baterię do poziomu 16,8V'),nl.

explain(nierowno) :-
   nl,
   write('Podłoże nie jest równe'),nl,
   write('Postaw drona na płaskiej i równej powierzchni'),nl.
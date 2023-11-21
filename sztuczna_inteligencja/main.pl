:- consult('getyesno.pl').

%%%%%%%%%%%
%% FAKTY %%
%%%%%%%%%%%


%
% Baza wiedzy, na temat elementow drona.
%

elementy_drona([silniki, smigla, kontroler, odbiornik_radiowy]).

%
% Baza wiedzy, na temat problemow z dronem.
%


defect_may_be(zbyt_malo_lat) :-
   user_says(age, A),
   A < 18,
   user_says(battery_is_connected,no).

defect_may_be(niepodlaczona_bateria) :-
   user_says(age, A),
   A > 18,
   user_says(battery_is_connected,no).

defect_may_be(uszkodzona_bateria) :-
   user_says(age, A),
   A > 18,
   user_says(battery_is_connected,yes),
   user_says(sound,no).

defect_may_be(sparowanie_radia) :-
   user_says(age, A),
   A > 18,
   user_says(battery_is_connected,yes),
   user_says(sound,yes),
   user_says(flashing_lights,yes).

defect_may_be(zly_kanal) :-
   user_says(age, A),
   A > 18,
   user_says(battery_is_connected,yes),
   user_says(sound,yes),
   user_says(flashing_lights,no),
   user_says(gogles_are_connected,no).

defect_may_be(rozladowana_bateria) :-
   user_says(age, A),
   A > 18,
   user_says(battery_is_connectes,yes),
   user_says(sound,yes),
   user_says(flashing_lights,no),
   user_says(gogles_are_connected,yes),
   user_says(battery_is_not_full, Blvl),
   Blvl < 16800.

defect_may_be(nierowno) :-
   user_says(age, A),
   A > 18,
   user_says(battery_is_connected,yes),
   user_says(sound,yes),
   user_says(flashing_lights,no),
   user_says(gogles_are_connected,yes),
   user_says(battery_is_not_full,Blvl),
   Blvl > 16800,
   user_says(correct_angle,no).


defect_may_be(odbiornik_radiowy) :-
  user_says(odbiornik_radiowy,no).


defect_may_be_add_parts(kontroler) :-
  user_says(kontroler,no).
defect_may_be_add_parts(smigla) :-
  user_says(smigla,yes).
defect_may_be_add_parts(silniki) :-
  user_says(silniki,no).
defect_may_be_add_parts(kamera) :-
  user_says(kamera,no).
defect_may_be_add_parts(swiatla) :-
  user_says(swiatla,no).
defect_may_be_add_parts(gps) :-
  user_says(gps,no).
%
% Wyjasnienia danych problemow.
% 

explain(uszkodzona_bateria) :-
   nl,
   write('Bateria jest uszkodzona. Zutylizuj ja i podlacz inna.'),nl.

explain(niepodlaczona_bateria) :-
   nl,
   write('Bateria jest niepodlaczona, podlacz ja.'),nl.

explain(sparowanie_radia) :-
   nl,
   write('Twoje radio nie jest sparowanie.'),nl,
   write('Nacisnij przycisk na dronie ktory znajduje sie z poblizu migajacych swiatel.'),nl,
   write('Na radiu odnajdz przycisk "pair" i nacisnij go.'),nl,
   write('Poczekaj az swiatla przestana migac.'),nl.

explain(zly_kanal) :-
   nl,
   write('Gogle sa ustawione na inny kanal odbioru.'),nl,
   write('Uzyj opcji automatycznego wyszukiwania lub manualnie przejdz przez kanaly az do uzyskania baterii'),nl.

explain(rozladowana_bateria) :-
   nl,
   write('Bateria nie jest w pelni naladowna'),nl,
   write('Naladuj baterie do poziomu 16,8V'),nl.

explain(nierowno) :-
   nl,
   write('Podloze nie jest rowne'),nl,
   write('Postaw drona na plaskiej i rownej powierzchni'),nl.

explain(zbyt_malo_lat) :-
   nl,
   write('Nie posiadasz wystarczajaco duzo lat aby latac dronem!'),nl.

explain_add_parts(kontroler) :-
  write("Dobierz na radiu odpowieni standard komunikacji zgody z kontrolerem"),nl.
explain_add_parts(smigla) :-
  write("Dokonaj NATYCHMIASTIOWEJ wymiany smigiel!"),nl.
explain_add_parts(silniki) :-
  write("Dokladnie usun wszystkie elementy (trawa, liscie) z silnika i powtorz probe."),nl.
explain_add_parts(kamera) :-
  write("Wloz karte microSD formratowana w systemie plikow FAT32."),nl.
explain_add_parts(swiatla) :-
  write("Sprawdz dokumentacje techniczna i podaj odpowiednie napiecie."),nl.
explain_add_parts(gps) :-
  write("W Betaflight/Arupilot ustaw przesylanie telemetrii"),nl.
%%%%%%%%%%%%%%%%%%%%%%%
%% FUNKCJE DODATKOWE %%
%%%%%%%%%%%%%%%%%%%%%%%

try_all_possibilities :-     % Backtrack through all possibilities...
   defect_may_be(D),
   explain(D),
   fail.

try_all_possibilities.       % ...then succeed with no further action.

:- dynamic(stored_answer/2).

   % (Clauses get added as user answers questions.)

clear_stored_answers :- retract(stored_answer(_,_)),fail.
clear_stored_answers.

user_says(Q,A) :- stored_answer(Q,A).

user_says(Q,A) :- \+ stored_answer(Q,_),
                  nl,nl,
                  ask_question(Q),
	          question_type(Q,T),
		  (
                      T == yn ->
            	          get_yes_or_no(Response),
            		  asserta(stored_answer(Q, Response)),
            		  Response = A
        	      ;
        	      T == i ->
           		  read(Response),
                          asserta(stored_answer(Q, Response)),
		          Response = A
                           
                  ).
			
		  
%
% Sprawdz czy element nalezy do listy.
%

czy_jest(Element, [Element|_]).
czy_jest(Element, [_|Reszta]) :- czy_jest(Element, Reszta).

%
% Sprawdz czy elemenety naleza do listy.
%

czy_jest_dwa([], _).
czy_jest_dwa([Element | Reszta], Lista) :-
    czy_jest(Element, Lista);
    czy_jest_dwa(Reszta, Lista).

%
% Wypisz elementy listy.
%

wypisz([]).
wypisz([Element | Reszta]) :- 
    wypisz(Reszta),
    write(Element),nl.

%%%%%%%%%%%%%
%% PYTANIA %%
%%%%%%%%%%%%%

%
% Obsluz pytanie o wystepowanie problemu.
%

czy_problem(1):-
	write('W takim razie postepuj zgodnie z instrukcjami!'),nl,nl.

czy_problem(2):-
	write('Lataj wysoko!'),fail.


%
% Dodawanie elementow dodatkowych
%

:- dynamic(elementy_drona/1).

dodanie_list([], L2, L2).    

dodanie_list([X | L1], L2, [X | L3]) :-
    dodanie_list(L1, L2, L3).

dodaj_elementy_drona(DodElementy) :-
    elementy_drona(StareElementy),
    retractall(elementy_drona(_)),
    dodanie_list(StareElementy, DodElementy, NoweElementy),
    assertz(elementy_drona(NoweElementy)),
    write('Elementy zostaly zaktualizowane.').

dodatkowe_elementy :-
    write('Czy twoj dron posiada jeszcze jakies elementy wypisane ponizej, które nie zajduja sie na liscie?'),nl,
    write('[kamera, swiatla, gps]'),nl,
    write('Jesli tak, wypisz powyzsze w postaci listy "[element1, element2, ... , element n]"'),nl,
    read(Czesci),
    (czy_jest_dwa(Czesci, [kamera, swiatla, gps]) ->
         dodaj_elementy_drona(Czesci),nl,
	 elementy_drona(Wszystko),
	 format('Aktualny stan bazy: ~w', [Wszystko]),nl;
         write('Zostaly wpisane niepoprawne elementy.'),nl,nl,
	 write('System zostanie uruchomiony ponownie.'),nl,nl,nl,start),
    nl.


%
% Pytania diagnostyczne
%

ask_question(battery_is_connected) :-
   write('Czy bateria jest podlaczona za posrednictwem wtyku XT30? :'),nl.


ask_question(sound) :-
   write('Czy dron emituje dzwiek po podlaczeniu baterii: '),nl.


ask_question(flashing_lights) :- 
   write('Czy blyskaja jakies swiatla: '),nl.


ask_question(gogles_are_connected) :-
   write('W;acz gogle. Czy jestes w stanie zobaczyc obraz z drona?: '),nl.


ask_question(battery_is_not_full) :-
   write('Podaj w mV oczyt z multitera po zbadaniu baterii: '),nl.


ask_question(correct_angle) :-
   write('Czy widzisz napis "ANGLE" na dole obrazu w goglach?: '),nl.

ask_question(age) :-
   write('Ile masz lat?'),nl.

ask_question(odbiornik_radiowy) :-
  write('Czy raio i odbiornik komunikuja sie w tym samym standardzie (ExpressELS, FRSKY) oraz czy radio jest zbindowane z odbiornikiem.: '),nl.

ask_question(kontroler) :-
  write("Czy kontroler lotu jest odpowiednio podlaczony"),nl.

ask_question(smigla) :-
  write("Czy zarowno krawedz smigla jak i reszta jest gladka i pozbawiona uszkodzen: "),nl.

ask_question(silniki) :-
  write("Wykonaj testory odrot silnika palcem. Czy silnik obraca sie lekko?: "),nl.

ask_question(kamera) :-
  write("Czy do kamery jest wlozona karta microSD?"),nl.

ask_question(swiatla) :-
  write("Czy swiatla otrzymuja odpowiednie napiecie (5V)?"),nl.

ask_question(gps) :-
  write("Czy kontroler lotu obsluguje przesylanie danych telemetrycznych?"),nl.


question_type(battery_is_connected, yn).
question_type(sound, yn).
question_type(flashing_lights, yn).
question_type(gogles_are_connected, yn).
question_type(battery_is_not_full, i).
question_type(correct_angle, yn).
question_type(age, i).
question_type(odbiornik_radiowy, yn).
question_type(kontroler, yn).
question_type(smigla, yn).
question_type(silniki, yn).
question_type(kamera, yn).
question_type(swiatla, yn).
question_type(gps, yn).

diagnose_parts([Element | Reszta]) :-
  defect_may_be_add_parts(Element),nl,
  explain_add_parts(Element).
  diagnose_parts(Reszta),

diagnose_parts([]).
diagnose_single_part(X):-
  defect_may_be_add_parts(X),
  explain_add_parts(X).

  
%%%%%%%%%%%%%%%%%%%%%
%% GLOWNY PREDYKAT %%
%%%%%%%%%%%%%%%%%%%%%

start :-
    write('System ekspercki "Diagnostyka dotyczaca drona"'),nl,nl,
    nl,
    write('Wpisz:'),nl,
    write('1 - Jesli masz problem z wystartowaniem drona'),nl,
    write('2 - Jesli zaden problem nie wystepuje'),nl,
    read(Response),
    nl,czy_problem(Response),
    write('Podstawowe elementy drona:'),nl,nl,
    elementy_drona(Elementy),
    wypisz(Elementy),nl,
    dodatkowe_elementy,
    clear_stored_answers,
    write("Diagnostyka poszczegolnych czesci drona: "),nl,nl,
    elementy_drona(Test),
    % \+ diagnose_parts(Test),
    maplist(diagnose_single_part, Test, Z),
    try_all_possibilities.


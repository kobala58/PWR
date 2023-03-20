/*********************************************
 * OPL 22.1.1.0 Model
 * Author: kobala
 * Creation Date: 20 mar 2023 at 20:41:06
 *********************************************/
 
 // NOTE: 2nd subject is taken from ibm community forum, but below in PL i tried to explain login behin this genius idea
 
tuple Edge {
  key int s; // 2 x key ensures us that two edges between same nodes do not exist. 
  key int e;
  int dist; // distanance between two nodes
}
int graph_cnt = 21;
Edge graph[1..graph_cnt] = [<1,2,9>,
	<1,3,9>,<1,4,8>,<1,10,18>,<2,3,3>,<2,6,6>,
	<3,4,9>,<3,5,2>,<3,6,2>,<4,5,8>,<4,7,7>,
	<4,9,9>,<4,10,10>,<5,6,2>,<5,7,9>,<6,7,9>,
	<7,8,4>,<7,9,5>,<8,9,1>,<8,10,4>,<9,10,3>
	]; // sample graph structure also taken from forum 

int st = 1; // start node
int en = 8; // end node

dvar boolean usage[1..graph_cnt]; // deciding witch nodes to select
dvar int dist; 
minimize dist; // more elegant way

// sum(i in a..b:[filter]) -> expr after colon filters 

subject to {
	dist == sum(e in 1..graph_cnt) usage[e] * graph[e].dist; // this is logical 
	forall(i in 1..graph_cnt) // 2nd restriction
		sum(e in 1..graph_cnt: graph[e].s==i) usage[e] - sum(e in 1..graph_cnt: graph[e].e==i) usage[e]
		 == ((i==st)?1:((i==en)?(-1):0)); // if statment?true:false (similar to eg. JS)
}

/*
Wytlumacznie ograniczenia nr. 2: 

Rozwiązanie jest genialne w swojej prostocie: 
badamy różnicę mocy zbioru wybranych krawędzi posiadających interator *i* jako wierzchołek "wejściowy" od 
mocy zbioru różniącego się o tyle, że wierzchołek jest "wyjściowy". Najważniejsza jest jednak konstrukcja logiczna 
"((i==st)?1:((i==en)?(-1):0))" -> ona pozwala nam na sterowanie ilością krawędzi. Opis wartości:
1 => przy wierzchołku początkowym,
-1 => przy wierzchołku końcowym, 
0 w p.p.
Idea sterowania:
zasada działania łańcucha, podczas startu (dla ułatwienia załóżmy, że st<en) dla pewnego <i,d> takiego, że i==st 
bilans (bilans tj. ta śmieszna różnica) wynosi 1, zatem gdy pętla forall osiągnie d to krawędź <i,d> przechodzi z odjemnej na odjemnik
co chwilowo tworzy nam bilas = -1 co musi zostać sprwadzone do 0, zatem z krawędzi które mają d jako wierzchołek "wejściowy" należy
wybrać jedą z dostępnych krawędzi co tworzy nam kolejny deficyt, aż do momentu osiągnięcia końcowego wierzchołka.
Zrozumienie tego zajęło mi zbyt dużo czasu.
*/

// link to forum page: https://community.ibm.com/community/user/ai-datascience/communities/community-home/digestviewer/viewthread?MessageKey=630ee7d5-c9cc-45e0-8eb3-b11fc4c7e9e6&CommunityKey=ab7de0fd-6f43-47a9-8261-33578a231bb7&tab=digestviewer#bm630ee7d5-c9cc-45e0-8eb3-b11fc4c7e9e6


/*********************************************
 * OPL 22.1.1.0 Model
 * Author: kobala
 * Creation Date: 8 mar 2023 at 14:24:15
 *********************************************/
 
 // size setup
int problems_cnt = 20;
int machines_cnt = 4;
 
// problems values 
int problems[1..problems_cnt] = 	[16, 6, 13, 5, 7, 4, 3, 19, 6, 18,
									3, 17, 12, 5, 18, 17, 13, 6, 19, 3];

//decision vars
dvar boolean machines[1..machines_cnt][1..problems_cnt];

// target funcion
minimize max(i in 1..machines_cnt) sum(a in 1..problems_cnt)machines[i][a]*problems[a];

// restricion 
subject to{
  forall (i in 1..problems_cnt)
    sum(a in 1..machines_cnt) machines[a][i] == 1;
}

// exec to show results
execute {
	for (var i=1; i < machines_cnt + 1; i++){
	  var sum = 0;
	  for (var t = 1; t < problems_cnt + 1; t++){
	    sum = sum + (machines[i][t]*problems[t]);
	  }
	  writeln("Machina nr.",i," RUNTIME: ",sum);
	}
}
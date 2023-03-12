/*********************************************
 * OPL 22.1.1.0 Model
 * Author: Jakub
 * Creation Date: Mar 7, 2023 at 4:00:08 PM
 *********************************************/
 
 int n = 20;
 range rang = 1..n;
 int ilosc_maszyn = 4;
 int Z[rang] = [16, 6, 13, 5, 7, 4, 3, 19, 6, 18, 3, 17, 12, 5, 18, 17, 13, 6, 19, 3];
 
 range dubel = 1..ilosc_maszyn; 

 dvar boolean x[dubel][rang];
 
 minimize sum(i in dubel) ((sum(j in rang) (Z[j]/ilosc_maszyn) - sum(l in rang)x[i][l]*Z[l])^2);
 
 subject to
 {
   sum(i in dubel)sum(j in rang)x[i][j] == 20;
   forall(i in rang) sum(j in dubel) (x[j][i]) == 1;
 }

 
 // exec to show results
execute {
	for (var i=1; i < ilosc_maszyn + 1; i++){
	  var sum = 0;
	  for (var t = 1; t < n + 1; t++){
	    sum = sum + (x[i][t]*Z[t]);
	  }
	  writeln("Machina nr.",i," RUNTIME: ",sum);
	}
}
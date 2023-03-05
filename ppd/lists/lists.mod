/*********************************************
 * OPL 22.1.1.0 Model
 * Author: kobala
 * Creation Date: 5 mar 2023 at 16:07:52
 *********************************************/

 
dvar int+ w1; //
dvar int+ w2; // 

maximize w1*3 + w2*4;

subject to {
  w1+w2 <=12;
  2*w1+4*w2 <=42;
  w1<=11;
  }

execute HELLO {writeln("Hello World."); }
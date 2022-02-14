/* Declare states that'll be used in Kripke structures */
mtype = {s0, s1, s2, s3}
/* Declare sa,... standing for kripke structure a, ... */
mtype = {sa, sb}

byte state=s0; /* Init state to s0 */
bit a=1; /* Initial values of a and b */
bit b=1;
proctype generic(mtype structure){
if
  :: structure==sa -> do
    :: d_step{state==s0;a=1;b=1} -> d_step{state=s1;a=0;b=1}
    :: d_step{state==s0;a=1;b=1} -> d_step{state=s2;a=1;b=0}
    :: d_step{state==s1;a=0;b=1} -> d_step{state=s2;a=1;b=0}
    :: d_step{state==s2;a=1;b=0} -> d_step{state=s2;a=1;b=0}
    :: d_step{state==s2;a=1;b=0} -> d_step{state=s1;a=0;b=1}
  od

  :: structure==sb -> do
    :: d_step{state==s0;a=1;b=1} -> d_step{state=s0;a=1;b=1}
    :: d_step{state==s0;a=1;b=1} -> d_step{state=s1;a=0;b=1}
    :: d_step{state==s0;a=1;b=1} -> d_step{state=s2;a=1;b=0}
    :: d_step{state==s1;a=0;b=1} -> d_step{state=s2;a=1;b=0}
    :: d_step{state==s2;a=1;b=0} -> d_step{state=s2;a=1;b=0}
    :: d_step{state==s2;a=1;b=0} -> d_step{state=s3;a=0;b=0}
    :: d_step{state==s3;a=0;b=0} -> d_step{state=s1;a=0;b=1}
  od
fi
}

init
{ run generic(sb) }

// never  {    /* !( !(<>([](a && b))) -> ((<>([]a)) || (<> (!a && !b)))) */
//   T0_init:
//     do
//       :: (! ((!a && !b)) && ! ((a)) && ! ((a && b))) -> goto accept_S81
//       :: (! ((!a && !b)) && ! ((a && b))) -> goto T1_S81
//       :: (! ((!a && !b))) -> goto T0_init
//     od;
//   accept_S81:
//     do
//       :: (! ((!a && !b))) -> goto T0_init
//     od;
//   T1_S81:
//     do
//       :: (! ((!a && !b)) && ! ((a))) -> goto accept_S81
//       :: (! ((!a && !b))) -> goto T1_S81
//     od;
// }

// sa doesn't satisfy this ltl, but sa does. Checked on cli


never  {    /* !( !(<>([](a && b))) -> ( (<>([]a)) || (<> (b)) ) ) */
  T0_init:
    do
      :: (! ((a)) && ! ((a && b)) && ! ((b))) -> goto accept_S81
      :: (! ((a && b)) && ! ((b))) -> goto T1_S81
      :: (! ((b))) -> goto T0_init
    od;
  accept_S81:
    do
      :: (! ((b))) -> goto T0_init
    od;
  T1_S81:
    do
      :: (! ((a)) && ! ((b))) -> goto accept_S81
      :: (! ((b))) -> goto T1_S81
    od;
}

// sa and sb satisfy this. Checked on cli. All states showed unreached, but no errors.

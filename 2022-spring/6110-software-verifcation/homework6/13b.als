one sig a extends U {}
sig S1,S2,S3 in U {}
some sig U {f : U}
pred P[x,y,z:U] {x in S1 and y in S2 and z in S3}

assert thirteenb {
  some z:U |
  (
    (all x:U | P[a,x,x])
    and
    (all x,y:U | P[x,y,z] => P[f[x],y,f[z]])
  )
  =>
  ( P[f[a],z,f[f[a]]])
}

check thirteenb

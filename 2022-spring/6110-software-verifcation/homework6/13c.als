one sig b extends U {}
sig S1,S2 in U {}
some sig U {s : U}
pred Q[x,y:U] {x in S1 and y in S2}

assert thirteenc {
  some z:U |
  (
    (all y:U | Q[b,y])
    and
    (all x,y:U | Q[x,y] => Q[s[x],s[y]])
  )
  =>
  (Q[b,z] and Q[z,s[s[b]]])
}

check thirteenc

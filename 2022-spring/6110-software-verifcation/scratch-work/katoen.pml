int x = 0;

proctype Inc() {
    do :: true -> if :: (x < 200) -> x = x + 1 fi od
}

proctype Dec() {
    do :: true -> if :: (x > 0) -> x = x - 1 fi od
}

proctype Reset() {
    do :: true -> if :: (x == 200) -> x = 0 fi od
}

proctype Check() {
    do :: true -> assert (x >= 0 && x <= 200) od
}

init {
    atomic{ run Inc() ; run Dec() ; run Reset() ; run Check() ; }
}


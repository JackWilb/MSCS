/*-- BEGIN: common to all three tree definitions --*/
sig Node {
tree: set Node
}
one sig root extends Node {} // root is a subset of Node
/*-- END : common to all three tree definitions --*/


pred GGTree{
no n : Node | root in n.^tree // Q-1
--
no n : Node | n in n.^tree // Q-2
--
all n : Node - root | n in root.^tree // Q-3
--
all n : Node |
all disj n1, n2 : n.tree | // Q-4
no (n1.*tree & n2.*tree)
}







// Round 2
pred GGTree{
 no n : Node | root in n.^tree
 --
 no n : Node | n in n.^tree
 --
 all n : Node - root | n in root.^tree
 -- 
 all n : Node |
 all disj n1, n2 : n.tree |  
   no (n1.*tree & n2.*tree) 
}


pred DJTree {
    Node in root.*tree // all reachable
    no iden & ^tree // no cycles
    tree in  Node lone -> Node // Q-5
    }

pred CostelloTree {
    // No node above root (no node maps to root)
    no tree.root
    // Can reach all nodes from root                
    all n: Node - root | n in root.^tree
    // No node maps to itself (irreflexive) 
    no iden & tree
    // No cycles                    
    no n: Node | Node in n.^tree
    // All nodes are distinct (injective)           
    tree.~tree in iden -- need this
}

// Set up relationship between search string and the data that it represents
sig DataItem {}
sig SearchTerm {}

sig SearchDataMap {
	search: one SearchTerm,
	data: one DataItem
}

// Ensure every data item is available from some search term and that every search term maps to data
fact {some SearchDataMap}
fact {all d: DataItem | one d.~data}
fact {all s: SearchTerm | one s.~search}

// Pending interest table mapping (nodes asking for specific search term)
sig PITMap {
	searchterm: one SearchTerm,
	requestor: some Node,
}

// Create nodes with:
// cache holding the search term -> data item maps
// PIT for showing who has requested the data from this node
sig Node {
	neighbors: some Node,
	cache: SearchDataMap,
	PIT:   PITMap
}


// Make sure that every data is attached to at least one node
fact {all s: SearchDataMap | some s.~cache}

// Make sure node isn't neighbor with itself and that neighbor relationships are bi-directional
fact {all n: Node | n not in n.neighbors}
fact {all n: Node | all nei: n.neighbors | n in nei.neighbors}

// Make sure the all nodes are reachable from any node
fact {all disj a,b: Node | a in  b.*neighbors or b in a.*neighbors} 

// Make sure that node in PIT isn't already caching data for searchTerm
fact {all n: Node | n.PIT.searchterm not in n.PIT.requestor.cache.search}

// Make sure self not in PIT
fact {all n: Node | n not in n.PIT.requestor}

// Make sure neighbor is only one in PIT
fact {all n: Node | n.PIT.requestor in n.neighbors}

// Make sure PITMap is connected to a node
fact {all p: PITMap | #p.~PIT != 0}




// Make sure that all search terms are reachable from any node
assert all_reachable {all n: Node | SearchDataMap =  n.*neighbors.cache}
//check all_reachable for 5


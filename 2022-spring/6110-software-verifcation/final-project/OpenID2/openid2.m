-- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
const
  SUPPRESS_SWAPPING: false;  -- invariants check only for session hijacking attacks
                             -- (i.e., ignoring session swapping attacks)

  NumInitiators:   1;   -- number of initiators
  NumResponders:   1;   -- number of responders
  NumProviders:    1;
  NumIntruders:    1;   -- number of intruders
  NetworkSize:     1;   -- max. number of outstanding messages in network
  MaxKnowledge:   3;   -- max. number of messages intruder can remember


-- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
type
  InitiatorId:  scalarset (NumInitiators);   -- identifiers
  ResponderId:  scalarset (NumResponders);
  ProviderId:   scalarset (NumProviders);
  IntruderId:   scalarset (NumIntruders);
  
  AgentId:      union {InitiatorId, ResponderId, ProviderId, IntruderId};
  --XSRFId: union {InitiatorId, IntruderId};
  -- GRIPE no subtyping relationships detected between unions

  MessageType : enum {
	M_Init, M_Request, M_Response
  };

  -- Glossary:
  -- OP: OpenID provider. RP: Relying Party. USI: User-supplied identifier (the "actual" OpenID)
  Message : record
    -- META fields: veridical fields that don't correspond to actual message elements
    source:   AgentId;           -- source of message
    dest:     AgentId;           -- intended destination of message
    mType:    MessageType;       -- type of message
    forward_to: AgentId; -- in indirect messaging, who the message should get sent to

    -- non-meta fields:
    user_id: AgentId; -- represents the USI, or more specifically, the "OP-local identifier"
    provider_id: AgentId; -- represents the OP's endpoint
    return_to: AgentId; -- RP's endpoint
    -- signature model: represents the two parties to the secret with which the message was signed
    responder_sig: AgentId;
    provider_sig: AgentId;

  end;

  InitiatorStates : enum {
    I_SLEEP,                     -- state after initialization
    I_WAIT,                      -- waiting for response from responder
    I_COMMIT                     -- initiator commits to session
  };                             --  (thinks responder is authenticated)

  Initiator : record
    state:     InitiatorStates;
    provider: AgentId;
    responder: AgentId;          -- agent with whom the initiator starts the
  end;                           --  protocol

  ResponderStates : enum {
    R_SLEEP,
    R_WAIT,
    R_COMMIT
  };

  -- provider does not commit to anyone, just shares secrets, processes auth
  -- messages, then goes back to sleep
  ProviderStates : enum {
    P_SLEEP, P_WAIT
  };

  Responder : record
    state:     ResponderStates;
    initiator: AgentId; -- this is a USI (the claimed ID with which the initiator is trying to authenticate)
    provider: AgentId; -- this is set to model the shared secret
    auth_party: AgentId; -- this is the entity (an IP address) to which the RP matches the USI
  end;

  Provider : record
    state: ProviderStates;
    responder: AgentId; -- this models the shared secret
  end;

  -- TODO change some of these fields to scalarsets?

  Intruder : record
    messages: multiset[MaxKnowledge] of Message;   -- known messages
  end;
    

-- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
var                                         -- state variables for
  net: multiset[NetworkSize] of Message;    --  network
  ini: array[AgentId] of Initiator;         --  initiators
  res: array[AgentId] of Responder;         --  responders
  pro: array[AgentId] of Provider;
  int: array[IntruderId] of Intruder;       --  intruders
-- TODO uncomment



--------------------------------------------------------------------------------
-- rules
--------------------------------------------------------------------------------

-- TODO figure out what the undefined fields are

--------------------------------------------------------------------------------
-- behavior of initiators

-- initiator i starts protocol with responder or intruder j (step 3)
ruleset i: InitiatorId do
  ruleset j: AgentId do
  ruleset k: ProviderId do
    rule 20 "initiator starts protocol (step 3)"

      ini[i].state = I_SLEEP &
      !ismember(j,InitiatorId) &               -- only responders and intruders
      !ismember(j,ProviderId) &
      multisetcount (l:net, true) < NetworkSize

    ==>
    
    var
      outM: Message;   -- outgoing message

    begin
      undefine outM;
      outM.source  := i;
      outM.dest    := j;
      outM.mType := M_Init;
      outM.provider_id := k;
      outM.user_id := i;

      multisetadd (outM,net);

      ini[i].state     := I_WAIT;
      ini[i].responder := j;
      ini[i].provider := k;
    end;
  end;
  end;
end;

ruleset i: InitiatorId do
  choose j: net do
    rule 20 "initiator forwards an indirect message"

      ini[i].state = I_WAIT & -- TODO what side should the state be on?
      net[j].dest = i
      --ismember(net[j].source,IntruderId)
    ==>

    var
      outM: Message;   -- outgoing message
      inM:  Message;   -- incoming message

    begin
      inM := net[j];
      multisetremove (j,net);

        if inM.mType=M_Request | inM.mType=M_Response then   -- correct message type
	  inM.source := i;
	  inM.dest := inM.forward_to;

	  multisetadd(inM, net);
        end;

    end;
  end;
end;

--------------------------------------------------------------------------------
-- behavior of responders

ruleset i: ResponderId do
  choose j: net do
    rule 20 "responder sends out auth request"

      -- TODO eliminate responder states?
      res[i].state = R_SLEEP &
      net[j].dest = i
    --ismember(net[j].source,IntruderId)
      -- TODO find out what's up with these hard-coded intruder things
      -- they save some steps, but do they prevent the process from proceeding
      -- normally up to a certain point? but then do the intruders replicate
      -- those steps?

    ==>

    var
      outM: Message;   -- outgoing message
      inM:  Message;   -- incoming message

    begin
      inM := net[j];
      multisetremove(j, net);

      if inM.mType=M_Init then   -- correct message type
        undefine outM;
        outM.source      := i;
        outM.dest        := inM.source;
      --outM.https       := false;
        outM.mType       := M_Request;
        outM.provider_id := inM.provider_id;
        outM.user_id     := inM.user_id;
        outM.forward_to  := inM.provider_id;
        outM.return_to   := i;
        
        multisetadd(outM, net);
        
        res[i].state     := R_WAIT;
        res[i].initiator := inM.user_id; -- note that this is a USI, not an IP
        res[i].provider  := inM.provider_id;
        pro[inM.provider_id].responder := i;
        pro[inM.provider_id].state := P_WAIT;
      end; -- if
    end; -- begin
  end; -- choose j
end; -- ruleset i

ruleset i: ResponderId do
  choose j: net do
    rule 20 "responder issues auth token"

      res[i].state = R_WAIT &
      net[j].dest = i

      ==>

      begin
        alias inM: net[j] do   -- incoming message

          if inM.return_to = i &
             inM.responder_sig = i &
             inM.provider_sig = res[i].provider &
             inM.responder_sig = i &
             inM.user_id = res[i].initiator &
             inM.provider_id = res[i].provider
          then
            res[i].state := R_COMMIT;
	        res[i].auth_party := inM.source; -- this is an IP address!
          end;

          multisetremove (j,net);
          
        end; -- alias inM
      end; -- begin

  end; -- choose j
end; -- ruleset i

--------------------------------------------------------------------------------
-- behavior of providers

-- TODO model client wanting to log in or not

-- provider i sends out a positive auth-response message
ruleset i: ProviderId do
  choose j: net do
    rule 20 "provider sends positive auth-response message"

      pro[i].state = P_WAIT & -- TODO set up provider wait states, signature locks
      net[j].dest = i
      --ismember(net[j].source,IntruderId)
      -- TODO find out what's up with these hard-coded intruder things
      -- they save some steps, but do they prevent the process from proceeding
      -- normally up to a certain point? but then do the intruders replicate
      -- those steps?

    ==>

    var
      outM: Message;   -- outgoing message
      inM:  Message;   -- incoming message

    begin
      inM := net[j];
      multisetremove (j,net);

      -- a stack of correctness conditions TODO check these, analogous places
      -- inM.source is the entity supplying the auth cookie, so must match user_id
      if inM.mType = M_Request &
         -- Crucial! OP can compare source, which is an IP, to user_id, which is a USI
         inM.user_id = inM.source &
         inM.provider_id = i
      then
        undefine outM;
        outM.source        := i;
        outM.dest          := inM.source; 
        outM.mType         := M_Response;
        -- TODO eliminate HTTPS?
        outM.provider_id   := i;
        outM.user_id       := inM.source; -- the source gave the cookie, the source gets the ID
        outM.return_to     := inM.return_to;
        outM.forward_to    := inM.return_to;
        outM.provider_sig  := i;
        outM.responder_sig := pro[i].responder;

        multisetadd (outM,net);

        pro[i].state       := P_SLEEP;
      end; -- if
    end; -- begin
    
  end; -- choose j
end; -- ruleset i

--------------------------------------------------------------------------------
-- behavior of intruders

-- intruder sends arbitrary init message with source s, user_id u, to
-- responder r and provider p (both of which could be intruders).  note
-- the key difference from the previous rule: there is no requirement upon
-- or modification of the purported initiator's state.
ruleset s: AgentId do
  ruleset u: AgentId do
  ruleset r: AgentId do
  ruleset p: AgentId do
    rule 20 "intruder starts protocol"

      (ismember(s, InitiatorId) | ismember(s, IntruderId)) &
      (ismember(u, InitiatorId) | ismember(u, IntruderId)) &
      (ismember(r, ResponderId) | ismember(r, IntruderId)) &
      (ismember(p, ProviderId)  | ismember(p, IntruderId)) &
      multisetcount (l:net, true) < NetworkSize

    ==>
    
    var
      outM: Message;   -- outgoing message

    begin
      undefine outM;
      outM.source      := u;
      outM.dest        := r;
      outM.mType       := M_Init;
      outM.provider_id := p;
      outM.user_id     := u;

      multisetadd (outM, net);
    end;
  end;
  end;
  end;
end;

ruleset i: IntruderId do
  choose n: net do
    rule 20 "intruder records message"
    
    net[n].dest = i & -- identifies both the intruder and its pawn
    multisetcount(l:int[i].messages, true) < MaxKnowledge
    
    ==>

    begin
      multisetadd(net[n], int[i].messages);
      multisetremove(n, net);
    end;
  end;
end;

ruleset i: IntruderId do
  choose m: int[i].messages do
    ruleset s: AgentId do
      ruleset d: AgentId do
        rule 20 "intruder reroutes message"

        (ismember(s, InitiatorId) | s = i) &
	-- stops the intruder from chasing its own tail:
	(!ismember(d, IntruderId)) &
        !(ismember(d, ResponderId) &
          int[i].messages[m].mType = M_Request) &
        !(ismember(d, ProviderId) &
          int[i].messages[m].mType = M_Response) &
        multisetcount(l:net, true) < NetworkSize
        
        ==>

        begin
          alias msg: int[i].messages[m] do
            msg.source := s;
            msg.dest   := d;
            multisetadd(msg, net);
          end;
        end;
        
      end;
    end;
  end;
end;

ruleset i: IntruderId do
  ruleset p: ProviderId do
    ruleset s: AgentId do
    ruleset d: AgentId do
    ruleset r: AgentId do
    ruleset u: AgentId do
      rule 20 "intruder synthesizes auth-request message"

      (ismember(s, InitiatorId) | s = i)
       -- this below forbids the message being sent to an intruder
       -- or to an responder, who won't understand it
      & (ismember(d, ProviderId) | isMember(d, InitiatorId))
      -- this below forbids return_to getting set to an initiator
      -- (in the actual protocol, it's a URI)
      & (ismember(r, ResponderId) | isMember(r, IntruderId))
      & (u = s | u = i)
      & multisetcount(l:net, true) < NetworkSize 
	==>

	var
	  outM: Message;
        begin
	  outM.mType := M_Request;
	  outM.source := s;
	  outM.dest := d;
	  outM.forward_to := p;
	  outM.return_to := r;
	  outM.user_id := u;
	  outM.provider_id := p;

	  multisetadd(outM, net);
	end;

     end;
     end;
     end;
     end;
  end;
end;


-- this rule covers direct and indirect sending to responders
ruleset i: IntruderId do
  ruleset r: ResponderId do
  ruleset p: AgentId do
  ruleset s: AgentId do
  ruleset d: AgentId do
  ruleset u: AgentId do
      rule 20 "intruder synthesizes auth-response message"

      (ismember(s, InitiatorId) | s = i)
      & (ismember(d, ResponderId) | isMember(d, InitiatorId))
      -- must respect the digital signatures; only sign if the dummy knows the secret
      & (pro[p].responder = r) & (res[r].provider = p) & (p = i)
      -- & (isMember(p, ProviderId) | isMember(p, IntruderId))
      & (u = s | u = i)
      & multisetcount(l:net, true) < NetworkSize 

	==>

	var
	  outM: Message;
        begin
	  outM.mType := M_Response;
	  outM.source := s;
	  outM.dest := d;
	  outM.forward_to := r;
	  outM.return_to := r;
	  outM.responder_sig := r;
	  outM.provider_id := p;
	  outM.provider_sig := p;
	  outM.user_id := u;

	  multisetadd(outM, net);
	end;

     end;
     end;
     end;
     end;
     end;
end;


-- dishonest responder associates with a provider (that doesn't already have
-- an association)
ruleset i: IntruderId do
ruleset p: ProviderId do
rule 20 "intruder makes association with responder"
   pro[p].responder = p

   ==>

   pro[p].responder := i;
   res[i].provider := p;
end;
end;
end;

--------------------------------------------------------------------------------
-- startstate
--------------------------------------------------------------------------------

startstate
  -- initialize initiators
  undefine ini;
  for i: InitiatorId do
    ini[i].state     := I_SLEEP;
    ini[i].responder := i;
    ini[i].provider := i;
  end;

  -- initialize responders
  undefine res;
  for i: AgentId do
    res[i].state     := R_SLEEP;
    res[i].initiator := i;
    res[i].provider := i;
    res[i].auth_party := i;
  end;

  undefine pro;
  for i: AgentId do
     pro[i].state := P_SLEEP;
     pro[i].responder := i;
  end;

  -- initialize intruders
  undefine int;

  -- initialize network 
  undefine net;
end;



--------------------------------------------------------------------------------
-- invariants
--------------------------------------------------------------------------------

/*
   -- this models willingness of the legitimate initiator to log in
invariant "initiator only logged in via request to the correct site"
  forall i: ResponderId do
    res[i].state = R_COMMIT
    & ismember(res[i].auth_party, InitiatorId)
    ->
    ini[res[i].auth_party].responder = i
  end;
*/

-- this is the important one
invariant "initiator correctly authenticated"
  forall i: ResponderId do
    res[i].state = R_COMMIT
    & (!SUPPRESS_SWAPPING | ismember(res[i].initiator, InitiatorId))
    -- (if suppress_swapping, examine only attempts to log in as legitimate parties)
    ->
    res[i].initiator = res[i].auth_party
  end;


invariant "messages not rerouted uselessly"
  multisetcount(m:net, net[m].mType = M_Response &
      ismember(net[m].dest, ProviderId)) = 0
  &
  multisetcount(m:net, net[m].mType = M_Request &
      ismember(net[m].dest, ResponderId)) = 0;

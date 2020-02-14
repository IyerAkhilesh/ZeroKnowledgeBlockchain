# ZeroKnowledgeBlockchain
Using Zero Knowledge Proof algorithms for authentication in services that run on blockchain

Steps to run the code:
  1. Open MYSQL Workbench 8.0 or higher, connect as root user with the password given in the code and see that there tables with the names      node1, node2, ... , node7
  2. Run all the verifiers one after the other: Node1_verifier_v2, Node2_verifier_v2, ... , Node7_verifier_v2
  3. This means that all the nodes have their "consensus-entities" in an always-on and connected mode
  4. Then run Node1_PowerRaiser_v2, Node3_PowerRaiser_v2, Node6_Authenticator_v2 and Node7_Authenticator_v2
  5. These are the container servers that will help in either the registration or login
  6. Then, run Node5_v2 with the login function call commented, and the registration function call uncommented if you want to register a        user. During this time, there will be a block mined with the Zero Knowledge Proof intermediate variables as parameters of                  transactions. You will get a message indicating if the registration and the block mining was successful 
  7. Do otherwise if you want to login as an existing user. There won't be any blocks mined for login (for now at least)
  8. If the whole system returns a true value, you'll be succcessfully logged in. Otherwise, it is bubye!

import java.util.ArrayList;
import java.util.HashSet;

public class TxHandler {
	UTXOPool unspent;

	/* Creates a public ledger whose current UTXOPool (collection of unspent 
	 * transaction outputs) is utxoPool. This should make a defensive copy of 
	 * utxoPool by using the UTXOPool(UTXOPool uPool) constructor.
	 */
	public TxHandler(UTXOPool utxoPool) {
		// Just set the local copy of the UTXO pool
		unspent = new UTXOPool(utxoPool);
	}

	/* Returns true if 
	 * (1) all outputs claimed by tx are in the current UTXO pool, 
	 * (2) the signatures on each input of tx are valid, 
	 * (3) no UTXO is claimed multiple times by tx, 
	 * (4) all of tx\u2019s output values are non-negative, and
	 * (5) the sum of tx\u2019s input values is greater than or equal to the sum of   
	        its output values;
	   and false otherwise.
	 */

	public boolean isValidTx(Transaction tx) {
		UTXOPool claimedUTXOs = new UTXOPool();
		
		int i = 0;
		double inputSum = 0;
		for (Transaction.Input input : tx.getInputs()) {
			UTXO nextClaimedUTXO = new UTXO(input.prevTxHash, input.outputIndex);
			// 1 
			if (!unspent.contains(nextClaimedUTXO))
				return false;
			
			// 2
			RSAKey pubKey = unspent.getTxOutput(nextClaimedUTXO).address;
			if (!pubKey.verifySignature(tx.getRawDataToSign(i), input.signature)) return false;
			
			
			// 3
			if (claimedUTXOs.contains(nextClaimedUTXO)) 
				return false;
			else
				claimedUTXOs.addUTXO(nextClaimedUTXO, null);
			
			i++;
			
			// 5a
			inputSum += unspent.getTxOutput(nextClaimedUTXO).value;
		}
		
		double outputSum = 0;
		for (Transaction.Output output : tx.getOutputs()) {
			// 4
			if (output.value < 0)
				return false;
			
			// 5b
			outputSum += output.value;
		}
		
		// 5c
		if (inputSum < outputSum)
			return false;
					
		return true;
	}

	/* Handles each epoch by receiving an unordered array of proposed 
	 * transactions, checking each transaction for correctness, 
	 * returning a mutually valid array of accepted transactions, 
	 * and updating the current UTXO pool as appropriate.
	 */
	public Transaction[] handleTxs(Transaction[] possibleTxs) {
		HashSet<Transaction> validTxns = new HashSet<Transaction>();
		
		// Check that each transaction is valid
		for (Transaction txn : possibleTxs) {
			if (isValidTx(txn)) {
				validTxns.add(txn);
				
				// Remove the transaction inputs from the pool
				for (Transaction.Input input : txn.getInputs()) {
					UTXO utxo = new UTXO(input.prevTxHash, input.outputIndex);
					unspent.removeUTXO(utxo);
				}
				
				// Add the unspent outputs to the pool
				byte[] txHash = txn.getHash();
				int i = 0;
				for (Transaction.Output output : txn.getOutputs()) {
					UTXO utxo = new UTXO(txHash, i);
					unspent.addUTXO(utxo, output);
					i++;
				}
			}
		}

		return validTxns.toArray(new Transaction[validTxns.size()]);
	}
} 

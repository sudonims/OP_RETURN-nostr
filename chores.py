import json
import subprocess


def shell_execute(cmd):
	out, err = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=".").communicate()
	if err:
		print(err)
	return out

def get_block(hash):
	block = json.loads(shell_execute("bitcoin-cli getblock {}".format(hash)))
	return block

def get_raw_trx(trx_hash, blk_hash):
	trx = json.loads(shell_execute("bitcoin-cli getrawtransaction {} true {}".format(trx_hash, blk_hash)))
	return trx

def run(block_hash, nostr_helper, nsec):
	block = get_block(block_hash)
	trxs = block.get('tx')[1:]
	print(len(trxs), block_hash)
	for trx in trxs:
		raw_vout = get_raw_trx(trx, block_hash).get('vout')
		for vout in raw_vout:
			asm = vout.get('scriptPubKey').get('asm')
			if 'OP_RETURN' in asm:
				try:
					msg = bytes.fromhex(asm.replace("OP_RETURN ", "")).decode("utf-8")
					a = shell_execute("{} {} {} \"{}\"".format(nostr_helper, nsec, trx, msg))
					# print(a)
				except Exception as e:
					# print(e)
					continue
	

# print(get_block("00000000000000000000faa17eccc2d5cc77dde99e8295955d2f416a9de6125d").get("tx")[0])
# pprint(get_raw_trx("88e8344716a5642276bb648e8459353dbddfc6c06f8dbda066120718e15918d1", "00000000000000000000faa17eccc2d5cc77dde99e8295955d2f416a9de6125d"))



# run("0000000000000000000703bb3c2a01b9ec6c7e2197d7460a8a1021cb92b459a5")
package main

import (
	"nostr_opreturn/src/nostrhelper"
	"os"
)

func main() {

	nsec := os.Args[1]
	trxHash := os.Args[2]
	msg := os.Args[3]

	// fmt.Println(trxHash, msg)

	nostrhelper.PostNote(trxHash, msg, nsec)

}

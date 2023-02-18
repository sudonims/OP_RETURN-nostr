package main

import (
	"nostr_opreturn/src/nostrhelper"
	"os"
)

func main() {

	trxHash := os.Args[1]
	msg := os.Args[2]

	// fmt.Println(trxHash, msg)

	nostrhelper.PostNote(trxHash, msg)

}

package main

import (
	"fmt"
	"os"
)

func main() {

	trxHash := os.Args[1]
	msg := os.Args[2]

	fmt.Println(trxHash, msg)

	// nostrhelper.PostNote(trxsHash, msg)

}

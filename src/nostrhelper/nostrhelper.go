package nostrhelper

import (
	"context"
	"fmt"
	"os"
	"strings"
	"time"

	"github.com/nbd-wtf/go-nostr"
	"github.com/nbd-wtf/go-nostr/nip19"
)

func PostNote(trxHash string, msg string, nsec string) bool {

	relayList := []string{"wss://nostr.zebedee.cloud", "wss://nostr-pub.wellorder.net", "wss://relay.damus.io"}

	ev := nostr.Event{}

	var sk string
	if _, s, e := nip19.Decode(nsec); e == nil {
		sk = s.(string)
	}

	if pub, e := nostr.GetPublicKey(sk); e == nil {
		ev.PubKey = pub
		if npub, e := nip19.EncodePublicKey(pub); e == nil {
			fmt.Fprintln(os.Stderr, "using:", npub)
		}
	} else {
		panic(e)
	}

	ev.CreatedAt = time.Now()
	ev.Kind = 1
	content := fmt.Sprintf("      New OP_RETURN      \n%s\nhttps://mempool.space/tx/%s", msg, trxHash)

	ev.Content = strings.TrimSpace(content)
	ev.Sign(sk)

	for _, url := range relayList {
		ctx, cancel := context.WithCancel(context.Background())

		relay, err := nostr.RelayConnect(ctx, url)

		if err != nil {
			panic(err)
		}

		relay.Publish(ctx, ev)

		cancel()
	}

	// if status == nostr.PublishStatusSucceeded {
	// 	return true
	// } else {
	// 	return false
	// }
	return true
}

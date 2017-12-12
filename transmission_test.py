#!/usr/bin/env python3

import transmissionrpc

tc = transmissionrpc.Client('localhost', port=9091)
tc.add_torrent("./Miss_Sloane.torrent")
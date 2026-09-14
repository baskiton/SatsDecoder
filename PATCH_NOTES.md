# N6RFM fork of SatsDecoder — patch notes

This fork of [baskiton/SatsDecoder](https://github.com/baskiton/SatsDecoder)
contains one change: a fix for a false "Connection lost" disconnect on the
`KISS TCP Client` connection type.

## The bug

When using `KISS TCP Client` mode, `ui.py`'s `_receive()` method reads a
frame via `utils.kiss_read_stream()` and then checks:

```python
if not frame:
    if not self.is_server:
        self.show_warn(message='%s: Connection lost' % self.name)
    return 1   # ends the read loop - the whole session stops
```

`kiss_read_stream()` (in `utils.py`) returns **`None`** when the TCP
connection has genuinely closed (any of its `recvall()` calls returning
empty bytes), but returns **`b''`** (empty bytes) when it successfully
parses a well-formed KISS data frame that just happens to carry zero
payload bytes (`FEND`, a data control byte, `FEND` — a legitimate, valid,
empty KISS frame).

`not frame` evaluates to `True` for **both** `None` and `b''`. The code
has no way to tell "the socket closed" apart from "I received a real,
empty frame" — both are treated identically as a fatal disconnect, ending
the session and requiring the user to manually reconnect.

## Why this matters in practice

This surfaced while building an automated multi-satellite relay
(`geoscan-fleet`) sitting upstream of SatsDecoder. Any mechanism that
legitimately produces a zero-length KISS frame — including a deliberate
TCP keepalive/heartbeat frame sent to keep an otherwise-idle connection
demonstrably alive — trips this exact code path and forces a full
disconnect, even though the connection itself is perfectly healthy. This
made an idle downstream connection indistinguishable, from the decoder's
point of view, from a genuinely dead one.

## The fix

One line, `SatsDecoder/ui.py`:

```diff
- if not frame:
+ if frame is None:
```

This makes the check specifically about "did the read function report
the connection closed" (`None`) rather than "is the frame falsy" (which
also incorrectly matches a legitimate empty frame). A real disconnect
still reports `None` and is still handled identically to before; a
legitimate empty/heartbeat frame is now correctly treated as "no data
this time" rather than "connection lost."

## Testing performed

- Traced `kiss_read_stream()`'s control-flow by hand against both a
  genuinely closed socket (all `recvall()` calls return `b''`, function
  returns `None` from three separate `return` statements) and a
  well-formed empty data frame (`FEND`, control byte in `KISS_CMD_DATA`,
  immediate closing `FEND` — function returns `b''`).
- Confirmed the pre-patch code treats both cases identically via
  `if not frame:`.
- Applied the one-line patch and confirmed via source inspection that the
  `is None` check correctly discriminates the two cases while leaving
  every other code path (real data frames, timestamp frames, genuine
  disconnects) unchanged.
- Deployed on a live multi-satellite ground station relay and confirmed
  the decoder no longer disconnects spuriously.

## Upstream contribution

This is a one-line, narrowly-scoped bug fix unrelated to any
project-specific customization. Per upstream's `CONTRIBUTING.md` (PRs
target the `dev` branch, contributions licensed as MIT), this is intended
to be offered upstream as a pull request in addition to living here.

## License

Unchanged from upstream: GPL-3.0-or-later, with the majority of the
codebase (including this changed line) under MIT. This fork's own
changes are contributed under the same terms as required by upstream's
`CONTRIBUTING.md`.

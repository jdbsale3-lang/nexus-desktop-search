# Making the confirm gate GLOBAL — wiring guide

The confirm_gate skill exists but is opt-in. To make every irreversible
answer require confirmation, wrap the answer path in the flagship/ZEUS engine:

## Where
- The ZEUS reach/answer router (agent-reach-bridge or flagship JS answer handler).

## What to change
1. Define IRREVERSIBLE intents: incident_create, quote_builder (accept/send),
   channel sends (twitter/linkedin post), file delete, DB writes.
2. Before emitting the final action for those intents, emit:
   `{"requires_confirmation": true, "confirm_token": "<crypto-token>", "summary": "...reveals what will happen..."}`
3. Execute the action ONLY when the caller echoes the same confirm_token.
4. Log every confirmed/unconfirmed attempt to the audit lane.

## Skills layer
- Use the existing undo_stack to register the action BEFORE acting, so even
  confirmed actions can be reversed.
- Keep incident_create in the ledger with a "pending_confirmation" status until
  the token is verified.

## Test
Fixture: every irreversible intent returns requires_confirmation; every
mismatched token is rejected without side effects. Confirm-then-report.

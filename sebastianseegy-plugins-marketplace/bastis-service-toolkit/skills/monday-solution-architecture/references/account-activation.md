# Account activation & entitlement reference (Bigbrain)

Use this when a client's underlying need isn't "how do we configure/build this" but
"can you turn X on for our account" — a trial, a feature grant, an integration package,
or a billing/account-state change. That's an **entitlement** question, not a board-
architecture one, and it routes differently.

Source: internal KB article "Bigbrain permissions"
(https://mondayall.com/knowledge/zoc6QeMcBkKevRLJQKc3). Bigbrain is monday's internal
admin tool with ~180 granular permissions; most are user-management or internal-tooling
noise. The subset below is what actually changes an account's capabilities or state.

**Important caveat:** almost none of these sit with a generic IC role — they're held by
CX, Billing, Renewal, Finance, and BizOps roles. This is "here's the lever that exists
and who to route to," not "here's what you can self-serve." Confirm current ownership
before promising a client a specific turnaround.

## Feature & product entitlement
- `grant_feature` / `ungrant_feature` — grant or revoke a free feature on the account
- `grant_integrations` — grant additional integrations
- `grant_automations` — grant automation/integration packages (check with billing/finance first)
- `grant_work_os_products` — grant WorkOS product infrastructure
- `start_trial_on_product_solution` — start a trial for a specific product (CRM, Dev, Service, etc.)
- `reset_trial` — extend/add days to a trial period
- `set_v9_transition` — move the account onto v9 pricing
- `start_automations_cycle` — renew the automation-actions limit mid-cycle
- `disable_automations` / `archive_automations` — turn off or archive an account's automations

## Account state
- `enable_account` / `disable_account` — reopen or disable (view-only) an account
- `block_account_for_x_days` / `unblock_account_for_x_days`
- `cancel_plan_for_account` / `reactivate_plan` / `cancel_plan_on_renewal`
- `change_from_trial_to_free_tier`
- `mark_account_as_npo` — move to NPO plan
- `set_free_users` / `set_negative_free_users` — grant extra free seats (verify with billing)

## Billing / payment activation
- `cc_manual_activate` / `wire_manual_activate` — activate an account after manually entering
  payment details
- `external_payment` / `revert_external_payment` — activate/deactivate a wire account
- `reactivate_bluesnap_subscription`
- `move_to_cc` / `wire_to_cc` / `swap_cc` — change payment method or update card details
- `import_so` / `scheduled_so` / `cancel_scheduled_activation` — Salesforce SO import and
  scheduled future activation
- `create_account_billing_contract`
- `apply_coupon_on_active_contract`, `refund`, `revert_chargeback`

## Account structure
- `merge_account(s)`, `start_consolidation_process` — combine ARR/account records
- `sm_revert_to_prev_subscription`, `sm_revoke_change_plan_on_renewal`, `sm_edit_customer_info`

## How to use this in a solution brief

1. **Name the lever** (e.g. "this needs `grant_integrations` on their account") in the
   internal brief so the right internal request goes to the right team.
2. **Don't expose internal permission names to the client** — state the outcome ("we
   can extend your trial by two weeks — confirming internally and I'll follow up") and
   avoid promising a timeline you can't back.
3. **Configuration beats entitlement by default.** If it's ambiguous whether the ask is
   solvable natively (this skill's usual territory) or needs a Bigbrain grant, answer the
   configuration question first — entitlement asks are the exception, not the rule.

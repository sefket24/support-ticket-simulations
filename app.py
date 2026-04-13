import streamlit as st

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Support Ticket Simulations",
    page_icon="🎫",
    layout="wide",
)

# ── Static ticket data ────────────────────────────────────────────────────────
TICKETS = {
    "Billing Issue": {
        "label": "💳  Billing Issue",
        "customer_message": (
            "Hi – I just got charged twice for my subscription this month. "
            "Once on the 1st and again on the 14th. I didn't change my plan or "
            "anything like that. I've been a paying customer for over a year and "
            "this has never happened before. Can you please look into this and "
            "refund the extra charge? I'm a little frustrated because I didn't "
            "get any email explaining it."
        ),
        "support_response": [
            "Thanks for flagging this — I can see why two charges in the same month "
            "would feel off, especially without any explanation.",
            "I'm going to review your billing timeline to confirm exactly what "
            "triggered the second charge. In cases like this, it's usually tied to "
            "a mid-cycle change (like a payment update or plan adjustment) that "
            "generates a prorated invoice alongside the regular renewal — but I'll "
            "verify that against your account activity.",
            "If this turns out to be a duplicate or unintended charge, I'll get a "
            "refund issued right away and make sure your billing cycle is corrected "
            "so it doesn't happen again. I'll follow up within one business day "
            "with a clear breakdown of what happened.",
            "Just to double check — have there been any recent changes to your "
            "payment method or plan on your end?",
        ],
        "internal_notes": {
            "root_cause": (
                "Most likely a mid-cycle billing event (payment method update or "
                "attempted plan change) generating a prorated invoice. Less likely: "
                "delayed payment retry overlapping with renewal cycle."
            ),
            "checking": (
                "Review subscription event log for: plan change attempts, payment "
                "method updates, retry logic between charge dates. "
                "Cross-check with Stripe charges to confirm whether this is a "
                "valid proration, duplicate charge, or retry artifact."
            ),
            "escalation": (
                "No escalation yet. Billing logs should confirm cause. Escalate to "
                "engineering only if no corresponding event is found (potential "
                "billing system inconsistency)."
            ),
            "product_gap": (
                "No proactive communication for mid-cycle charges. This creates "
                "avoidable confusion. Recommend adding a transactional email "
                "explaining why the charge occurred and how it affects the "
                "billing cycle."
            ),
        },
    },
    "Permissions Issue": {
        "label": "🔒  Permissions Issue",
        "customer_message": (
            "Hey, we're having a really annoying problem. Our whole design team "
            "got added to a shared library two weeks ago but half of them still "
            "can't access the files. They can see the library listed but when they "
            "click into it they get an error that says they don't have permission. "
            "We've tried removing and re-adding them, logging out, even switching "
            "browsers. Nothing works. This is blocking us from starting a project."
        ),
        "support_response": [
            "Thanks for the detailed rundown—that kind of systematic troubleshooting "
            "on your end actually helps a lot and rules out the most common fixes.",
            "The symptom you're describing—library visible but inaccessible—is "
            "usually caused by a permissions state mismatch between the team roster "
            "and the library's access control list. This can happen when members "
            "are added while the library is in a transitional state (e.g., during "
            "a plan upgrade or org restructure).",
            "I'd like you to share the affected library's URL and the email addresses "
            "of two or three blocked users so I can inspect the permission records "
            "directly. In the meantime, a temporary workaround is to duplicate the "
            "library and share the copy fresh—it won't carry the broken permissions.",
        ],
        "internal_notes": {
            "root_cause": (
                "Likely a permission propagation failure. Members show as added in "
                "the UI but the ACL (access control list) on the library resource "
                "was not updated server-side. Can happen after bulk-adds or during "
                "plan-tier changes that temporarily lock library records."
            ),
            "checking": (
                "Need the library ID and affected user IDs to query the permissions "
                "table directly. Will check for any recent org-level changes "
                "(seat additions, plan upgrades) that correlate with the onset of "
                "the issue. Also checking for any known incidents flagged in the "
                "past two weeks."
            ),
            "escalation": (
                "Will escalate to Tier 2 / platform engineering if the permissions "
                "table shows the users as correctly added but the library still "
                "denies access. That gap would indicate a caching or auth token "
                "issue that requires a backend fix."
            ),
            "product_gap": (
                "Bulk-add workflows don't include a confirmation state that verifies "
                "ACL propagation succeeded. A lightweight async check after bulk "
                "adds would catch this class of failure before users are blocked."
            ),
        },
    },
    "Feature Issue": {
        "label": "🔄  Feature Issue",
        "customer_message": (
            "Something is really wrong with my syncing. I made a bunch of updates "
            "to a component in the main file and my teammates are telling me they "
            "still see the old version. I've published the changes, refreshed "
            "multiple times, and even asked them to hard reload. It's been almost "
            "a day and they're still not seeing the updates. We're on a deadline "
            "and this is really stressful."
        ),
        "support_response": [
            "I hear you—this is a frustrating situation, especially with a deadline "
            "in play. Let's get this resolved as quickly as possible.",
            "When published component changes aren't reflected for other editors, "
            "it's usually a sync cache issue on their end or a publish that "
            "technically completed but didn't propagate to all connected files. "
            "One thing worth checking: in the affected files on your teammates' "
            "end, go to the Libraries panel and look for an 'Update available' "
            "prompt. Even after a hard reload, library updates sometimes need to "
            "be accepted explicitly from within the subscriber file.",
            "If the update prompt isn't appearing, that points to a propagation "
            "failure on our side. Please share the main file link and one affected "
            "subscriber file link so I can check the publish event log and confirm "
            "the update was registered correctly.",
        ],
        "internal_notes": {
            "root_cause": (
                "Two probable causes: (1) the publish completed client-side but "
                "failed to register on the server, leaving subscriber files "
                "unaware of the new version; or (2) the publish succeeded but "
                "cache invalidation didn't propagate within the expected TTL. "
                "A 24-hour lag points more strongly to a server-side event failure."
            ),
            "checking": (
                "Need the main file and one subscriber file to pull publish event "
                "logs. Looking for the timestamp of the last publish event, whether "
                "a version bump was registered, and whether subscriber files "
                "received the update webhook. Will also check for any publish "
                "service degradation in the past 48 hours."
            ),
            "escalation": (
                "Escalating to Tier 2 if the publish event log shows a successful "
                "publish but subscriber files have no update record. That gap is "
                "not resolvable at Tier 1. If it's a cache issue, Tier 2 can force "
                "an invalidation. Marking as high priority due to active deadline."
            ),
            "product_gap": (
                "Library update prompts rely on polling rather than push "
                "notification. Users have no visibility into whether a publish "
                "succeeded or is propagating. A publish confirmation state with "
                "a visible propagation status would reduce time-to-awareness of "
                "failures like this one."
            ),
        },
    },
}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Tickets")
    ticket_keys = list(TICKETS.keys())
    selected = st.radio(
        label="Select a ticket",
        options=ticket_keys,
        format_func=lambda k: TICKETS[k]["label"],
        label_visibility="collapsed",
    )

# ── Main panel ────────────────────────────────────────────────────────────────
ticket = TICKETS[selected]

st.title("Support Ticket Simulations")
st.caption(
    "A portfolio artifact showing how a support specialist works through "
    "customer issues end-to-end."
)

st.divider()

# Section 1 – Customer Message
st.subheader("1. Customer Message")
st.markdown(
    f"""
    <div style="
        background-color: #f7f7f7;
        border-left: 3px solid #d0d0d0;
        padding: 16px 20px;
        border-radius: 4px;
        font-size: 0.95rem;
        line-height: 1.65;
        color: #333;
    ">
        {ticket["customer_message"]}
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")  # breathing room

# Section 2 – Support Response
st.subheader("2. Support Response")
for paragraph in ticket["support_response"]:
    st.write(paragraph)

st.write("")

# Section 3 – Internal Notes (collapsible)
with st.expander("3. Internal Notes"):
    notes = ticket["internal_notes"]

    st.markdown("**Suspected root cause**")
    st.write(notes["root_cause"])

    st.markdown("**What is being checked**")
    st.write(notes["checking"])

    st.markdown("**Escalation decision**")
    st.write(notes["escalation"])

    st.markdown("**Product / process gap**")
    st.write(notes["product_gap"])

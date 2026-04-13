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
            "Just to double check — have there been any recent changes to your "
            "payment method or plan on your end?",
            "If this is a duplicate or unintended charge, I'll issue a refund right "
            "away and make sure your billing cycle is corrected so it doesn't happen "
            "again. I'll follow up within one business day with a clear breakdown "
            "of what happened.",
        ],
        "internal_notes": {
            "root_cause": (
                "Most likely a mid-cycle billing event (payment method update or "
                "attempted plan change) given the timing between charges."
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
            "Thanks for laying all of that out — and for trying those steps already. "
            "I know this is blocking your team, so I'm going to check this from our "
            "side so we can pinpoint what's blocking access.",
            "What you're seeing — being able to view the library but not access it — "
            "usually points to access not fully applying to some members. I'll verify "
            "that directly against the library's access settings and your team roster.",
            "Could you share the library link and one or two affected user emails? "
            "That's enough for me to trace this quickly.",
            "In the meantime, I'd avoid duplicating the library since that can create "
            "version inconsistencies. If this is a permissions sync issue, we should "
            "be able to resolve it without needing a workaround.",
            "I'll follow up as soon as I've confirmed the cause and next steps.",
        ],
        "internal_notes": {
            "root_cause": (
                "Most likely permission propagation failure given partial impact "
                "across users (not a full outage)."
            ),
            "checking": (
                "Library ID + affected user IDs. "
                "Permissions table vs UI state. "
                "Recent org-level changes (bulk adds, plan updates). "
                "Any related incidents in the same timeframe."
            ),
            "escalation": (
                "Escalate to engineering if users are correctly present in ACL but "
                "access is denied — likely caching or auth inconsistency."
            ),
            "product_gap": (
                "No validation step after bulk member adds to confirm ACL "
                "propagation. Adding a post-action verification would prevent "
                "partial access states."
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
            "I can see why this is stressful, especially with a deadline — "
            "let's get this unblocked.",
            "When published component changes don't show up for other editors, "
            "it's usually one of two things: the update hasn't been applied in "
            "their file yet, or the publish didn't fully propagate.",
            "In the affected files, ask your teammates to open the Libraries panel "
            "and check for an 'Update available' prompt. Even after a hard reload, "
            "updates sometimes need to be accepted from within the file.",
            "If there's no update prompt showing, that likely means the publish "
            "didn't propagate correctly on our side. Please share the main file "
            "link and one affected subscriber file so I can check the publish event "
            "log and confirm the update registered properly.",
            "I'll prioritize this given the deadline and follow up as soon as I've "
            "confirmed what's happening.",
        ],
        "internal_notes": {
            "root_cause": (
                "Most likely a publish propagation failure; secondary possibility "
                "is cache invalidation delay."
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

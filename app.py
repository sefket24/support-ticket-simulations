import streamlit as st

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Support Ticket Simulations",
    page_icon="🎫",
    layout="centered",
)

# --- STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@300;400;600;700&display=swap');

    :root {
        --text-primary: #f7f9f9;
        --text-secondary: #8b98a5;
        --bg-main: #15202b;
        --bg-card: #1e2732;
        --accent: #1d9bf0;
        --border: #38444d;
    }

    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        font-family: 'Inter', sans-serif;
        background-color: var(--bg-main) !important;
        color: var(--text-primary) !important;
    }

    /* Custom Header */
    .candidate-header { border-bottom: 1px solid var(--border); padding-bottom: 16px; margin-bottom: 24px; }
    .candidate-name { font-size: 22px; font-weight: 700; color: var(--text-primary); }
    .candidate-title { font-size: 13px; color: var(--accent); font-weight: 500; margin-bottom: 4px; }
    .contact-links { font-size: 11px; color: #ffffff; display: flex; gap: 12px; margin-top: 4px; }
    .contact-links a { 
        color: #ffffff; 
        text-decoration: none; 
        border-bottom: 1px solid rgba(255,255,255,0.3); 
        padding-bottom: 1px;
        transition: all 0.2s ease;
    }
    .contact-links a:hover { 
        color: var(--accent); 
        border-bottom-color: var(--accent);
        opacity: 0.9;
    }
    
    /* Completely Fix Expanders (Internal Notes) */
    [data-testid="stExpander"] {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        margin-top: 10px !important;
    }
    
    /* Target the clickable header part specifically */
    [data-testid="stExpander"] details summary {
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border-radius: 12px 12px 0 0 !important;
        padding: 0.5rem 1rem !important;
    }
    
    /* Remove default hover highlights that turn white */
    [data-testid="stExpander"] details summary:hover {
        background-color: var(--bg-main) !important;
        color: var(--accent) !important;
    }

    [data-testid="stExpander"] [data-testid="stVerticalBlock"] {
        background-color: var(--bg-card) !important;
        padding: 1rem !important;
        border-radius: 0 0 12px 12px !important;
    }
    
    /* Ensure all text inside the expander is primary color */
    [data-testid="stExpander"] * {
        color: var(--text-primary) !important;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: var(--bg-main) !important;
        border-right: 1px solid var(--border) !important;
    }
    [data-testid="stSidebar"] * {
        color: var(--text-primary) !important;
    }
    
    /* Hide Streamlit components */
    #MainMenu, footer, header, [data-testid="stHeader"] { visibility: hidden; display: none; }
</style>
""", unsafe_allow_html=True)

# ── Static ticket data ────────────────────────────────────────────────────────
TICKETS = {
    "Seat Management & Billing": {
        "label": "💳  Seat Management & Billing",
        "customer_message": (
            "Hey, I just noticed an extra charge on our team account. We're on a "
            "Professional plan and I'm the only admin, but there's a second $15 charge "
            "on the 12th. I didn't add anyone new. Can you explain why we're being billed twice?"
        ),
        "support_response": [
            "This usually comes down to a seat upgrade mid-cycle. In Figma, adding a new "
            "editor—or even a viewer taking an action that requires a full seat—generates "
            "a pro-rated invoice for the rest of the billing period.",
            "I'll check the 'Members' tab in your team settings to see exactly which user "
            "was upgraded. If this was accidental, like someone being invited to a file "
            "with 'Can Edit' instead of 'Can View,' I can revert the seat and help with "
            "a credit for the unused time.",
            "Moving forward, it might be worth setting your default seat type to 'Viewer-restricted' "
            "for new invites. It prevents these surprise upgrades while still letting "
            "everyone jump into files as needed.",
            "I should have an answer for you in just a few minutes once I’ve audited the logs.",
        ],
        "internal_notes": {
            "root_cause": (
                "Mid-month seat upgrade triggered by an invitation or permission change."
            ),
            "checking": (
                "Access logs for the 'Professional' team. Identifying which 'Viewer' "
                "was promoted to 'Editor' and cross-referencing with the Stripe invoice ID."
            ),
            "escalation": (
                "Not required. Simple seat audit and potential refund/credit."
            ),
            "product_gap": (
                "The 'Invite' flow doesn't clearly show that 'Can Edit' in a professional "
                "team creates an immediate billable seat. A warning modal would reduce "
                "billing friction here."
            ),
        },
    },
    "Permissions & Libraries": {
        "label": "🔒  Permissions & Libraries",
        "customer_message": (
            "Our developers are invited to the project but they can't see the 'Core UI' "
            "library in their assets panel. I've definitely published it and they have "
            "'Can View' access. What are we missing? They used to see it fine last week."
        ),
        "support_response": [
            "If they can see project files but not the library itself, it's usually "
            "because library visibility is managed separately from file permissions. "
            "In most cases, even with 'View' access, it won't appear in the Assets panel "
            "unless it's explicitly enabled for the team.",
            "Start by checking the 'Libraries' dashboard to ensure Core UI is toggled "
            "to 'on' for everyone. If that’s already enabled, it’s worth having them "
            "verify they haven't accidentally filtered their Assets panel to 'Current file' only.",
            "If that settings check doesn't clear it up, I can loop in our engineers "
            "directly to track down why the library metadata isn't surfacing for your team.",
            "Let me know what you find on that libraries toggle.",
        ],
        "internal_notes": {
            "root_cause": (
                "Library disabled at the team level or user-level asset filtering."
            ),
            "checking": (
                "Team-wide library defaults. Verify if 'Core UI' is set to 'All files' "
                "or if it needs to be manually enabled per-file."
            ),
            "escalation": (
                "Engineering if the library is enabled but metadata isn't "
                "populating in the Assets panel for specific users (ACL sync issue)."
            ),
            "product_gap": (
                "There's no visual indicator in 'Can View' mode that a library exists "
                "but is disabled. Improving the search empty-state in the Assets panel "
                "could guide users to Enable hidden libraries."
            ),
        },
    },
    "Components & Syncing": {
        "label": "🔄  Components & Syncing",
        "customer_message": (
            "I published an update to our button component (changed the 8px radius to 4px). "
            "Most of the team sees the update, but in one specific file, the buttons still "
            "have the old 8px radius. I've refreshed, but nothing is changing. Is it a bug?"
        ),
        "support_response": [
            "This usually happens when a specific instance has a local 'override' "
            "taking precedence. If someone manually adjusted the radius before the "
            "update was published, Figma tries to preserve that local change so we "
            "don't accidentally break your layout.",
            "One thing to try is selecting that button and clicking 'Reset all overrides' "
            "in the right-hand panel. If the radius jumps to 4px, we’ve confirmed it was "
            "a local override blocking the sync.",
            "If you’re seeing this frequently, it might be worth using 'Variants' for "
            "these button states. It makes it much harder for local overrides to stick "
            "around when you update the main library components.",
            "If resetting those overrides doesn't fix it, feel free to share the link "
            "to the file and I can investigate if there is a propagation delay on the service side.",
        ],
        "internal_notes": {
            "root_cause": (
                "Local instance override blocking library style propagation."
            ),
            "checking": (
                "Selection state of the affected instance. 'Reset all overrides' "
                "is the primary validation step here."
            ),
            "escalation": (
                "Engineering only if 'Reset all overrides' fails to pull the "
                "latest library definition (potential cache invalidation failure)."
            ),
            "product_gap": (
                "Users don't have visibility into which properties are 'overridden' "
                "vs 'inherited' without manual checking. A 'Conflict' indicator in "
                "the Properties panel would help troubleshoot this instantly."
            ),
        },
    },
    "System Outage": {
        "label": "🚨  System Outage (Escalation)",
        "customer_message": (
            "None of our team can open files right now. It just keeps loading and then "
            "gives a connection error. We’ve tried different browsers and it’s the same "
            "for everyone. Is this something on our end? We have a deadline in an hour."
        ),
        "support_response": [
            "I'm seeing similar reports on our side, so this doesn't look specific "
            "to your team or machine. Given this is affecting everyone right now, "
            "I'm treating this as high priority and tracking the fix minute-by-minute.",
            "Our engineering team is already on it, but while we wait for a fix, it's "
            "worth checking if you can access files through the Desktop App or a "
            "mobile hotspot, as that can sometimes bypass localized connection hiccups.",
            "I've also looped in our technical leads so I can keep you updated the "
            "second I have a firm timeline for a resolution. We’re working to get "
            "you back into your files as fast as possible.",
            "I'll keep a close eye on this—if anything changes on your end, let me know.",
        ],
        "internal_notes": {
            "root_cause": (
                "Unconfirmed. Likely a CDN or API service degradation."
            ),
            "checking": (
                "Engineering incident logs, status page updates, and error rate "
                "metrics. Investigating potential regional outages."
            ),
            "escalation": (
                "High. Active engineering investigation in progress. Escalated to "
                "Tier 2 for immediate user outreach once resolved."
            ),
            "product_gap": (
                "In-app status indicators are currently too subtle during partial "
                "outages. Improving global incident notifications would reduce "
                "support volume and user anxiety during these events."
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

# Candidate Header
st.markdown(f"""
<div class="candidate-header">
    <div class="candidate-name">Sefket Nouri</div>
    <div class="candidate-title">Figma Product Support Specialist candidate</div>
    <div class="contact-links">
        <a href="mailto:me@sefketnouri.com">me@sefketnouri.com</a>
        <a href="https://www.linkedin.com/in/sefketnouri/" target="_blank">LinkedIn</a>
        <a href="https://github.com/sefket24" target="_blank">GitHub</a>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="color: var(--text-secondary); font-size: 14px; margin-top: -20px; margin-bottom: 24px; line-height: 1.4;">
    Simulated support scenarios showing how I investigate issues, identify root causes, and guide users to clear, confident resolutions.
</div>
""", unsafe_allow_html=True)

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
        background-color: var(--bg-card);
        border: 1px solid var(--border);
        border-left: 4px solid var(--accent);
        padding: 16px 20px;
        border-radius: 12px;
        font-size: 0.95rem;
        line-height: 1.65;
        color: var(--text-primary);
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

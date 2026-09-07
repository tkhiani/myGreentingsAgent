# Time-Based Greeting Agent

## Business challenge

Build an AI agent that greets users based on the time of day (morning, afternoon, evening, night), delivering personalized, context-aware salutations automatically.

## Business Goals & Success Criteria

| Metric | Baseline | Target | Timeline | Process / Capability | Source |
|--------|----------|--------|----------|----------------------|--------|
| Correct time-based greeting delivered | 0% automated | 100% accurate greetings (morning/afternoon/evening/night) | Immediate | User Engagement | user |

## Key Milestones

1. **User Request Received** — Agent receives a greeting request from the user.
2. **Time Detection** — Agent determines the current time of day.
3. **Greeting Generated** — Agent produces the appropriate greeting based on time.
4. **Response Delivered** — Greeting is returned to the user.

## Business Architecture (RBA)

### End-to-End Process
Lead to Cash (BPS-370)

### Process Hierarchy
```
Lead to Cash (E2E)
└── Manage Customers and Channels
    └── Manage customers (generic) (BPS-370)
        └── Manage customer experience
```

### Summary
The time-based greeting agent maps to customer experience management within the Lead to Cash process, enabling personalized, context-aware user interactions.

## Fit Gap Analysis

| Requirement | Standard asset(s) found | API ORD ID | MCP Server ORD ID | MCP Server Version | Gap? | Notes |
|-------------|------------------------|------------|-------------------|-------------------|------|-------|
| Time-based personalized greeting | No standard SAP product covers this directly | — | — | — | Yes | Custom AI agent required |
| User engagement platform | SAP Customer Data Platform (Customer Journey Orchestration) | — | — | — | No | Out of scope for this simple use case |

### Key findings
- No standard SAP product delivers a time-aware greeting agent out of the box — custom development is required.
- A lightweight Python AI agent (A2A protocol) is the simplest and most appropriate solution.
- No external API integrations are needed; the agent only requires system time access.
- The solution is self-contained and deployable on SAP BTP.

## Recommendations

### Time-Based Greeting AI Agent

#### Executive Summary
Lightweight Python AI agent delivering time-aware greetings.

#### Recommended Solution
A pro-code Python agent following the A2A protocol, deployed on SAP BTP. The agent detects the current time of day and responds with an appropriate greeting (Good Morning / Good Afternoon / Good Evening / Good Night).

#### Recommended solution category
AI Agent

#### Intent fit
95%

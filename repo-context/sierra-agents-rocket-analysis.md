# Repository Analysis: sierra-agents-rocket

**Repository URL:** `No git remote configured (local repository)`
**Analysis Date:** 2026-03-02
**Analyzer:** repo-analyzer sub-agent

---

## 1. Repository Overview

**Project Type:** Monorepo containing multiple conversational AI agents
**Purpose:** Conversational AI agents for Rocket Companies' mortgage and real estate services, built on the Sierra Agent Platform. Provides intelligent customer assistance across purchase, refinance, servicing, and property search use cases.
**Key Characteristics:**
- Multi-agent architecture supporting 10+ distinct conversational agents (Rocket Assist, RMA, RMO, Servicing, Outbound Voice, etc.)
- Shared component library enabling code reuse across agents
- Complex integration with multiple contact center systems (Bananaphone, LiveAgent, MIAW)
- Production-grade mortgage assistance with TRID compliance, PAL (Pre-Approval Loan) application flows, and IPAC (Interactive Pre-Approval Chat)
- JSX-based conversational programming model using Sierra Agent SDK

## 2. Technology Stack

**Languages:** TypeScript (ES2024, strict mode) - 628+ source files
**Framework:** Sierra Agent SDK (v0.20260227.7180733) with custom JSX pragma for conversational flows
**Key Dependencies:**
- `@sierra/agent` - Core agent framework with conversational primitives
- `@sierra/lib` - Contact center integrations (LiveAgent, MIAW, Bananaphone)
- `@sierra/content-schema` - CMS-driven content management
- `@sierra/web` & `@sierra/web-react` - Custom React UI components for chat interface
- `@sierra/cli` - Build, upload, and deployment tooling
**Build/Package:** pnpm (workspaces), Sierra CLI for agent builds
**Database:** N/A (stateless agent with external API integrations)
**Infrastructure:** Sierra cloud platform, Node.js 20 runtime, multi-environment deployment (production/staging/mock)

**Testing:** Jest 29.7.0 with @swc/jest, Sierra test framework for scenario/compliance tests
**Code Quality:** Pre-commit hooks (Prettier, detect-secrets, large file checks), ESLint

## 3. Architectural Patterns

### Primary Pattern

**Domain-Driven Monorepo Architecture**
**Rationale:** Supports multiple product-specific agents (Rocket Mortgage, RMA, RMO, Servicing) while sharing common infrastructure (contact center, APIs, UI components). Each agent is a self-contained domain with its own conversational logic, skills, and test suite, but leverages shared libraries to maintain consistency and reduce duplication.

### Secondary Patterns

**Skills-Based Conversational Architecture** (`agents/rocket/skills/`)
- Modular skill system where each skill represents a distinct capability (transfer, lead-collection, knowledge, listings, calculators)
- Skills are JSX components that define conversational flows with state management and API integration
- Priority-based skill exceptions for handling critical scenarios (death mentions, TRID compliance, client frustration)

**Content Management System Pattern** (`content-schema.ts`)
- Declarative CMS schema using `@sierra/content-schema` for managing dynamic content (phone numbers, operating hours, transfer destinations, guardrails)
- Content validated at build time and accessed via strongly-typed `content-types.ts`
- Enables non-developer content updates without code changes

**Composite Contact Center Pattern** (`shared/contact-center/`)
- Adapter pattern wrapping multiple contact center systems (Bananaphone, LiveAgent, MIAW, RocketContactCenter)
- CompositeContactCenter provides unified interface for transfers, message handling, and conversation management
- Graceful fallback between systems based on availability

**API Layer Abstraction** (`agents/rocket/api/`)
- Abstract API interface with MockAPI and ProductionAPI implementations
- Environment-based API switching (production/staging/mock)
- Centralized error handling and response mapping

### Design Principles

- [x] Separation of Concerns - Clear separation between conversational logic (skills), API integration, content management, and UI components
- [x] Single Responsibility - Each skill handles one domain (transfer, lead collection, knowledge search)
- [x] Dependency Inversion - API abstraction allows testing with MockAPI without modifying agent code
- [x] DRY - Shared libraries (`agents/shared/`) for contact center, API types, IPAC flows, web components

**Notes:**
- Strong adherence to Sierra's conversational programming model using JSX for agent flows
- Comprehensive guardrails system (refusal guardrails, respond guardrails, risk categories) embedded in conversational logic
- Memory/state management using Sierra's `useMemory` and custom `useRocketRootStore` hooks
- Post-conversation hooks for lead creation, IPAC submission, and analytics tracking

## 4. Module Structure

### Directory Layout
```
sierra-agents-rocket/
├── agents/                           # All conversational agents
│   ├── rocket/                      # Primary Rocket Assist agent
│   ├── rma/                         # Rocket Mortgage Application agent
│   ├── rmo/                         # Rocket Mortgage Origination agent
│   ├── servicing/                   # Servicing agent
│   ├── servicing-ivr/               # IVR-specific servicing
│   ├── pro/                         # Professional/partner agent
│   ├── outbound-voice/              # Outbound calling agent
│   ├── outbound-proactive-retention/# Retention campaigns
│   ├── redfin-buying-power/         # Redfin partnership agent
│   ├── parent-agent/                # Parent orchestration agent
│   └── shared/                      # Shared libraries
├── bin/                             # Build and deployment scripts
├── packages/                        # Shared npm packages
├── .github/workflows/               # CI/CD pipelines
├── pnpm-workspace.yaml              # Monorepo workspace config
└── jest.config.base.js              # Base test configuration
```

### Core Modules

**Rocket Assist Agent** (`agents/rocket/`)
- Responsibility: Primary conversational agent for Rocket Mortgage customer interactions
- Key files: `main.tsx` (entry point), `agent-goal.tsx` (GoalAgent flow), `store.ts` (state management), `post-conversation.ts` (hooks)
- Dependencies: Sierra SDK, shared contact center, shared API types, shared web components

**Skills System** (`agents/rocket/skills/`)
- Responsibility: Modular conversational capabilities (transfer, lead collection, knowledge, listings, calculators)
- Key files:
  - `transfer.tsx` / `transfer-scheduling.tsx` - Banker/client relations transfers with availability checks
  - `lead-collection/chat-now-or-ipac.tsx` - Lead capture and IPAC flow orchestration
  - `knowledge.tsx` - Knowledge base Q&A with guardrails
  - `listings/` - Property search via Redfin integration
  - `flightpath/` - Guided data collection tool for loan applications
  - `estimates/` - Home estimate greeting and flow
  - `custom-attachment-handler.tsx` - File attachment processing
- Dependencies: API layer, shared IPAC types, state management

**API Layer** (`agents/rocket/api/`)
- Responsibility: External API integration for leads, listings, banker availability, IPAC, PAL
- Key files:
  - `api.ts` - API context and factory (MockAPI vs ProductionAPI)
  - `production.ts` - Production API implementation with error handling
  - `mock.ts` - Test fixtures and mock responses
  - `types.ts` - API request/response types
  - `internal/` - Internal API implementations (IPAC, PAL, Segment analytics)
- Dependencies: Shared API types, fetch utilities, JWT handling

**Shared Libraries** (`agents/shared/`)
- Responsibility: Cross-agent reusable code (contact center, API types, IPAC, web components)
- Key modules:
  - `contact-center/` - Bananaphone, Rocket contact center integrations
  - `api/` - Shared API types and interfaces (PAL, IPAC, Rocket Graph)
  - `ipac/` - Interactive Pre-Approval Chat flow and validation logic
  - `web/` - React component library (primitives, blocks, experiential) with Storybook
  - `guardrails/` - Refusal and respond guardrail implementations
  - `logging/` - RocketLogger singleton for structured logging
  - `jwt/` - JWE/JWS encryption/decryption utilities
  - `estimate/` - Home estimate card data and validation
- Dependencies: Sierra SDK, third-party libraries (React, Radix UI, Tailwind)

**Web Components** (`agents/rocket/web/`)
- Responsibility: Custom React UI for conversational chat interface
- Key files:
  - `embed.ts` / `embed.css` - Chat widget embedding logic
  - `components/` - Custom React components for chat UI
  - `rocket-carousel-adapter.tsx` - Property listing carousel
  - `build-deps.sh` - Dependency build script
- Dependencies: React 19, Radix UI, Tailwind CSS, Embla Carousel, Lucide icons

### Layer Architecture
```
[Presentation Layer: Web Components]
       ↓
[Agent Layer: main.tsx → agent-goal.tsx → Skills]
       ↓
[State Management: store.ts, env.ts, memory]
       ↓
[Business Logic: Skills, Guardrails, IPAC flows]
       ↓
[API Layer: api.ts → ProductionAPI/MockAPI]
       ↓
[External Services: Contact Centers, Internal APIs, Segment]
```

**Communication Pattern:**
- User message → Sierra Agent runtime → JSX skill evaluation → API calls → State updates → Response generation
- Post-conversation hooks trigger lead creation, IPAC submission, analytics
- Contact center transfers use CompositeContactCenter adapter for routing

## 5. Data Flow & Communication

### Request Flow
```
Client Chat → Sierra Platform → Agent Entry Point (main.tsx)
  → Brand Config & Hooks
  → AgentGoal JSX Evaluation
  → Skill Exception Priority Check
  → Skill Execution (API calls, state updates)
  → Response Generation
  → Post-Conversation Hooks
  → Contact Center Transfer (if triggered)
```

**Detailed Flow:**
1. Client initiates conversation via web embed or contact center
2. `main.tsx` initializes agent with brand configuration, contact center integration, and hooks
3. `agent-goal.tsx` evaluates GoalAgent logic with intent detection and skill routing
4. Skills execute conversational flows, calling APIs for data (leads, listings, banker availability)
5. State persists in `useRocketRootStore` and memory variables
6. Responses formatted with Sierra JSX and sent to client
7. Post-conversation hooks (`post-conversation.ts`) submit leads, IPAC data, and analytics
8. Transfers route through CompositeContactCenter to appropriate destination

**State Management:**
- `store.ts` defines `RocketRootStore` with lead information, IPAC answers, launchpad responses, transfer scenarios, experiment variants
- Sierra's `useMemory` hook persists conversation data across turns (WEB_NAME, DOMAIN, SUBPATH, encrypted payload)
- Custom fields tagged with `fmtCustomFieldTag` for external system integration

**Inter-Module:** Skills communicate via shared state (`useRocketRootStore`), API context (`useAPI`), and Sierra primitives (`useConversation`, `useEffect`)

**Events:** Post-conversation hooks triggered by conversation end, transfers, or explicit skill completion

## 6. Integration Points

### External Services

| Service | Purpose | Method | Location |
|---------|---------|--------|----------|
| Bananaphone | Voice conversation support (primary contact center) | Sierra contact center SDK | `shared/contact-center/bananaphone.ts` |
| LiveAgent | Legacy chat transfer system | Sierra contact center SDK | `@sierra/lib/contact-center/liveagent` |
| MIAW | Legacy messaging system | Sierra contact center SDK | `@sierra/lib/contact-center/miaw` |
| RocketContactCenter | Custom Rocket contact center orchestration | Custom adapter | `shared/contact-center/rocket.ts` |
| Internal Lead API | Lead creation and submission | REST (fetch) | `api/production.ts` |
| Internal IPAC API | Pre-approval chat data submission | REST (fetch) | `api/internal/ipac-internal.ts` |
| Internal PAL API | Pre-approval loan application submission | REST (fetch) | `api/internal/pal-internal.ts` |
| Rocket Graph API | Mortgage data retrieval (GraphQL) | GraphQL | `shared/api/rocket-graph/` |
| Redfin Listings API | Property search and listing data | REST (internal proxy) | `api/production.ts` |
| Segment Analytics | Event tracking and analytics | REST (fetch) | `api/internal/segment-internal.ts` |
| Banker Availability | Real-time banker status checks | REST (fetch) | `api/is-banker-available.ts` |

### Database
**Type:** N/A (stateless agent)
**Access:** All persistent data accessed via external REST/GraphQL APIs
**Location:** API integrations in `api/` directories

### Critical Dependencies

1. **@sierra/agent** (v0.20260227.7180733) - Core agent SDK providing JSX conversational primitives, hooks, state management, and runtime
2. **@sierra/cli** - Build, type-check, upload, and watch commands for agent development
3. **@sierra/lib** - Contact center integrations (LiveAgent, MIAW, Bananaphone adapters)
4. **@sierra/content-schema** - CMS schema definition and validation framework
5. **@sierra/web-react** (v0.20260227.7180733) - React components for web chat interface

## 7. Key Components Deep Dive

### Component 1: Agent Goal Flow (`agent-goal.tsx`)

**Path:** `agents/rocket/agent-goal.tsx`
**Purpose:** Defines the primary conversational logic using Sierra's GoalAgent pattern. Orchestrates intent detection, skill routing, and handles critical exceptions (death mentions, TRID compliance, client frustration). This is the brain of the conversational agent.

**Key classes/functions:**
- `AgentGoal()` - Main component rendering GoalAgent with policies, rules, and skill exceptions
- `initializePALFlow()` - Initializes Pre-Approval Loan flow with tagging and state updates
- `useShouldRenderMockCarousel()` - Conditional rendering for property listing UI

**Patterns:**
- Goal-based conversational architecture (Sierra pattern)
- Priority-based exception handling (Priority 0-3 for skill exceptions)
- JSX-based declarative conversation flow

**Example:**
```tsx
export function AgentGoal() {
    const [rootStore, updateRootStore] = useRocketRootStore();
    const memory = useMemory();
    const isPALStandalone = memory.variable(MemoryVariable.PAL_STANDALONE) === "true";

    useEffectOnce(() => {
        updateRootStore(prevStore => ({
            ...prevStore,
            isWithinGoalAgent: true,
            isPALEnabled: true,
        }));
    });

    // Priority-based skill exceptions
    return (
        <GoalAgent>
            <Goal>
                <Policy>Handle client inquiries about mortgages</Policy>
                <Rule>NEVER do math calculations for clients</Rule>

                {/* Priority 0: Death mentioned - immediate client relations transfer */}
                <SkillException priority={0}>
                    <Condition>Client mentions death of family member</Condition>
                    <TransferToClientRelations />
                </SkillException>
            </Goal>
        </GoalAgent>
    );
}
```

### Component 2: Transfer & Scheduling System (`transfer.tsx`, `transfer-scheduling.tsx`)

**Path:** `agents/rocket/skills/transfer.tsx`, `agents/rocket/skills/transfer-scheduling.tsx`
**Purpose:** Manages complex transfer logic to human bankers or client relations with real-time availability checks, callback scheduling, and IPAC/PAL data submission during transfers. Critical for human handoff and lead conversion.

**Key classes/functions:**
- `TransferToBankerOrClientRelations()` - Orchestrates banker availability check and transfer/scheduling logic
- `isBankerAvailable()` - Real-time banker availability API call with business hours validation
- `TransferOrScheduleCallbackGoal()` - Goal-based component offering transfer or callback scheduling
- `submitPALLoanDuringTransfer()` - Submits PAL loan application data before transfer
- `extractAndPostIPAC()` - Extracts and posts IPAC data to internal API

**Patterns:**
- Strategy pattern (different transfer destinations: banker, client relations origination, client relations servicing)
- Composite contact center pattern for routing transfers
- Fallback pattern (callback scheduling when banker unavailable)

**Example:**
```tsx
export function TransferToBankerOrClientRelations() {
    const api = useAPI();
    const [rootStore] = useRocketRootStore();
    const contactCenter = useContactCenter<CompositeContactCenter>();

    // Check banker availability with business hours
    const isAvailable = await isBankerAvailable(api, rootStore);

    if (isAvailable) {
        // Submit PAL data before transfer
        await submitPALLoanDuringTransfer(api, rootStore);

        // Transfer to banker via contact center
        await contactCenter.transfer({
            destination: TransferDestination.BANKER,
            leadState: rootStore.leadState,
            transferReason: rootStore.transferReason
        });
    } else {
        // Offer callback scheduling
        return <TransferOrScheduleCallbackGoal />;
    }
}
```

### Component 3: Production API Layer (`api/production.ts`)

**Path:** `agents/rocket/api/production.ts`
**Purpose:** Production implementation of API interface handling all external service calls (leads, listings, IPAC, PAL, banker availability, Segment analytics). Provides error handling, response mapping, and request validation.

**Key classes/functions:**
- `ProductionAPI` - Implements API interface with staging/production environment support
- `handleProductionInternalResponse()` - Generic error handler and response mapper
- `createLead()` - Lead creation with Segment tracking
- `searchListings()` - Property search via internal listings API
- `submitIPAC()` - IPAC data submission with validation
- `submitPALLoanApplication()` - PAL loan application submission

**Patterns:**
- Adapter pattern (converts internal API responses to public types)
- Template method pattern (`handleProductionInternalResponse` generic handler)
- Environment-based configuration (staging vs production credentials)

**Example:**
```tsx
export class ProductionAPI implements API {
    private internal: InternalAPI;

    constructor(staging?: boolean, subpath?: string, clientIP?: string) {
        this.internal = new ProductionInternalAPI(staging, subpath, clientIP);
    }

    async createLead(request: CreateLeadRequest): Promise<CreateLeadResponse | APIError> {
        addAgentTags([fmtCustomFieldTag("leadCreationAttempted", "true")]);

        const internalResponse = await this.internal.createLead({
            ...request,
            leadLoanPurpose: loanPurposeToLeadLoanPurpose(request.loanPurpose),
        });

        return this.handleProductionInternalResponse({
            internalResponse,
            request,
            successMapper: (internal) => ({
                leadId: internal.leadId,
                isTestLead: internal.isTestLead,
            }),
            errorContext: "createLead",
        });
    }
}
```

### Component 4: State Management (`store.ts`)

**Path:** `agents/rocket/store.ts`
**Purpose:** Centralized state management for the agent using Sierra's `useRootStore` pattern. Maintains conversation context including lead information, IPAC answers, launchpad responses, transfer scenarios, property search data, and experiment variants. Critical for maintaining conversation continuity.

**Key types/functions:**
- `RocketRootStore` - Main state interface with 50+ fields
- `useRocketRootStore()` - Custom hook wrapping Sierra's `useRootStore`
- `useInitStore()` - Hook for initializing store with memory variables and encrypted payloads
- `LaunchpadResponses` - Type defining all launchpad form data

**Patterns:**
- Repository pattern (centralized state storage)
- Hook pattern (React-style custom hooks for state access)
- Immutable updates (updateRootStore returns new state object)

**Example:**
```tsx
export type RocketRootStore = {
    isWithinGoalAgent?: boolean;
    isPALEnabled?: boolean;
    palCollectIPACStarted?: boolean;

    // Lead information
    leadState?: LeadState;
    leadId?: string;
    email?: string;
    phoneNumber?: string;
    firstName?: string;
    lastName?: string;

    // IPAC answers
    ipacAnswers?: IPACAnswers;

    // Launchpad responses (50+ fields)
    launchpadResponses?: LaunchpadResponses;

    // Transfer state
    transferScenario?: TransferScenario;
    transferReason?: TransferReason;

    // Experiment variants
    callbackSchedulingExperimentVariant?: CallbackSchedulingExperimentVariant;
};

export function useRocketRootStore(): [RocketRootStore, (update: (prev: RocketRootStore) => RocketRootStore) => void] {
    return useRootStore<RocketRootStore>();
}
```

### Component 5: IPAC Flow System (`shared/ipac/`, `skills/lead-collection/collect-ipac-goal.tsx`)

**Path:** `agents/shared/ipac/` (shared logic), `agents/rocket/skills/lead-collection/collect-ipac-goal.tsx` (agent-specific)
**Purpose:** Interactive Pre-Approval Chat flow guiding clients through pre-qualification questions. Collects structured data (property address, credit profile, employment status, down payment, mortgage status) for loan application. Shared across multiple agents for consistency.

**Key classes/functions:**
- `RocketCollectIPACGoal()` - Goal-based IPAC collection with validation
- `IPACAnswers` - Type defining all IPAC question responses
- `serializeIPACAnswers()` - Converts IPAC answers to API-ready format
- `validateCreditProfile()`, `validateEmploymentStatus()` - Input validation functions
- `PAL_SAFETY_CONFIG` - Safety guardrails for IPAC data collection

**Patterns:**
- Wizard/stepped flow pattern (sequential question collection)
- Validation pattern (schema validation before submission)
- Shared library pattern (reusable across agents)

**Example:**
```tsx
export function RocketCollectIPACGoal() {
    const [rootStore, updateRootStore] = useRocketRootStore();

    return (
        <Goal>
            <Policy>Collect pre-approval information from client</Policy>

            <CollectIPACGoal
                onComplete={(ipacAnswers: IPACAnswers) => {
                    updateRootStore(prev => ({
                        ...prev,
                        ipacAnswers,
                        palCriteriaEligible: isEligibleForPAL(ipacAnswers),
                    }));
                    addAgentTags([IPAC_MATERIAL_INFO_COLLECTED_TAG]);
                }}
                safetyConfig={PAL_SAFETY_CONFIG}
            />
        </Goal>
    );
}
```

## 8. Configuration & Infrastructure

**Config Approach:**
- Environment variables for runtime configuration (Sierra platform env)
- Memory variables for per-conversation configuration
- Content schema (CMS) for dynamic content (phone numbers, operating hours, guardrails)
- TypeScript enums for type-safe configuration constants

**Config Location:**
- `agents/rocket/env.ts` - Environment variables, memory variables, secrets enumeration
- `agents/rocket/content-schema.ts` - CMS schema definitions
- `agents/rocket/content-types.ts` - Strongly-typed CMS content access
- `.pre-commit-config.yaml` - Pre-commit hook configuration
- `jest.config.base.js` - Shared test configuration
- `pnpm-workspace.yaml` - Monorepo workspace configuration

**Deployment:**
- Sierra CLI (`pnpm run upload`) uploads compiled agent to Sierra platform
- GitHub Actions workflow for CI/CD (build, test, deploy)
- Multi-environment deployment (production, staging, mock)
- Agent builds produce `main.js` (compiled agent), `main.js.map` (source map), `all.tests.js` (test suite)

**Containers:** Not applicable (serverless Sierra platform deployment)

### Key Environment Variables

| Variable | Purpose | Required |
|----------|---------|----------|
| `WEB_NAME` | Website name for branding | No |
| `DOMAIN` | Domain for URL construction | No |
| `SUBPATH` | Subpath for routing (e.g., /rocket, /rma) | No |
| `STAGING_CLIENT_ID` | OAuth client ID for staging APIs | Yes (staging) |
| `STAGING_CLIENT_SECRET` | OAuth client secret for staging APIs | Yes (staging) |
| `PRODUCTION_CLIENT_ID` | OAuth client ID for production APIs | Yes (production) |
| `PRODUCTION_CLIENT_SECRET` | OAuth client secret for production APIs | Yes (production) |
| `JWE_SIERRA_PRIVATE_KEY_PEM` | Private key for JWE decryption | Yes |
| `ENABLE_PAL_TRANSFER_WAITING` | Enable PAL transfer waiting screen | No |
| `ENABLE_IPAC_V2` | Enable IPAC v2 flow | No |
| `FLIGHTPATH_V2_EXPERIMENT_PERCENTAGE` | Flightpath v2 experiment rollout % | No |

### Memory Variables (per-conversation)

| Variable | Purpose | Example |
|----------|---------|---------|
| `ENCRYPTED_PAYLOAD` | JWE-encrypted sensitive data (Flightpath) | (encrypted JWT) |
| `servicingLoanNumber` | Loan number for servicing inquiries | "1234567890" |
| `leadTypeCode` | Lead type classification | "COOPFLIGHTPATH" |
| `palCriteriaEligible` | PAL eligibility flag | "true" |
| `CURRENT_TIME_OVERRIDE` | Override current time (testing) | "2024-03-15T14:30:00Z" |

## 9. Quality Attributes

**Error Handling:**
- Centralized error handling in `api/production.ts` with `handleProductionInternalResponse()`
- API errors typed as `APIError | BankerAPIError | LeadAPIError`
- Graceful degradation for contact center failures (fallback between LiveAgent, MIAW, Bananaphone)
- User-facing error messages configured via CMS content schema
- Location: `api/production.ts`, `api/types.ts`, contact center adapters

**Logging:**
- Custom `RocketLogger` singleton in `shared/logging/log.ts`
- Structured logging with contextual metadata (agent name, conversation ID)
- Sierra platform logging primitives (`info()`, `warn()`, `debug()`)
- Agent tags for conversation tracking and analytics

**Security:**
- JWE/JWS encryption for sensitive data (`shared/jwt/`)
- OAuth 2.0 for API authentication (client credentials flow)
- Secret detection via pre-commit hooks (detect-secrets)
- PEM-encoded keys for encryption/decryption
- TCPA consent collection for SMS/phone contact
- TRID compliance with automatic transfer when material information collected

**Testing:**
- Unit tests in `__tests__/` directories using Jest + @swc/jest
- Scenario tests using Sierra test framework (`tests/*.tests.ts`)
- Compliance tests for regulatory requirements (`tests/compliance/`)
- Mock API for isolated testing (`api/mock.ts`)
- Coverage thresholds: 80% branches, 80% functions, 80% lines, 80% statements
- Test commands: `pnpm test`, `pnpm test:watch`, `pnpm test:coverage`, `pnpm test:ci`
- Storybook for web component testing (`agents/shared/web/.storybook/`)

## 10. Architectural Decisions & Trade-offs

### Decision: Monorepo with Shared Libraries

- **Choice:** Monorepo architecture with `agents/shared/` for reusable code
- **Alternatives:** Separate repositories per agent, shared npm packages, duplicated code
- **Rationale:**
  - Multiple agents (10+) with significant code overlap (contact center, IPAC, API types)
  - Shared web component library ensures UI consistency across agents
  - Atomic changes across multiple agents (e.g., contact center updates)
  - Simplified dependency management with pnpm workspaces
- **Trade-offs:**
  - **Gains:** Code reuse, consistency, easier refactoring, single CI/CD pipeline
  - **Losses:** Build complexity, potential for tight coupling, larger repository size
  - **Mitigation:** Clear separation between shared and agent-specific code, comprehensive testing

### Decision: Sierra Agent SDK with JSX Conversational Model

- **Choice:** Build on Sierra Agent Platform using JSX-based conversational programming
- **Alternatives:** Custom agent framework, OpenAI Assistants API, Dialogflow, Rasa
- **Rationale:**
  - Sierra SDK provides production-grade conversational primitives (Goals, Policies, Rules, Guardrails)
  - JSX declarative model simplifies complex conversation flows vs imperative state machines
  - Integrated contact center support (LiveAgent, MIAW, Bananaphone)
  - CMS-driven content management for non-developer updates
  - Built-in testing framework for scenario/compliance tests
- **Trade-offs:**
  - **Gains:** Faster development, declarative flows, built-in safety, integrated contact centers
  - **Losses:** Platform lock-in, less control over runtime, learning curve for JSX conversational model
  - **Mitigation:** Abstract API layer allows migration, comprehensive documentation (CLAUDE.md files)

### Decision: Composite Contact Center with Multiple Adapters

- **Choice:** CompositeContactCenter wrapping multiple contact center systems (Bananaphone, LiveAgent, MIAW)
- **Alternatives:** Single contact center, custom integration per agent, no contact center integration
- **Rationale:**
  - Legacy systems (LiveAgent, MIAW) still in production requiring support
  - Bananaphone migration in progress (voice-first contact center)
  - Different agents have different contact center requirements
  - Graceful fallback if one system unavailable
- **Trade-offs:**
  - **Gains:** Flexibility, backward compatibility, graceful degradation, migration path
  - **Losses:** Increased complexity, potential inconsistencies, testing overhead
  - **Mitigation:** Unified interface, comprehensive adapter tests, clear migration plan

**Scalability:**
- Serverless Sierra platform handles scaling automatically
- Stateless agent design enables horizontal scaling
- API rate limiting and retry logic in production API layer
- Caching potential for CMS content and API responses (not yet implemented)

**Performance:**
- SWC-based compilation for fast builds
- Lazy loading of web components
- Optimized API calls (batch where possible, e.g., banker availability)
- Memory variable caching to avoid repeated computation

## 11. Extension Points

**Plugin System:** No formal plugin system, but modular skill architecture allows adding new skills

**Adding Features:**
- **New Conversational Skill:** Create new skill file in `agents/rocket/skills/`, import in `agent-goal.tsx`, add to skill exceptions or main goal
- **New API Integration:** Add methods to API interface in `api/api.ts`, implement in `production.ts` and `mock.ts`
- **New Contact Center:** Create adapter implementing Sierra ContactCenter interface in `shared/contact-center/`
- **New Agent:** Create new directory under `agents/`, copy structure from `agents/rocket/`, add to `pnpm-workspace.yaml`
- **New Web Component:** Add to `agents/shared/web/components/`, export in `index.ts`, create Storybook story
- **New CMS Content:** Define in `content-schema.ts`, access via `content-types.ts`

**Customization:**
- Brand configuration in `main.tsx` (`brand()` function)
- Language guidance in `guidance.ts` (tone, voice, rules)
- Operating hours via CMS content schema
- Guardrails via CMS content schema (refusal/respond guardrails)
- Transfer destinations and phone numbers via CMS
- Experiment variants via environment variables and A/B testing framework

## 12. Technical Debt & Improvements

### Technical Debt

1. **Legacy Contact Center Migration** - Location: `shared/contact-center/`, `main.tsx` | Impact: High | Fix: Complete Bananaphone migration, deprecate LiveAgent/MIAW adapters. Remove conditional logic for legacy systems once migration complete.

2. **Duplicated API Types** - Location: `agents/rocket/api/types.ts`, `agents/shared/api/types.ts` | Impact: Medium | Fix: Consolidate all API types in `agents/shared/api/`, ensure single source of truth for request/response types.

3. **Magic Strings for Agent Tags** - Location: Throughout skills and main logic | Impact: Medium | Fix: Centralize all agent tag constants in `tags.ts` enums, replace string literals with enum references.

4. **Post-Conversation Hook Complexity** - Location: `post-conversation.ts` | Impact: Medium | Fix: Extract lead creation, IPAC submission, analytics tracking into separate modules with clear interfaces. Current 300+ line file handles too many responsibilities.

5. **Inconsistent Error Handling** - Location: Various skill files | Impact: Medium | Fix: Standardize error handling pattern across all skills using shared error boundary components or utility functions.

### Refactoring Opportunities

1. **State Management** - Current: Single monolithic RocketRootStore with 50+ fields | Improvement: Split into domain-specific stores (leadStore, ipacStore, transferStore, experimentStore) with composition | Benefit: Easier testing, reduced coupling, clearer ownership

2. **API Layer Testing** - Current: Manual mocks in `api/mock.ts` | Improvement: Generate mocks from TypeScript interfaces using tools like ts-auto-mock or MSW (Mock Service Worker) | Benefit: Reduced maintenance, type-safe mocks, fewer mock/production mismatches

3. **Content Schema Validation** - Current: Build-time validation only | Improvement: Add runtime validation for CMS content with Zod or similar schema validator | Benefit: Catch content errors before deployment, better error messages for content editors

4. **Transfer Logic Consolidation** - Current: Transfer logic spread across `transfer.tsx`, `transfer-scheduling.tsx`, contact center adapters | Improvement: Create unified transfer orchestration service with clear separation between decision logic and execution | Benefit: Easier testing, reduced duplication, clearer transfer flow

5. **Test Coverage Improvements** - Current: 80% coverage target, scenario tests for happy paths | Improvement: Increase coverage to 90%, add comprehensive edge case tests, add integration tests for full conversation flows | Benefit: Catch more bugs, confidence in refactoring, better regression detection

### Evolution Suggestions

1. **GraphQL Federation for API Layer** - Limitation: Multiple REST APIs with different authentication, error handling, schemas | Approach: Implement GraphQL federation gateway consolidating all internal APIs (leads, IPAC, PAL, listings, banker availability) behind unified GraphQL schema | Effort: Large (3-6 months) | Benefit: Simplified API consumption, better type safety, single authentication layer, easier API versioning

2. **Real-time Banker Availability Stream** - Limitation: Polling-based banker availability checks cause delays and stale data | Approach: Implement WebSocket or Server-Sent Events for real-time banker status updates, cache availability in agent state | Effort: Medium (4-6 weeks) | Benefit: Instant transfer routing, reduced API calls, better user experience

3. **AI-Powered Intent Classification** - Limitation: Rule-based intent detection in GoalAgent can miss complex queries | Approach: Fine-tune LLM for Rocket-specific intent classification with conversation history, integrate as pre-processing step before skill routing | Effort: Medium (6-8 weeks) | Benefit: More accurate skill routing, handle ambiguous queries, improved conversation success rate

4. **Conversation Analytics Dashboard** - Limitation: Limited visibility into conversation flows, drop-off points, skill usage | Approach: Build analytics dashboard consuming agent tags, conversation events, transfer outcomes. Visualize conversation funnels, identify optimization opportunities | Effort: Medium (6-8 weeks) | Benefit: Data-driven optimization, identify user pain points, measure feature impact

5. **Multi-Language Support** - Limitation: English-only conversations | Approach: Integrate i18n framework (i18next), translate CMS content, language detection at conversation start, language-specific skills | Effort: Large (4-6 months) | Benefit: Reach Spanish-speaking market (40M+ US Spanish speakers), improved accessibility, competitive advantage

## 13. Quick Reference

**Entry Points:**
- Main agent: `agents/rocket/main.tsx`
- Agent goal: `agents/rocket/agent-goal.tsx`
- API factory: `agents/rocket/api/api.ts`
- Web embed: `agents/rocket/web/embed.ts`

**Config Files:**
- Environment: `agents/rocket/env.ts`
- Content schema: `agents/rocket/content-schema.ts`
- Store types: `agents/rocket/store.ts`
- Language guidance: `agents/rocket/guidance.ts`

**Dev Commands:**
```bash
# From agents/rocket/ directory
pnpm run build          # Compile agent
pnpm run watch          # Watch mode for development
pnpm run upload         # Upload to Sierra platform
pnpm run check          # Type checking
pnpm run setup-deps     # Build web dependencies
pnpm test               # Run tests
pnpm test:watch         # Test watch mode
pnpm test:coverage      # Test with coverage
```

**From repository root:**
```bash
make setup              # Install development dependencies (Homebrew, Node 20)
pnpm i                  # Install all dependencies
```

## 14. Summary

### Strengths

1. **Modular Skills Architecture** - Clear separation of conversational capabilities (transfer, lead collection, knowledge, listings) with well-defined responsibilities. Easy to add new skills or modify existing ones without affecting other parts of the agent.

2. **Comprehensive Shared Library** - `agents/shared/` provides high-quality reusable code (contact center integrations, API types, IPAC flows, web components with Storybook). Reduces duplication across 10+ agents and ensures consistency.

3. **Strong Type Safety** - TypeScript with strict mode, comprehensive type definitions for API requests/responses, state management, CMS content. Catch errors at compile time rather than runtime.

4. **Production-Grade Testing** - Jest unit tests, Sierra scenario tests, compliance tests, 80% coverage thresholds, Storybook for component testing. High confidence in code quality.

5. **Declarative Conversational Model** - Sierra JSX pattern makes complex conversation flows readable and maintainable. Guardrails, policies, and rules clearly expressed in code.

### Improvements

1. **Documentation Coverage** - While CLAUDE.md files exist for main agents, many shared libraries lack comprehensive documentation. Need architecture diagrams, API documentation, and contribution guides.

2. **Legacy System Migration** - Multiple contact center adapters (Bananaphone, LiveAgent, MIAW) create complexity. Complete Bananaphone migration to simplify codebase.

3. **State Management Complexity** - `RocketRootStore` with 50+ fields is difficult to reason about. Split into domain-specific stores with clear boundaries.

4. **API Layer Consolidation** - Multiple REST APIs with different patterns (authentication, error handling, response formats). Consider GraphQL federation or API gateway for unified interface.

5. **Observability Gaps** - Limited real-time visibility into conversation flows, skill usage, transfer outcomes. Need comprehensive analytics dashboard and monitoring.

### Next Steps

1. **High Priority** - Complete Bananaphone contact center migration, remove LiveAgent/MIAW legacy code (reduces technical debt, simplifies maintenance)

2. **High Priority** - Consolidate API types in `agents/shared/api/` to eliminate duplication and establish single source of truth (improves type safety, reduces bugs)

3. **Medium Priority** - Implement real-time banker availability stream to replace polling-based checks (improves user experience, reduces API load)

4. **Medium Priority** - Build conversation analytics dashboard to visualize flows, drop-off points, and optimization opportunities (enables data-driven improvements)

5. **Low Priority** - Explore multi-language support (i18n) for Spanish-speaking market (strategic growth opportunity, requires significant investment)

---

**Notes:**

- This is a mature, production-grade conversational AI system serving Rocket Companies' mortgage business
- Strong engineering practices: monorepo with shared libraries, comprehensive testing, type safety, modular architecture
- Primary improvement areas: legacy system migration, observability, state management simplification
- Sierra Agent SDK provides excellent foundation for conversational AI but creates platform lock-in
- Well-positioned for AI enhancements (better intent classification, dynamic content generation, personalization)
- Recommend regular architecture reviews as conversation patterns evolve and new Sierra SDK features become available

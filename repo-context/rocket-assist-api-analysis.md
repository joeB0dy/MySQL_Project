# Repository Analysis: Rocket Assist API

**Repository URL:** `https://github.com/RocketMortgage/rocket-assist-api`
**Analysis Date:** 2026-03-02
**Analyzer:** repo-analyzer sub-agent

---

## 1. Repository Overview

**Project Type:** NestJS API Monorepo (Conversational AI Gateway)
**Purpose:** Backend API that enables chat experiences to interact with external AI vendor services (IBM Watson, OpenAI ChatGPT, AWS Bedrock) and internal Rocket Mortgage microservices. Acts as an orchestration layer for conversational AI across multiple business channels.
**Key Characteristics:**
- Multi-channel conversational AI platform supporting 15+ distinct chat channels (SFWC, SMS, WhatsApp, RMA, Servicing)
- Strategy pattern-driven architecture enabling channel-specific AI processing pipelines
- Heavy integration layer connecting to 20+ internal and external services
- Extensive prompt engineering and LLM management across Azure OpenAI, OpenAI, and AWS Bedrock
- Production-grade observability with OpenTelemetry, Pino logging, and extensive PII redaction

## 2. Technology Stack

**Languages:** TypeScript (ES2024, strict mode)
**Framework:** NestJS v11.1.4 (Node.js backend framework built on Express)
**Key Dependencies:**
- **AI/LLM:** `openai` ^4.47.1, `@azure/openai` ^1.0.0-beta.6, `@aws-sdk/client-bedrock-runtime` ^3.846.0, `ibm-watson` ^9.0.0
- **Database:** AWS DynamoDB (`@RocketMortgage/rocket-dynamodb-client` ^2.15.0)
- **Internal Libraries:** `@RocketMortgage/rocket-types`, `@rocket-libraries/rocket-request-js`, `@rocket-logic/rocket-logic-api-models`
- **Feature Flags:** `@splitsoftware/splitio` ^10.23.1
- **Analytics:** `@segment/analytics-node` ^2.1.3, `node-avo-inspector` ^1.1.0
- **Logging:** `nestjs-pino` ^2.5.2, `@rocket-libraries/pino-log-transport` ^2.0.0
- **Observability:** `@opentelemetry/sdk-metrics` ^1.27.0, `@opentelemetry/exporter-metrics-otlp-proto` ^0.54.1
**Build/Package:** Yarn 1.22.22, Nx v21.2.4 (monorepo build system), Webpack
**Database:** AWS DynamoDB (NoSQL) - chat context, conversation history, CSAT feedback
**Infrastructure:** Kubernetes/Helm, Docker multi-stage builds, CircleCI for CI/CD, HAL deployment platform

## 3. Architectural Patterns

### Primary Pattern

**Strategy Pattern + Experience-Based Routing**
The application uses a sophisticated implementation of the Strategy pattern where each chat channel (platform) has a dedicated strategy class that implements `IRocketAssistStrategy`. Within strategies, an emerging "Experience" pattern subdivides behavior based on user state (authenticated vs. unauthenticated, delinquent vs. standard, etc.).

**Rationale:** Enables independent evolution of 15+ distinct chat channels with different AI models, prompts, business logic, and integration requirements without coupling. Each channel's complexity is encapsulated within its strategy.

### Secondary Patterns

**Layered Architecture (NestJS Modules)**
- Controllers: HTTP request handling and validation
- Services: Business logic and external integrations
- Repositories: Data access abstraction for DynamoDB
- Providers: Dependency injection configuration
Located: Standard NestJS module structure in `/apps/rocket-assist-api/src/app/app.module.ts`

**Interceptor Chain (Cross-Cutting Concerns)**
NestJS interceptors handle pre/post-processing: session validation, chat session ID injection, LLM preprocessing, special message handling, request logging.
Located: `/apps/rocket-assist-api/src/interceptors/`

**Repository Pattern (Data Access Layer)**
Abstract base repository (`BaseRepository<RecordType, TableKeys>`) provides common CRUD operations with TTL management for DynamoDB entities.
Located: `/apps/rocket-assist-api/src/repositories/base/base.repository.ts`

**Provider/Client Pattern (External Integrations)**
Service-specific clients encapsulate API interactions with clear interfaces (`IAzureOpenAIClient`, `IOpen_AIClient`).
Located: `/apps/rocket-assist-api/src/services/` and `/apps/rocket-assist-api/src/providers/`

### Design Principles

- [x] Separation of Concerns - Clear layering with controllers, services, repositories
- [x] Single Responsibility - Each strategy handles one channel, each service has focused purpose
- [x] Dependency Inversion - Heavy use of DI via NestJS, interface-based external integrations
- [x] DRY - Base repository pattern, shared helper utilities, common prompt components

**Notes:** The codebase demonstrates strong adherence to NestJS best practices. The strategy pattern implementation is particularly well-executed with 38+ strategy files providing channel-specific behavior. However, there's visible architectural evolution: newer channels use "Experience" classes within strategies (e.g., `RocketApplicationAuthExperience`, `StandardAuthAIExperience`) while older channels are monolithic strategy classes.

## 4. Module Structure

### Directory Layout
```
rocket-assist-api/
├── apps/
│   ├── rocket-assist-api/        # Main API application
│   │   ├── src/
│   │   │   ├── app/              # NestJS app module and route controllers
│   │   │   ├── services/         # Business logic layer (41 service directories)
│   │   │   ├── repositories/     # Data access layer (DynamoDB)
│   │   │   ├── interceptors/     # Cross-cutting concerns (16 interceptors)
│   │   │   ├── providers/        # Dependency injection setup
│   │   │   ├── types/            # TypeScript type definitions
│   │   │   ├── utilities/        # Helper functions
│   │   │   ├── config/           # Configuration management
│   │   │   └── main.ts           # Application bootstrap
│   └── integration-tests/        # End-to-end tests (Playwright)
├── .helm/                        # Kubernetes Helm charts
├── .circleci/                    # CI/CD pipeline configuration
├── bin/                          # Scripts (DB provisioning, k8s config)
├── docs/                         # Documentation
└── Infrastructure/               # Infrastructure-as-code
```

### Core Modules

**App Module** (`apps/rocket-assist-api/src/app/app.module.ts`)
- Responsibility: Root module orchestrating all controllers, services, repositories, and strategies
- Key files: `app.module.ts` (227 lines with 127 providers, 13 controllers)
- Dependencies: Imports LoggerModule, CacheModule, OtelModule, LoanApplicationModule; exports all strategies and services

**Services Layer** (`apps/rocket-assist-api/src/services/`)
- Responsibility: 41 distinct service modules handling business logic and external integrations
- Key services:
  - `open-ai/` - OpenAI/Azure OpenAI integration with chat completions
  - `bedrock-agent/`, `bedrock-model/` - AWS Bedrock LLM integration
  - `ibm-watson/` - IBM Watson Assistant integration
  - `strategies/` - 38 strategy implementation files (11MB total)
  - `rocket-logic/` - Integration with Rocket Logic API (loan processing)
  - `prompts/` - Prompt engineering and management
  - `split/` - Feature flag service
- Dependencies: Heavy interdependencies with DI-managed circular dependency resolution

**Strategies Module** (`apps/rocket-assist-api/src/services/strategies/`)
- Responsibility: Implements Strategy pattern for channel-specific chat processing
- Key files:
  - `RocketAssistStrategyInterface.ts` - Contract for all strategies
  - `RocketAssistStrategyContext.ts` - Strategy selector
  - 38 strategy implementation files including `SfwcAuthStrategy.ts`, `PIIStrategy.ts`, `RocketApplicationStrategy.ts`
  - Subdirectories: `servicing/`, `rma/`, `whatsapp/`, `origination/`, `tpo/` containing experience classes
- Dependencies: All strategies depend on ChatCompletionsService, LoggerService, ConfigService

**Routes/Controllers** (`apps/rocket-assist-api/src/app/routes/`)
- Responsibility: HTTP endpoint definitions with DTOs and request validation
- Key controllers:
  - `message/` - Primary chat endpoint (`POST /api/message`)
  - `message-ext/` - External messaging (WhatsApp webhooks)
  - `agent-chat/` - Agent-assisted chat flows
  - `sms/`, `sms-v2/` - SMS-based chat
  - `loan-application/` - Loan application workflows (separate module)
  - `health/` - Health checks
- Dependencies: Each controller injects relevant strategies and services

**Repositories Layer** (`apps/rocket-assist-api/src/repositories/`)
- Responsibility: DynamoDB data access with TTL management
- Key files:
  - `base/base.repository.ts` - Abstract base providing get, save, update, delete, query
  - `chat-context/chat-context.repository.ts` - Stores chat session context
  - `chat-conversation-history/` - Persists conversation messages
  - `csat-feedback/` - Customer satisfaction feedback storage
- Dependencies: `@RocketMortgage/rocket-dynamodb-client`, `luxon` for date handling

### Layer Architecture
```
[Controllers]  →  [Interceptors]  →  [Strategies]  →  [Services]  →  [Repositories]
     ↓                  ↓                 ↓               ↓              ↓
  DTOs/Validation  Session/Logging   AI Routing    External APIs    DynamoDB
```

**Communication Pattern:**
1. Controller receives HTTP request, validates via DTOs
2. Interceptor chain processes: session validation, chat session ID assignment, LLM preprocessing
3. Controller selects strategy via `RocketAssistStrategyContext.getStrategy(platform)`
4. Strategy orchestrates: prompt selection, LLM invocation, external API calls, context persistence
5. Response flows back through interceptors for logging and transformation
6. Controller returns structured MessageResponseType

## 5. Data Flow & Communication

### Request Flow
```
Client → Load Balancer → /api/message → MessageController
                                          ↓
                              [Interceptor Chain]
                              • ChatSessionIdInterceptor
                              • SessionValidationInterceptor
                              • SpecialDayWelcomeMessageInterceptor
                              • LLMPreprocessorInterceptor
                              • ChatActionInterceptor
                                          ↓
                              RocketAssistStrategyContext
                                          ↓
                              Platform-Specific Strategy
                              (e.g., SfwcUnAuthAIStrategy)
                                          ↓
                              ChatCompletionsService
                                          ↓
                              [AI Provider Selection]
                              • Azure OpenAI
                              • OpenAI
                              • AWS Bedrock
                                          ↓
                              [External Service Calls]
                              • Kendra (knowledge base)
                              • Rocket Logic (loan data)
                              • Client Platform API
                              • Servicing Data Service
                                          ↓
                              [Context Persistence]
                              ChatContextRepository → DynamoDB
                                          ↓
                              Response → Client
```

**Brief description:** Requests enter through NestJS controllers with DTO validation. An interceptor chain handles cross-cutting concerns (session management, logging, preprocessing). The controller delegates to a strategy selected by platform type. Strategies orchestrate LLM calls (selecting between OpenAI, Azure, Bedrock), query external APIs for context, and persist chat state to DynamoDB. Responses are structured as `MessageResponseType` with text, context, and metadata.

**State Management:**
- **Session State:** Stored in DynamoDB via `ChatContextRepository` (TTL-based expiration)
- **Conversation History:** Persisted in `ChatConversationHistoryRepository` for multi-turn conversations
- **Feature Flags:** In-memory cache via Split.io SDK with session-aware overrides
- **Prompts:** Loaded at runtime from `PromptService` based on channel and context

**Inter-Module Communication:**
- Dependency Injection via NestJS (constructor injection)
- Event-driven via AWS SNS (`SnsService`) for async notifications
- HTTP clients for external APIs (`@rocket-libraries/rocket-request-js`)

**Events:**
- Analytics events published to Segment via `AvoService`
- OpenTelemetry metrics exported to OTLP endpoint
- Pino structured logs streamed to Splunk

## 6. Integration Points

### External Services
| Service | Purpose | Method | Location |
|---------|---------|--------|----------|
| Azure OpenAI | LLM chat completions (primary) | REST API | `services/open-ai/` |
| OpenAI | LLM chat completions (fallback) | REST API | `services/open-ai/` |
| AWS Bedrock | LLM via Claude/Titan models | AWS SDK | `services/bedrock-model/`, `services/bedrock-agent/` |
| IBM Watson | Legacy chatbot (phasing out) | Watson SDK | `services/ibm-watson/` |
| AWS Kendra | Knowledge base search | AWS SDK | `services/kendra/` |
| Rocket Logic API | Loan data and processing | HTTP/REST | `services/rocket-logic/` |
| RMA API | Application data | HTTP/REST | `services/rma-api/` |
| Client Platform API | Client profile data | HTTP/REST | `services/client-platform/` |
| Servicing Data Service | Servicing account data | HTTP/REST | `services/servicing-data/` |
| Rocket Homes | Home search integration | HTTP/REST | `services/rocket-homes/` |
| Submission Engine | Lead/application submission | HTTP/REST | `services/submission-engine/` |
| WhatsApp Business API | WhatsApp messaging | HTTP/REST | `services/whatsapp/` |
| AWS SNS | Async notifications | AWS SDK | `services/sns/` |
| Segment | Analytics tracking | REST API | `services/avo/segment-destination.ts` |
| Split.io | Feature flags | Split SDK | `services/split/` |

### Database
**Type:** AWS DynamoDB (NoSQL)
**Access:** `@RocketMortgage/rocket-dynamodb-client` (custom client wrapper)
**Location:** `repositories/` with base abstract repository pattern
**Tables:**
- Chat context (session state with TTL)
- Conversation history (message logs)
- CSAT feedback (customer satisfaction ratings)

### Critical Dependencies
1. **@nestjs/core** - Framework foundation for dependency injection, module system, decorators
2. **openai & @azure/openai** - Primary LLM integration for 70%+ of AI interactions
3. **@RocketMortgage/rocket-dynamodb-client** - Stateful conversation persistence (critical for multi-turn chat)
4. **@splitsoftware/splitio** - Feature flag control enabling gradual rollouts and A/B testing
5. **nestjs-pino & @rocket-libraries/pino-log-transport** - Production logging with PII redaction (141 redacted fields)

## 7. Key Components Deep Dive

### MessageController (Primary Chat Endpoint)
**Path:** `apps/rocket-assist-api/src/app/routes/message/message.controller.ts`
**Purpose:** Main entry point for all chat interactions. Routes requests to appropriate strategies based on platform type and feature flags. Critical to 100% of chat traffic.
**Key methods:**
- `postMessage(payload: MessageRequestDto)` - Processes user prompt, applies strategy, returns response
**Patterns:**
- Strategy pattern delegation via `RocketAssistStrategyContext.getStrategy(platform)`
- Interceptor chain for cross-cutting concerns (7 interceptors)
- Feature flag-driven platform override (e.g., SFWC_UNAUTH → SFWC_UNAUTH_AI)
**Example:**
```typescript
@Post()
@UseInterceptors(
    ChatSessionIdInterceptor,
    SessionValidationInterceptor,
    SpecialDayWelcomeMessageInterceptor,
    LLMPreprocessorInterceptor,
    ChatActionInterceptor
)
public async postMessage(@Body() payload: MessageRequestDto): Promise<MessageResponseType> {
    const strategy = this.rocketAssistStrategyContext.getStrategy(payload.platform);
    const strategyResponse = await strategy.applyStrategy(payload);
    return strategyResponse.response;
}
```

### ChatCompletionsService (LLM Orchestration)
**Path:** `apps/rocket-assist-api/src/services/open-ai/services/chat-completions.service.ts`
**Purpose:** Central LLM invocation service. Routes to Azure OpenAI, OpenAI, or AWS Bedrock based on channel type. Handles prompt construction, context injection, and response parsing. Processes 100% of AI-generated responses.
**Key methods:**
- `generateText(input: string, options: CompletionOptions): Promise<string[]>` - Main text generation
- `getChatCompletions(input: string, opts: CompletionOptions): Promise<Message[]>` - Channel-specific routing (15+ branches)
**Patterns:**
- Template method pattern with channel-specific implementations
- Tagged template literals for prompt construction (`system`, `user`, `assistant`)
- JSON vs. text response format selection
**Example:**
```typescript
private async getSfwcUnAuthAICompletions(
    input: string,
    basePrompt: string,
    context: SalesforceUnAuthAICompletionsCtx,
    config: OpenAICompletionsConfig
): Promise<Message[]> {
    const additionalContext = this.buildSalesforceUnAuthAIPrompt(context);
    const messages = [system`${basePrompt}${additionalContext}`, user`${input}`];
    const result = await this.openAI.getOpenAIChatCompletions(messages, config, ChatChannelEnum.SFWC_UNAUTH);
    return result.messages;
}
```

### RocketAssistStrategyContext (Strategy Router)
**Path:** `apps/rocket-assist-api/src/services/strategies/RocketAssistStrategyContext.ts`
**Purpose:** Factory/Registry pattern implementation that maps platform enums to strategy instances. Enables runtime strategy selection without conditional logic in controllers.
**Key functionality:**
- Maintains map of `ChatChannelEnum → IRocketAssistStrategy` instances
- Injected with all strategies via NestJS DI
- Single `getStrategy(platform: ChatChannelEnum)` method used by all controllers
**Patterns:** Factory pattern, Registry pattern, Strategy pattern enabler

### BaseRepository (Data Access Layer)
**Path:** `apps/rocket-assist-api/src/repositories/base/base.repository.ts`
**Purpose:** Abstract base class providing CRUD operations for all DynamoDB entities. Implements consistent TTL management, timestamp tracking, and error handling. Foundation for all data persistence.
**Key methods:**
- `get(tableKeys)`, `save(data, ttl)`, `update(tableKeys, attributesToUpdate)`, `delete(tableKeys)`, `query(queryCommand)`
**Patterns:**
- Template method pattern (abstract TABLE_NAME and TTL_IN_DAYS)
- Generic typing for type-safe repository implementations
- Automatic timestamp injection (createdAt, updatedAt)
- TTL calculation using Luxon for timezone-safe expiration
**Example:**
```typescript
export abstract class BaseRepository<RecordType, TableKeys> {
    protected abstract TABLE_NAME: string;
    protected abstract TTL_IN_DAYS: number;

    public async save(data: RecordType, ttl = this.ttl()) {
        const newRecord: RecordType & BaseRecordType = {
            ...data,
            createdAt: DateTime.utc().toISO(),
            updatedAt: DateTime.utc().toISO(),
            ttl,
        };
        return this.databaseClient.save(this.TABLE_NAME, newRecord);
    }
}
```

### ServicingStrategy (Multi-Experience Routing)
**Path:** `apps/rocket-assist-api/src/services/strategies/servicing/servicing.strategy.ts`
**Purpose:** Demonstrates evolved strategy architecture with sub-experience routing. Handles authenticated servicing customers with different experiences (delinquent, Schwab, standard AI). Shows architectural direction for future strategies.
**Key classes:**
- `ServicingStrategy` - Top-level strategy implementing `IRocketAssistStrategy`
- `RocketServicingDelinquentExperience`, `SchwabServicingDelinquentExperience`, `StandardAuthAIExperience` - Experience-specific implementations
**Patterns:**
- Strategy within strategy (experience selection)
- Delegation to legacy `SfwcAuthStrategy` for standard path
- Feature flag-driven routing to AI experiences
**Example:**
```typescript
private async getMessage(input: string, workingContext: ServicingContextType): Promise<MessageResponseType> {
    const { experienceType } = workingContext;
    if (experienceType === ServicingExperience.DelinquentSchwab)
        return await this.schwabDelinquentExperience.applyStrategyExperience(input, workingContext);
    if (experienceType === ServicingExperience.Delinquent)
        return await this.rktDelinquentExperience.applyStrategyExperience(input, workingContext);
    if (experienceType === ServicingExperience.Schwab)
        return await this.schwabExperience.applyStrategyExperience(input, workingContext);
}
```

## 8. Configuration & Infrastructure

**Config Approach:**
- Environment variables loaded via dotenv and validated by `ConfigService`
- Runtime config accessed through centralized `@RocketMortgage/rocket-config` library
- Feature flags managed via Split.io with session-level overrides
- Secret management through MyVault (Rocket's secret management system)

**Config Location:**
- `apps/rocket-assist-api/src/config/` - Configuration services
- `.env` (local, gitignored) - Local development secrets
- `.env.sample` - Template for required variables
- Helm values files: `.helm/values.{env}.yaml` - Kubernetes configuration per environment

**Deployment:**
- **Build:** CircleCI pipeline compiles TypeScript, runs tests, builds Docker image
- **Containerization:** Multi-stage Dockerfile (base → dev → cloud → default)
- **Orchestration:** Kubernetes via Helm charts with HAL deployment platform
- **Environments:** 4 tiers with ephemeral PR environments
  - Ephemeral (PR-based, auto-destroy weekly)
  - Test (us-east-2)
  - Beta (us-east-2, us-west-2)
  - Production (us-east-2, us-west-2)

**Containers:**
- **Base image:** `node:22-bullseye-slim`
- **Multi-region deployment:** us-east-2 (primary), us-west-2 (disaster recovery)
- **Health checks:** `/api/health` endpoint
- **Port:** 80 (containerized), 5000 (local dev)

### Key Environment Variables

| Variable | Purpose | Required |
|----------|---------|----------|
| AZURE_OPENAI_BASE_URL | Azure OpenAI endpoint | Yes |
| AZURE_OPENAI_SECRET | API key for Azure OpenAI | Yes |
| OPENAI_API_KEY | OpenAI API key (fallback) | Yes |
| AWS_ACCESS_KEY_ID | AWS credentials for Bedrock/DynamoDB | Yes |
| AWS_SECRET_ACCESS_KEY | AWS secret key | Yes |
| AWS_SESSION_TOKEN | Temporary session token | Yes (dev) |
| PREPROCESSOR_MODEL_NAME | LLM model for preprocessing | No |
| environment | Deployment environment (test/beta/prod) | Yes |
| NODE_ENV | Node.js environment | Yes |

## 9. Quality Attributes

**Error Handling:**
- Centralized error handling via NestJS exception filters (`apps/rocket-assist-api/src/filters/`)
- Custom `HttpException` usage with appropriate status codes
- Strategy-level error handling with fallback responses
- LLM call failures return `DEFAULT_ASSISTANT_ERROR_MESSAGE` to maintain conversation flow
- Graceful degradation when external services are unavailable

**Logging:**
- **Library:** Pino (high-performance JSON logging) via `nestjs-pino`
- **Transport:** Custom `@rocket-libraries/pino-log-transport` for Rocket infrastructure
- **PII Redaction:** 141+ field paths automatically redacted in production/beta (defined in `config/loggerConfig.ts`)
- **Context Enrichment:** Automatic injection of `chatSessionId`, `platform`, request params into every log
- **Exclusions:** Health check endpoint excluded from request logs
- **Location:** Configured in `apps/rocket-assist-api/src/config/loggerConfig.ts`

**Security:**
- **Authentication:** JWT bearer tokens validated via Auth0 integration (via `ApiBearerAuth` decorator)
- **PII Protection:** Extensive redaction in logs (SSN, addresses, emails, phone numbers)
- **Input Sanitization:** XSS library for HTML sanitization, class-validator for DTO validation
- **Session Validation:** `SessionValidationInterceptor` enforces session integrity
- **AWS IAM:** Role-based access to DynamoDB and Bedrock
- **Secret Management:** MyVault integration for credential storage, not committed to repo

**Testing:**
- **Unit Tests:** Jest with 198 `.spec.ts` files distributed across codebase
- **Coverage:** SonarQube integration tracking code coverage (visible in CircleCI)
- **Integration Tests:** Playwright-based in `apps/integration-tests/` with loan application smoke/critical/purchase flows
- **Test Commands:** `yarn test` (all), `yarn test:cov` (with coverage), `yarn test:integration`
- **CI Execution:** Tests run in CircleCI with `--silent` flag, large resource class for parallel execution

## 10. Architectural Decisions & Trade-offs

### Decision: Multi-Provider LLM Architecture

- **Choice:** Support Azure OpenAI, OpenAI, and AWS Bedrock simultaneously with runtime selection
- **Alternatives:**
  - Single provider (vendor lock-in risk)
  - Abstract LLM interface with pluggable backends (more complexity)
- **Rationale:**
  - Risk mitigation: Provider outages don't take down all channels
  - Cost optimization: Different channels use different pricing tiers
  - Feature access: Bedrock provides specific capabilities (knowledge bases, agents) not available elsewhere
  - Gradual migration: Watson → OpenAI → Bedrock transition path
- **Trade-offs:**
  - **Gains:** Resilience, flexibility, cost optimization, feature access
  - **Losses:** Increased complexity in ChatCompletionsService (560 lines with 15+ branches), multiple API keys to manage, inconsistent response formats requiring normalization

### Decision: Strategy Pattern for Channel Routing

- **Choice:** Each chat platform (SFWC, SMS, WhatsApp, RMA, etc.) implemented as separate strategy class
- **Alternatives:**
  - Single service with large if/else chains
  - Microservices per channel (separate deployments)
- **Rationale:**
  - Isolation: Changes to one channel don't risk others
  - Scalability: Team can work on channels independently
  - Testability: Each strategy has isolated test coverage
  - Evolution: Newer "experience" pattern can be adopted incrementally
- **Trade-offs:**
  - **Gains:** Clean separation, parallel development, reduced regression risk, independent testing
  - **Losses:** Large number of files (38 strategy files), potential code duplication across strategies, 227-line AppModule with 127 providers

### Decision: DynamoDB for Session State

- **Choice:** Store chat context, conversation history, and CSAT feedback in DynamoDB with TTL-based expiration
- **Alternatives:**
  - Redis (in-memory cache)
  - PostgreSQL (relational)
  - ElastiCache (managed Redis)
- **Rationale:**
  - Automatic TTL cleanup reduces operational overhead
  - Serverless scaling without manual capacity planning
  - AWS ecosystem integration with existing infrastructure
  - Key-value access pattern fits chat session lookup
- **Trade-offs:**
  - **Gains:** Automatic scaling, TTL cleanup, low operational overhead, cost-effective for read-heavy workload
  - **Losses:** Limited query capabilities (no complex joins), eventual consistency, higher latency than in-memory cache (though sufficient for chat use case)

**Scalability:**
- **Horizontal scaling:** Kubernetes HPA can scale pods based on CPU/memory
- **Database:** DynamoDB auto-scales with on-demand capacity mode
- **LLM calls:** Rate limiting handled by providers; retry logic in place
- **Multi-region:** Deployment to us-east-2 and us-west-2 for geographic distribution
- **Limitations:** Stateful conversations require session affinity (handled by Kubernetes service mesh)

**Performance:**
- **Webpack build optimization:** Compiles TypeScript to optimized JavaScript bundle
- **Caching:** NestJS cache manager for frequently accessed data
- **Response streaming:** Not currently implemented for LLM responses (opportunity for improvement)
- **Logging:** Pino chosen specifically for high-performance JSON serialization
- **OpenTelemetry:** Metrics exported to monitor P95/P99 latencies

## 11. Extension Points

**Plugin System:** No formal plugin architecture, but strategy pattern enables clean extension.

**Adding Features:**

1. **New Chat Channel:**
   - Create new strategy class implementing `IRocketAssistStrategy<MessageResponseType>`
   - Add channel to `ChatChannelEnum` in types
   - Register strategy in `AppModule` providers array
   - Add strategy to `RocketAssistStrategyContext` strategy map
   - Define prompts in `PromptService`
   - Create controller if distinct endpoint needed

2. **New LLM Provider:**
   - Create client implementing `IAzureOpenAIClient` or `IOpen_AIClient` interface
   - Add provider configuration to `ConfigService`
   - Register in `providers/` directory
   - Add branch in `ChatCompletionsService.getChatCompletions()` for new provider routing

3. **New External Integration:**
   - Create service in `services/{integration-name}/`
   - Define service interface and implementation
   - Add to `AppModule` providers
   - Inject into relevant strategies

4. **New Experience within Existing Strategy:**
   - Create experience class implementing `IRocketAssistStrategyExperience<ContextType, ResponseType>`
   - Add experience enum value to relevant types
   - Update strategy to route to new experience based on context
   - Register experience in `AppModule` providers

**Customization:**

- **Prompts:** Centralized in `PromptService.getPrompt(channel, options)` - modify without code changes
- **Feature Flags:** Add new flags in Split.io dashboard, reference via `FeatureFlagService.getFeatureFlag()`
- **Logging Fields:** Add to `reqCustomProps` function in `loggerConfig.ts`
- **PII Redaction:** Extend `redactedFieldsList` array in `loggerConfig.ts`
- **Interceptors:** Add custom interceptors to controller decorator chain
- **OpenTelemetry Metrics:** Add custom metrics via `OpenTelemetryService`

## 12. Technical Debt & Improvements

### Technical Debt

1. **Watson Decommission** - Location: `services/ibm-watson/`, `strategies/RocketApplicationWatsonStrategy.ts` | Impact: Medium | Fix: Complete migration to OpenAI/Bedrock, remove Watson dependencies (noted in code comments)

2. **Strategy Evolution Inconsistency** - Location: `services/strategies/` | Impact: Medium | Fix: Migrate all strategies to "Experience" pattern (currently only ServicingStrategy, RMAStrategy use it)

3. **Large AppModule** - Location: `app/app.module.ts` (227 lines, 127 providers) | Impact: Low | Fix: Split into feature modules following NestJS module best practices

4. **ChatCompletionsService Complexity** - Location: `services/open-ai/services/chat-completions.service.ts` (560 lines, 15+ channel branches) | Impact: High | Fix: Extract channel-specific completion logic into strategy pattern or dedicated services

5. **Hardcoded Constants** - Location: Throughout strategies and services | Impact: Low | Fix: Move to configuration service or environment variables

6. **Limited Response Streaming** - Location: All LLM integrations | Impact: Medium | Fix: Implement Server-Sent Events for streaming LLM responses (improves perceived performance)

### Refactoring Opportunities

1. **Feature Module Architecture** - Current: Monolithic AppModule with 127 providers | Improvement: Split into ChatModule, IntegrationModule, AnalyticsModule, ServicingModule | Benefit: Better code organization, lazy loading, clearer dependency boundaries

2. **Strategy Factory Pattern** - Current: Manual strategy map in RocketAssistStrategyContext | Improvement: Auto-discovery pattern using NestJS module introspection | Benefit: New strategies automatically registered, less boilerplate

3. **Prompt Engineering Service** - Current: Prompts scattered in `PromptService.getPrompt()` with string concatenation | Improvement: Dedicated prompt templates with variable substitution (e.g., Mustache, Handlebars) | Benefit: Non-developers can modify prompts, version control, A/B testing

4. **Typed Configuration** - Current: String-based environment variable access | Improvement: Strongly-typed config objects with validation (using class-validator) | Benefit: Compile-time safety, IDE autocomplete, runtime validation

5. **Repository Pattern Enhancement** - Current: Basic CRUD in BaseRepository | Improvement: Add transaction support, batch operations, query builder | Benefit: More complex data access patterns, reduced DynamoDB costs through batch operations

### Evolution Suggestions

1. **GraphQL Gateway** - Limitation: REST-only API requires multiple round trips for complex data | Approach: Add GraphQL resolver layer on top of existing services using @nestjs/graphql | Effort: Large | Benefit: Reduced client requests, flexible querying, better mobile performance

2. **Event-Driven Architecture** - Limitation: Synchronous strategy execution blocks request | Approach: Introduce message queue (SQS/EventBridge) for async processing, webhook callbacks | Effort: Medium | Benefit: Improved response times, better handling of long-running LLM calls, offline processing

3. **Response Caching** - Limitation: Repeated identical questions make expensive LLM calls | Approach: Implement semantic similarity caching (vector search) with Redis/OpenSearch | Effort: Medium | Benefit: Cost reduction, faster responses for common questions

4. **Multi-Model Routing** - Limitation: Single model per channel | Approach: Intent classification layer routes to cheapest/fastest model that can handle request (GPT-3.5 for simple, GPT-4 for complex) | Effort: Medium | Benefit: Significant cost savings, improved latency for simple queries

5. **Observability Enhancement** - Limitation: Limited distributed tracing | Approach: Full OpenTelemetry instrumentation with trace propagation across LLM calls and external APIs | Effort: Small | Benefit: Root cause analysis, latency breakdown, cost attribution per channel

## 13. Quick Reference

**Entry Points:**
- Main: `apps/rocket-assist-api/src/main.ts`
- Primary API: `POST /api/message` via `app/routes/message/message.controller.ts`
- Health: `GET /api/health` via `app/routes/health/health.controller.ts`
- Swagger: `/docs` (non-prod environments)

**Config Files:**
- `package.json` - Dependencies and scripts
- `nx.json` - Monorepo build configuration
- `.circleci/config.yml` - CI/CD pipeline
- `.helm/values.{env}.yaml` - Kubernetes deployment config
- `apps/rocket-assist-api/tsconfig.app.json` - TypeScript compiler settings
- `apps/rocket-assist-api/project.json` - Nx project configuration

**Dev Commands:**
```bash
nvm use                     # Switch to Node 18
yarn install                # Install dependencies
bin/start                   # Start Docker (DynamoDB local)
bin/provision-db-local      # Provision DynamoDB tables
yarn start                  # Start dev server (localhost:5000)
yarn lint                   # Run ESLint + Prettier + spell check
yarn test                   # Run all unit tests
yarn test:cov               # Generate coverage report
yarn build                  # Build production bundle
```

## 14. Summary

### Strengths

1. **Well-Architected Strategy Pattern** - Clean separation of concerns across 15+ chat channels with independent evolution paths. Each strategy encapsulates channel-specific logic without coupling.

2. **Production-Grade Observability** - Comprehensive logging with 141+ PII-redacted fields, OpenTelemetry metrics, Segment analytics, and health monitoring. Audit-ready logging for financial services compliance.

3. **Multi-Provider LLM Resilience** - Support for Azure OpenAI, OpenAI, and AWS Bedrock provides redundancy and enables cost optimization. Demonstrates forward-thinking vendor risk management.

4. **Strong TypeScript Practices** - Strict typing, explicit interfaces, comprehensive DTOs with validation, and clear separation between types and implementations. Minimal use of `any`.

5. **Scalable Infrastructure** - Multi-region Kubernetes deployment with auto-scaling, ephemeral PR environments for testing, and HAL-managed CI/CD pipeline. Battle-tested in production.

### Improvements

1. **ChatCompletionsService Refactoring** - The 560-line service with 15+ conditional branches for channel routing is the highest-priority refactoring target. Extract channel-specific completion logic into dedicated services or apply strategy pattern.

2. **Strategy Pattern Evolution** - Complete migration from monolithic strategies (e.g., `SfwcUnAuthAIStrategy`, `PIIStrategy`) to experience-based architecture demonstrated by `ServicingStrategy`. This will improve maintainability and testability.

3. **Module Architecture** - Break apart the 227-line `AppModule` with 127 providers into feature modules (ChatModule, IntegrationModule, AnalyticsModule). This will improve code organization and enable lazy loading.

4. **Response Streaming** - Implement Server-Sent Events for LLM responses to improve perceived performance. Current synchronous responses create long wait times for complex queries.

5. **Semantic Caching** - Implement vector-based similarity caching to reduce redundant LLM calls for common questions. Could reduce costs by 20-30% based on typical conversation patterns.

### Next Steps

1. **High Priority** - Refactor ChatCompletionsService: Extract channel-specific completion methods into dedicated services (2-3 weeks effort)
2. **High Priority** - Complete Watson decommission: Remove `ibm-watson` dependencies and `RocketApplicationWatsonStrategy` (1 week)
3. **Medium Priority** - Implement response streaming: Add SSE support to MessageController and update client integrations (2 weeks)
4. **Medium Priority** - Migrate remaining strategies to experience pattern: Convert `SfwcUnAuthAIStrategy`, `PIIStrategy`, `WebLeadFormAIStrategy` (3-4 weeks)
5. **Low Priority** - Feature module architecture: Split AppModule into domain-specific modules (1-2 weeks)

---

**Notes:** This API serves as a critical orchestration layer for Rocket Mortgage's conversational AI strategy across 15+ distinct channels. The architecture demonstrates strong software engineering practices with the Strategy pattern enabling independent channel evolution. The primary opportunities for improvement center on reducing complexity in the ChatCompletionsService and completing the architectural evolution to the experience-based pattern. The codebase is production-ready with comprehensive observability, security, and scalability features appropriate for a financial services environment.

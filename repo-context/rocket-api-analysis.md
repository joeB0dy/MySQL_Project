# Repository Analysis: Rocket API (v2)

**Repository URL:** `https://git.rockfin.com/RocketMortgage/rocket-api`
**Analysis Date:** 2026-03-02
**Analyzer:** repo-analyzer sub-agent

---

## 1. Repository Overview

**Project Type:** RESTful API / Microservice Backend
**Purpose:** Digital mortgage application backend serving as the API for Rocket Mortgage Application (RMA). Enables clients to apply for mortgages online and provides seamless transitions between self-service digital experiences and banker-assisted processing.
**Key Characteristics:**
- Monorepo structure with 4 packages managed by Lerna
- Supports both Purchase and Refinance mortgage loan types with differentiated experiences
- Integrates with Rocket Logic API as single source of truth for loan data
- Implements sophisticated PitStop system for quality control and routing
- Handles 10,000+ API requests with comprehensive middleware and validation

## 2. Technology Stack

**Languages:** TypeScript (ES2022, strict mode with selective strictness), Node.js
**Framework:** Hapi.js 21.4.0 (HTTP server framework)
**Key Dependencies:**
- `@RocketMortgage/rocket-dynamodb-client` 2.15.0 - Database abstraction
- `@RocketMortgage/rocket-config` 4.6.0 - Configuration management
- `@rocket-logic/rocket-logic-api-models` 1.35.0 - Rocket Logic integration models
- `@rocket-libraries/rocket-request-js` 3.6.0 - HTTP client with Auth0 support
- `@splitsoftware/splitio` 11.1.0 - Feature flag management
- `@redis/client` 1.6.0 - Caching layer
- `joi` 17.13.3 - Request validation
**Build/Package:** Yarn 1.22.22 (workspace monorepo), TypeScript compiler, Lerna 8.2.1 for multi-package orchestration
**Database:** DynamoDB (with local emulation via amazon/dynamodb-local)
**Infrastructure:** Docker Compose (development), Kubernetes (production via HAL), AWS services (S3, SNS, DynamoDB)

## 3. Architectural Patterns

### Primary Pattern

**Layered Architecture with Domain-Driven Design**
**Rationale:** The codebase is organized into feature-specific domains (credit, solutions, assets, income, etc.) with clear separation between Controllers, Services, Repositories, and Routes. This enables independent development of mortgage application features while maintaining consistency through shared infrastructure.

### Secondary Patterns

**Dependency Injection Container Pattern** (`Container.ts`)
- Location: `/rocket-api/src/Container.ts` (113KB, 150+ service registrations)
- Purpose: Centralized service instantiation with request-scoped and server-scoped lifecycles
- Enables testability and loose coupling across 79 feature modules

**Middleware Pipeline Pattern**
- Location: `/rocket-api/src/Middleware.ts` and `/rocket-api/src/middleware/`
- Key middleware: `RunPitStopEngine`, `RocketLogicSync`, `ValidatePayload`, `RunRoutingEngine`
- Purpose: Cross-cutting concerns applied consistently across all routes

**Strategy Pattern for Integration Sync**
- Location: `/rocket-api/src/thirdPartyServices/rocketLogic/strategies/`
- Purpose: Synchronize RMA data to Rocket Logic API using pluggable strategies per data domain
- Enables flexible data synchronization without tight coupling

**Repository Pattern for Data Access**
- Each domain has dedicated repository (e.g., `CreditRepository`, `LoanApplicationRepository`)
- Abstracts DynamoDB operations behind interfaces
- Enables testing with mock repositories

**Priority List Pattern for PitStop Evaluation**
- Location: `/rocket-api/src/pitStop/` (7 priority lists)
- Purpose: Define evaluation order for quality control checkpoints at different stages
- Enables complex business rules without tight coupling

### Design Principles

- [x] Separation of Concerns
- [x] Single Responsibility
- [x] Dependency Inversion
- [x] DRY

**Notes:** Strong adherence to separation through layered architecture. Dependency injection enables proper inversion of control. Some duplication exists in mapper classes and request builders due to domain-specific requirements. The Container.ts is a 113KB god object that coordinates all dependencies but maintains loose coupling through interfaces.

## 4. Module Structure

### Directory Layout

```
rocket-api/ (root)
├── rocket-api/                 # Main API application
│   ├── src/                    # 79 feature modules + infrastructure
│   │   ├── app.ts              # Application entry point
│   │   ├── Container.ts        # DI container (113KB)
│   │   ├── serverFactory.ts    # Hapi.js server configuration
│   │   ├── config.ts           # Environment configuration
│   │   ├── middleware/         # Cross-cutting concerns (13 middleware)
│   │   ├── pitStop/            # Quality control system (7 priority lists)
│   │   ├── thirdPartyServices/ # External integrations (30+ services)
│   │   ├── loanApplications/   # Core loan domain
│   │   ├── credit/             # Credit pull and analysis
│   │   ├── solutions/          # Loan products and pricing
│   │   ├── approval/           # Automated underwriting
│   │   └── [70+ other domains]
├── rocket-api-validation/      # Joi schema validation library
├── shared-libs/                # Common utilities and documentation tools
├── integration-tests/          # API integration test suite
├── documentation/              # Feature documentation (markdown + diagrams)
├── infrastructure/             # AWS resource policies and configuration
├── .helm/                      # Kubernetes deployment charts
└── scripts/                    # Build and deployment automation
```

### Core Modules

**Container & Dependency Injection** (`/rocket-api/src/Container.ts`)
- Responsibility: Centralized service instantiation, lifecycle management, request/server scoping
- Key files: `Container.ts` (1450+ lines), `ContainerProvider.ts`
- Dependencies: All services, repositories, controllers, middleware, third-party clients
- Pattern: Factory with static methods (`Container.withRequest()`, `Container.withServer()`)

**Application Startup** (`/rocket-api/src/app.ts`, `/rocket-api/src/serverFactory.ts`)
- Responsibility: Bootstrap Hapi.js server, register routes, initialize infrastructure (Redis, Kafka, Split.io)
- Key files: `app.ts` (389 lines), `serverFactory.ts` (157 lines)
- Dependencies: All route definitions (300+ routes), middleware, plugins
- Pattern: Server initialization with graceful shutdown handling

**PitStop Quality Control System** (`/rocket-api/src/pitStop/`)
- Responsibility: Evaluate loan application conditions to determine if banker assistance is required
- Key files: `PitStopEngine.ts` (9.5KB), 7 priority list files
- Dependencies: Loan application state, credit data, solution data
- Pattern: Rule engine with priority-based evaluation order
- Categories: Default, PreCredit, Credit, PostCredit, PreSolution, PostSolution, PostApproval

**Rocket Logic Integration** (`/rocket-api/src/thirdPartyServices/rocketLogic/`, `/rocket-api/src/middleware/RocketLogicSync.ts`)
- Responsibility: Synchronize loan data from RMA to Rocket Logic API (single source of truth)
- Key files: Strategy implementations, mappers, service layer, orchestrators
- Dependencies: Rocket Logic API models, synchronization strategies, mappers
- Pattern: Strategy pattern for domain-specific synchronization, middleware-driven sync
- Integration domains: Loan, Client, Property, Income, Assets, Application Flow

**Third-Party Service Layer** (`/rocket-api/src/thirdPartyServices/`)
- Responsibility: Abstract 30+ downstream service integrations
- Key services:
  - `loanEngine/` - Legacy loan processing system
  - `einsteinHub/` - Legacy solution retrieval
  - `creditPull/` - Credit bureau integration
  - `rocketGraph/` - Client data and prefill
  - `docServices/` - Document generation
  - `CDM/`, `GAM/`, `LES/`, `QKS/` - Various Rocket internal services
- Dependencies: `@rocket-libraries/rocket-request-js` (HTTP client with Auth0)
- Pattern: Service classes with request builders and mappers per integration

### Layer Architecture

```
[Presentation Layer] → [Business Logic Layer] → [Data Access Layer] → [External Systems]
Routes/Controllers    →  Services/Orchestrators → Repositories/Clients  → DynamoDB/APIs
```

**Presentation Layer:** Route definitions map HTTP endpoints to controllers. Controllers handle request/response transformation and orchestration. Middleware executes cross-cutting concerns (validation, auth, PitStops, syncing).

**Business Logic Layer:** Services implement domain logic. Orchestrators coordinate complex multi-service workflows. Builders construct complex request objects. Helpers provide domain-specific utilities.

**Data Access Layer:** Repositories abstract DynamoDB operations. Third-party clients abstract external API calls. Mappers transform between RMA and external system models.

**Communication Pattern:** Request flows through middleware pipeline → controller → service → repository/client. Responses follow reverse path with transformation at each layer.

## 5. Data Flow & Communication

### Request Flow

```
HTTP Request → Hapi.js Server → Middleware Pipeline → Controller → Service → Repository/Client → DynamoDB/External API
    ↓                              ↓                      ↓            ↓          ↓
[Auth/Validation]  → [PitStopEngine] → [RocketLogicSync] → [Business Logic] → [Data Access]
```

**Typical Flow for Saving Loan Data:**
1. Request enters via route (e.g., `POST /applications/{applicationId}/credit`)
2. `onPostAuth` middleware logs request details
3. `ValidateRequest` middleware checks authorization header
4. `ValidatePayload` middleware validates request body against Joi schema
5. `GetLoan` middleware loads loan application from DynamoDB
6. Controller method executes business logic via service layer
7. `RocketLogicSync` middleware synchronizes data to Rocket Logic API
8. `RunPitStopEngine` middleware evaluates quality control conditions
9. Response returned with standardized format
10. `onResponse` event logs response details

**State Management:**
- Loan application state stored in DynamoDB with TTL (365 days)
- Request-scoped state managed via `RocketApiRequest` object extended from Hapi.js request
- Session state cached in Redis for performance
- Feature flags managed via Split.io SDK

**Inter-Module Communication:**
- Direct method calls via dependency injection (no event bus for internal communication)
- Asynchronous communication via Kafka for cross-system events
- Qtweet events published to SNS for downstream system notifications

**Events:**
- Kafka consumer for loan document events from Rocket Logic
- SNS publisher for PitStop events and application state changes
- ODS (Operational Data Store) events for analytics

## 6. Integration Points

### External Services

| Service | Purpose | Method | Location |
|---------|---------|--------|----------|
| Rocket Logic API | Single source of truth for loan data, pricing, underwriting | REST | `thirdPartyServices/rocketLogic/` |
| Einstein Hub | Legacy loan product retrieval | REST | `thirdPartyServices/einsteinHub/` |
| Loan Engine | Legacy loan processing and rate lock | SOAP/XML | `thirdPartyServices/loanEngine/` |
| Credit Pull Service | Credit bureau integration | REST | `thirdPartyServices/creditPull/` |
| Rocket Graph | Client data and prefill | GraphQL | `thirdPartyServices/rocketGraph/` |
| Submission Engine | Submit loans offline to bankers | REST | `thirdPartyServices/submissionEngine/` |
| TheKey | Lead validation and routing | REST | Referenced in PitStop flow |
| OurHouse | Banker assignment | REST | `thirdPartyServices/ourHouseSystem/` |
| Plaid | Asset import and verification | REST | Integrated in `asset/` module |
| CDM (Client Data Management) | Client information | REST | `thirdPartyServices/CDM/` |
| Auth0 | Authentication and authorization | OAuth2 | `thirdPartyServices/auth0/` |

### Database

**Type:** NoSQL (AWS DynamoDB)
**Access:** `@RocketMortgage/rocket-dynamodb-client` (custom ORM/abstraction layer)
**Location:** Repository implementations in each domain module
**Tables:** Environment-prefixed tables (e.g., `test-LoanApplications`, `beta-LoanApplications`, `production-LoanApplications`)
**Local Development:** DynamoDB Local on port 7777 with Docker Compose

### Critical Dependencies

1. **@RocketMortgage/rocket-dynamodb-client (2.15.0)** - Database abstraction providing repository pattern, connection pooling, TTL management, and retry logic for DynamoDB operations
2. **@rocket-logic/rocket-logic-api-models (1.35.0)** - TypeScript models for Rocket Logic API integration, ensuring type safety across system boundaries
3. **@rocket-libraries/rocket-request-js (3.6.0)** - HTTP client with Auth0 token management, automatic retry, circuit breaker, and request/response logging
4. **@hapi/hapi (21.4.0)** - Core HTTP server framework providing routing, lifecycle events, request/response handling
5. **@splitsoftware/splitio (11.1.0)** - Feature flag management enabling A/B testing and progressive rollout of new features

## 7. Key Components Deep Dive

### PitStopEngine

**Path:** `/rocket-api/src/pitStop/PitStopEngine.ts`
**Purpose:** Evaluates loan application conditions against business rules to determine if special handling (banker assistance) is required. Critical for maintaining service quality and ensuring every client can successfully complete their mortgage application regardless of complexity.

**Key classes/functions:**
- `PitStopEngine.run()` - Main evaluation method accepting loan state and priority list
- `PitStopPriority` - Interface defining code, priority, condition function, action code
- Priority Lists: `DefaultPitStopPriority`, `PreCreditPitStopPriorityList`, `CreditPitStopPriority`, `PostCreditPitStopPriority`, `PreSolutionPitStopPriority`, `PostSolutionPitStopPriority`, `PostApprovalPitStopPriority`

**Patterns:** Strategy pattern for condition evaluation, Priority pattern for evaluation order

**Example:**
```typescript
// PitStop evaluation triggered by middleware
const pitStops = await PitStopEngine.run(
    loanApplication,
    credit,
    PostCreditPitStopPriority,
    logger
);

if (pitStops.length > 0) {
    // Trigger submission engine to route to banker
    await submissionEngineService.submit(loanApplication, pitStops);
}
```

**Categories and Purpose:**
- **PreCredit** - Validate basic eligibility before credit pull
- **Credit** - Handle credit pull issues (bureau failures, no credit score)
- **PostCredit** - Evaluate credit quality (low scores, derogatory marks)
- **PreSolution** - Check scenario viability before product retrieval
- **PostSolution** - Validate solution availability and product fit
- **PostApproval** - Final checks before loan commitment

### Container (Dependency Injection)

**Path:** `/rocket-api/src/Container.ts`
**Purpose:** Central service registry and factory providing dependency injection throughout the application. Manages service lifecycles (request-scoped vs server-scoped) and ensures consistent instantiation of 150+ services, repositories, and controllers.

**Key classes/functions:**
- `Container.withRequest(request)` - Creates request-scoped container
- `Container.withServer(server)` - Creates server-scoped container
- Service accessor methods (e.g., `container.loanApplicationService()`, `container.creditService()`)
- Lazy initialization for performance

**Patterns:** Factory, Singleton (per scope), Dependency Injection

**Example:**
```typescript
// Request-scoped container usage in controller
const container = Container.withRequest(request);
const loanService = container.loanApplicationService();
const creditService = container.creditService();

// Services share request context and logger
const loan = await loanService.getLoan(applicationId);
const credit = await creditService.getCredit(loan.loanId);
```

### Rocket Logic Synchronization Middleware

**Path:** `/rocket-api/src/middleware/RocketLogicSync.ts`
**Purpose:** Automatically synchronizes loan data changes from RMA to Rocket Logic API, ensuring data consistency across systems. Enables seamless handoff from digital to banker-assisted experiences by keeping Rocket Logic (single source of truth) up-to-date in real-time.

**Key classes/functions:**
- `RocketLogicSyncMiddleware` - Main middleware class
- Strategy Registry - Maps data domains to synchronization strategies
- `SyncStrategies` - Domain-specific sync implementations (Employment, Income, Assets, Credit, Solutions, etc.)

**Patterns:** Middleware pattern, Strategy pattern, Orchestration pattern

**Example:**
```typescript
// Middleware configuration on route
{
    method: 'POST',
    path: '/applications/{applicationId}/income',
    handler: saveIncomeController,
    options: {
        pre: [
            { method: GetLoan },
            { method: RocketLogicSync }, // Syncs after save
        ]
    }
}

// Strategy determines what data to sync
class IncomeStrategy {
    async sync(loan, rocketLogicService) {
        const incomeData = this.mapToRocketLogicFormat(loan.income);
        await rocketLogicService.updateIncome(loan.rocketLogicId, incomeData);
    }
}
```

### Hapi.js Server Factory

**Path:** `/rocket-api/src/serverFactory.ts`
**Purpose:** Configures and initializes the Hapi.js HTTP server with all necessary plugins, middleware, routes, timeout settings, and logging. Establishes the HTTP server lifecycle and request/response pipeline.

**Key classes/functions:**
- `serverFactory()` - Main factory function returning configured Hapi.js server
- Timeout configuration: 60s server timeout with hierarchical connection timeouts
- Plugin registration: Pino logger, Inert (file serving for docs)
- Lifecycle extensions: `onRequest`, `onPostAuth`, `onPreResponse`, `response` events

**Patterns:** Factory pattern, Builder pattern, Lifecycle hooks

**Example:**
```typescript
const server = await serverFactory(
    containerProvider,
    routes,
    convertRoute,
    new MiddlewareImpl()
);

// Timeout hierarchy for Istio compatibility:
// serverTimeout (60s) < keepAliveTimeout (1hr 5m) < headersTimeout (1hr 5m 5s)
server.listener.keepAliveTimeout = 3_900_000;
server.listener.headersTimeout = 3_905_000;

await server.start();
```

## 8. Configuration & Infrastructure

**Config Approach:** Environment variables (`.env` files for local), ConfigMap from `@RocketMortgage/rocket-config`, ECS variables for cloud environments
**Config Location:**
- `/rocket-api/src/config.ts` (16KB) - Main configuration with 100+ mappings
- `/rocket-api/.env` (gitignored) - Local secrets and overrides
- `/rocket-api/.env.runtime` - Feature flags and common runtime config (committed)

**Deployment:**
- **Local:** Docker Compose with 6 services (node, dynamo, redis, mocks, localstack, dynamo-admin)
- **Cloud:** Kubernetes on AWS EKS via HAL deployment system
- **CI/CD:** CircleCI pipeline → HAL (Helm) → EKS clusters in us-east-2 and us-west-2

**Containers:** Docker (Dockerfile with multi-stage builds: `dev` and `cloud` targets)

### Key Environment Variables

| Variable | Purpose | Required |
|----------|---------|----------|
| ENVIRONMENT | Environment name (local, test, beta, prod) | yes |
| AWS_REGION | AWS region for DynamoDB and other services | yes |
| AUTH0_CLIENT_ID | Auth0 client for service-to-service auth | yes |
| AUTH0_CLIENT_SECRET | Auth0 client secret | yes |
| CACHE_ENDPOINT_READ | Redis read endpoint | yes |
| CACHE_ENDPOINT_WRITE | Redis write endpoint | yes |
| SPLIT_API_KEY | Split.io feature flag API key | yes |
| DYNAMODB_HOST | DynamoDB endpoint (local override) | local only |
| APP_ID | Application ID (201901) | yes |
| ROCKET_LOGIC_BASE_URL | Rocket Logic API base URL | yes |
| SUBMISSION_ENGINE_BASE_URL | Submission Engine API base URL | yes |

## 9. Quality Attributes

**Error Handling:**
- Centralized error class: `RocketApiError` with typed error categories (NOT_FOUND, BAD_REQUEST, BAD_GATEWAY, INTERNAL_SERVER_ERROR, UNAUTHORIZED)
- HTTP status code mapping from error types
- Error cause chaining for root cause analysis
- Boom error responses via Hapi.js with consistent JSON format
- Location: `/rocket-api/src/errors/`

**Logging:**
- Library: Pino (structured JSON logging) via `hapi-pino` plugin
- Approach: Request-scoped loggers with context propagation (`ConsoleLogger.fromRequest()`)
- Log levels: error, warn, info, debug
- Event types: SESSION, TOOL, HOOK, SKILL, COMMAND
- Centralized logging utility: `/rocket-api/src/Logger.ts` with `ServerLogger`, `ConsoleLogger`, `AppSetupLogger`
- Integration: Splunk for log aggregation and dashboards

**Security:**
- Auth0 authentication with JWT token validation
- Authorization header parsing and validation (`parseAuthorizationHeader` middleware)
- Request payload validation via Joi schemas (rocket-api-validation package)
- Partner permission checks (`CheckPartnerPermissions` middleware)
- Redbird header validation for internal service calls
- PII redaction in logs (XML payloads redacted, sensitive fields filtered)

**Testing:**
- **Unit Tests:** Mocha + Chai + Sinon, 656+ test files
- **Location:** `__tests__/` directories colocated with source files
- **Coverage:** NYC (Istanbul) with threshold checks
- **Integration Tests:** Separate package (`integration-tests/`) with full API test suite
- **Mocking:** Mountebank for downstream service mocks in local development
- **Commands:** `yarn test` (parallel execution), `yarn test:coverage`, `yarn api-unit-tests`

## 10. Architectural Decisions & Trade-offs

### Decision: Monorepo with Lerna

- **Choice:** Lerna-managed monorepo with 4 workspaces (rocket-api, rocket-api-validation, shared-libs, integration-tests)
- **Alternatives:** Separate repositories per package, single package repository
- **Rationale:**
  - Shared code (validation schemas, types) needs to stay synchronized with API changes
  - Integration tests require access to API types and test utilities
  - Atomic commits across API and validation ensure consistency
  - Simplified dependency management and version control
- **Trade-offs:**
  - **Gains:** Single PR for cross-package changes, consistent tooling, easier refactoring
  - **Losses:** Larger repository size, longer CI builds, all packages versioned together

### Decision: Hapi.js Framework (Not Express)

- **Choice:** Hapi.js 21.4.0 as HTTP framework
- **Alternatives:** Express, Fastify, Koa
- **Rationale:**
  - Built-in request lifecycle with extensive extension points (onRequest, onPostAuth, onPreResponse, etc.)
  - Rich plugin ecosystem for enterprise features
  - Configuration-based routing reduces boilerplate
  - Strong validation support via Joi (same author)
  - Request-scoped app context without global state
- **Trade-offs:**
  - **Gains:** Structured middleware pipeline, robust lifecycle hooks, less boilerplate
  - **Losses:** Smaller community than Express, steeper learning curve, fewer third-party plugins

### Decision: DynamoDB with Custom ORM

- **Choice:** DynamoDB with custom `@RocketMortgage/rocket-dynamodb-client` abstraction layer
- **Alternatives:** PostgreSQL/RDS with TypeORM/Sequelize, MongoDB, direct DynamoDB SDK
- **Rationale:**
  - NoSQL fits variable loan application schemas (different data for Purchase vs Refinance)
  - Serverless/managed service reduces operational overhead
  - Custom ORM provides enterprise features (TTL, retry logic, connection pooling)
  - AWS integration simplifies infrastructure
- **Trade-offs:**
  - **Gains:** High scalability, low latency, managed service, flexible schema
  - **Losses:** No complex queries/joins, eventual consistency challenges, vendor lock-in, custom ORM maintenance burden

**Scalability:**
- Horizontally scalable via Kubernetes pod replication
- DynamoDB auto-scales with load
- Redis caching reduces database load
- Feature flags enable gradual rollout of changes

**Performance:**
- Redis caching for frequently accessed data (sessions, configuration)
- In-memory cache (`Container.inMemoryCache`) for high-frequency lookups
- Parallel test execution for faster CI builds
- Connection pooling for HTTP clients and database

## 11. Extension Points

**Plugin System:** No formal plugin system, but Hapi.js plugin architecture enables modular features. New plugins registered in `serverFactory.ts`.

**Adding Features:**
1. **New API Endpoint:**
   - Create domain module directory (e.g., `/rocket-api/src/newFeature/`)
   - Implement Controller, Service, Repository following existing patterns
   - Define route in `newFeatureRoutes.ts`
   - Add route to `app.ts` routes array
   - Add validation schema to `rocket-api-validation` package
   - Add integration test to `integration-tests` package

2. **New PitStop Condition:**
   - Add condition to appropriate priority list (e.g., `PostCreditPitStopPriority.ts`)
   - Define condition function taking loan/credit/solution state
   - Assign unique code number and action code
   - Document in `/documentation/pitstops/PitStopDirectory.md`

3. **New Third-Party Integration:**
   - Create service directory in `/thirdPartyServices/serviceName/`
   - Implement service class with HTTP client
   - Create request builder and mapper classes
   - Register service factory in `Container.ts`
   - Add configuration variables to `config.ts`

**Customization:**
- Feature flags via Split.io for gradual rollout
- Environment-specific configuration via ConfigMap
- Middleware can be toggled per-route in route definitions
- PitStop conditions can be enabled/disabled via configuration

## 12. Technical Debt & Improvements

### Technical Debt

1. **Container.ts God Object** - Location: `/rocket-api/src/Container.ts` | Impact: H | Fix: Refactor into domain-specific sub-containers or use proper DI framework (InversifyJS, tsyringe)

2. **Mixed Rocket Logic and Legacy Einstein Hub** - Location: `/rocket-api/src/solutions/`, `/rocket-api/src/thirdPartyServices/` | Impact: M | Fix: Complete migration to Rocket Logic API and deprecate Einstein Hub integration

3. **Inconsistent Error Handling** - Location: Various service classes | Impact: M | Fix: Standardize error handling with proper error cause chaining and consistent error types

4. **Limited Type Safety in DynamoDB Operations** - Location: Repository implementations | Impact: M | Fix: Add stronger typing to custom ORM or migrate to TypeORM/Prisma

5. **Manual Synchronization Logic** - Location: `/rocket-api/src/middleware/RocketLogicSync.ts` | Impact: M | Fix: Explore event-driven architecture with Change Data Capture (CDC) for automatic sync

### Refactoring Opportunities

1. **Split Container into Domain Containers** - Current: Single 113KB Container.ts with 150+ registrations | Improvement: Create domain-specific containers (LoanContainer, CreditContainer, etc.) with composition | Benefit: Improved maintainability, faster builds, clearer dependencies

2. **Extract Mappers into Shared Library** - Current: Duplicate mapping logic across strategies | Improvement: Create reusable mapper utilities with composition | Benefit: Reduced duplication, consistent transformations, easier testing

3. **Consolidate Configuration Management** - Current: Mix of environment variables, ConfigMap, and hardcoded defaults | Improvement: Single configuration source with schema validation | Benefit: Type-safe configuration, easier onboarding, reduced config errors

4. **Migrate from Mocha to Jest** - Current: Mocha + Chai + Sinon test suite | Improvement: Adopt Jest with built-in mocking and parallel execution | Benefit: Faster tests, better DX, snapshot testing, integrated coverage

### Evolution Suggestions

1. **Adopt Event-Driven Architecture** - Limitation: Synchronous middleware-based sync is brittle | Approach: Implement CDC with Kafka/SNS for async data propagation | Effort: L

2. **Implement GraphQL Layer** - Limitation: 300+ REST endpoints with inconsistent patterns | Approach: Add GraphQL gateway for client-facing APIs while keeping REST for internal services | Effort: L

3. **Add OpenAPI/Swagger Documentation** - Limitation: Documentation is manual markdown files | Approach: Generate OpenAPI spec from Joi schemas and Hapi.js routes, integrate with Swagger UI | Effort: M

4. **Implement Circuit Breaker Pattern** - Limitation: No systematic failure isolation for downstream services | Approach: Add circuit breaker to rocket-request-js library | Effort: M

5. **Upgrade to Hapi.js v21+ Features** - Limitation: Not using latest framework capabilities | Approach: Adopt async/await lifecycle methods, new validation features | Effort: S

## 13. Quick Reference

**Entry Points:**
- Main: `/rocket-api/src/app.ts`
- Server Factory: `/rocket-api/src/serverFactory.ts`
- Container: `/rocket-api/src/Container.ts`

**Config Files:**
- Application Config: `/rocket-api/src/config.ts`
- Environment Variables: `/rocket-api/.env` (local), `/rocket-api/.env.runtime`
- TypeScript Config: `/tsconfig.base.json`, `/rocket-api/tsconfig.json`
- Lerna Config: `/lerna.json`
- Package Config: `/package.json`, `/rocket-api/package.json`

**Dev Commands:**

```bash
# Setup - MUST use Node 22
nvm use 22 && yarn install && yarn compile

# Development
yarn start                    # Start API with mocks
yarn start:no-mocks          # Start API without mocks
yarn stop                    # Stop all services

# Testing
yarn test                    # Run all tests (parallel)
yarn api-unit-tests         # API unit tests only
yarn test:coverage          # With coverage report
cd integration-tests && yarn test  # Integration tests

# Code Quality
yarn lint                    # ESLint check
yarn lint-fix               # Auto-fix issues
yarn format                 # Prettier formatting
yarn prePushChecks          # Pre-commit validation

# Database
yarn provision-db-local     # Setup local DynamoDB
yarn redis-flushall         # Clear Redis cache

# Documentation
yarn generate-docs          # Generate API docs
yarn validate-docs          # Validate documentation
```

## 14. Summary

### Strengths

1. **Well-Documented Domain Logic** - Comprehensive markdown documentation for PitStops, Rocket Logic integration, Prefill system, Solution system with clear purpose, implementation details, and business context
2. **Robust Quality Control System** - PitStop engine provides systematic evaluation of loan conditions with 7 priority lists, ensuring every client gets appropriate support regardless of complexity
3. **Clean Separation of Concerns** - Layered architecture with clear boundaries between controllers, services, repositories, and external integrations enables independent development and testing
4. **Strong Type Safety** - TypeScript throughout with strict compiler options, comprehensive Joi validation schemas, and typed models for external integrations
5. **Production-Ready Infrastructure** - Docker Compose for local development, Kubernetes deployment, comprehensive logging/monitoring, feature flags, Redis caching, graceful shutdown handling

### Improvements

1. **Dependency Injection Complexity** - 113KB Container.ts god object managing 150+ services creates maintenance burden and unclear dependency graphs
2. **Mixed Legacy and Modern Systems** - Dual integration with both Einstein Hub (legacy) and Rocket Logic API (modern) creates complexity and potential inconsistencies
3. **Limited Observability** - No distributed tracing, circuit breakers, or systematic performance monitoring beyond basic logging
4. **Configuration Management** - Mix of environment variables, ConfigMap, and hardcoded defaults makes configuration discovery difficult
5. **Testing Strategy** - Test coverage gaps in integration scenarios, heavy reliance on mocked services may hide integration issues

### Next Steps

1. **H** - Implement distributed tracing with OpenTelemetry to diagnose performance issues and track cross-system flows
2. **H** - Complete migration from Einstein Hub to Rocket Logic API for solution retrieval to simplify architecture
3. **M** - Refactor Container.ts into domain-specific sub-containers to improve maintainability and reduce cognitive load
4. **M** - Add circuit breaker pattern to rocket-request-js for systematic failure isolation
5. **L** - Explore event-driven architecture with CDC for more robust Rocket Logic synchronization

---

**Notes:** This is a mature, production-grade API serving critical business functions in the mortgage origination process. The architecture demonstrates strong separation of concerns with domain-driven design, but suffers from some technical debt accumulated over multiple years of development. The PitStop system is a sophisticated business rule engine that ensures quality control throughout the loan application lifecycle. The Rocket Logic integration represents a strategic shift toward unified data management across Rocket Mortgage systems. Primary improvement opportunities lie in modernizing dependency injection, completing the migration from legacy systems, and enhancing observability for distributed system debugging.

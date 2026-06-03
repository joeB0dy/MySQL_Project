# Repository Analysis: cx-funnel-rocket-local

**Repository URL:** `https://github.com/RocketMortgage/cx-funnel-rocket-local`
**Analysis Date:** 2026-03-02
**Analyzer:** repo-analyzer sub-agent

---

## 1. Repository Overview

**Project Type:** NX Monorepo - Multi-application system with data pipeline, API backend, and web frontend

**Purpose:** Rocket Local is a comprehensive directory system for local Rocket Mortgage Franchise Loan Officers. It provides searchable, enriched loan officer profiles with geolocation capabilities, social proof integration, and lead submission workflows. The system enables agents to connect with local bankers in their neighborhood for in-person consultations, humanizing the Rocket brand beyond its online-only perception.

**Key Characteristics:**
- Three-tier architecture with automated daily data synchronization
- Geo-spatial search capabilities powered by OpenSearch
- Integration with internal RHDS (Rock Human Data Service) and external Social Proof APIs
- NX monorepo structure with independent deployment pipelines
- Public-facing customer portal with private internal data sources

## 2. Technology Stack

**Languages:**
- TypeScript (ES2022) - API and UI (~9,086 LOC combined)
- JavaScript (ES6+) - Lambda import function (~566 LOC)
- SCSS - UI styling with Angular Material theming

**Frameworks:**
- Backend: NestJS 10.x (Node.js Express platform)
- Frontend: Angular 19.x (standalone components)
- Build Tool: NX 21.x monorepo orchestration

**Key Dependencies:**
- **Database:** OpenSearch 2.13.0 (AWS-managed, geo-spatial search)
- **API Layer:** @opensearch-project/opensearch client with AWS Sigv4 auth
- **Data Sources:** GraphQL (graphql-request for RHDS), Web scraping (Cheerio for Social Proof)
- **Maps:** @angular/google-maps with Google Geocoding API
- **Logging:** Pino (nestjs-pino) with structured logging
- **Metrics:** @rocklib/metrics, @rocklib/healthcheck
- **Testing:** Jest (API), Karma/Jasmine (UI), Cypress (E2E)

**Build/Package:**
- NX CLI with caching and task orchestration
- Webpack (Lambda bundling)
- SWC/TypeScript compiler
- npm for package management

**Database:** OpenSearch 2.13.0 (index: "local") - Geo-point mapping for location-based search

**Infrastructure:**
- **Deployment:** AWS (Lambda, EKS, Akamai NetStorage)
- **Containerization:** Docker (API only)
- **IaC:** Terraform/Terragrunt
- **CI/CD:** GitHub Actions with HAL deployment automation
- **Scheduling:** AWS EventBridge (daily 7-8 AM ET cron)

## 3. Architectural Patterns

### Primary Pattern

**Event-Driven Batch Processing + Backend-For-Frontend (BFF)**

**Rationale:** The system follows a data pipeline pattern where scheduled events trigger batch imports that populate a search-optimized datastore, which is then queried by a lightweight BFF API serving a public-facing SPA. This pattern optimizes for:
- Read-heavy workload with infrequent writes (daily batch updates)
- Separation of data ingestion complexity from query performance
- Independent scaling of import, API, and UI layers
- Resilience (failed imports don't impact user-facing search)

### Secondary Patterns

**1. Repository Pattern** (`apps/rocket-local-api/src/search/search.service.ts`)
- SearchService abstracts OpenSearch client operations
- Clean separation between data access and business logic
- Centralized error handling and logging

**2. Data Transfer Objects (DTO)** (`apps/rocket-local-api/src/search/search.dto.ts`)
- Strong typing for API contracts with class-validator decorators
- Consistent data shape between layers

**3. Service Locator** (NestJS Dependency Injection)
- Module-based dependency injection across API
- Singleton services for Config, Logger, OpenSearch client

**4. Adapter/Mapper Pattern** (`apps/rocket-local-api/src/search/search.mapper.ts`)
- Transforms OpenSearch responses to UI-compatible DTOs
- Decouples internal data structure from external API contract

**5. Fallback/Default Pattern** (Lambda import - `apps/rocket-local-import/scrape.js`)
- Graceful degradation when Social Proof scraping fails
- Default Rocket logo and generic bio ensure banker still appears in search

### Design Principles

- [x] **Separation of Concerns** - Clear boundaries between import, API, and UI with independent deployment
- [x] **Single Responsibility** - Each app has one purpose: import data, serve data, or display data
- [x] **Dependency Inversion** - API depends on Config/Logger abstractions, not concrete implementations
- [x] **DRY** - Shared configuration in nx.json, tsconfig.base.json; reusable components in UI

**Notes:**
- Strong adherence to NestJS conventions (modules, controllers, services, DTOs)
- UI uses modern Angular standalone components (no NgModules)
- Lambda import is imperative JavaScript (not class-based) for simplicity in Lambda environment
- Error boundaries at each layer with structured logging for debugging

## 4. Module Structure

### Directory Layout

```
cx-funnel-rocket-local/
├── apps/                       # NX application projects
│   ├── rocket-local-import/    # Lambda: Daily data sync (RHDS + Social Proof → OpenSearch)
│   ├── rocket-local-api/       # NestJS: BFF API (OpenSearch → REST endpoints)
│   └── rocket-local-ui/        # Angular: Public-facing search and profile pages
├── iac/                        # Terraform infrastructure (by env/region/service)
│   ├── 359077869784/           # Beta AWS account
│   └── 475709878609/           # Prod AWS account
├── tools/                      # Utility scripts
│   └── scripts/                # SauceLabs config generator
├── .github/workflows/          # CI/CD pipelines (API, UI, Import, Load Test)
├── nx.json                     # NX workspace configuration
├── package.json                # Root dependencies and scripts
├── tsconfig.base.json          # Shared TypeScript configuration
├── README.md                   # Setup and architecture overview
├── ROCKET_LOCAL_OVERVIEW.md    # Detailed technical documentation
├── CLAUDE.md                   # AI assistant guidance
└── ROCKET_LOCAL_FLOW_INDEX.json # Architecture metadata
```

### Core Modules

**1. rocket-local-import** (`apps/rocket-local-import/`)
- **Responsibility:** Daily batch import orchestrating data fetch from RHDS GraphQL API and Social Proof web scraping, enrichment with geocoding, and bulk upload to OpenSearch
- **Key files:**
  - `index.js` - Main Lambda handler with orchestration logic, SPECIAL_USERS map for URL overrides
  - `query.graphql` - RHDS GraphQL query filtering active bankers with Franchise_Banker skill
  - `scrape.js` - Social Proof web scraper using Cheerio with fallback defaults
  - `es-schema.json` - OpenSearch index schema with geo_point mapping
- **Dependencies:**
  - Internal: RHDS (GraphQL), Google Geocoding API
  - External: Social Proof (web scraping), OpenSearch, AWS Lambda runtime

**2. rocket-local-api** (`apps/rocket-local-api/`)
- **Responsibility:** Backend-For-Frontend API exposing search and profile endpoints, querying OpenSearch with geo-spatial filters
- **Key files:**
  - `src/main.ts` - Bootstrap with Swagger, CORS, validation pipes, metrics middleware
  - `src/app.module.ts` - Root module importing Search, Lead, Google, Health, Global modules
  - `src/search/search.service.ts` - OpenSearch client wrapper with geo_bounding_box queries
  - `src/search/search.controller.ts` - REST endpoints: GET /search, GET /search/:id
  - `src/lead/lead.controller.ts` - POST /lead for referral submissions
  - `src/global/config/config.service.ts` - Environment configuration
  - `src/global/logger/logger.service.ts` - Pino structured logging
- **Dependencies:**
  - Internal: OpenSearch (AWS-managed)
  - External: @nestjs framework, @opensearch-project/opensearch, AWS SDK (Sigv4 auth)

**3. rocket-local-ui** (`apps/rocket-local-ui/`)
- **Responsibility:** Single-page Angular application providing search and profile pages with Google Maps integration, geolocation, and TypeForm referral modal
- **Key files:**
  - `src/app/app-routing.module.ts` - Routes: /, /search, /profile/:nmls/**, /submit-a-referral
  - `src/app/search/search.component.ts` - Search orchestrator with map and result list
  - `src/app/profile/profile.component.ts` - Profile page orchestrator fetching banker by NMLS
  - `src/app/components/search-bar/` - Google Places autocomplete input
  - `src/app/search/map/map.component.ts` - Google Maps with banker markers
  - `src/app/profile/bio-hero/` - Profile header with photo, rating, contact info
  - `src/app/components/testimonials/` - Reviews carousel with star ratings
  - `src/app/services/` - API client services
- **Dependencies:**
  - Internal: rocket-local-api (REST)
  - External: @angular/google-maps, @rocketcentral/rocket-design-system-angular, RxJS

**4. iac** (`iac/`)
- **Responsibility:** Terraform infrastructure definitions for OpenSearch, Lambda, EventBridge, EKS deployments across beta and prod environments
- **Key files:**
  - `{account}/{region}/{env}/aws-lambda-tf/terraform.tfvars` - Lambda configuration
  - `{account}/{region}/{env}/aws-eventbridge-tf/terraform.tfvars` - Daily cron schedule (0 12 * * ? *)
  - `{account}/{region}/{env}/aws-opensearch-tf/terraform.tfvars` - OpenSearch cluster config
- **Dependencies:** Terraform modules from git.rockfin.com/terraform/*

### Layer Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│ PRESENTATION LAYER (Angular UI)                                 │
│ - Search page with map and result cards                         │
│ - Profile pages with testimonials                               │
│ - Google Maps integration                                       │
│ - TypeForm referral modal                                       │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP REST API
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│ APPLICATION LAYER (NestJS BFF API)                              │
│ - Search/Profile endpoints                                      │
│ - Lead submission                                               │
│ - OpenSearch query orchestration                               │
│ - Error handling and logging                                    │
└────────────────────────────┬────────────────────────────────────┘
                             │ OpenSearch Client (AWS Sigv4)
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│ DATA LAYER (OpenSearch)                                         │
│ - Index: "local"                                                │
│ - Geo-spatial search with geo_point mapping                     │
│ - Document store with enriched banker profiles                  │
└────────────────────────────┬────────────────────────────────────┘
                             ↑ Bulk updates (daily)
┌─────────────────────────────────────────────────────────────────┐
│ DATA INGESTION LAYER (Lambda Import)                            │
│ - Scheduled EventBridge trigger (daily 7-8 AM ET)               │
│ - RHDS GraphQL queries (auth + filtering)                       │
│ - Social Proof web scraping (with fallbacks)                    │
│ - Google Geocoding enrichment                                   │
│ - OpenSearch bulk upload                                        │
└─────────────────────────────────────────────────────────────────┘
```

**Communication Pattern:**
- **UI → API:** Synchronous HTTP REST (search queries, profile requests)
- **API → OpenSearch:** Synchronous query/response with AWS Sigv4 authentication
- **Lambda → RHDS:** Synchronous GraphQL request with Auth0 token
- **Lambda → Social Proof:** Asynchronous web scraping with retry/fallback
- **Lambda → OpenSearch:** Bulk synchronous upserts/deletes
- **EventBridge → Lambda:** Event-driven scheduled invocation (cron)

## 5. Data Flow & Communication

### Request Flow

```
User searches "Detroit MI"
    ↓
UI: Geocode address via Google Places API → lat/lng
    ↓
UI: HTTP GET /search?lat=42.33&lng=-83.04&northLat=...&southLat=...&eastLng=...&westLng=...&page=1
    ↓
API: SearchController.findLocations() → SearchService.findBankersByLocation()
    ↓
API: OpenSearch geo_bounding_box query with _geo_distance sort
    ↓
OpenSearch: Returns paginated results (20 per page)
    ↓
API: SearchMapper.mapSearchResults() → DTO transformation
    ↓
UI: Display result cards + map markers

User clicks profile
    ↓
UI: Navigate to /local-loan-officers/profile/1234567/City-State/Name
    ↓
UI: HTTP GET /search/1234567 (NMLS ID)
    ↓
API: SearchController.getLocation() → SearchService.findBanker()
    ↓
API: OpenSearch GET document by ID
    ↓
API: SearchMapper.mapLocation() → DTO transformation
    ↓
UI: Render bio hero, testimonials, contact info
```

**State Management:**
- **UI:** RxJS BehaviorSubjects for search results and map data (reactive state)
- **API:** Stateless - no session/cache (pure request/response)
- **Lambda:** Stateless - ephemeral execution with token caching in local ENV=LOCAL mode

**Inter-Module Communication:**
- **UI ↔ API:** HTTP REST with Angular HttpClient, CORS enabled on API
- **API ↔ OpenSearch:** @opensearch-project/opensearch Client with AWS Sigv4 signer
- **Lambda ↔ RHDS:** graphql-request with Auth0 client credentials flow
- **Lambda ↔ Social Proof:** axios HTTP scraping with Cheerio HTML parsing

**Events:**
- **EventBridge Cron:** Triggers Lambda daily at 0 12 * * ? * (UTC) = 7-8 AM ET
- **No internal event bus:** Direct synchronous communication only

## 6. Integration Points

### External Services

| Service | Purpose | Method | Location |
|---------|---------|--------|----------|
| RHDS (Rock Human Data Service) | Core banker data (name, NMLS, contact, address, skills) | GraphQL (Auth0 token) | `apps/rocket-local-import/index.js`, `query.graphql` |
| Social Proof | Enrichment data (photos, bios, ratings, reviews) | Web scraping (Cheerio) | `apps/rocket-local-import/scrape.js` |
| Google Geocoding API | Lat/lng from zip codes | REST | `apps/rocket-local-import/index.js` (getLatLong) |
| Google Places API | Address autocomplete in search bar | @angular/google-maps | `apps/rocket-local-ui/src/app/components/search-bar/` |
| Google Maps API | Map display with banker markers | @angular/google-maps | `apps/rocket-local-ui/src/app/search/map/` |
| Rocket Mortgage API | Lead submission (not shown in code) | REST | `apps/rocket-local-api/src/lead/` module |

### Database

**Type:** OpenSearch 2.13.0 (AWS-managed, Elasticsearch fork)

**Access:** OpenSearch Client with AWS Sigv4 authentication (production), unauthenticated (local dev)

**Location:**
- API client: `apps/rocket-local-api/src/search/search.service.ts` (lines 19-41)
- Lambda client: `apps/rocket-local-import/index.js` (lines 46-58)

**Schema:** `apps/rocket-local-import/es-schema.json` - Geo-point mapping for address.location, keyword types for NMLS/city/state

**Key Operations:**
- Lambda: `indices.create()`, `index()` (upsert), `delete()`, `cat.indices()`
- API: `search()` with geo_bounding_box filter, `get()` by document ID

### Critical Dependencies

1. **@nestjs/core + @nestjs/platform-express** - Core NestJS framework powering the API layer with modular architecture, dependency injection, and middleware support
2. **@opensearch-project/opensearch** - OpenSearch client enabling geo-spatial search queries with AWS Sigv4 authentication for secure cluster access
3. **@angular/core + @angular/router** - Angular framework providing reactive UI with component-based architecture and client-side routing
4. **@angular/google-maps** - Google Maps integration for displaying banker locations and enabling map-based search interactions
5. **graphql-request** - GraphQL client for querying RHDS API with Auth0 authentication to fetch banker core data
6. **cheerio** - HTML parsing library for scraping Social Proof profiles to enrich banker data with photos/bios/reviews

## 7. Key Components Deep Dive

### Component 1: Lambda Import Orchestrator

**Path:** `apps/rocket-local-import/index.js`

**Purpose:** Daily batch job orchestrating the complete data pipeline from source systems (RHDS + Social Proof) through enrichment (geocoding) to OpenSearch bulk upload. Critical for keeping banker profiles current and ensuring data quality through filtering rules.

**Key functions:**
- `handler()` - AWS Lambda entry point (lines ~400+)
- `main()` - Core orchestration logic
- `fetchRHDSData()` - GraphQL query to RHDS with Auth0 token
- `getSocialProofURL()` - URL construction with SPECIAL_USERS override logic
- `updateElasticSearch()` - Upsert individual banker document
- `deleteFromElasticSearch()` - Remove inactive bankers
- `getLatLong()` - Google Geocoding API call for zip → lat/lng

**Patterns:**
- **Special Case Handling:** SPECIAL_USERS constant (lines 22-43) maps NMLS IDs to custom Social Proof URLs for non-standard name formats (e.g., "Joel-Rodgers" vs "JoelRodgers")
- **Graceful Degradation:** Social Proof failures don't block import; default Rocket logo and generic bio used
- **Token Caching:** ENV=LOCAL enables file-based token caching for local development
- **Set-Based Filtering:** Compares NMLS sets between RHDS and OpenSearch to identify inactive bankers for deletion

**Example:**
```javascript
// Special users with non-standard Social Proof URL formats
const SPECIAL_USERS = {
  '448483': 'https://social.pr/p/rocket-mortgage-franchise/Joel-Rodgers/',
  '1554069': 'https://social.pr/p/rocket-mortgage-franchise/AlexanderVulaj/',
  // ... 19 more entries
}

// Main import flow
async function main() {
  await ensureElasticSearchSchema();
  const rhdsData = await fetchRHDSData();
  for (const banker of rhdsData) {
    if (!banker.licenseData?.nmlsId) continue; // Skip if no NMLS
    const socialProofData = await scrapeSocialProof(banker);
    const geoCoords = await getLatLong(banker.address.zip);
    await updateElasticSearch({ ...banker, ...socialProofData, ...geoCoords }, banker.nmls);
  }
  await removeInactiveBankers();
}
```

### Component 2: OpenSearch Service (Repository Layer)

**Path:** `apps/rocket-local-api/src/search/search.service.ts`

**Purpose:** Repository pattern implementation abstracting OpenSearch operations with geo-spatial query capabilities. Centralizes data access logic, error handling, and AWS authentication for the API layer.

**Key methods:**
- `constructor()` - Initializes OpenSearch client with environment-specific auth (AWS Sigv4 for prod, unsecured for dev)
- `findBankersByLocation()` - Geo-bounded search with pagination and distance-based sorting
- `findBanker()` - Get single banker profile by NMLS ID

**Patterns:**
- **Environment-Specific Configuration:** Dev mode uses unsecured client, prod uses AWS Sigv4 Signer
- **Error Transformation:** Catches OpenSearch errors and throws HTTP exceptions with user-friendly messages
- **Pagination:** Fixed page size of 20 with offset calculation (from: page * pageSize - pageSize)
- **Geo-Spatial Queries:** geo_bounding_box filter + _geo_distance sort for location-based search

**Example:**
```typescript
public async findBankersByLocation(
  lat: number, lon: number,
  northLat: number, southLat: number,
  eastLng: number, westLng: number,
  page: number
) {
  const response = await this.openSearchClient.search({
    index: this.index,
    body: {
      from: page * this.pageSize - this.pageSize,
      query: {
        bool: {
          filter: [{
            geo_bounding_box: {
              'address.location': {
                bottom_right: { lat: southLat, lon: eastLng },
                top_left: { lat: northLat, lon: westLng }
              }
            }
          }],
          must: { match_all: {} }
        }
      },
      size: this.pageSize,
      sort: [{
        _geo_distance: {
          'address.location': { lat, lon },
          order: 'asc',
          unit: 'mi'
        }
      }]
    }
  });
  return response.body;
}
```

### Component 3: Search Component (UI Orchestrator)

**Path:** `apps/rocket-local-ui/src/app/search/search.component.ts`

**Purpose:** Angular component orchestrating the search experience with reactive state management, coordinating map display, result cards, pagination, and geolocation. Serves as the primary user entry point for finding loan officers.

**Key methods:**
- `ngOnInit()` - Subscribe to route query params and search results observable
- `onQueryParamsChangeEvent()` - Route parameter handler dispatching to appropriate search method
- `onGeolocationAttemptEvent()` - Browser geolocation API integration
- `onSearchTermChangeEvent()` - Address-based search with geocoding
- `setResults()` - Update UI state with search results, map data, pagination

**Patterns:**
- **Reactive State:** BehaviorSubject for map data, RxJS observables for search results
- **Router-Driven State:** Query params control search term and page (enables deep linking)
- **Progressive Enhancement:** Falls back from geolocation → address search → error display
- **Separation of Concerns:** SearchService handles API calls, component handles UI orchestration

**Example:**
```typescript
public ngOnInit(): void {
  this.showLoading = true;
  this.route.queryParams.subscribe((params) =>
    this.onQueryParamsChangeEvent(params)
  );
  const searchResults = this.searchService.searchResult$.subscribe(
    (results) => this.setResults(results)
  );
  this.subscriptions.push(searchResults);
}

private onQueryParamsChangeEvent(params: Params): void {
  if (params.page) {
    this.onPageChangeEvent(parseInt(params.page, 10), params.searchTerm);
  } else if (params.searchTerm) {
    this.onSearchTermChangeEvent(params.searchTerm, 1);
  } else if (navigator.geolocation) {
    this.onGeolocationAttemptEvent(1);
  } else {
    this.onErrorEvent();
  }
}
```

### Component 4: RHDS GraphQL Query

**Path:** `apps/rocket-local-import/query.graphql`

**Purpose:** GraphQL query definition that fetches franchise banker data from RHDS with precise filtering and field selection. The query enforces business rules at the data source level (status=active, Franchise_Banker skill) to minimize processing overhead.

**Key fields:**
- `teamMembers.licenseData.nmlsId` - Required unique identifier for banker profiles
- `teamMembers.teamMemberJobs.skills` - Filtered by code: "Franchise_Banker"
- `teamMembers.status` - Filtered by "a" (active)
- `phones` - Landline/Mobile with isPrivate: false filter
- `teamMemberAddresses` - Primary address with city/state/zip for geolocation

**Patterns:**
- **Server-Side Filtering:** Where clause at query level reduces payload and processing
- **Field-Level Selection:** Only requests needed fields (avoids over-fetching)
- **Nested Filtering:** where: { isPrimary: true }, where: { isPrivate: false }

**Example:**
```graphql
query {
  teamMembers(
    where: {
      status: "a"
      teamMemberJobs: { skills: { code: "Franchise_Banker" } }
    }
  ) {
    preferredFirstName
    preferredLastName
    licenseData { nmlsId }
    phones(where: { isPrivate: false }) {
      phoneNumber
      phoneDeviceType
    }
    teamMemberAddresses(where: { isPrimary: true }) {
      address { city, region, postalCode }
    }
    teamMemberJobs {
      email
      displayJobTitle
    }
  }
}
```

**Critical Filtering Rules** (Why bankers get excluded):
1. Must have `licenseData.nmlsId` (checked in import script with "Missing NMLS!!" log)
2. Must have `teamMemberJobs.skills.code = "Franchise_Banker"` (GraphQL where clause)
3. Must have `status = "a"` (active) (GraphQL where clause)

## 8. Configuration & Infrastructure

**Config Approach:**
- **Environment Variables:** .env files for local development (import), process.env for Lambda/NestJS
- **Terraform:** Infrastructure as Code with environment-specific tfvars files
- **NestJS Config Service:** Centralized config injection (`apps/rocket-local-api/src/global/config/config.service.ts`)
- **Angular Environments:** Build-time environment files (`apps/rocket-local-ui/src/environments/`)

**Config Location:**
- Lambda: `.env` file in `apps/rocket-local-import/` (gitignored, .env.example provided)
- API: Environment variables injected by HAL/EKS
- UI: `apps/rocket-local-ui/src/environments/environment.{prod,beta}.ts`
- Infrastructure: `iac/{account}/{region}/{env}/*/terraform.tfvars`

**Deployment:**
- **UI:** GitHub Actions → Build → Akamai NetStorage (static hosting)
- **API:** GitHub Actions → Docker build → ECR → HAL → AWS EKS
- **Import:** GitHub Actions → Webpack bundle → Zip → HAL → AWS Lambda

**Containers:**
- API uses Docker (`apps/rocket-local-api/Dockerfile`)
- Lambda uses zip deployment (Webpack bundle)
- UI is static files (no container)

### Key Environment Variables

| Variable | Purpose | Required | Location |
|----------|---------|----------|----------|
| ELASTIC_SEARCH_URL | OpenSearch cluster endpoint | Yes | Import, API |
| GOOGLE_API_KEY | Google Geocoding/Maps API key | Yes | Import, UI |
| RHDS_URL | RHDS GraphQL endpoint | Yes | Import |
| RHDS_CLIENT_ID | Auth0 client ID for RHDS | Yes | Import |
| RHDS_CLIENT_SECRET | Auth0 client secret | Yes | Import |
| RHDS_AUDIENCE | Auth0 audience for RHDS | Yes | Import |
| AUTH_TOKEN_URL | Auth0 token endpoint | Yes | Import |
| ENV | Environment name (dev/test/beta/prod) | Yes | All apps |
| PORT | API server port | No (default: 3333) | API |

**Secrets Management:** MyVault (links in README.md) - Google API key, RHDS credentials, RHDS audience

## 9. Quality Attributes

**Error Handling:**
- **Strategy:** Layered error handling with transformation at boundaries
- **API:** NestJS HttpException with status codes (404 for not found, 400 for validation)
- **Lambda:** Try-catch with console.log for CloudWatch, continues on Social Proof failures
- **UI:** Observable error handlers with user-friendly error display (showError flag)
- **Location:**
  - API: `search.service.ts` (lines 94-97, 117-123) - catches OpenSearch errors, throws HTTP exceptions
  - Lambda: `index.js` - scattered try-catch blocks with fallback logic
  - UI: `search.component.ts` - subscription error handlers

**Logging:**
- **Library:** Pino (nestjs-pino) for structured JSON logging
- **Approach:** Request-scoped loggers with trace IDs, log levels (debug/info/warn/error)
- **Location:**
  - API: `apps/rocket-local-api/src/global/logger/logger.service.ts`, `logger.middleware.ts`
  - Lambda: Console.log statements for CloudWatch Logs (searchable via Splunk)
- **Integration:** @rocklib/pino-log-transport for Rocket-specific log aggregation
- **Metrics:** @rocklib/metrics Express middleware for request metrics

**Security:**
- **Authentication:** AWS Sigv4 for OpenSearch (API + Lambda), Auth0 client credentials for RHDS (Lambda)
- **Authorization:** No user auth (public-facing UI), backend services secured via AWS IAM roles
- **Input Validation:** NestJS ValidationPipe with class-validator decorators on DTOs
- **CORS:** Enabled on API with origin: true (allows all origins for public API)
- **Secrets:** Stored in MyVault, injected via environment variables
- **Network Security:** API in EKS with security groups, Lambda in VPC (if configured)
- **Dependency Scanning:** Snyk security checks in CI/CD pipelines (.snyk policy file)

**Testing:**
- **Unit Tests:**
  - API: Jest (`apps/rocket-local-api/src/**/*.spec.ts`) - 100% test file coverage requirement
  - UI: Karma/Jasmine (`apps/rocket-local-ui/src/**/*.spec.ts`) - ChromeHeadlessCI for CI
  - Import: No unit tests (echo "No unit tests" in package.json)
- **E2E Tests:** Cypress (`apps/rocket-local-ui/cypress/`) - dev and beta configurations
- **Browser Compatibility:** SauceLabs for cross-browser testing (Chrome, Edge, Firefox, Safari)
- **Load Testing:** Separate workflow (`ui-load-test.yml`) for performance validation
- **Coverage:** API requires coverage reports, UI runs with --code-coverage flag
- **Location:**
  - Unit tests: Co-located with source files (*.spec.ts)
  - E2E tests: `apps/rocket-local-ui/cypress/integration/`
  - Test commands: `npm run test:ui:cov`, `npm run test:api:cov`, `npm run e2e:dev`

## 10. Architectural Decisions & Trade-offs

### Decision 1: OpenSearch Over Relational Database

**Choice:** OpenSearch (Elasticsearch fork) as primary datastore

**Alternatives:**
- PostgreSQL with PostGIS extension for geo-spatial queries
- DynamoDB with GSI for querying
- MySQL with spatial indexing

**Rationale:**
- Optimized for geo-spatial search with native geo_point and geo_bounding_box queries
- Full-text search capabilities for future name/bio searching
- Horizontal scalability for read-heavy workload
- Document model aligns with denormalized banker profiles (no joins needed)
- AWS-managed service reduces operational overhead

**Trade-offs:**
- **Gains:** Sub-second geo-spatial queries, no complex joins, schema flexibility, built-in pagination
- **Losses:** No ACID transactions (acceptable for read-heavy workload), eventual consistency, higher cost than RDS, requires separate backup strategy, no foreign key constraints (data integrity enforced in import layer)

### Decision 2: Daily Batch Import vs Real-Time Sync

**Choice:** Scheduled daily batch import (7-8 AM ET) via AWS Lambda triggered by EventBridge cron

**Alternatives:**
- Real-time CDC (Change Data Capture) from RHDS with streaming updates
- Hourly batch imports for fresher data
- On-demand import triggered by RHDS webhooks
- API-level caching with periodic refresh

**Rationale:**
- Banker profile data changes infrequently (contact info, ratings update rarely)
- Social Proof requires web scraping (no API), making real-time impractical
- Batch processing simplifies error handling and retry logic
- Decouples data ingestion from user-facing performance
- Reduces load on upstream systems (RHDS, Social Proof, Google Geocoding API)
- Morning sync ensures fresh data for business day

**Trade-offs:**
- **Gains:** Simplified architecture, predictable load patterns, resilient to upstream failures, lower API costs (Google Geocoding), reduced RHDS query volume
- **Losses:** Up to 24-hour staleness for profile updates (acceptable per business requirements), urgent updates require manual Lambda trigger, increased complexity for debugging import issues (must check Lambda logs)

### Decision 3: Monorepo with NX vs Multi-Repo

**Choice:** NX monorepo with three applications (import, api, ui) in single repository

**Alternatives:**
- Separate repositories for each application
- Polyrepo with shared libraries published to npm
- Monolith single-application combining all layers

**Rationale:**
- Shared configuration (TypeScript, ESLint, build tools) across applications
- Atomic commits affecting multiple layers (e.g., OpenSearch schema change requires import + API updates)
- Simplified dependency management (single package.json)
- NX caching speeds up CI/CD builds (only rebuilds changed apps)
- Easier local development (single git clone, npm install)
- Clear bounded contexts with apps/ directory structure

**Trade-offs:**
- **Gains:** Reduced configuration duplication, faster iteration on cross-layer changes, single source of truth, NX task orchestration, easier onboarding
- **Losses:** Larger repository size, potential for unintended coupling between apps, CI/CD path filters required to avoid rebuilding unchanged apps, requires NX knowledge for developers

**Scalability:** NX supports large monorepos (100+ apps), current size (~10K LOC) is well within limits

**Performance:** NX computation caching reduces build times by 50-70% for incremental changes

## 11. Extension Points

**Plugin System:** No formal plugin architecture; extensibility through:
- **NX Generators:** Can create custom workspace generators for new apps/components
- **NestJS Modules:** API extensible via new modules imported into AppModule
- **Angular Components:** UI extensible via new standalone components

**Adding Features:**

1. **New Search Filters (e.g., filter by language spoken):**
   - Update OpenSearch schema: Add `languages` field to `es-schema.json`
   - Update Lambda import: Extract language data from RHDS or Social Proof, add to document
   - Update API: Add query parameter to `SearchController`, modify `SearchService` to add bool filter
   - Update UI: Add filter dropdown to search bar component, pass parameter to API

2. **Additional Data Source (e.g., integrate LinkedIn profiles):**
   - Create new scraper module in Lambda: `scrape-linkedin.js`
   - Add LinkedIn profile URL field to OpenSearch schema
   - Update import orchestration to fetch LinkedIn data after Social Proof
   - Update API mapper to include LinkedIn URL in profile DTO
   - Update UI profile component to display LinkedIn link

3. **Real-Time Chat with Bankers:**
   - Add WebSocket module to API: New NestJS WebSocketGateway
   - Create chat component in UI: Angular component with Socket.io client
   - Store chat history in separate datastore (DynamoDB or RDS)
   - Update profile page to embed chat widget

4. **Admin Panel for Managing SPECIAL_USERS:**
   - Create new Angular app in monorepo: `apps/rocket-local-admin/`
   - Build CRUD API in NestJS for SPECIAL_USERS configuration
   - Store SPECIAL_USERS in DynamoDB instead of hardcoded constant
   - Update Lambda to fetch SPECIAL_USERS from DynamoDB at runtime

**Customization Points:**

- **Search Algorithm:** Modify `SearchService.findBankersByLocation()` to adjust sorting (e.g., rating-weighted distance)
- **Profile Layout:** UI component structure is modular; swap bio-hero, testimonials with custom components
- **Data Enrichment:** Add new scraping functions to `scrape.js` for additional Social Proof data
- **OpenSearch Mapping:** Extend `es-schema.json` with new fields, analyzers, or index settings
- **Authentication:** Add authentication guards to API controllers, integrate with Rocket SSO
- **Rate Limiting:** Add NestJS throttler module to API for request rate limiting
- **Caching:** Add Redis caching layer between API and OpenSearch for hot profiles

## 12. Technical Debt & Improvements

### Technical Debt

1. **Hardcoded SPECIAL_USERS Map** - Location: `apps/rocket-local-import/index.js` (lines 22-43) | Impact: High | Fix: Migrate to DynamoDB table with admin UI for managing URL overrides. Reduces deployment friction for adding new special cases and enables non-technical users to update mappings.

2. **No Unit Tests for Lambda Import** - Location: `apps/rocket-local-import/` | Impact: Medium | Fix: Add Jest test suite with mocked OpenSearch, RHDS, and Social Proof clients. Increases confidence in import logic changes and prevents regressions during refactors.

3. **Mixed Imperative JavaScript in Lambda** - Location: `apps/rocket-local-import/index.js` | Impact: Medium | Fix: Refactor to TypeScript with class-based architecture matching API pattern. Improves type safety, maintainability, and enables code reuse with API OpenSearch client.

4. **Inadequate Error Handling in Lambda** - Location: `apps/rocket-local-import/index.js` | Impact: Medium | Fix: Implement structured error reporting with categorization (RHDS failure, Social Proof failure, OpenSearch failure) and alerting. Currently relies on manual Splunk log analysis to detect import issues.

5. **No API Response Caching** - Location: `apps/rocket-local-api/src/search/` | Impact: Low | Fix: Add Redis cache layer for popular searches and profiles with 1-hour TTL. Reduces OpenSearch load and improves response times for hot queries.

6. **CORS Allows All Origins** - Location: `apps/rocket-local-api/src/main.ts` (line 22) | Impact: Low | Fix: Restrict CORS origin to production domains (rocketmortgage.com, np.rocketmortgage.com). Current configuration allows any origin, increasing CSRF risk.

### Refactoring Opportunities

1. **OpenSearch Client Duplication** - Current: Separate OpenSearch client initialization in API and Lambda with duplicated auth logic | Improvement: Extract to shared library package (@rocket-local/opensearch-client) with reusable configuration | Benefit: Reduces code duplication, ensures consistent connection pooling and error handling, enables easier upgrade to new OpenSearch client versions

2. **Social Proof Scraping Brittleness** - Current: Web scraping relies on HTML structure remaining stable; breaks silently with fallback to defaults | Improvement: Implement monitoring alerts when scraping failures exceed threshold (e.g., >10% failure rate), add comprehensive integration tests with VCR-style HTTP replay | Benefit: Early detection of Social Proof website changes, faster response to data quality degradation

3. **Search Component Complexity** - Current: SearchComponent handles routing, state management, geolocation, and UI orchestration (~200 lines) | Improvement: Extract geolocation service, state management to NgRx store, separate search orchestration from presentation | Benefit: Improved testability, reusable geolocation logic, clearer separation of concerns

4. **Lack of API Versioning** - Current: Single unversioned API endpoint structure (/search, /search/:id) | Improvement: Implement versioned routes (/v1/search) with OpenAPI 3.0 specification, use @nestjs/swagger decorators for auto-generated docs | Benefit: Enables backward-compatible API changes, supports mobile app integration in future, clearer API contract documentation

### Evolution Suggestions

1. **GraphQL Federation Gateway** - Limitation: UI directly queries BFF REST API; future microservices would require multiple API calls | Approach: Introduce Apollo Federation Gateway aggregating Rocket Local API + future services (e.g., mortgage rates, document upload) into unified GraphQL schema | Effort: Large (4-6 weeks) - Requires schema design, resolver implementation, client migration, testing

2. **Real-Time Profile Updates via WebSockets** - Limitation: Profile changes require 24-hour wait for batch import to reflect | Approach: Implement NestJS WebSocket gateway with Redis pub/sub for profile change events, emit to connected clients when banker updates Social Proof profile | Effort: Medium (2-3 weeks) - Requires WebSocket infrastructure, state synchronization, fallback for offline clients

3. **Advanced Search Filters** - Limitation: Only geo-spatial search supported; no filtering by specialty, language, rating, or review count | Approach: Extend OpenSearch mapping with faceted fields, add filter UI components (multi-select dropdowns, sliders), implement bool query with filters in SearchService | Effort: Medium (3-4 weeks) - Requires schema migration, Lambda import updates, API changes, UI components

4. **A/B Testing Framework** - Limitation: No capability to experiment with UI layouts, search algorithms, or profile page variations | Approach: Integrate Split.io feature flags (already in package.json but not used), instrument UI components with treatment tracking, add analytics events for conversion funnel | Effort: Small (1-2 weeks) - SDK already available, requires analytics integration and feature flag configuration

5. **Mobile Application** - Limitation: Only web UI supported; no native mobile experience | Approach: Build React Native mobile app consuming same Rocket Local API, add push notifications for new bankers in saved locations, implement offline caching of profiles | Effort: Large (8-12 weeks) - Requires mobile development expertise, app store deployment, API enhancements for mobile-specific features

## 13. Quick Reference

**Entry Points:**
- UI Production: https://www.rocketmortgage.com/local-loan-officers
- UI Beta: https://www.np.rocketmortgage.com/local-loan-officers
- API: Health check at /health endpoint (EKS load balancer)
- Lambda: Triggered by EventBridge cron (arn:aws:lambda:us-east-2:475709878609:function:prod-213530-rocket-local-import)

**Config Files:**
- NX Workspace: `nx.json`, `tsconfig.base.json`
- API: `apps/rocket-local-api/src/global/config/config.service.ts`, `.env` (local)
- UI: `apps/rocket-local-ui/src/environments/environment.{prod,beta}.ts`
- Import: `apps/rocket-local-import/.env` (local), HAL environment variables (prod)
- Infrastructure: `iac/{account}/{region}/{env}/*/terraform.tfvars`

**Dev Commands:**

```bash
# Install dependencies
npm i

# Run UI (opens browser)
npm run start:ui

# Run API (requires OpenSearch Docker container)
docker run -it -p 9200:9200 -p 9600:9600 -e DISABLE_SECURITY_PLUGIN=true -e "discovery.type=single-node" --name opensearch-node opensearchproject/opensearch:2.13.0
cd apps/rocket-local-api && ./hydrate-test-data.sh
npm run start:api:dev

# Run Import (requires .env configuration)
npm run start:import:local

# Test
npm run test:ui:cov      # UI unit tests with coverage
npm run test:api:cov     # API unit tests with coverage
npm run e2e:dev          # Cypress E2E tests

# Lint
npm run lint             # Lint all projects

# Build
npm run build:ui:prod    # UI production build
npm run build:api        # API build
npm run build:import     # Lambda webpack bundle
```

## 14. Summary

### Strengths

1. **Clear Separation of Concerns** - Three-tier architecture with distinct responsibilities (import, API, UI) enables independent scaling, testing, and deployment. Each application has a single purpose and minimal coupling.

2. **Optimized for Read Performance** - Daily batch import with OpenSearch enables sub-second geo-spatial queries on 10,000+ banker profiles. Decoupling data ingestion from query performance ensures consistent user experience regardless of upstream system health.

3. **Comprehensive Documentation** - Exceptional documentation with README.md, ROCKET_LOCAL_OVERVIEW.md, and CLAUDE.md covering architecture, debugging, data flow, and component structure. Includes Splunk query templates, troubleshooting scenarios, and detailed glossary.

4. **Mature CI/CD Pipeline** - Automated deployments with GitHub Actions, path-based filters, quality gates (SonarQube, Snyk), and environment-specific workflows. HAL integration provides controlled rollouts across test/beta/prod.

5. **Resilient Data Pipeline** - Graceful degradation when Social Proof scraping fails (fallback to defaults), continues import on individual banker failures, removes inactive bankers automatically. SPECIAL_USERS map handles edge cases without blocking deployments.

### Improvements

1. **Testing Coverage Gaps** - Lambda import has no unit tests, E2E tests only cover happy path, no integration tests for Social Proof scraping. Add Jest test suite for import with mocked dependencies, expand Cypress coverage to error scenarios, implement VCR-style Social Proof scraping tests.

2. **Operational Observability** - Limited monitoring beyond Splunk logs and Dynatrace APM. No alerting for import failures, Social Proof scraping degradation, or OpenSearch performance issues. Implement CloudWatch alarms for Lambda failures, track scraping success rate as custom metric, add API error rate dashboards.

3. **Data Quality Validation** - No automated validation that imported data meets quality standards (e.g., all bankers have photos, valid phone numbers, non-empty bios). Add data quality metrics to Lambda output, alert when quality thresholds breached (e.g., >20% using default photo).

### Next Steps

1. **High Priority** - Add Lambda import unit tests and operational monitoring. Current lack of tests creates risk during refactors, and manual Splunk analysis is inefficient for detecting issues.

2. **Medium Priority** - Migrate SPECIAL_USERS map to database-backed configuration with admin UI. This unblocks non-technical users from managing URL overrides and reduces deployment friction.

3. **Low Priority** - Implement API response caching with Redis for popular searches and profiles. Current OpenSearch query performance is acceptable, but caching would reduce costs and improve scalability as usage grows.

---

**Notes:**
- The monorepo structure with NX provides excellent developer experience with caching and task orchestration
- Social Proof web scraping is a technical debt risk; consider working with Social Proof team to provide API access
- The daily batch import schedule (7-8 AM ET) is well-suited to current business needs but may require adjustment if real-time updates become critical
- OpenSearch geo-spatial capabilities are underutilized; advanced filtering (language, rating, review count) would enhance user experience
- Existing infrastructure (EventBridge, Lambda, OpenSearch, EKS) provides solid foundation for future features (real-time updates, mobile app, advanced search)

# CLIDE Architecture Visualizations (v0.6.0)

## 1. System Architecture (Component Map)
This diagram illustrates the separation of concerns between the Observer (Monitor), the Forge (Synthesis), and the State Layer.

```mermaid
graph TD
    User(("User"))
    Monitor["CLIDE Monitor"]
    Forge["Asset Forge"]
    AG["agents.md"]
    VR["Vector Registry"]
    StateMCP["State Management MCP"]
    DB[("core/state.db")]

    User --> Monitor
    Monitor --> Forge
    Forge --> AG
    Forge --> VR
    Monitor --> VR

    subgraph Core ["Core Constitution"]
        AG
    end

    subgraph Assets ["The Asset Forge"]
        Forge
    end

    subgraph State ["State Layer (Project Atlas)"]
        StateMCP
        DB
    end

    StateMCP --- DB
    Forge -.-> StateMCP
```

## 2. Data Flow: From Intent to Artifact
This diagram shows the lifecycle of a user request—from raw text to a saved, hotswapped tool.

```mermaid
sequenceDiagram
    participant U as User
    participant M as Monitor
    participant C as Classifier
    participant F as Forge
    participant DB as Vector Registry
    participant S as Shell

    U->>M: Request Tool
    M->>C: Analyze Intent
    C-->>M: Category: NEW_COMMAND
    M->>F: Request Asset (MCP)
    F->>F: Read agents.md
    F->>F: Synthesize Code
    F->>F: Dry Run and Repair
    F->>DB: Register Asset
    F->>S: Hotswap
    S-->>U: Tool Ready
```

## 3. Database Schema (Project Atlas)
The internal structure of `core/state.db`, managed by the `state_manager` MCP.

```mermaid
erDiagram
    ENTITIES ||--o{ ARTIFACTS : has
    ENTITIES ||--o{ TASKS : contains
    
    ENTITIES {
        int id PK
        string type
        string name
        string status
        int risk_score
        datetime created_at
    }

    ARTIFACTS {
        int id PK
        int entity_id FK
        string type
        string content
        boolean is_approved
    }

    TASKS {
        int id PK
        int entity_id FK
        string description
        string track
        string status
        int weight
    }
```

## 4. ASCII Architecture (Text-Only Fallback)

### A. System Map
[ User ]
   | (Shell / Chat)
   v
[ CLIDE Monitor ]  <-- (Analyzes Intent)
   |
   +--> [ Asset Forge ]
   |       |
   |       +--> (Reads) --> [ Core: agents.md ]
   |       +--> (Synthesizes) --> [ Assets: TOML / MCP ]
   |
   +--> [ Registry ] (Search / Discovery)

[ State Layer ]
   |
   +--> [ State Management MCP ] <--> [ core/state.db (SQLite) ]
           ^            ^
           |            |
      (Tool Call)  (Tool Call)
           |            |
      [ Dev Agent ] [ Bug Agent ]

### B. Data Flow
1. User: "Create a scanner"
2. Monitor: "Intent = NEW_COMMAND"
3. Forge: Synthesizes Code + Constitution
4. Forge: Saves to 'commands/' & Registers
5. Shell: Hotswaps new command
6. User: "Run scanner" -> IT WORKS.

### C. Database Schema
[ ENTITIES ]
+ id (PK)
+ type (FEATURE/BUG)
+ name
+ risk_score
+ status
      |
      +---< [ ARTIFACTS ]
      |     + id
      |     + type (RSD/STORY)
      |     + content
      |     + is_approved
      |
      +---< [ TASKS ]
            + id
            + description
            + track (CODE/DOCS)
            + status

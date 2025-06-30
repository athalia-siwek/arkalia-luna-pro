---
title: "Arkalia-LUNA Security Architecture"
description: "Diagramme complet architecture sécurité et flux entre modules IA"
---

# 🏗️ Architecture Sécurité Arkalia-LUNA

## 🔒 Vue d'Ensemble Sécurité Multi-Couches

```mermaid
graph TB
    subgraph "🌐 Couche Externe"
        Internet[Internet]
        User[Utilisateur]
        Admin[Administrateur]
    end

    subgraph "🛡️ Couche Protection Périmètre"
        Firewall[Firewall/iptables]
        Fail2Ban[Fail2Ban]
        RateLimit[Rate Limiting]
        TLS[TLS 1.3]
    end

    subgraph "🐳 Couche Container Security"
        DockerHost[Docker Host]
        SecComp[SecComp Profile]
        AppArmor[AppArmor]
        Capabilities[Cap Drop ALL]
    end

    subgraph "🧠 Couche IA Cognitive"
        PromptValidator[Prompt Validator]
        SandozIA[SandozIA Monitor]
        AntiInjection[Anti-Injection]
    end

    subgraph "💾 Couche Données"
        AtomicIO[Atomic I/O]
        Encryption[Encryption]
        Backup[Backup Chiffré]
        StateValidation[State Validation]
    end

    Internet --> Firewall
    User --> Firewall
    Admin --> Firewall

    Firewall --> Fail2Ban
    Fail2Ban --> RateLimit
    RateLimit --> TLS

    TLS --> DockerHost
    DockerHost --> SecComp
    SecComp --> AppArmor
    AppArmor --> Capabilities

    Capabilities --> PromptValidator
    PromptValidator --> SandozIA
    SandozIA --> AntiInjection

    AntiInjection --> AtomicIO
    AtomicIO --> Encryption
    Encryption --> Backup
    Backup --> StateValidation

    style Internet fill:#ff9999
    style Firewall fill:#99ccff
    style DockerHost fill:#99ff99
    style PromptValidator fill:#ffcc99
    style AtomicIO fill:#cc99ff
```

## 🚀 Flux Modules IA et États

```mermaid
graph TD
    subgraph "🔄 Orchestrateur Principal"
        MainLoop[Main Loop]
        ErrorHandler[Error Handler]
        StateManager[State Manager]
    end

    subgraph "🧠 Modules IA Core"
        Reflexia[Reflexia<br/>Monitoring]
        ZeroIA[ZeroIA<br/>Decision Engine]
        AssistantIA[AssistantIA<br/>LLM Interface]
    end

    subgraph "🌐 Services Support"
        Helloria[Helloria<br/>FastAPI Server]
        Nyxalia[Nyxalia<br/>Mobile Interface]
        Taskia[Taskia<br/>Task Manager]
    end

    subgraph "💾 États Persistants"
        ReflexiaState[(reflexia_state.toml)]
        ZeroiaState[(zeroia_state.toml)]
        GlobalState[(global_context.toml)]
        Dashboard[(zeroia_dashboard.json)]
    end

    subgraph "🔍 Monitoring & Logs"
        PrometheusMetrics[Prometheus Metrics]
        SecurityLogs[Security Logs]
        AuditTrail[Audit Trail]
    end

    MainLoop --> Reflexia
    MainLoop --> ZeroIA
    MainLoop --> AssistantIA

    Reflexia --> ReflexiaState
    Reflexia --> PrometheusMetrics
    ReflexiaState --> ZeroIA

    ZeroIA --> ZeroiaState
    ZeroIA --> Dashboard
    ZeroIA --> GlobalState

    AssistantIA --> SecurityLogs
    AssistantIA --> AuditTrail

    Helloria --> AssistantIA
    Nyxalia --> Helloria
    Taskia --> StateManager

    StateManager --> ReflexiaState
    StateManager --> ZeroiaState
    StateManager --> GlobalState

    ErrorHandler --> SecurityLogs
    ErrorHandler --> AuditTrail

    style MainLoop fill:#ff6b6b
    style Reflexia fill:#4ecdc4
    style ZeroIA fill:#45b7d1
    style AssistantIA fill:#96ceb4
    style PrometheusMetrics fill:#feca57
    style SecurityLogs fill:#ff9ff3
```

## 🔐 Flux Sécurité et Validation

```mermaid
sequenceDiagram
    participant User as 👤 Utilisateur
    participant API as 🌐 API Gateway
    participant Validator as 🔍 Prompt Validator
    participant Assistant as 🧠 AssistantIA
    participant Monitor as 👁️ SandozIA Monitor
    participant Logger as 📝 Security Logger
    participant Response as 📤 Response Handler

    User->>API: Prompt Request
    API->>Validator: Validate Input

    alt Prompt Malicious
        Validator->>Logger: Log Security Event
        Validator->>User: Block + Warning
    else Prompt Safe
        Validator->>Assistant: Process Prompt
        Assistant->>Monitor: Cognitive Analysis

        alt Anomaly Detected
            Monitor->>Logger: Log Anomaly
            Monitor->>Assistant: Intervention
        else Normal Processing
            Assistant->>Response: Generate Response
            Response->>Logger: Log Interaction
            Response->>User: Send Response
        end
    end

    Logger->>Logger: Audit Trail Update
```

## 🏗️ Architecture Containers et Réseaux

```mermaid
graph TB
    subgraph "🖥️ Host System"
        HostOS[Host OS]
        DockerDaemon[Docker Daemon]
        HostNetwork[Host Network]
    end

    subgraph "🐳 Docker Network"
        ArkaliaNetwork[arkalia-network<br/>bridge]
        PrometheusNetwork[monitoring<br/>internal]
    end

    subgraph "📦 Core Containers"
        APIContainer[arkalia-api (port 8000)<br/>:8000]
        ReflexiaContainer[reflexia<br/>internal]
        ZeroiaContainer[zeroia<br/>internal]
    end

    subgraph "🧠 AI Containers"
        AssistantiaContainer[assistantia<br/>internal]
        OllamaContainer[ollama<br/>:11434]
    end

    subgraph "📊 Monitoring Stack"
        PrometheusContainer[prometheus<br/>:9090]
        MetricsContainer[arkalia-metrics<br/>:8001]
    end

    subgraph "💾 Data Volumes"
        StateVolume[States Volume<br/>RW]
        LogsVolume[Logs Volume<br/>RW]
        ModelsVolume[Models Volume<br/>RO]
        BackupVolume[Backup Volume<br/>encrypted]
    end

    HostOS --> DockerDaemon
    DockerDaemon --> ArkaliaNetwork
    DockerDaemon --> PrometheusNetwork

    ArkaliaNetwork --> APIContainer
    ArkaliaNetwork --> ReflexiaContainer
    ArkaliaNetwork --> ZeroiaContainer
    ArkaliaNetwork --> AssistantiaContainer
    ArkaliaNetwork --> OllamaContainer

    PrometheusNetwork --> PrometheusContainer
    PrometheusNetwork --> MetricsContainer

    APIContainer --> StateVolume
    ReflexiaContainer --> StateVolume
    ZeroiaContainer --> StateVolume

    APIContainer --> LogsVolume
    AssistantiaContainer --> LogsVolume

    OllamaContainer --> ModelsVolume

    StateVolume --> BackupVolume
    LogsVolume --> BackupVolume

    HostNetwork --> APIContainer

    style HostOS fill:#333,color:#fff
    style ArkaliaNetwork fill:#4ecdc4
    style APIContainer fill:#ff6b6b
    style StateVolume fill:#feca57
    style BackupVolume fill:#ff9ff3
```

## 🔄 États et Transitions Sécurité

```mermaid
stateDiagram-v2
    [*] --> SystemInit

    state SystemInit {
        [*] --> SecurityCheck
        SecurityCheck --> ConfigValidation
        ConfigValidation --> DockerSecurity
        DockerSecurity --> ModuleInit
        ModuleInit --> [*]
    }

    SystemInit --> NormalOperation

    state NormalOperation {
        [*] --> Monitoring
        Monitoring --> RequestProcessing
        RequestProcessing --> StateUpdate
        StateUpdate --> Monitoring

        state RequestProcessing {
            [*] --> InputValidation
            InputValidation --> PromptSecurity
            PromptSecurity --> AIProcessing
            AIProcessing --> ResponseGeneration
            ResponseGeneration --> [*]
        }
    }

    NormalOperation --> SecurityIncident : Threat Detected

    state SecurityIncident {
        [*] --> ThreatAnalysis
        ThreatAnalysis --> ContainmentMode
        ContainmentMode --> IncidentResponse
        IncidentResponse --> Recovery
        Recovery --> [*]
    }

    SecurityIncident --> NormalOperation : Threat Resolved
    SecurityIncident --> EmergencyShutdown : Critical Threat

    state EmergencyShutdown {
        [*] --> ServiceStop
        ServiceStop --> StateBackup
        StateBackup --> SystemLockdown
        SystemLockdown --> [*]
    }

    EmergencyShutdown --> SystemInit : Manual Recovery

    NormalOperation --> Maintenance : Scheduled
    Maintenance --> NormalOperation : Complete

    note right of SecurityIncident
        Triggers:
        - Prompt Injection
        - Container Escape
        - State Corruption
        - Anomalous Behavior
    end note
```

## 🧠 Flux Cognitif IA et Décisions

```mermaid
graph LR
    subgraph "📥 Input Layer"
        UserPrompt[User Prompt]
        SystemEvent[System Event]
        MetricData[Metric Data]
    end

    subgraph "🔍 Security Layer"
        PromptFilter[Prompt Filter]
        ThreatDetection[Threat Detection]
        InputValidation[Input Validation]
    end

    subgraph "🧠 Cognitive Layer"
        ContextBuilder[Context Builder]
        DecisionEngine[Decision Engine]
        ResponseGenerator[Response Generator]
    end

    subgraph "⚡ Reflexive Layer"
        PerformanceMonitor[Performance Monitor]
        AnomalyDetector[Anomaly Detector]
        AdaptiveControl[Adaptive Control]
    end

    subgraph "💾 Persistence Layer"
        StateWriter[State Writer]
        LogWriter[Log Writer]
        MetricsCollector[Metrics Collector]
    end

    subgraph "📤 Output Layer"
        UserResponse[User Response]
        SystemAction[System Action]
        AlertGeneration[Alert Generation]
    end

    UserPrompt --> PromptFilter
    SystemEvent --> ThreatDetection
    MetricData --> InputValidation

    PromptFilter --> ContextBuilder
    ThreatDetection --> ContextBuilder
    InputValidation --> ContextBuilder

    ContextBuilder --> DecisionEngine
    DecisionEngine --> ResponseGenerator

    DecisionEngine --> PerformanceMonitor
    PerformanceMonitor --> AnomalyDetector
    AnomalyDetector --> AdaptiveControl

    ResponseGenerator --> StateWriter
    AdaptiveControl --> LogWriter
    PerformanceMonitor --> MetricsCollector

    StateWriter --> UserResponse
    LogWriter --> SystemAction
    MetricsCollector --> AlertGeneration

    style UserPrompt fill:#96ceb4
    style PromptFilter fill:#ff6b6b
    style DecisionEngine fill:#45b7d1
    style AnomalyDetector fill:#feca57
    style StateWriter fill:#ff9ff3
```

## 📊 Monitoring et Métriques Sécurité

```mermaid
graph TB
    subgraph "📈 Data Sources"
        ContainerMetrics[Container Metrics]
        ApplicationLogs[Application Logs]
        SecurityEvents[Security Events]
        PerformanceData[Performance Data]
    end

    subgraph "🔄 Collection Layer"
        PrometheusAgent[Prometheus Agent]
        LogCollector[Log Collector]
        MetricsExporter[Metrics Exporter]
    end

    subgraph "💾 Storage Layer"
        PrometheusDB[Prometheus TSDB]
        LogStorage[Log Storage]
        StateBackup[State Backup]
    end

    subgraph "🧠 Analysis Layer"
        MetricsAnalyzer[Metrics Analyzer]
        LogAnalyzer[Log Analyzer]
        ThreatIntel[Threat Intelligence]
    end

    subgraph "🚨 Alert Layer"
        AlertManager[Alert Manager]
        NotificationEngine[Notification Engine]
        EscalationLogic[Escalation Logic]
    end

    subgraph "📊 Visualization"
        GrafanaDashboard[Grafana Dashboard]
        SecurityDashboard[Security Dashboard]
        ComplianceReports[Compliance Reports]
    end

    ContainerMetrics --> PrometheusAgent
    ApplicationLogs --> LogCollector
    SecurityEvents --> MetricsExporter
    PerformanceData --> PrometheusAgent

    PrometheusAgent --> PrometheusDB
    LogCollector --> LogStorage
    MetricsExporter --> PrometheusDB

    PrometheusDB --> MetricsAnalyzer
    LogStorage --> LogAnalyzer
    SecurityEvents --> ThreatIntel

    MetricsAnalyzer --> AlertManager
    LogAnalyzer --> AlertManager
    ThreatIntel --> AlertManager

    AlertManager --> NotificationEngine
    NotificationEngine --> EscalationLogic

    PrometheusDB --> GrafanaDashboard
    LogStorage --> SecurityDashboard
    MetricsAnalyzer --> ComplianceReports

    style SecurityEvents fill:#ff6b6b
    style ThreatIntel fill:#ff9ff3
    style AlertManager fill:#feca57
    style SecurityDashboard fill:#4ecdc4
```

---

*Diagrammes maintenus par Arkalia-LUNA Architecture Team — Version sécurité renforcée*
*🏗️ "Architecture défensive, sécurité par conception" — Arkalia Security Design*

sequenceDiagram
    participant Z as ZeroIA
    participant S as Sandozia
    participant C as CognitiveReactor
    participant V as CrossValidator
    participant R as Reflexia
    participant E as ErrorRecovery
    participant T as Chronalia
    participant M as Monitoring

    Note over Z,M: Cycle de décision standard
    Z->>S: Détection pattern
    S->>C: Analyse pattern
    C->>V: Demande validation
    V->>R: Vérification cohérence
    R-->>E: Si erreur détectée
    E-->>Z: Recovery si nécessaire

    par Flux parallèles
        Z->>M: Métriques décision
    and
        S->>M: Métriques pattern
    and
        R->>M: Métriques système
    end

    T->>M: Archivage timeline

    Note over Z,M: Boucle cognitive complète

# Module 2 Assignment: Data Analytics in Industry

## Prompt

Data analytics has transformed many industries by enabling better decision-making, optimizing processes, and uncovering new insights. From predicting consumer behavior in retail to improving patient outcomes in healthcare, the applications of data analytics are vast and varied.

Think of an industry or field you are interested in (e.g., healthcare, finance, education, sports, etc.). How has data analytics been applied in that industry to solve real-world problems or improve outcomes? Provide specific examples of how data analytics has added value or could add value in the future. What challenges do you think organizations face when implementing these data analytics solutions, and how might they overcome them?

---

## Response: AI Infrastructure Scaling Through Data Analytics & AI

### Overview

Growing AI and LLM adoption is creating unprecedented demand for compute infrastructure. New data center construction remains necessary for long-term growth — but it is expensive, slow, and increasingly constrained by community opposition ($64B in US projects blocked or delayed, 2024–25) and environmental regulation. The immediate opportunity is to use data analytics and AI to maximize utilization of existing on-premises, private cloud, and public cloud resources — reducing the scale and frequency of new builds required, lowering costs, and minimizing environmental impact.

### Situation & Task

AI and LLM adoption is driving 7–8× more compute demand per workload (MIT, 2025), with global data center energy consumption projected to grow from 415 TWh (2024) to 650–1,050 TWh by 2026 (IEA). New data center builds face growing opposition — $64B in US projects were blocked or delayed in 2024–25 (Data Center Watch). The opportunity is to use data analytics and AI to maximize utilization of existing on-premises, private cloud, and public cloud infrastructure — reducing the scale and frequency of new builds required, cutting costs, and minimizing environmental impact.

---

## 1. How Data Analytics and AI Amplifies Existing Capacity

| Domain | Analytics Used Today | How AI Reduces Need for New Infrastructure |
|---|---|---|
| **Capacity Planning** | Historical trends & manual quarterly reviews; over-provisioning is common to avoid shortfalls | ML demand forecasting enables just-in-time procurement. Software optimizations improve utilization compounding to potentially significant infrastructure savings. |
| **GPU & Resource Utilization** | Dashboards track CPU/GPU idle time. GPU inference averages 40–50% utilization; non-AI racks were 15% underutilized in 2024 (IDC) | AIOps auto-consolidates workloads and packs jobs intelligently, pushing GPU cluster efficiency — extracting more AI output from existing hardware before new GPUs are needed. |
| **Workload Scheduling & FinOps** | Rule-based schedulers and monthly bill reviews. eBay's GPU chargeback cut demand up to 25% through cost visibility alone. | AI schedulers shift batch LLM training to off-peak windows and auto-use spot instances. Mature AI FinOps programs deliver cost efficiency gains — making existing capacity go further. |
| **Power & Cooling** | Static PUE dashboards; reactive cooling adjustments. Industry PUE averages 1.5–1.6 — up to 50% extra energy beyond IT load. | AI-driven cooling (Google DeepMind for energy reduction) moves PUE toward 1.1–1.2, delivering energy savings — expanding the effective power budget of existing facilities without new electrical infrastructure. |
| **Predictive Maintenance** | Threshold alerts and reactive repairs. GPU failure rate ~9%/yr causes unplanned outages that reduce effective cluster capacity. | ML failure prediction flags at-risk GPUs days in advance for proactive replacement, maximizing cluster uptime and reducing the over-build buffer organizations provision as insurance against failures. |

---

## 2. Key Challenges — and How AI Helps Overcome Them

| Challenge | Root Cause | Traditional Mitigation | How AI Accelerates the Fix |
|---|---|---|---|
| **Data Silos** | Metrics fragmented across on-prem, private, and public cloud | Centralized observability platforms (Datadog, Dynatrace) | AI data fabric auto-discovers sources and reconciles metrics continuously — no manual integration. |
| **Data Quality** | Incomplete telemetry corrupts optimization decisions | Data governance frameworks and manual audits | ML anomaly detection flags bad data in real time before it reaches decision models. |
| **Hybrid Complexity** | Legacy and cloud systems use incompatible formats and APIs | OpenTelemetry standards and abstraction layers | AI placement engines evaluate cost, latency, and compliance across all tiers simultaneously. |
| **Resistance to Automation** | Ops teams distrust algorithmic recommendations | Human-in-the-loop workflows; gradual automation rollout | Explainable AI (XAI) shows plain-language rationale for every recommendation, building trust faster. |
| **Skill Gaps** | Few teams span AI, cloud, and infrastructure expertise | FinOps / Platform Engineering centers of excellence | AIOps platforms encode expert knowledge into automated workflows; natural language interfaces lower the skills bar. |

---

## 3. Conclusion

New infrastructure will always be part of AI's growth story — but data analytics and AI-driven optimization can significantly reduce how much is needed and how soon. Recovering underutilized GPU and server capacity, cutting cloud waste through FinOps, and AI-driven cooling all translate into deferred capital expenditure and fewer new builds. When expansion does become necessary, predictive analytics ensures investment is right-sized rather than speculative.

This approach is also good for the environment. Every data center deferred, every cooling watt saved, and every GPU hour reclaimed reduces energy consumption and carbon emissions. Training a single large LLM emits an estimated 284 tonnes of CO₂ — equivalent to five cars' lifetime emissions. Maximizing existing infrastructure is one of the most impactful steps the technology industry can take toward sustainable AI growth.

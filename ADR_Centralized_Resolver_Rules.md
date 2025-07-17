Architecture Decision Record

**Title:** Centralization of Route 53 Outbound Resolver Rules

**Status:** Proposed

**Date:** 2025-07-17

**Author:** Ramon Vignali

# 1. Context

Currently, each AWS account manages its own Route 53 outbound resolver rules. This results in duplicated configuration, increased operational complexity, and higher costs. Resolver endpoints must be deployed in each account/region where resolution is needed, which leads to approximately $700 per account in monthly costs. With around 40 accounts (mix of dev and prod), the total monthly cost is significant. In addition, managing and troubleshooting DNS resolution configurations across dozens of accounts increases the burden on engineering teams.

# 2. Decision

We will move to a shared resolver rule model, where outbound Route 53 resolver rules are managed in a central DNS account and shared with other accounts in the AWS Organization using AWS Resource Access Manager (RAM). Only one set of resolver endpoints will be created per region in the central account, and rules will be associated with VPCs in other accounts as needed.

# 3. Motivation

- Cost reduction: Decreases infrastructure spend from $700 per account to a centralized model with significantly fewer endpoints.
- Simplified management: Centralizes rule management, reduces configuration drift, and eases DNS troubleshooting.
- Improved scalability: Makes onboarding new accounts or regions simpler through shared resources.

# 4. Impact Assessment

Approximately 40 accounts will be affected by this change. These accounts span both development and production workloads.
- DNS traffic will route through centralized endpoints, requiring proper routing and failover planning.
- Engineering teams will have reduced autonomy in managing their own rules but will benefit from consistent policy enforcement.
- Implementation will require coordination to disassociate local rules and endpoints before associating shared ones.

# 5. Consequences

- Positive: Significant cost savings and reduced operational burden.
- Neutral: Requires central team to manage shared DNS rules.
- Negative: Potential risk of central point of failure; mitigated with HA resolver endpoints.

# 6. Alternatives Considered

- Maintain current model: Retains autonomy but continues cost and management burdens.
- Hybrid model: Share rules only for production; dismissed due to added complexity and uneven benefit.

# 7. Additional Technical Considerations

- Routing: No additional routing changes are anticipated. The existing Transit Gateway (TGW) design provides adequate connectivity for DNS resolution traffic between VPCs and centralized resolver endpoints. All accounts are expected to continue using the same route propagation and association model.

- Firewall Rules and Connectivity: Connectivity testing has been performed successfully. No updates to AWS firewalls, security groups, or network ACLs are currently required to support the use of shared resolver rules. All traffic paths for DNS resolution have been validated within the existing security design.

- Logging and Auditing: Console and administrative access will continue to be logged using the existing CloudTrail configuration. Route 53 Resolver query logging is currently under review and may be implemented in a separate initiative to enhance visibility into DNS activity.

- Hybrid Cloud Guidance: While this effort focuses on centralizing DNS within AWS, teams are encouraged to leverage Amazon Route 53 for DNS resolution whenever possible, especially in hybrid cloud environments. Doing so supports consistent resolution behavior, simplifies operations, and integrates well with AWS-native monitoring and access control mechanisms.
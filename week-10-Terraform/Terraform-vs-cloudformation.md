# Day 70: Terraform vs CloudFormation, Documentation and Teardown

## Objective

Compare Terraform with AWS CloudFormation, document the completed Week 10 architecture, and safely remove all lab resources.

## Terraform vs CloudFormation

| Area                  | Terraform                                                                                                                                                                                  | AWS CloudFormation                                                                                                                                                                                                         |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| HCL vs YAML/JSON      | Primarily uses human-readable HCL, with variables, expressions, loops, functions and dynamic blocks. Terraform also supports JSON syntax.                                                  | Templates use YAML or JSON. Logic is expressed through parameters, conditions, mappings and intrinsic functions such as `!Ref`, `!Sub` and `!GetAtt`.                                                                      |
| Provider scope        | Provider-based and designed to manage AWS, Azure, GCP, Kubernetes, GitHub, SaaS platforms and other APIs from one workflow.                                                                | AWS-managed and optimized for AWS. It can support third-party resources through the CloudFormation Registry and custom resources, but AWS remains its central platform.                                                    |
| State                 | Requires a state file that maps HCL resource addresses to real infrastructure IDs. Your Week 10 state is remotely stored in S3.                                                            | AWS maintains stack information, resource mappings, events and status inside the CloudFormation service. There is no customer-managed state file.                                                                          |
| Previewing changes    | `terraform plan` refreshes managed objects, compares configuration with state and proposes actions. A saved plan can later be applied exactly.                                             | A change set previews additions, modifications, replacements and deletions before execution. Neither mechanism guarantees that execution will succeed.                                                                     |
| Reusability           | Terraform modules package reusable configuration. Modules normally share the root configuration’s state unless deployed from separate root configurations.                                 | Nested stacks deploy reusable templates as child stacks beneath a root stack, with their own stack events and identities.                                                                                                  |
| Import                | `terraform import` or declarative `import` blocks bind an existing resource to a Terraform address. Matching resource configuration is still required.                                     | Resource import uses an `IMPORT` change set and is limited to supported resource types. Identifiers, template configuration and an appropriate deletion policy are required.                                               |
| Drift detection       | A normal `terraform plan` refreshes provider-managed resources and exposes differences. Terraform CLI does not continuously monitor drift unless planning is scheduled through automation. | CloudFormation has an explicit drift-detection operation. It checks supported resource types and only properties explicitly declared in the template or parameters. Nested stacks must be checked separately.              |
| Rollback and recovery | Terraform has no automatic transactional rollback. Successful operations remain recorded in state; fix the problem and rerun the plan/apply workflow.                                      | Standard CloudFormation operations can automatically roll back to the last stable stack state. It also supports preserving successful resources, continuing failed rollbacks and manual rollback operations.               |
| Teardown              | `terraform destroy` creates and executes a destroy plan for everything tracked in the selected state. Resources outside that state are unaffected.                                         | Deleting a root stack removes its managed resources unless termination protection, dependencies, `DeletionPolicy: Retain`, `Snapshot`, or another failure prevents it. Stack deletion cannot be cancelled after it starts. |
| Secrets and state     | `sensitive = true` hides values from normal CLI output but does not remove them from state or saved plan files. State, plans and private tfvars must be protected.                         | Do not embed credentials in templates. Use Secrets Manager or Parameter Store dynamic references. `NoEcho` masks parameter display but does not make every use of that value safe.                                         |
| When to choose        | Prefer Terraform for multi-provider environments, reusable infrastructure modules, consistent workflows across platforms and teams prepared to secure remote state.                        | Prefer CloudFormation/SAM for AWS-only environments, AWS-native governance, StackSets, serverless deployments and teams wanting AWS-managed stack state and rollback.                                                      |

## Tool Selection

Terraform was selected for the Week 10 platform stack because it provided reusable modules, provider-driven infrastructure management, execution planning and remote state.

CloudFormation/SAM remains suitable for AWS-native serverless deployments where managed stack state, change sets and rollback are valuable.

## Security Decisions

- Remote Terraform state stored in a private, encrypted, versioned S3 bucket.
- Native S3 state locking enabled.
- State, plan files and private tfvars excluded from Git.
- RDS credentials generated and managed through AWS Secrets Manager.
- RDS deployed in private database subnets.
- PostgreSQL access restricted to the application security group.
- Application S3 bucket encrypted, versioned and publicly blocked.

## Cost Decisions

- NAT Gateway remained optional.
- Development-sized EC2 and RDS instances were used.
- ALB, EC2 and RDS were deleted after evidence collection.
- RDS backups, snapshots, Secrets Manager secrets and S3 object versions were checked after teardown.
- The remote-state bucket was handled last.

## Teardown Evidence

- Destroy-plan resource count:
- Terraform destroy result:
- Remaining Terraform state:
- Remaining billable-resource checks:
- Backend teardown result:

## Lessons Learned

Terraform requires more deliberate state protection and recovery planning, while CloudFormation provides AWS-managed stack state and stronger native rollback. Terraform offered the better reusable structure for the Week 10 platform project.

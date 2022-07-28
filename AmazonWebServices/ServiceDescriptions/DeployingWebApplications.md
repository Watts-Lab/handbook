
### Deploying Web Applications

The following are AWS Services useful for deploying web applications. 

**Related Concepts:**
- Containerized Applications

### AWS App Runner
- [Summary](https://aws.amazon.com/apprunner/)
- [FAQ](https://aws.amazon.com/apprunner/faqs/)
AppRunner is a fully managed container deployment service. Supports following infrastrucutre development steps:
- AutoBuild & Deploy
- Load Balancing
- Autoscaling
- Certificate Setup
- Metric Dashboard

**Use Cases**
- For quickly developing and deploying lightweight applications with exepectedly low demand
- 

**Integration & Configuration Steps**
1) Connect to source (recommend ECR Image Upload)
2) Configure service
- Specify vCPUs and Memory (resources) for containers 
3) Launch 

**Pricing Model**
- Provisioned Instances: $0.007 / GB hour
- Active Instances: $0.064 / vCPU hour + $0.007 / GB hour
- Cloudwatch logs: $0.50 GB

**Gotchas**
- VPC connectivity is not yet supported 
- Can't scale down to 0

**Demo Videos/Articles**
- https://www.youtube.com/watch?v=TKirecwhJ2c
- https://www.youtube.com/watch?v=SVfIdT38i9I
- https://www.youtube.com/watch?v=x_1X_4j16A4
    - https://www.reddit.com/r/aws/comments/v1hax5/aws_app_runner_deep_dive_my_summary/
- https://aws.amazon.com/blogs/aws/new-for-app-runner-vpc-support/
- https://semaphoreci.com/blog/aws-app-runner



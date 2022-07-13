
## Use Patterns

**Standard Job / Job Arrays (qsub) and Head Node Interactive Development (qlogin)**
- Submitting job arrays and developing interactively on the HPCC head node do not incur any marginal cost
- For Job configurations requiring GPUs, we are able to submit jobs at no marginal cost in free tier, but jobs will automatically shut down after 4 hours
- for each job submission, we are able to set the: 
    - GPU number (-l gpu), 
    - Available Memory (-l m_mem_free), 
    - process count (-t) which sets the count of tasks for a job submitted as a job array

**Cloud Bursting Job / Job Array Submission (qsub-aws) & Interactive Development (qlogin-aws)**
- https://research-it.wharton.upenn.edu/documentation/cloud-bursting/
- We pay for hours of dedicated instance usage, at a 40% discount
- The AWS instances would only be running when jobs are submitted to and running in the dedicated queue. These shutdown as jobs complete. We only pay for the hours they are running jobs, so excludes start up, shut down, and any idle time. AWS instances will be automatically shut down when idle for one billable hour to conserve budget
- The billing is sent out the month after, for the previous month of usage.

**Cloud Bursting Configuration for CSSLab:**
- AWS Instance type/Configuration for Jobs invoking AWS resources:
    - max number of concurrent jobs:
    - max number of queued jobs:


## General Use

**Logging Into HPCC**
- 




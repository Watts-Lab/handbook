
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


**Monitoring Active Use**
- You will be able to see the current usage costs with the `unicloud-dbr` command on the hpcc-login node.


## General Use

**Logging Into HPCC Outside Penn Network: VPN**
- 

**Using the Head Node via `qlogin`**
- `ssh mriv@hpcc.wharton.upenn.edu`
- `qlogin -now no`
- `python -m venv myvenv`  --> to create a new virtual env
- `module load python/python-3.9.6` --> Setting default Python version
- `module load gcc/gcc-11.1.0`
- `source myenv0/bin/activate` --> given 'myenv0' is your venv
- `pip install -U pip`
- `pip install -U setuptools wheel`
- create requirements.txt file for virtual env
- `pip install -r requirements.txt`

**Running Jupyter when connected via VPN**
- ask Wharton Support to set up port forwarding on your HPCC environment
Follow these steps:
- follow General `qlogin` steps above 
- `jupyter lab`
- Open another terminal window on your local computer and copy / paste the ssh tunnel command from the output from above (below is just an example, it won't work for you):
    -  `ssh mriv@hpcc.wharton.upenn.edu -f -N -L 47686:hpcc019:47686`
- Then open a local browser and copy / paste the 127.0.0.1 URL from the output from the 'jupyter lab' command, similar (but not the same!) as the example below:
    - http://127.0.0.1:47686/lab?token=41a0db54573edaf50e661b3a88894dbe28c4db9003f

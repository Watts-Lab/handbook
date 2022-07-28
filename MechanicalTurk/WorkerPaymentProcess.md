
### Current Payment Notification Process: Deliberation-Empirica

- The following details the current payment process for Mechanical Turk (MTurk) survey-takers used in tasks involved with the Deliberation-Empirica project that involve MTurk workers drawn from the Panel
- Deliberation-Empirica repository [here](https://github.com/Watts-Lab/deliberation-empirica)
- From a high level, the payment process is currently executed manually via a script found in the Turk-Interface [repository](https://github.com/Watts-Lab/deliberation-project/blob/main/survey_workflows/sending-notifications.R)
- The process has three steps, and is designed to include intermediate steps that allow for lab members to opine or intervene in the process. This is as opposed to a fully automated payment system with no opportunity for human input 


- Receive file received with payment specifications
    - This just includes a list of worker ID’s and associated Bonus Amounts to be distributed
- update `sending-notifications.R`, and runnnig each of the following sections independently as three steps:
    - Section 1 —> Organizing Payments Data, line 714:
        - primary function: create `unpaid_people` dataframe, which contains table of Worker ID's and associated payment amount
    - Section 2 —> Registering Payments Data for Internal Review, line 744:
        - primary function: create and send notifcation of payment summary to monitoring-panel slack channel
        - this allows for team to review payment summary before payments are actually distributed, in case something needs to be addressed. 
    - Seciton 3 —> Execute Payments, line 769:
        - Primary function: Execute payment of workers listed in the `unpaid_people` table
        - Involves authentication with MTurk API and MTurk payment token 


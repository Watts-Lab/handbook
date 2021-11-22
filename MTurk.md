## HIT Instructions and design
Unsatisfactory responses to HITs are often due to poor instructions or design. Instructions should be very detailed, but also easy to hide or skipped over, so familiar workers aren't frustrated or slowed by repeatedly interacting with information they already know. 

## HIT Payments
**Pay, at a minimum, $15/hour to the median worker.**[^fairwork] 

One low-effort way to do this is by leveraging [Fair Work](https://fairwork.stanford.edu), which will calculate the completion time for a HIT and bonus workers up to the correct rate if needed the next day. Enable this by adding the following tag to the HTML of a HIT:

```html
<script src="https://fairwork.stanford.edu/fairwork.js?aws_account=088838630371"></script>
```
NOTE: This is a custom script for the lab turk account and will not work for other accounts. If you are using another account, get a script at [Fair Work](https://fairwork.stanford.edu). 

Also, double check the final HIT as Fairwork can cause rendering errors in some cases.

[^fairwork]: Whiting, Mark E., Grant Hugh, and Michael S. Bernstein. "[Fair Work: Crowd Work Minimum Wage with One Line of Code.](https://hci.stanford.edu/publications/2019/fairwork/fairwork-hcomp2019.pdf)" Proceedings of the AAAI Conference on Human Computation and Crowdsourcing. Vol. 7. No. 1. 2019.

## Emails from workers
Worker emails should be automatically forwarded to our internal worker communication email list. If you are running HITs on MTurk, you should be on that list so you can receive emails from workers. 

1. **Respectfully reply to all worker emails** and try to do it within 24 hours.
2. When replying, `reply all` so that everyone on our list knows the issue has been handled.
3. If the discussion continues, adjust the recipients to avoid overloading inboxes.
4. Communicate respectfully and without jargon.

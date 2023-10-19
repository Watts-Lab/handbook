
Attached is your AWS credentials. Attached within the credentials are the username, password,
and link to login to AWS. Can you please try and let me know if you are able to login?

The password policy when they ask you to change the password is the following:

If you need to reset your password, here’s the rules:
Minimum password length of 8 characters and a maximum length of 128 characters
Minimum of three of the following mix of character types: uppercase, lowercase,
numbers, and! @ # $ % ^ & * ( ) _ + - = [ ] { } | 'symbols
Not be identical to your AWS account name or email address

When you are able to login, please send me an update and I'll have more instructions for getting
you access to the ParallelCluster, which we need to work to create a private key/public key pair.

### Add your IP Address to the Security Group

- Make sure you are working out of the US East (N. Virginia);us-east-1 region.
- Go tohttps://www.ipchicken.com/and write down yourIP Address.
- Go to the EC2 Service and click on all the thingshighlighted in Red:
- Click Edit inbound rules ; add the IP address fromipchicken with SSH access on
port 22 like everyone else has, with a Description if you would like.

### Create a public/private key pair

- Run the command on a terminal and accept all the default settings (i.e. click 'enter' all the way through):
    ```powershell
    ssh-keygen
    ```
- Run the command and send me the public key that you generated:
  ```powershell 
  cat ~/.ssh/id_rsa.pub
  ```

If this works, then we can further set up SSH instructions for you and then you should have
access to the cluster!

Awesome, I just added your public key to the EC2 instance. Can you try the command below
and see if you can login? If you could check the IPaddress one last time to make sure that it
didn't change onipchicken.comand that the ip addressis correctly reflected in the AWS security
group , then run the command attached.

Example (See below): Replace epflcollab with the nameof the public/private key pair you
generated:
```powershell
ssh -i ~/.ssh/epflcollab ec2-user@ec2-34-197-75-53.compute-1.amazonaws.com
```

If you can login, congratulations! You have access to the environment.

## Accessing Jupyter Notebooks
Then there are additional instructions you need in order to access Jupyter Notebook:

1. To use Jupyter Notebook, logout of the EC2 instance by typing exit. Then login again with the the -L option and any port number 98xx where the last two digits are your choice:
    ```powershell
    ssh -i ~/.ssh/mykey ec2-user@ec2-34-197-75-53.compute-1.amazonaws.com -L 98xx:localhost:98xx
    ```
2. Run the source command:
    ```powershell
    source /fsx/homa/venv3/bin/activate
    ```
3. Run the Jupyter Notebook command with the port you specified to login:
    ```powershell
    jupyter notebook --port=98xx
    ```
4. If Jupyter Notebook asks for a password, the password is: `pennpass_v`
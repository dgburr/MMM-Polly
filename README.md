# MMM-Speech-Dispatcher
A MagicMirror² Module for performing Text-to-Speech using Amazon Polly

## Installation

1. Close repository:

```sh
git clone http://github.com/dgburr/MMM-Polly.git
```

2.  Install the `boto3` python module:

```sh
pip3 install boto3
```

3. Set up AWS account and get your credentials.  A good introduction guide can be found at http://2017.compciv.org/guide/topics/aws/intro-to-aws-boto3.html

4. Create `~/.aws/credentials` containing your credentials, e.g.:

```
[default]
region = eu-central-1
aws_access_key_id = XXXXXXXXX
aws_secret_access_key = YYYYYYYYYY
```
5. Test to make sure that you can communicate with Polly:

```sh
echo "Hello world" | python3 polly_client.py
```

## Configuration

```javascript
{
    module: "MMM-Polly",
    config: {
        voice: "Nicola",    // OPTIONAL: voice for Polly to use, e.g. "Nicola"
        language: "en-AU", // OPTIONAL: language for Polly to use, e.g. "en-AU"
        notification: "SPEECH_DISPATCHER_SAID", // OPTIONAL: notification to send after text has been spoken
    }
}
```


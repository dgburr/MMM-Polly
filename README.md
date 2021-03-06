# MMM-Polly
A MagicMirror² Module for performing Text-to-Speech using Amazon Polly

## Screenshot

[![Screenshot of MMM-Polly](screenshot.png)](https://www.youtube.com/watch?v=xdLz0bdxO58)

## Installation

1. Close repository:

```sh
$ git clone http://github.com/dgburr/MMM-Polly.git
```

2. Install `mpg321`:
```sh
$ sudo apt-get install mpg321
```

3. Install the `boto3` python module:

```sh
$ pip3 install boto3
```

Note: as of the time of writing (March 2019) the `python3-boto3` package included in Raspbian (1.4.2-1) is too old and does not support the Polly service.

4. Set up AWS account and get your credentials.  A good introduction guide can be found at http://2017.compciv.org/guide/topics/aws/intro-to-aws-boto3.html

5. Create `~/.aws/credentials` containing your credentials, e.g.:

```
[default]
region = eu-central-1
aws_access_key_id = XXXXXXXXX
aws_secret_access_key = YYYYYYYYYY

```
6. Test to make sure that you can communicate with Polly:

```sh
echo "Hello world" | python3 polly_client.py
```

## Configuration

```javascript
{
    module: "MMM-Polly",
    config: {
        voice: null,    // Voice for Polly to use, e.g. "Nicole".
        language: null, // Language for Polly to use, e.g. "en-AU".
        rate: 100,      // Specify a percentage to increase or decrease the speed of the speech. 100% indicates no change from the normal rate.  Percentages greater than 100% increase the rate.  Percentages below 100% decrease the rate.  The minimum value you can provide is 20%.
        pitch: 0,       // Specify a percentage to raise or lower the tone (pitch) of the speech.  The maximum value allowed is +50%.  The smallest value allowed is -33.3%.
        volume: 0,      // Change the volume of speech (in decibels).  +6dB is approximately twice the current amplitude. The maximum positive value is about +4.08dB.  -6dB means approximately half the current amplitude.
        playProgram:  "mpg321", // Sound playing program.
        notification: "SPEECH_DISPATCHER_SAID", // notification to send after text has been spoken
    }
}
```

The command `polly-client.py --debug` can be used to determine the list of supported voices, e.g.:

```sh
$ ./polly_client.py --debug --lang=en-GB
pi@raspberrypi:~/MagicMirror/modules/MMM-Polly $ ./polly_client.py --debug --lang=en-GB
{'Voices': [{'Id': 'Emma', 'LanguageName': 'British English', 'Gender': 'Female', 'LanguageCode': 'en-GB', 'Name': 'Emma'}, {'Id': 'Brian', 'LanguageName': 'British English', 'Gender': 'Male', 'LanguageCode': 'en-GB', 'Name': 'Brian'}, {'Id': 'Amy', 'LanguageName': 'British English', 'Gender': 'Female', 'LanguageCode': 'en-GB', 'Name': 'Amy'}], 'ResponseMetadata': {'HTTPHeaders': {'x-amzn-requestid': '4966bbcb-54a4-11e9-ae73-f120f3632c1c', 'content-type': 'application/json', 'connection': 'keep-alive', 'date': 'Mon, 01 Apr 2019 17:33:39 GMT', 'content-length': '426'}, 'RequestId': '4966bbcb-54a4-11e9-ae73-f120f3632c1c', 'RetryAttempts': 0, 'HTTPStatusCode': 200}}
```

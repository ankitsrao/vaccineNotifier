# Covid Vaccine Availability Notifier
Notification mechanism for Covid vaccine availability

## Usage [vaccine_notifier.py]
- Update the notificationmap with required details
- Update the Twilio [https://www.twilio.com/blog/what-does-twilio-do] id and auth token, for sending notifications
- Execute the script periodically using a cronjob or serverless functions on cloud.

## Usage [vaccine_notifier_lambda.py]
- This script can be used as it is and scheduled to run on AWS Lambda
- Create a new Lambda function, use the provided code and in the environment variables add TWILIO_ACCOUNT_SID and TWILIO_ACCOUNT_SID with their appropriate values.
- Using CloudWatch Events [https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/RunLambdaSchedule.html], trigger the Lambda as per your requirement.


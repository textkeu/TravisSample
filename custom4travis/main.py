from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import SignedJwtAssertionCredentials
import base64, httplib2, pprint, subprocess, datetime
from string import capwords

# from google API console - convert private key to base64 or load from file
id = "478917391271-e8pktjg0e8nbv2iev5vvbqo7i6jpiech@developer.gserviceaccount.com"
key = base64.b64decode('MIIGwAIBAzCCBnoGCSqGSIb3DQEHAaCCBmsEggZnMIIGYzCCAygGCSqGSIb3DQEHAaCCAxkEggMVMIIDETCCAw0GCyqGSIb3DQEMCgECoIICsjCCAq4wKAYKKoZIhvcNAQwBAzAaBBT+AdBoh5pt3QCbPvCKHeVztgTVBAICBAAEggKA7AVTWg/0r3RAxkbG89rEFStbgOYBrx/pPiDPi29epRdHptClPZGoRDdXirtoxM9cHkCguwl98IP5eNpba66BJ9xAqP9ZI+FX613LQnh/ih9sRxZjsAUJWxZ+NQVUta5Zcg4ji1/PMfwmRwryG39cJAUymrd3AYVfr3bN+Erm4kfxPSTrBljmR7UQjKs3twHc3vFudNWOuvvUl4MBMt+1lxSvh2MQvEbdNsTbERPprGYGF2YpWEyt1GMoi+IXejygjgDOPu2UQ3vp5zsmywdJ5xIz1TRr6daHqWJY3qh95j8U3GywGoqw/x0ink5RMMiIbT5mXPUAzbwOK+k9lSnCeOOG5Hdsh9vFc60SBi+i/eObTDjEi/D0TvKBCXOyf3p9ok1XJeg7GlO11felvRmSuAO6o9RayulCJ0vD39jlrLn9kw95aLq0Dq1pi066XR4+r+aZFLWy0Ky3l9a2iQylRwZ3iesfVRG5OF2+b15NQUFFHibEAUAurlLqX9xbGvsw4L+hDoaijqgz5IUtEdsEBV9VvmK2bOoHXqVBB++JTfmvsJeQ/HYnp2n9hqez0fzIvH+rixJtRaS8ZiO0UJGAREOFmeYU1RTIfpUz19tjWt7fID6R+u8sl9m1FfrPVL9spbk3yLoetFrl0ydqz08izrz9i+t9JBHQPjknGRdadzBWDkWMdWnoZ8souIeURPMQehkCASqN82oBg4S4mQOU5GeQT0kiCRz1zjlSgs2wkVGuSgl1gHSycSlB7y9eXrbzMqf47ybEGr9zzS5dVR4dhPUgjwkpthLa3PMKlEC+Xz5Z5wshH27986z2oHMsP8Lk4KLZv5ne5E6rd08YTf0JzzFIMCMGCSqGSIb3DQEJFDEWHhQAcAByAGkAdgBhAHQAZQBrAGUAeTAhBgkqhkiG9w0BCRUxFAQSVGltZSAxNDE2MTkxODIwNjQ4MIIDMwYJKoZIhvcNAQcGoIIDJDCCAyACAQAwggMZBgkqhkiG9w0BBwEwKAYKKoZIhvcNAQwBBjAaBBRsEW6Gpj/Yze14pLTjsZvZ3Yy+EAICBACAggLgCotbg2pio6rpmQtYBCUZAcAN99sLPctGz4BgW+1C0ZhSY6rjUgqqSxcEWz/T9DQlYCUwLwmZ+gU5j3XgxIVZVYMmJJ8vuCZIc0PPZyBOnXOS24+mRMm3+4AZ+z3qqCPdQUuccattYk6ps+aAOaDgOGE228S++xIy+gSCuU6iPdHktaQcIG1BfXi5iOcBitMGMWfjvafpY84bVBBGj2vfeMYdQFB0VqVjHBHRfJpXqTO4i1tv77RGwHJa6kKVM0G46MnkaeG/Bf7D23mYSo1Qp296brFW6DIHO9KhvaqY7C6HuErh9JN57wFwkffFPp1L43WhJ3zakFinYIQtypnGVKHtRQaisQeCMXRifQ7G9x9ytgq/SG57GrocAJx8mch6sr4TfIAHMrw3F6zj1ABHrOfjFHRXSDRcm/EA8549cme98JIMT+gysLK5+MPb6D1F08GPcb/Y5UFdSHCQk7ZxkJUGUOyZxcxzq/m+wjxgtYYRFcDuNfpkNlscGXNnOHTOmO7jYN+DJzJYZsHQJYC+b6ft0SOVZGVz4PR8FIMUYTrqqTcIpvwcQj21nA19BCQqUPHutxCtlysyhUogpetbl+OCgsFrvCmt8dasP3+3aa+M2o07bIF/vKV9Rx9fI43od2cAZ8Cq9F/fvJTEIclzHSycgzpbcryiZrFA+FiUjtX5wNjPW0MF3VZXbCHkbuesOatd9l/M5RXYDScMu6SvJg64ja+kKdQgiFGp0ermsROWDwpQFDUldmAJd1JmkomHfV1v+DYLlYDe9SdJw95LLPO7nUyMAFWwJWO3UfVAa8QYZDcd0jXXC5C0SBVGTjdAbSUnT0mQS1K/GgFKAXW9s6MuweCdkscx80L0e+SBciR2nyl0QDV3KlzG5PaY8oEMZCvH02OPBhWFHByHxXbnpcmWW41WV8X0u1qZY04JCWuOkD62+2KbtsjDvzR/nh2srXhNc7MNsCKxGLEveewKZjA9MCEwCQYFKw4DAhoFAAQUK/FGkWgVE3SKwDYpkHsbNb3auN4EFHUpDaV/qH/6e24nfuX2I/7epLU4AgIEAA==')

credentials = SignedJwtAssertionCredentials(id, key, scope='https://www.googleapis.com/auth/drive')
http = httplib2.Http()
http = credentials.authorize(http)

drive_service = build('drive', 'v2', http=http)

COMMAND_GIT_LOG = 'git log -1 --pretty=%B'
print COMMAND_GIT_LOG
p = subprocess.Popen(COMMAND_GIT_LOG, stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()
pprint.pprint(capwords(output.rstrip('\n')).replace(" ", ""));

DATETIME = datetime.datetime.now().strftime("%Y%m%d%H%M")
pprint.pprint(DATETIME);

# Insert a file
FILENAME = 'TravisSample-debug.apk'
media_body = MediaFileUpload(FILENAME, mimetype='application/apk', resumable=True)
body = {
  'title': 'TravisSample-debug.apk',
  'description': 'TravisSample-debug',
  'mimeType': 'application/apk'
}
body['parents'] = [{'id': '0B7YoFYpWOn-FUnVzaTZ2cDB1N0E'}]

file = drive_service.files().insert(body=body, media_body=media_body).execute()
pprint.pprint(file)

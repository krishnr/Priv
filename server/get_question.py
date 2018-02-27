def get_question(dim):
    dim_to_question = {
    "Identification": "Collects my IP address or device ID?",
    "Targeted Advertising": "Performs targeted advertising?",
    "Policy Change": "Can update privacy policy without informing you?",
    "Do Not Track": "Ignores Do Not Track?",
    "Security": "Insecure data storage?",
    "Retention": "Retains data indefinitely?",
    "Action": "Does not allow user choice/opt out?",
    "Location": "Tracks my location?",
    "Payment": "Collects my payment information?",
    "Disclosure": "Discloses information for legal purposes?",
    "Health": "Collects my health information?",
    "Activity": "Tracks my browsing patterns/activity?",
    "Deletion": "Allows deletion of my account?",
    "Social Media": "Accesses my social media profiles?",
    "Personalization": "Uses my data to personalize content?",
    "Contact Info": "Collects my contact information?",
    "Personal Info": "Collects personally identifiable information?",
    "3P Analysis": "Shares data to third parties for analysis?",
    "1P Analaysis": "Performs demographic analysis on data collected about me?",
    "3P Collection": "Shares data with third parties?",
    "1P Collection": "Collects data about me?",
    "Cookies": "Uses cookies to create a web profile about me?",
    }

    return dim_to_question[dim]